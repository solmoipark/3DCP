# -*- coding: utf-8 -*-
"""Generate the LaTeX inputs of the paper from the benchmark runs and the project data.

  python scripts/paper_render.py [--provider claude_sdk] [--runs paper/eval/runs] [--results paper/eval/results]

Writes into paper/gen/:
  case_<ID>.tex          chat transcript boxes (user / agent / tool) for the showcase tasks
  mcp_<ID>.tex           request / response box of the first tool call of a task
  benchmark_table.tex    per-group results for both backends
  numbers.tex            \newcommand macros with DB sizes, model counts, benchmark aggregates
  models_table.tex       the 27-model quality table (general + 3DCP variants)
  tools_table.tex        the tool registry table
and copies the figure artifacts of the showcase runs into paper/figures/.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
GEN = ROOT / "paper" / "gen"
FIG = ROOT / "paper" / "figures"


# ------------------------------------------------------------------------------------------------------ LaTeX helpers
UNI = {"⁻": "^-", "⁺": "^+", "⁰": "^0", "¹": "^1", "⁴": "^4", "⁵": "^5", "⁶": "^6", "⁷": "^7", "⁸": "^8", "⁹": "^9", "≈": "~=", "≠": "!=", "∞": "inf",
       "Δ": "Delta ", "γ": "gamma", "σ": "sigma", "α": "alpha", "β": "beta", "ω": "omega", "κ": "kappa", "λ": "lambda", "η": "eta", "′": "'", "″": "''",
       "…": "...", "✓": "[ok]", "✔": "[ok]", "⬜": "[ ]", "‑": "-", " ": " ", " ": " ", " ": " ", "‘": "'", "’": "'", "“": '"', "”": '"',
       "→": "->", "←": "<-", "↑": "up", "↓": "down", "≥": ">=", "≤": "<=", "–": "-", "—": "--", "·": ".", "×": "x", "±": "+/-", "°": " deg", "µ": "u",
       "τ": "tau", "ρ": "rho", "√": "sqrt", "²": "^2", "³": "^3", "ε": "eps", "✅": "[ok]", "⚠": "[!]", "️": "", "❌": "[x]", "🔧": "", "📊": "", "📁": "", "🧱": "",
       "ü": "ue", "ö": "oe", "ä": "ae", "é": "e", "è": "e", "ñ": "n", "ç": "c"}


SYSTEM_NAME = "3DCP-Agent"          # the package's internal name is replaced by the public system name in transcripts (stated in the paper)


def uni(s: str) -> str:
    """Map characters outside Latin-1 that pdflatex cannot typeset to ASCII equivalents (verbatim listings use the same map)."""
    out = []
    s = str(s).replace("pmpredict's", SYSTEM_NAME + "'s").replace("pmpredict", SYSTEM_NAME)
    for ch in str(s):
        if ch in UNI:
            out.append(UNI[ch])
        elif ord(ch) < 0x250 or ch in "\n\t":
            out.append(ch)
        elif "가" <= ch <= "힣":           # Hangul from Korean tool summaries: keep a marker, the model translates them
            out.append("")
        else:
            out.append("?")
    return "".join(out)


def esc(s: str) -> str:
    s = uni(s)
    rep = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    out = "".join(rep.get(ch, ch) for ch in s)
    out = out.replace("≥", r"$\geq$").replace("≤", r"$\leq$").replace("→", r"$\rightarrow$").replace("–", "--").replace("—", "---")
    out = out.replace("τ", r"$\tau$").replace("ρ", r"$\rho$").replace("√", r"$\surd$").replace("·", r"$\cdot$").replace("²", r"$^2$").replace("³", r"$^3$")
    out = out.replace("µ", r"$\mu$").replace("ε", r"$\varepsilon$").replace("°", r"$^\circ$").replace("±", r"$\pm$").replace("×", r"$\times$")
    out = out.replace("✅", r"[ok]").replace("⚠️", r"[!]").replace("❌", r"[x]").replace("🔧", "")
    return out


MAX_TABLE_ROWS = 7


def md_to_tex(text: str, max_chars: int = 2600) -> str:
    """Markdown-lite (bold, bullets, headings, code spans, tables) -> LaTeX; truncated with [...]."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)            # links -> label
    text = re.sub(r"\(</?[^)]*>\)", "", text)
    if len(text) > max_chars:
        text = text[:max_chars].rsplit("\n", 1)[0] + "\n[...]"
    lines = text.split("\n")
    out, in_list, in_table = [], False, False
    for ln in lines:
        s = ln.rstrip()
        if re.match(r"^\s*\|", s):                                     # markdown table row
            if re.match(r"^\s*\|\s*-{2,}", s):
                continue
            cells = [c.strip() for c in s.strip().strip("|").split("|")]
            if not in_table:
                w = 0.94 / max(1, len(cells))
                spec = "".join([r"p{" + f"{w:.2f}" + r"\linewidth}"] * len(cells))
                out.append(r"\par\smallskip\begin{adjustbox}{max width=\linewidth}\begin{tabular}{" + spec + "}"); in_table = True
                table_rows = 0
            table_rows += 1
            if table_rows <= MAX_TABLE_ROWS:                           # tables cannot break across pages inside the chat box
                out.append(" & ".join(_inline(c) for c in cells) + r" \\")
            continue
        elif in_table:
            if table_rows > MAX_TABLE_ROWS:
                out.append(r"\multicolumn{1}{l}{\textit{\ldots " + str(table_rows - MAX_TABLE_ROWS) + r" further rows in the transcript}} \\")
            out.append(r"\end{tabular}\end{adjustbox}\par\smallskip"); in_table = False
        if re.match(r"^\s*[-*•]\s+", s):
            if not in_list:
                out.append(r"\begin{itemize}[nosep,leftmargin=1.2em]"); in_list = True
            out.append(r"\item " + _inline(re.sub(r"^\s*[-*•]\s+", "", s)))
            continue
        elif in_list and s.strip() == "":
            out.append(r"\end{itemize}"); in_list = False
            continue
        elif in_list:
            out.append(r"\end{itemize}"); in_list = False
        if re.match(r"^\s*#{1,4}\s", s):
            out.append(r"\textbf{" + _inline(re.sub(r"^\s*#{1,4}\s", "", s)) + r"}\par")
        elif s.strip() == "":
            out.append(r"\par")
        else:
            out.append(_inline(s) + r"\par")
    if in_list:
        out.append(r"\end{itemize}")
    if in_table:
        out.append(r"\end{tabular}\end{adjustbox}\par\smallskip")
    return "\n".join(out)


def _inline(s: str) -> str:
    """Escape text, keeping `code` spans verbatim and converting **bold** (which may enclose code spans)."""
    codes: list[str] = []

    def stash(m):
        codes.append(r"\texttt{" + esc(m.group(1)) + "}")
        return f"\x00{len(codes) - 1}\x00"
    s = re.sub(r"`([^`]*)`", stash, s)
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s)
    s = re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], s)
    return s


def json_box(obj, max_chars: int = 900) -> str:
    s = uni(json.dumps(obj, ensure_ascii=False, indent=1, default=str))
    if len(s) > max_chars:
        s = s[:max_chars].rsplit("\n", 1)[0] + "\n ..."
    return r"\begin{lstlisting}[style=jsonstyle]" + "\n" + s + "\n" + r"\end{lstlisting}"


def result_digest(result: dict, max_chars: int = 900) -> dict:
    """Keep the informative part of a tool result for the figure: summary + the scalar fields + first rows of tables."""
    data = result.get("data") or {}

    def shallow(v, depth):
        if isinstance(v, bool) or v is None:
            return v
        if isinstance(v, (int, float)):
            return round(v, 4) if isinstance(v, float) else v
        if isinstance(v, str):
            return v if len(v) <= 80 else v[:77] + "..."
        if isinstance(v, dict):
            if depth >= 2:
                return "{...}"
            return {k: shallow(x, depth + 1) for k, x in list(v.items())[:12] if k not in ("text", "csv", "traceback_tail")}
        if isinstance(v, list):
            if not v:
                return []
            return [shallow(x, depth + 1) for x in v[:2]] + (["..."] if len(v) > 2 else [])
        return str(v)[:60]
    keep = {k: shallow(v, 0) for k, v in data.items() if k not in ("text", "csv", "traceback_tail")}
    if result.get("artifacts"):
        keep["artifacts"] = [Path(a["path"]).name for a in result["artifacts"]]
    if result.get("summary"):
        keep = {"summary": uni(result["summary"]), **keep}
    while len(json.dumps(keep, ensure_ascii=False, default=str)) > max_chars * 1.3 and len(keep) > 3:
        keep.pop(list(keep)[-1])
    return keep


# ------------------------------------------------------------------------------------------------------ transcripts
def render_case(rec: dict, task: dict, max_answer: int = 2600, max_calls: int = 7) -> str:
    NL = chr(10)
    out = []
    for s_i, sess in enumerate(rec["sessions"]):
        if len(rec["sessions"]) > 1:
            out.append(r"\sessionsep{Session " + str(s_i + 1) + "}")
        for tr in sess["turns"]:
            out.append(r"\begin{userbox}" + NL + esc(tr["user"]) + NL + r"\end{userbox}")
            calls = tr["calls"]
            for c in calls[:max_calls]:
                err = " [error]" if c.get("is_error") else ""
                el = "" if c.get("elapsed_s") is None else f", {c['elapsed_s']:.1f} s"
                args = uni(json.dumps(c.get("input") or {}, ensure_ascii=False, default=str))
                if len(args) > 260:
                    args = args[:260] + " ...}"
                out.append(r"\begin{toolbox}{" + esc(c["name"]) + esc(err) + esc(el) + "}" + NL + r"\begin{lstlisting}[style=argstyle]" + NL
                           + args + NL + r"\end{lstlisting}" + NL + r"\end{toolbox}")
            if len(calls) > max_calls:
                out.append(r"\toolmore{" + str(len(calls) - max_calls) + "}")
            out.append(r"\begin{agentbox}" + NL + md_to_tex(tr["text"], max_answer) + NL + r"\end{agentbox}")
    return NL.join(out)


def render_mcp(rec: dict, tool_name: str | None = None) -> str:
    for sess in rec["sessions"]:
        for tr in sess["turns"]:
            for c in tr["calls"]:
                if tool_name is None or c["name"] == tool_name:
                    req = {"tool": c["name"], "arguments": c.get("input")}
                    resp = result_digest(c.get("result") or {})
                    return (r"\begin{mcpbox}{Tool request (client $\rightarrow$ server)}" + "\n" + json_box(req) + "\n" + r"\end{mcpbox}" + "\n"
                            r"\begin{mcpbox}{Tool response (server $\rightarrow$ client, digest)}" + "\n" + json_box(resp) + "\n" + r"\end{mcpbox}")
    return ""


def copy_artifacts(rec: dict, prefix: str) -> list[str]:
    """Copy the image artifacts of a task into paper/figures and write gen/figs_<ID>.tex that includes them side by side."""
    FIG.mkdir(parents=True, exist_ok=True)
    copied, titles = [], []
    for sess in rec["sessions"]:
        for tr in sess["turns"]:
            for c in tr["calls"]:
                for a in (c.get("result") or {}).get("artifacts", []):
                    p = Path(a["path"])
                    if p.suffix.lower() in (".png", ".pdf") and p.exists():
                        dst = FIG / f"{prefix}_{p.name}"
                        shutil.copy(p, dst); copied.append(dst.name); titles.append(a.get("title", p.stem))
    if copied:
        w = max(0.3, min(0.95, 0.98 / len(copied)))
        parts = [r"\includegraphics[width=" + f"{w:.2f}" + r"\textwidth]{" + n + "}" for n in copied[:3]]
        (GEN / f"figs_{prefix}.tex").write_text((r"\hfill" + "\n").join(parts) + "\n", encoding="utf-8")
    return copied


# ------------------------------------------------------------------------------------------------------ tables
def models_table() -> str:
    man = json.loads((ROOT / "artifacts" / "manifest.json").read_text(encoding="utf-8"))["models"]
    rows = []
    for k, m in sorted(man.items(), key=lambda kv: (kv[1]["target"], kv[1].get("variant") != "general")):
        rows.append((m["target"], m.get("variant"), m.get("unit"), m.get("n_train"), m.get("n_papers"), m.get("r2_log") if m.get("r2_log") is not None else m.get("r2"),
                     m.get("spearman"), m.get("coverage80"), "yes" if m.get("weak_model") else ""))
    tex = [r"\begin{tabular}{llrrrrrrc}", r"\toprule", r"target & variant & unit & rows & papers & R$^2_{\log}$ & Spearman & cov$_{80}$ & weak \\", r"\midrule"]
    for r in rows:
        tex.append(f"{esc(r[0])} & {r[1]} & {esc(r[2])} & {r[3]} & {r[4]} & {_f(r[5])} & {_f(r[6])} & {_f(r[7])} & {r[8]} \\\\")
    tex += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(tex)


def _f(x, d=2):
    try:
        return f"{float(x):.{d}f}"
    except (TypeError, ValueError):
        return "--"


def tools_table() -> str:
    import os
    os.environ.setdefault("PMPREDICT_LANG", "en")
    from pmpredict.agent.tools import REGISTRY
    purpose = {
        "list_models": "predictable targets and model quality", "describe_vocabulary": "material classes, specimen groups, curing presets",
        "build_mix_spec": "validate a mix description", "predict_properties": "properties with 80\\,\\% intervals",
        "flow_curve": "Bingham flow curve + measured analogues", "structuration_curve": "$\\tau_s(t)$ + measured analogues",
        "retrieve_literature": "published mixes near target values", "design_mix": "inverse mix design (Sobol $\\rightarrow$ screening $\\rightarrow$ DE)",
        "assess_buildability": "verdict, schedule window, similar prints", "print_schedule": "layer cycle-time / speed window",
        "similar_prints": "nearest published print runs", "design_for_print_job": "job $\\rightarrow$ required rheology $\\rightarrow$ mixes $\\rightarrow$ re-assessment",
        "describe_schema": "tables, columns, samples of the databases", "sql_query": "read-only SELECT (authorizer-guarded)",
        "save_report": "report of a session (text and spreadsheet)", "remember": "durable note included in later prompts",
    }
    tex = [r"\begin{tabular}{@{}lp{0.8cm}p{4.9cm}p{5.4cm}@{}}", r"\toprule", r"tool & kind & purpose & inputs \\", r"\midrule"]
    for n, t in REGISTRY.items():
        kind = "slow" if t.slow else ("read" if t.read_only else "write")
        ins = ", ".join(f"\\texttt{{{esc(k)}}}" for k in t.input_schema.get("properties", {}).keys())   # breakable between tokens
        tex.append(f"\\texttt{{{esc(n)}}} & {kind} & {purpose.get(n, '')} & {ins} \\\\")
    tex += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(tex)


GROUP_LABEL = {"predict": "forward prediction", "curves": "rheology curves", "retrieve": "literature retrieval", "design": "inverse design",
               "buildability": "buildability / schedule", "job_design": "job $\\rightarrow$ mix", "sql": "database questions", "sql_guard": "write attempt (guard)",
               "hallucination": "unsupported requests", "memory": "durable memory"}
PROV_LABEL = {"claude_sdk": "claude-sonnet-5", "codex": "gpt-6-astra", "codex_sol": "gpt-6-sol", "codex_luna": "gpt-6-luna", "codex_61sol": "gpt-6.1-sol",
              "codex_56sol": "gpt-5.6-sol", "anthropic": "Claude API", "openai": "OpenAI API"}
DEFAULT_MODEL = {"codex": "gpt-6-astra", "codex_sol": "gpt-6-sol", "codex_luna": "gpt-6-luna", "codex_61sol": "gpt-6.1-sol", "codex_56sol": "gpt-5.6-sol",
                 "claude_sdk": "claude-sonnet-5"}   # recorded model is empty when the backend default is used
PROV_TAG = {"claude_sdk": "Cl", "codex": "Cx", "codex_sol": "Cs", "codex_luna": "Cu", "codex_61sol": "Cv", "codex_56sol": "Cw", "codex_mini": "Cm", "anthropic": "An", "openai": "Oa"}


def benchmark_tables(results: Path) -> tuple[str, dict]:
    import pandas as pd
    scores = json.loads((results / "scores.json").read_text(encoding="utf-8"))
    for r in scores:
        r["model"] = r.get("model") or DEFAULT_MODEL.get(r.get("provider"), r.get("provider"))
    df = pd.DataFrame(scores)
    order = ["codex", "codex_sol", "codex_luna", "codex_61sol", "codex_56sol", "claude_sdk", "codex_mini", "anthropic", "openai"]
    provs = sorted(set(df["provider"]), key=lambda p: order.index(p) if p in order else 9)
    for p in provs:
        PROV_LABEL.setdefault(p, esc(str(df[df["provider"] == p]["model"].iloc[0] or p)))
    groups = [g for g in GROUP_LABEL if g in set(df["group"])]
    # Table A: one row per model (summary); Table B: pass counts per task group and model
    tex = [r"\begin{tabular}{lrrrrrrrrr}", r"\toprule",
           r"model & pass & checks & truth & fidelity & control & tool errors & calls & median s & p90 s \\", r"\midrule"]
    agg = {}
    for p in provs:
        gg = df[df["provider"] == p]
        tex.append(f"{PROV_LABEL.get(p, p)} & {int(gg['overall'].sum())}/{len(gg)} & {int(gg['param_ok'].sum())}/{len(gg)} & "
                   f"{int(gg['truth_ok'].fillna(False).sum())}/{int(gg['truth_ok'].notna().sum())} & {gg['fidelity'].mean():.3f} & {gg['control_rate'].dropna().mean():.2f} & "
                   f"{int(gg['n_tool_errors'].sum())} & {gg['n_calls'].median():.0f} & {gg['wall_s'].median():.0f} & {gg['wall_s'].quantile(.9):.0f} \\\\")
        u = gg["usage"].apply(lambda d: d if isinstance(d, dict) else {})
        agg[p] = dict(n=len(gg), pass_n=int(gg["overall"].sum()), pass_rate=gg["overall"].mean(), tool_ok=int(gg["tool_ok"].sum()), param_ok=int(gg["param_ok"].sum()),
                      n_checks=int(gg["n_checks"].sum()), fidelity=gg["fidelity"].mean(), n_numbers=int(gg["n_numbers"].sum()), n_untraced=int(gg["n_untraced"].sum()),
                      calls_median=gg["n_calls"].median(), tool_errors=int(gg["n_tool_errors"].sum()), wall_median=gg["wall_s"].median(), wall_pninety=gg["wall_s"].quantile(.9),
                      wall_max=gg["wall_s"].max(), cost=gg["cost_usd"].sum(), model=gg["model"].iloc[0],
                      in_tokens=int(u.apply(lambda d: d.get("input_tokens", 0)).sum()), out_tokens=int(u.apply(lambda d: d.get("output_tokens", 0)).sum()),
                      cache_tokens=int(u.apply(lambda d: d.get("cache_read_input_tokens", 0)).sum()),
                      control=gg["control_rate"].dropna().mean() if "control_rate" in gg else float("nan"),
                      truth_n=int(gg["truth_ok"].notna().sum()) if "truth_ok" in gg else 0, truth_ok=int(gg["truth_ok"].fillna(False).sum()) if "truth_ok" in gg else 0,
                      fatal=int(gg["fatal"].notna().sum()) if "fatal" in gg else 0)
    tex += [r"\bottomrule", r"\end{tabular}"]
    # Table B
    texb = [r"\begin{tabular}{lr" + "r" * len(provs) + "}", r"\toprule", "task group & $n$ & " + " & ".join(PROV_LABEL.get(p, p) for p in provs) + r" \\", r"\midrule"]
    n_tasks = {g: int(df[df["group"] == g].groupby("provider").size().max()) for g in groups}
    for g in groups:
        cells = []
        for p in provs:
            gg = df[(df["group"] == g) & (df["provider"] == p)]
            cells.append(f"{int(gg['overall'].sum())}" if len(gg) == n_tasks[g] else f"{int(gg['overall'].sum())}/{len(gg)}")
        texb.append(f"{GROUP_LABEL[g]} & {n_tasks[g]} & " + " & ".join(cells) + r" \\")
    texb.append(r"\midrule")
    texb.append("all tasks & " + str(sum(n_tasks.values())) + " & " + " & ".join(str(int(df[df["provider"] == p]["overall"].sum())) for p in provs) + r" \\")
    texb += [r"\bottomrule", r"\end{tabular}"]
    (GEN / "benchmark_groups.tex").write_text("\n".join(texb), encoding="utf-8")
    return "\n".join(tex), agg


def tasks_table(tasks: dict) -> str:
    tex = [r"\begin{tabular}{llp{8.6cm}rl}", r"\toprule", r"id & group & prompt (abridged) & checks & expected tools \\", r"\midrule"]
    for tid, t in tasks.items():
        prompts = t.get("sessions") or t.get("turns") or [t.get("prompt", "")]
        txt = " / ".join(prompts)
        if len(txt) > 150:
            txt = txt[:150].rsplit(" ", 1)[0] + " ..."
        exp = ", ".join(t.get("expect_tools") or t.get("expect_tools_any") or ["(none)"])
        extra = []
        for k in ("truth", "expect_question", "db_unchanged", "no_prediction_for", "answer_mentions_any"):
            if t.get(k):
                extra.append({"truth": "ground truth", "expect_question": "must ask", "db_unchanged": "DB unchanged", "no_prediction_for": "no prediction", "answer_mentions_any": "wording"}[k])
        n = len(t.get("checks", []))
        tex.append(f"{tid} & {GROUP_LABEL.get(t.get('group'), t.get('group'))} & {esc(txt)} & {n}{(' + ' + ', '.join(extra)) if extra else ''} & \\texttt{{{esc(exp)}}} \\\\")
    tex += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(tex)


def db_numbers() -> dict:
    import sqlite3
    m = sqlite3.connect(f"file:{ROOT / 'data' / 'master.db'}?mode=ro", uri=True)
    p = sqlite3.connect(f"file:{ROOT / 'data' / 'print_process.db'}?mode=ro", uri=True)
    q = lambda con, s: con.execute(s).fetchone()[0]
    bs = json.loads((ROOT / "data" / "build_summary.json").read_text(encoding="utf-8"))
    man = json.loads((ROOT / "artifacts" / "manifest.json").read_text(encoding="utf-8"))["models"]
    cal = json.loads((ROOT / "configs" / "buildability_calibration.json").read_text(encoding="utf-8"))
    return dict(
        papers=q(m, "SELECT COUNT(*) FROM papers"), papersIncluded=q(m, "SELECT COUNT(*) FROM papers WHERE screening_status='included'"),
        papersThreeDCP=q(m, "SELECT COUNT(*) FROM papers WHERE is_3dcp_study='1'"), mixes=q(m, "SELECT COUNT(*) FROM mixes"),
        measurements=q(m, "SELECT COUNT(*) FROM measurements"), measurementsValued=q(m, "SELECT COUNT(*) FROM measurements WHERE value_canonical!='' AND fig_only='0'"),
        curves=q(m, "SELECT COUNT(*) FROM curves"), curvePoints=q(m, "SELECT COUNT(*) FROM curve_points"),
        printRuns=q(p, "SELECT COUNT(*) FROM print_runs"), printPapers=q(p, "SELECT COUNT(DISTINCT paper_uid) FROM print_runs"),
        printPrintable=q(p, "SELECT COUNT(*) FROM print_runs WHERE printability_label='printable'"), printNon=q(p, "SELECT COUNT(*) FROM print_runs WHERE printability_label='non_printable'"),
        printBorder=q(p, "SELECT COUNT(*) FROM print_runs WHERE printability_label='borderline'"), printCollapses=q(p, "SELECT COUNT(*) FROM print_runs WHERE outcome='collapsed'"),
        printSTF=q(p, "SELECT COUNT(*) FROM print_runs WHERE stack_to_failure=1"), protocolRows=q(p, "SELECT COUNT(*) FROM rheology_protocols"),
        nMixesNorm=bs["n_normalised"], nFeatures=bs["n_features"], nModels=len(man), nTargets=len({v["target"] for v in man.values()}),
        rFailN=cal["R_fail"]["n"], rFailPapers=cal["R_fail"]["n_papers"], rFailMedian=cal["R_fail"]["p50"], rFailPtf=cal["R_fail"]["p25"], rFailPsf=cal["R_fail"]["p75"],
        nTools=16,
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", default="claude_sdk")
    ap.add_argument("--runs", default=str(ROOT / "paper/eval/runs"))
    ap.add_argument("--results", default=str(ROOT / "paper/eval/results"))
    ap.add_argument("--paper-dir", default=str(ROOT / "paper"), help="version folder holding main.tex (gen/ and figures/ are written inside it)")
    ap.add_argument("--no-artifact-copy", action="store_true", help="keep figs_<ID>.tex written by paper_regen_figs.py")
    a = ap.parse_args()
    global GEN, FIG
    GEN = Path(a.paper_dir) / "gen"; FIG = Path(a.paper_dir) / "figures"
    import yaml
    GEN.mkdir(parents=True, exist_ok=True)
    tasks = {t["id"]: t for t in yaml.safe_load(open(ROOT / "paper/eval/tasks.yaml", encoding="utf-8"))}
    runs = Path(a.runs) / a.provider
    nums = db_numbers()
    for tid, t in tasks.items():
        f = runs / f"{tid}.json"
        if not f.exists():
            continue
        rec = json.loads(f.read_text(encoding="utf-8"))
        if rec.get("fatal") or not rec.get("sessions"):
            continue
        if t.get("showcase") or tid in ("B06", "P05", "H03", "S06"):
            (GEN / f"case_{tid}.tex").write_text(render_case(rec, t), encoding="utf-8")
            mcp = render_mcp(rec)
            # on the Codex path the recorded response is a truncated text digest; paper_regen_figs.py writes the real digest
            # from a re-executed call, so an existing file is kept when the recorded response carries nothing useful
            recorded_empty = mcp.split("Tool response")[-1].strip().endswith("{}\n\\end{lstlisting}\n\\end{mcpbox}") or "\n{}\n" in mcp.split("Tool response")[-1]
            if not recorded_empty or not (GEN / f"mcp_{tid}.tex").exists():
                (GEN / f"mcp_{tid}.tex").write_text(mcp, encoding="utf-8")
            if not a.no_artifact_copy:
                copy_artifacts(rec, tid)
    (GEN / "models_table.tex").write_text(models_table(), encoding="utf-8")
    (GEN / "tasks_table.tex").write_text(tasks_table(tasks), encoding="utf-8")
    (GEN / "tools_table.tex").write_text(tools_table(), encoding="utf-8")
    res = Path(a.results)
    if (res / "scores.json").exists():
        tex, agg = benchmark_tables(res)
        (GEN / "benchmark_table.tex").write_text(tex, encoding="utf-8")
        for p, d in agg.items():
            tag = PROV_TAG.get(p, re.sub(r"[^A-Za-z]", "", p).title())
            for k, v in d.items():
                nums[f"bench{tag}{k[0].upper()}{k[1:]}".replace("_", "")] = v
    lines = []
    for k, v in nums.items():
        if isinstance(v, float):
            if any(t in k for t in ("wall", "calls", "Wall", "Calls")):
                vs = f"{v:.0f}"
            elif any(t in k for t in ("fidelity", "control", "pass_rate", "Fidelity", "Control", "Passrate")):
                vs = f"{v:.3f}"
            else:
                vs = f"{v:.2f}" if abs(v) < 100 else f"{v:,.0f}"
        elif isinstance(v, int):
            vs = f"{v:,}"
        else:
            vs = esc(v)
        lines.append(f"\\newcommand{{\\n{k.replace('_', '')}}}{{{vs}}}")
    (GEN / "numbers.tex").write_text("\n".join(lines), encoding="utf-8")
    print("written", sorted(p.name for p in GEN.iterdir()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
