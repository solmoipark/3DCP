# -*- coding: utf-8 -*-
"""Regenerate the tool figures of the showcase tasks from the RECORDED tool arguments (no LLM involved).

  python scripts/paper_regen_figs.py --paper-dir paper/v01 [--provider codex] [--ids P05,P07,B01,J01,M01,H03]

The Codex path only records a digest of each tool result, so the artifact list is incomplete there; re-executing the same
tool call with the same arguments reproduces the figures deterministically (the models and the calculator are
deterministic), with the interface language set to English so that labels are English. Writes
<paper-dir>/figures/<ID>_<name>.png and <paper-dir>/gen/figs_<ID>.tex.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ["PMPREDICT_LANG"] = "en"
os.environ["PYTHONIOENCODING"] = "utf-8"

FIG_TOOLS = {"predict_properties", "flow_curve", "structuration_curve", "assess_buildability", "print_schedule", "design_mix", "design_for_print_job"}
# which figure files of a task go into the paper, in order (None = every image artifact)
PICK = {"P07": ["flow_curve_", "structuration_"], "B01": ["cycle_sweep"], "J01": ["cycle_sweep_job", "pareto"], "J02": ["cycle_sweep"],
        "D01": ["pareto", "parallel_coords"]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper-dir", required=True)
    ap.add_argument("--provider", default="codex")
    ap.add_argument("--ids", default="P05,P07,B01,J01,J02,M01,H03,D01")
    a = ap.parse_args()
    paper = Path(a.paper_dir); fig_dir = paper / "figures"; gen = paper / "gen"
    fig_dir.mkdir(parents=True, exist_ok=True); gen.mkdir(parents=True, exist_ok=True)
    from pmpredict.agent.tools import REGISTRY, call_tool  # noqa: F401
    from pmpredict.agent.tools.registry import ToolContext
    from pmpredict.agent.tools.runtime import get_runtime
    rt = get_runtime()
    for tid in a.ids.split(","):
        f = ROOT / "paper" / "eval" / "runs" / a.provider / f"{tid}.json"
        if not f.exists():
            print("no run for", tid); continue
        rec = json.loads(f.read_text(encoding="utf-8"))
        out_dir = ROOT / "artifacts" / "reports" / "paper_figs" / tid
        if out_dir.exists():
            shutil.rmtree(out_dir)
        ctx = ToolContext(runtime=rt, session_id=f"paper_{tid}", artifact_dir=out_dir)
        images: list[Path] = []
        for s in rec["sessions"]:
            for tr in s["turns"]:
                for c in tr["calls"]:
                    if c["name"] not in FIG_TOOLS or c.get("is_error"):
                        continue
                    if c["name"] in ("design_mix", "design_for_print_job"):
                        args = dict(c["input"]); args["budget"] = dict(args.get("budget") or {}, n_samples=1024)   # same pipeline, faster
                    else:
                        args = c["input"]
                    res = call_tool(c["name"], args, ctx)
                    if not (gen / f"mcp_{tid}.done").exists() and not res.is_error:
                        # real request / response digest for the MCP figure (the Codex path records only a truncated text)
                        sys.path.insert(0, str(ROOT / "scripts"))
                        from paper_render import json_box, result_digest  # noqa: E402
                        req = {"tool": c["name"], "arguments": c["input"]}
                        dig = result_digest(res.to_dict(), 1200)
                        for k in ("job", "mix", "material", "conditions", "warnings", "csv", "artifacts"):
                            dig.pop(k, None)                                # echoes of the request; the page has room for the verdict only
                        order = ["summary", "verdict", "schedule", "predictions", "tau_s0_Pa", "athix_Pa_s", "tau_s_at_max_rest"]
                        dig = {k: dig[k] for k in order if k in dig} | {k: v for k, v in dig.items() if k not in order}
                        while len(json.dumps(dig, ensure_ascii=False, default=str)) > 720 and len(dig) > 2:
                            dig.pop(list(dig)[-1])
                        tex = (r"\begin{mcpbox}{Tool request (client $\rightarrow$ server)}" + "\n" + json_box(req) + "\n" + r"\end{mcpbox}" + "\n"
                               r"\begin{mcpbox}{Tool response (server $\rightarrow$ client, digest)}" + "\n" + json_box(dig, 900) + "\n" + r"\end{mcpbox}")
                        (gen / f"mcp_{tid}.tex").write_text(tex, encoding="utf-8")
                        (gen / f"mcp_{tid}.done").write_text("", encoding="utf-8")
                    for art in res.artifacts:
                        p = Path(art.path)
                        if p.suffix.lower() == ".png" and p.exists() and p not in images:
                            images.append(p)
                    print(f"  {tid} {c['name']}: {len(res.artifacts)} artifacts{' ERROR' if res.is_error else ''}")
        pick = PICK.get(tid)
        chosen = [p for p in images if pick is None or any(k in p.name for k in pick)]
        if pick:
            chosen.sort(key=lambda p: next((i for i, k in enumerate(pick) if k in p.name), 99))
        copied = []
        for p in chosen[:3]:
            dst = fig_dir / f"{tid}_{p.name}"
            shutil.copy(p, dst); copied.append(dst.name)
        if copied:
            w = max(0.3, min(0.95, 0.98 / len(copied)))
            parts = [r"\includegraphics[width=" + f"{w:.2f}" + r"\textwidth]{" + n + "}" for n in copied]
            (gen / f"figs_{tid}.tex").write_text((r"\hfill" + "\n").join(parts) + "\n", encoding="utf-8")
        print(tid, "->", copied)
    return 0


if __name__ == "__main__":
    sys.exit(main())
