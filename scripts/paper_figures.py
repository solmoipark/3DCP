# -*- coding: utf-8 -*-
"""Publication figures (matplotlib). Journal contract: Arial/Helvetica 7-8 pt, 90 mm (single) or 190 mm (double) widths,
vector PDF with editable text (fonttype 42) plus 600 dpi PNG, panel letters, one axis per panel, fixed categorical colours.

  python scripts/paper_figures.py [--paper-dir paper/v03] [models] [bench] [rfail]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "paper" / "figures"
MM = 1 / 25.4
SINGLE, DOUBLE = 90 * MM, 190 * MM
# Okabe-Ito in fixed order; one colour per model/series, never cycled
OI = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9"]
INK, MUTED, GRID = "#1a1a1a", "#666666", "#DDDDDD"
mpl.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"], "font.size": 7,
    "axes.titlesize": 7.5, "axes.labelsize": 7, "xtick.labelsize": 6.5, "ytick.labelsize": 6.5, "legend.fontsize": 6.5,
    "axes.spines.right": False, "axes.spines.top": False, "axes.linewidth": 0.6, "axes.edgecolor": INK,
    "xtick.major.width": 0.6, "ytick.major.width": 0.6, "xtick.major.size": 2.5, "ytick.major.size": 2.5,
    "axes.grid": False, "legend.frameon": False, "pdf.fonttype": 42, "svg.fonttype": "none", "figure.dpi": 150,
})


def save(fig, name: str):
    fig.savefig(FIG / f"{name}.pdf", bbox_inches="tight", pad_inches=0.02)
    fig.savefig(FIG / f"{name}.png", dpi=600, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    print(name)


def panel(ax, letter: str, dx=-0.18, dy=1.02):
    ax.text(dx, dy, letter, transform=ax.transAxes, fontsize=8.5, fontweight="bold", va="bottom", ha="left")


def grid_y(ax):
    ax.yaxis.grid(True, color=GRID, lw=0.5); ax.set_axisbelow(True)


def grid_x(ax):
    ax.xaxis.grid(True, color=GRID, lw=0.5); ax.set_axisbelow(True)


# ----------------------------------------------------------------------------------------------- model quality
def fig_models():
    man = json.loads((ROOT / "artifacts" / "manifest.json").read_text(encoding="utf-8"))["models"]
    gen = {m["target"]: m for m in man.values() if m.get("variant") == "general"}
    tdc = {m["target"]: m for m in man.values() if m.get("variant") == "3dcp"}
    order = sorted(gen, key=lambda t: -(gen[t].get("spearman") or 0))
    y = np.arange(len(order))
    fig, axes = plt.subplots(1, 3, figsize=(DOUBLE, 95 * MM), sharey=True, gridspec_kw={"width_ratios": [1.15, 1.0, 0.85], "wspace": 0.08})
    for ax, key in zip(axes, ("spearman", "r2_log", "n_train")):
        for i, t in enumerate(order):
            g, d = gen.get(t), tdc.get(t)
            if g and g.get(key) is not None:
                ax.plot(g[key], i, "o", color=OI[0], ms=4.2, zorder=3, mec="white", mew=0.5)
            if d and d.get(key) is not None:
                ax.plot(d[key], i, "s", color=OI[1], ms=3.8, zorder=3, mfc="white", mew=1.1)
        grid_x(ax)
    axes[0].set_xlabel("Spearman rank correlation"); axes[0].axvline(0, color=INK, lw=0.6); axes[0].set_xlim(-0.75, 0.85)
    axes[1].set_xlabel("$R^2$ in log space"); axes[1].axvline(0, color=INK, lw=0.6); axes[1].axvline(0.15, color=MUTED, lw=0.6, ls="--"); axes[1].set_xlim(-0.85, 0.7)
    axes[1].text(0.16, len(order) - 0.6, "weak-model\nthreshold", fontsize=6, color=MUTED, va="bottom", ha="left")
    axes[2].set_xlabel("training rows"); axes[2].set_xscale("log")
    axes[0].set_yticks(y); axes[0].set_yticklabels([t.replace("_", " ") for t in order]); axes[0].invert_yaxis()
    axes[0].plot([], [], "o", color=OI[0], label="general model"); axes[0].plot([], [], "s", color=OI[1], mfc="white", mew=1.1, label="3DCP-specific model")
    axes[0].legend(loc="upper left", bbox_to_anchor=(0.0, 1.0), handletextpad=0.3)
    for ax, letter in zip(axes, "abc"):
        panel(ax, letter, dx=(-0.95 if letter == "a" else -0.12))
        ax.tick_params(axis="y", length=0)
    fig.subplots_adjust(left=0.22, right=0.99, top=0.93, bottom=0.12)
    save(fig, "fig_models")


# ----------------------------------------------------------------------------------------------- benchmark
GROUP_LABEL = {"predict": "forward prediction", "curves": "rheology curves", "retrieve": "literature retrieval", "design": "inverse design",
               "buildability": "buildability / schedule", "job_design": "job to mix", "sql": "database questions", "sql_guard": "write attempt",
               "hallucination": "unsupported requests", "memory": "durable memory"}
PROV_ORDER = ["codex", "codex_sol", "codex_luna", "codex_61sol", "codex_56sol", "claude_sdk", "anthropic", "openai"]
DEFAULT_MODEL = {"codex": "gpt-6-astra", "codex_sol": "gpt-6-sol", "codex_luna": "gpt-6-luna", "codex_61sol": "gpt-6.1-sol", "codex_56sol": "gpt-5.6-sol",
                 "claude_sdk": "claude-sonnet-5"}


def fig_bench(results=ROOT / "paper/eval/results"):
    import pandas as pd
    df = pd.DataFrame(json.loads((results / "scores.json").read_text(encoding="utf-8")))
    provs = sorted(set(df["provider"]), key=lambda p: PROV_ORDER.index(p) if p in PROV_ORDER else 9)[:6]
    cols = {p: c for p, c in zip(provs, OI)}
    labels = {p: (str(df[df["provider"] == p]["model"].iloc[0]) or DEFAULT_MODEL.get(p, p)) for p in provs}
    groups = [g for g in GROUP_LABEL if g in set(df["group"])]
    fig, axes = plt.subplots(1, 3, figsize=(DOUBLE, 80 * MM), gridspec_kw={"width_ratios": [1.25, 1.0, 1.0], "wspace": 0.42})
    # (a) median wall time per group, dot plot (one marker per model, fixed colour)
    ax = axes[0]
    y = np.arange(len(groups))
    for i, p in enumerate(provs):
        vals = [df[(df["group"] == g) & (df["provider"] == p)]["wall_s"].median() for g in groups]
        ax.plot(vals, y + (i - (len(provs) - 1) / 2) * 0.12, "o", color=cols[p], ms=3.6, mec="white", mew=0.4, label=labels[p], zorder=3)
    ax.set_yticks(y); ax.set_yticklabels([GROUP_LABEL[g] for g in groups]); ax.invert_yaxis(); ax.tick_params(axis="y", length=0)
    ax.set_xlabel("median wall time per task (s)"); ax.set_xlim(0, None); grid_x(ax)
    ax.legend(loc="lower right", handletextpad=0.3, borderaxespad=0.2)
    panel(ax, "a", dx=-0.75)
    # (b) wall-time ECDF
    ax = axes[1]
    for p in provs:
        w = np.sort(df[df["provider"] == p]["wall_s"].values)
        ax.step(w, np.arange(1, len(w) + 1) / len(w), where="post", color=cols[p], lw=1.3)
    ax.set_xscale("log"); ax.set_xticks([10, 20, 50, 100, 200]); ax.set_xticklabels(["10", "20", "50", "100", "200"]); ax.minorticks_off()
    ax.set_xlabel("wall time per task (s)"); ax.set_ylabel("fraction of tasks"); ax.set_ylim(0, 1.02); grid_y(ax)
    panel(ax, "b")
    # (c) tool calls per task, ECDF
    ax = axes[2]
    for p in provs:
        c = np.sort(df[df["provider"] == p]["n_calls"].values)
        ax.step(c, np.arange(1, len(c) + 1) / len(c), where="post", color=cols[p], lw=1.3)
    ax.set_xlabel("tool calls per task"); ax.set_ylabel("fraction of tasks"); ax.set_ylim(0, 1.02); ax.set_xlim(0, None); grid_y(ax)
    panel(ax, "c")
    fig.subplots_adjust(left=0.2, right=0.99, top=0.92, bottom=0.17)
    save(fig, "fig_bench")


# ----------------------------------------------------------------------------------------------- collapse ratio
def fig_rfail():
    cal = json.loads((ROOT / "configs" / "buildability_calibration.json").read_text(encoding="utf-8"))["R_fail"]
    R = np.array(cal["ecdf_R"], dtype=float)
    fig, ax = plt.subplots(figsize=(SINGLE, 62 * MM))
    ax.step(R, np.arange(1, len(R) + 1) / len(R), where="post", color=OI[0], lw=1.4)
    ax.axvline(1.0, color=INK, lw=0.6, ls="--")
    ax.text(0.93, 0.03, "R = 1, static criterion ", fontsize=6.5, color=INK, ha="right", va="bottom")
    ax.axvline(cal["p50"], color=OI[1], lw=0.9)
    ax.text(cal["p50"], 0.97, f" median {cal['p50']:.2f}", fontsize=6.5, color=OI[1], ha="left", va="top")
    ax.set_xscale("log"); ax.set_xticks([0.01, 0.1, 1, 10, 100]); ax.set_xticklabels(["0.01", "0.1", "1", "10", "100"]); ax.minorticks_off()
    ax.set_xlabel(r"$R_{\mathrm{fail}} = \rho g H_{\mathrm{collapse}} \,/\, (\sqrt{3}\,\tau_s)$")
    ax.set_ylabel("empirical cumulative fraction"); ax.set_ylim(0, 1.02); grid_y(ax)
    ax.set_title(f"{cal['n']} stack-to-failure collapses from {cal['n_papers']} papers", fontsize=7, color=MUTED, loc="left")
    fig.subplots_adjust(left=0.14, right=0.98, top=0.9, bottom=0.2)
    save(fig, "fig_rfail")


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--paper-dir" in args:
        i = args.index("--paper-dir"); FIG = Path(args[i + 1]) / "figures"; FIG.mkdir(parents=True, exist_ok=True); del args[i:i + 2]
    what = args or ["models", "rfail", "bench"]
    for w in what:
        {"models": fig_models, "bench": fig_bench, "rfail": fig_rfail}[w]()
