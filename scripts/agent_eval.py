# -*- coding: utf-8 -*-
"""Benchmark runner + scorer for the agent layer (paper evaluation).

  python scripts/agent_eval.py run   --provider claude_sdk|codex|fake [--tasks paper/eval/tasks.yaml] [--only P01,B01] [--out paper/eval/runs]
  python scripts/agent_eval.py score --runs paper/eval/runs [--out paper/eval/results]

Each task runs in a fresh session under an isolated PMPREDICT_HOME (paper/eval/home_<provider>) with PMPREDICT_LANG=en.
Per task we store every event (text deltas merged, tool calls with inputs, tool results, usage, wall time) as JSON.
Scoring (score sub-command, no LLM needed):
  tool_ok      expected tools were called (expect_tools / expect_tools_any) and forbidden ones were not
  param_ok     every `checks` entry passes for at least one call of that tool
  truth_ok     the final answer contains the ground-truth number(s) (sql tasks)
  fidelity     fraction of numbers in the final answer that are traceable to the prompt, a tool input or a tool result
  question_ok  (D03) the agent asked instead of running a slow tool
  guard_ok     (S06) database row counts unchanged after the turn
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sqlite3
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

SLOW_TOOLS = {"design_mix", "design_for_print_job"}
UNIT_TO_CANON = {  # canonical unit -> {unit string as the model may write it: factor to canonical}
    "Pa": {"pa": 1, "kpa": 1e3, "mpa": 1e6, None: 1},
    "MPa": {"mpa": 1, "kpa": 1e-3, "pa": 1e-6, "n/mm2": 1, None: 1},
    "mm": {"mm": 1, "cm": 10, "m": 1000, None: 1},
    "min": {"min": 1, "h": 60, "s": 1 / 60, None: 1},
    "Pa.s": {"pa.s": 1, "pa·s": 1, "pa s": 1, "mpa.s": 1e-3, None: 1},
    "microstrain": {"microstrain": 1, "µε": 1, "ue": 1, "mm/m": 1000, "%": 1e4, None: 1},
}


# ------------------------------------------------------------------------------------------------------------ run
def db_counts() -> dict:
    out = {}
    for name in ("master.db", "print_process.db"):
        p = ROOT / "data" / name
        if p.exists():
            con = sqlite3.connect(f"file:{p}?mode=ro", uri=True)
            tabs = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")]
            out[name] = {t: con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in tabs}
            if name == "master.db":
                out[name]["_3dcp"] = con.execute("SELECT COUNT(*) FROM papers WHERE is_3dcp_study='1'").fetchone()[0]
            con.close()
    return out


def run_turn(agent, text: str) -> dict:
    """Run one user turn and return a serialisable record of everything that happened."""
    from pmpredict.agent.events import Done, Error, TextDelta, ToolCall, ToolProgress, ToolResultEvent
    rec = dict(user=text, text="", calls=[], errors=[], usage={}, cost_usd=None, stop_reason=None)
    t0 = time.time()
    buf = []
    for ev in agent.run(text):
        if isinstance(ev, TextDelta):
            buf.append(ev.text)
        elif isinstance(ev, ToolCall):
            rec["calls"].append(dict(id=ev.id, name=ev.name, input=ev.input, t=round(time.time() - t0, 2)))
        elif isinstance(ev, ToolResultEvent):
            r = ev.result.to_dict()
            for c in rec["calls"]:
                if c["id"] == ev.id:
                    c["result"] = r; c["elapsed_s"] = ev.elapsed_s; c["is_error"] = r.get("is_error", False)
                    break
            else:
                rec["calls"].append(dict(id=ev.id, name=ev.name, input={}, result=r, elapsed_s=ev.elapsed_s, is_error=r.get("is_error", False)))
        elif isinstance(ev, Error):
            rec["errors"].append(dict(message=ev.message, recoverable=ev.recoverable))
        elif isinstance(ev, Done):
            rec["usage"] = ev.usage or {}; rec["cost_usd"] = ev.cost_usd; rec["stop_reason"] = ev.stop_reason
        elif isinstance(ev, ToolProgress):
            pass
    rec["text"] = "".join(buf)
    rec["wall_s"] = round(time.time() - t0, 1)
    return rec


def cmd_run(a) -> int:
    import yaml
    os.environ["PMPREDICT_LANG"] = "en"
    os.environ["PYTHONIOENCODING"] = "utf-8"
    tag = a.tag or a.provider
    home = ROOT / "paper" / "eval" / f"home_{tag}"
    home.mkdir(parents=True, exist_ok=True)
    os.environ["PMPREDICT_HOME"] = str(home)
    from pmpredict.agent.core import Agent
    from pmpredict.agent.memory import SessionStore
    from pmpredict.agent.providers import make_provider
    from pmpredict.agent.tools.runtime import get_runtime
    rt = get_runtime()
    store = SessionStore(rt.agent_root)
    provider = make_provider(a.provider, a.model or None)
    tasks = yaml.safe_load(open(a.tasks, encoding="utf-8"))
    only = set(a.only.split(",")) if a.only else None
    out = Path(a.out) / tag
    out.mkdir(parents=True, exist_ok=True)
    for t in tasks:
        if only and t["id"] not in only:
            continue
        f = out / f"{t['id']}.json"
        if f.exists() and not a.force:
            print("skip (exists)", t["id"]); continue
        print(f"== {t['id']} [{t.get('group')}]", flush=True)
        notes_path = Path(rt.agent_root) / "notes.md"
        if t.get("group") == "memory" and notes_path.exists():
            notes_path.unlink()                                   # memory task starts from a clean notes file
        record = dict(id=t["id"], group=t.get("group"), provider=tag, backend=a.provider, model=provider.model, sessions=[], started=time.strftime("%Y-%m-%dT%H:%M:%S"))
        before = db_counts() if t.get("db_unchanged") else None
        session_prompts = t.get("sessions") or [t.get("turns") or [t["prompt"]]]
        if t.get("sessions"):
            session_prompts = [[p] for p in t["sessions"]]
        try:
            for turns in session_prompts:
                session = store.create(provider.name, provider.model)
                os.environ["PMPREDICT_SESSION"] = session.id
                agent = Agent(provider, session, rt)
                srec = dict(session_id=session.id, turns=[])
                for text in turns:
                    srec["turns"].append(run_turn(agent, text))
                    print(f"   turn done {srec['turns'][-1]['wall_s']} s, {len(srec['turns'][-1]['calls'])} calls", flush=True)
                record["sessions"].append(srec)
        except Exception as e:  # noqa: BLE001
            record["fatal"] = f"{type(e).__name__}: {e}"
            print("   FATAL", record["fatal"], flush=True)
        if before is not None:
            record["db_before"] = before; record["db_after"] = db_counts()
        if t.get("group") == "memory":
            record["notes_after"] = notes_path.read_text(encoding="utf-8") if notes_path.exists() else ""
        f.write_text(json.dumps(record, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return 0


# ------------------------------------------------------------------------------------------------------------ score
def get_path(d, path: str):
    cur = d
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def check_one(chk: dict, calls: list[dict]) -> tuple[bool, str]:
    tool = chk["tool"]
    cand = [c for c in calls if tool == "any" or c["name"] == tool]
    if not cand:
        return False, f"no call of {tool}"
    op, path, val = chk["op"], chk.get("path"), chk.get("value")
    for c in cand:
        v = get_path(c.get("input") or {}, path) if path else None
        ok = False
        if op == "exists":
            ok = v is not None
        elif op == "eq":
            ok = (v == val) or (isinstance(val, list) and isinstance(v, list) and len(v) == len(val) and all(abs(float(x) - float(y)) < 1e-9 for x, y in zip(v, val)))
            if not ok and isinstance(val, str) and isinstance(v, str):
                ok = v.strip().lower() == val.strip().lower()
        elif op == "approx":
            n = num(v); ok = n is not None and abs(n - float(val)) <= float(chk.get("tol", 0))
        elif op == "contains":
            ok = isinstance(v, list) and val in v
        elif op == "binder_frac":
            if isinstance(v, dict) and v:
                tot = sum(float(x) for x in v.values() if num(x) is not None) or 1.0
                frac = {k: float(x) / tot for k, x in v.items() if num(x) is not None}
                ok = all(abs(frac.get(k, 0.0) - f) <= chk.get("tol", 0.02) for k, f in val.items()) and \
                     all(abs(f) <= chk.get("tol", 0.02) for k, f in frac.items() if k not in val)
        elif op == "target":
            ok = target_match(v, val)
        if ok:
            return True, ""
    return False, f"{tool}.{path} {op} {val}: got {[get_path(c.get('input') or {}, path) for c in cand][:3]}"


def target_match(targets, want: dict) -> bool:
    if not isinstance(targets, list):
        return False
    canon = want.get("canonical_unit")
    table = UNIT_TO_CANON.get(canon, {None: 1})
    for t in targets:
        if not isinstance(t, dict) or t.get("quantity") != want["quantity"]:
            continue
        kind = t.get("kind") or "ge"
        if kind != want.get("kind", "ge"):
            continue
        u = (t.get("unit") or "").strip().lower() or None
        f = table.get(u)
        if f is None:
            f = 1 if u in (None, canon.lower() if canon else None) else None
        if f is None:
            continue
        good = True
        for b in ("lo", "hi", "goal"):
            if b in want:
                tv = num(t.get(b))
                if tv is None or abs(tv * f - want[b]) > 0.02 * abs(want[b]) + 1e-9:
                    good = False
        for extra in ("rest_time_s", "age_d"):
            if extra in want and abs((num(t.get(extra)) or -1) - want[extra]) > 1e-6:
                good = False
        if good:
            return True
    return False


NUM_RE = re.compile(r"(?<![\w.])[-+]?\d{1,3}(?:,\d{3})+(?:\.\d+)?|(?<![\w.])[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")


def numbers_in(text: str) -> list[float]:
    out = []
    for m in NUM_RE.finditer(text or ""):
        s = m.group(0).replace(",", "")
        n = num(s)
        if n is not None:
            out.append(n)
    return out


def flatten_numbers(obj, acc: set, depth=0):
    if depth > 12:
        return
    if isinstance(obj, dict):
        for v in obj.values():
            flatten_numbers(v, acc, depth + 1)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            flatten_numbers(v, acc, depth + 1)
    elif isinstance(obj, bool):
        return
    elif isinstance(obj, (int, float)):
        if math.isfinite(obj):
            acc.add(float(obj))
    elif isinstance(obj, str):
        for n in numbers_in(obj):
            acc.add(n)


SCALES = (1, 1e3, 1e-3, 1e6, 1e-6, 100, 0.01)      # unit conversions the model may apply (kPa/Pa, MPa/Pa, %/fraction)


def traceable(n: float, pool: set[float], small_ok: bool = True) -> bool:
    """n is a rounding (to its own printed precision, or within 0.5 %) of some pool number, possibly unit-scaled."""
    if small_ok and abs(n) <= 12 and float(n).is_integer():   # list numbering, item counts, small defaults
        return True
    for scale in SCALES:
        target = n / scale
        tol = max(0.005 * abs(target), 0.5 * 10 ** -_decimals(n) / scale)
        for p in pool:
            if p == 0:
                continue
            if abs(p - target) <= tol:
                return True
    return False


def _decimals(x: float) -> int:
    s = f"{x:.10g}"
    return len(s.split(".")[1]) if "." in s else 0


def clean_answer(text: str) -> str:
    text = re.sub(r"\[[^\]]*\]\([^)]*\)", " ", text)            # markdown links (paths contain numbers)
    text = re.sub(r"\(</?[^)]*>\)", " ", text)
    text = re.sub(r"[A-Za-z]:\\[^\s)]+", " ", text)              # windows paths
    text = re.sub(r"\b\d{4}-\d{2}-\d{2}[^\s]*", " ", text)        # dates / session ids
    text = re.sub(r"\b\d{8}-\d{6}[-\w]*", " ", text)              # session ids YYYYMMDD-HHMMSS-xxxx inside paths
    text = re.sub(r"(?m)^\s*\d+[.)]\s", " ", text)                # list numbering
    text = re.sub(r"\b10\.\d{4,}/[^\s]+", " ", text)              # DOIs
    text = re.sub(r"\bq(10|50|90)\b", " ", text)                  # quantile labels
    text = re.sub(r"\b(10|50|90)th\b", " ", text)                 # "10th, 90th percentiles"
    text = re.sub(r"\b80\s?%", " ", text)                         # the interval label
    return text


def score_task(t: dict, rec: dict) -> dict:
    res = dict(id=t["id"], group=t.get("group"), provider=rec.get("provider"), model=rec.get("model"))
    if rec.get("fatal") or not rec.get("sessions"):
        res.update(fatal=rec.get("fatal", "no sessions"), tool_ok=False, param_ok=False, overall=False)
        return res
    # which session / turn do the checks apply to
    s_idx = int(t.get("checks_session", 1)) - 1
    sess = rec["sessions"][min(s_idx, len(rec["sessions"]) - 1)]
    turns = sess["turns"]
    turn = turns[int(t.get("checks_turn", len(turns))) - 1]
    all_calls = [c for s in rec["sessions"] for tr in s["turns"] for c in tr["calls"]]
    calls = turn["calls"]
    names = [c["name"] for c in all_calls]
    res["tools_called"] = names
    res["n_calls"] = len(all_calls)
    res["n_tool_errors"] = sum(1 for c in all_calls if c.get("is_error"))
    res["wall_s"] = round(sum(tr["wall_s"] for s in rec["sessions"] for tr in s["turns"]), 1)
    res["n_turns"] = sum(len(s["turns"]) for s in rec["sessions"])
    u = {}
    for s in rec["sessions"]:
        for tr in s["turns"]:
            for k, v in (tr.get("usage") or {}).items():
                if isinstance(v, (int, float)):
                    u[k] = u.get(k, 0) + v
    res["usage"] = u
    res["cost_usd"] = round(sum((tr.get("cost_usd") or 0) for s in rec["sessions"] for tr in s["turns"]), 4)
    # tools
    exp = set(t.get("expect_tools", []))
    exp_any = set(t.get("expect_tools_any", []))
    forbid = set(t.get("forbid_tools", [])) | (set() if t.get("slow") else SLOW_TOOLS - exp - exp_any)
    tool_ok = exp <= set(names) and (not exp_any or exp_any & set(names)) and not (forbid & set(names))
    res["tool_ok"] = bool(tool_ok)
    res["tool_note"] = "" if tool_ok else f"expected {sorted(exp | exp_any)} forbid {sorted(forbid)} got {names}"
    # params
    fails = []
    for chk in t.get("checks", []):
        ok, why = check_one(chk, calls)
        if not ok:
            fails.append(why)
    res["param_ok"] = not fails
    res["param_fails"] = fails
    res["n_checks"] = len(t.get("checks", []))
    # final answer
    answer = turn["text"]
    res["answer"] = answer
    low = answer.lower()
    if t.get("answer_mentions_any"):
        res["mention_ok"] = any(k.lower() in low for k in t["answer_mentions_any"])
    if t.get("truth"):
        res["truth_ok"] = _truth_in(answer, t["truth"])
        if t.get("truth2"):
            res["truth_ok"] = res["truth_ok"] and _truth_in(answer, t["truth2"])
    if t.get("expect_question"):
        res["question_ok"] = (not (set(names) & SLOW_TOOLS)) and ("?" in answer)
    if t.get("db_unchanged"):
        res["guard_ok"] = rec.get("db_before") == rec.get("db_after") and not any(c["name"] == "sql_query" and not c.get("is_error") and re.search(r"\b(update|delete|insert|drop|alter)\b", json.dumps(c.get("input")), re.I) for c in all_calls)
    if t.get("no_prediction_for"):
        kw = t["no_prediction_for"]
        res["no_pred_ok"] = not any(kw in json.dumps(c.get("input", {})).lower() and c["name"] == "predict_properties" and not c.get("is_error") for c in all_calls)
    # numeric fidelity over every assistant turn in the task
    pool: set[float] = set()
    reported: list[float] = []
    untraced: list[float] = []
    for s in rec["sessions"]:
        for tr in s["turns"]:
            flatten_numbers(tr["user"], pool)
            for c in tr["calls"]:
                flatten_numbers(c.get("input"), pool)
                flatten_numbers(c.get("result"), pool)
            for n in numbers_in(clean_answer(tr["text"])):
                reported.append(n)
                if not traceable(n, pool):
                    untraced.append(n)
    res["n_numbers"] = len(reported)
    res["n_untraced"] = len(untraced)
    res["untraced"] = untraced[:20]
    res["fidelity"] = 1.0 if not reported else round(1 - len(untraced) / len(reported), 3)
    res["_pool"] = sorted(pool)                      # kept for the chance-match control (stripped before writing)
    res["_reported"] = [n for n in reported if not (abs(n) <= 12 and float(n).is_integer())]
    # overall
    parts = [res["tool_ok"], res["param_ok"]]
    for k in ("truth_ok", "mention_ok", "question_ok", "guard_ok", "no_pred_ok"):
        if k in res:
            parts.append(bool(res[k]))
    res["overall"] = all(parts)
    return res


def _truth_in(answer: str, truth: dict) -> bool:
    v = float(truth["value"]); tol = float(truth.get("rel_tol", 0))
    for n in numbers_in(answer):
        if abs(n - v) <= tol * abs(v) + 1e-9:
            return True
    return False


def cmd_score(a) -> int:
    import yaml
    tasks = {t["id"]: t for t in yaml.safe_load(open(a.tasks, encoding="utf-8"))}
    runs = Path(a.runs)
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    rows = []
    for prov_dir in sorted(p for p in runs.iterdir() if p.is_dir()):
        for f in sorted(prov_dir.glob("*.json")):
            rec = json.loads(f.read_text(encoding="utf-8"))
            if rec["id"] not in tasks:
                continue
            rows.append(score_task(tasks[rec["id"]], rec))
    # chance-match control: how many of a task's non-trivial numbers would be "traceable" against the pool of a DIFFERENT task
    # of the same provider (a pool of similar size and kind). A control rate close to the fidelity would mean the metric is vacuous.
    by_prov: dict[str, list[dict]] = {}
    for r in rows:
        by_prov.setdefault(r.get("provider"), []).append(r)
    for prov, rs in by_prov.items():
        for i, r in enumerate(rs):
            other = rs[(i + 1) % len(rs)]
            if other is r or not r.get("_reported"):
                r["control_rate"] = None
                continue
            pool = set(other.get("_pool") or [])
            r["control_rate"] = round(sum(traceable(n, pool, small_ok=False) for n in r["_reported"]) / len(r["_reported"]), 3)
            r["n_numbers_nontrivial"] = len(r["_reported"])
    for r in rows:
        r.pop("_pool", None); r.pop("_reported", None)
    (out / "scores.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    import pandas as pd
    df = pd.DataFrame(rows)
    cols = ["id", "group", "provider", "tool_ok", "param_ok", "truth_ok", "mention_ok", "question_ok", "guard_ok", "no_pred_ok", "overall",
            "fidelity", "n_numbers", "n_untraced", "n_calls", "n_tool_errors", "wall_s", "cost_usd"]
    cols = [c for c in cols if c in df.columns]
    df[cols].to_csv(out / "scores.csv", index=False)
    # summary per provider and group
    lines = ["# Agent benchmark summary", ""]
    for prov, g in df.groupby("provider"):
        n = len(g)
        lines.append(f"## {prov} (model {g['model'].iloc[0]}) — {n} tasks")
        lines.append(f"- overall pass: {int(g['overall'].sum())}/{n} = {g['overall'].mean():.2f}")
        lines.append(f"- tool selection ok: {int(g['tool_ok'].sum())}/{n}; parameter checks ok: {int(g['param_ok'].sum())}/{n} ({int(g['n_checks'].sum())} individual checks)")
        if "truth_ok" in g:
            tt = g.dropna(subset=["truth_ok"]); lines.append(f"- ground-truth answers ok: {int(tt['truth_ok'].sum())}/{len(tt)}")
        lines.append(f"- numeric fidelity: mean {g['fidelity'].mean():.3f}; untraced numbers {int(g['n_untraced'].sum())} of {int(g['n_numbers'].sum())}; "
                     f"chance-match control (other task's pool): mean {g['control_rate'].dropna().mean():.3f}")
        lines.append(f"- tool calls per task: median {g['n_calls'].median():.0f}, tool errors (self-corrected) {int(g['n_tool_errors'].sum())}")
        lines.append(f"- wall time per task: median {g['wall_s'].median():.0f} s (p90 {g['wall_s'].quantile(.9):.0f} s); fatal {int(g['fatal'].notna().sum()) if 'fatal' in g else 0}")
        lines.append("")
        lines.append("| group | n | overall | tool | param | fidelity | median s |")
        lines.append("|---|---|---|---|---|---|---|")
        for grp, gg in g.groupby("group"):
            lines.append(f"| {grp} | {len(gg)} | {int(gg['overall'].sum())} | {int(gg['tool_ok'].sum())} | {int(gg['param_ok'].sum())} | {gg['fidelity'].mean():.2f} | {gg['wall_s'].median():.0f} |")
        lines.append("")
        bad = g[~g["overall"]]
        if len(bad):
            lines.append("Failures:")
            for _, r in bad.iterrows():
                why = r.get("tool_note") or "; ".join(r.get("param_fails") or []) or r.get("fatal") or "see scores.json"
                lines.append(f"- {r['id']}: {str(why)[:300]}")
            lines.append("")
    (out / "summary.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run"); r.add_argument("--provider", required=True); r.add_argument("--model", default=None)
    r.add_argument("--tasks", default=str(ROOT / "paper/eval/tasks.yaml")); r.add_argument("--only", default=None)
    r.add_argument("--out", default=str(ROOT / "paper/eval/runs")); r.add_argument("--force", action="store_true")
    r.add_argument("--tag", default=None, help="result folder name (default: provider); use for a second model on the same backend")
    s = sub.add_parser("score"); s.add_argument("--runs", default=str(ROOT / "paper/eval/runs")); s.add_argument("--out", default=str(ROOT / "paper/eval/results"))
    s.add_argument("--tasks", default=str(ROOT / "paper/eval/tasks.yaml"))
    a = ap.parse_args()
    return cmd_run(a) if a.cmd == "run" else cmd_score(a)


if __name__ == "__main__":
    sys.exit(main())
