# Schematic figure briefs for the 3DCP-Agent manuscript (v02)

Purpose: concept schematics for a journal paper (Automation in Construction) on an LLM agent that gives
natural-language access to literature-trained property models, inverse mix design and buildability
assessment for 3D concrete printing (3DCP). Audience: civil-engineering researchers. Style for all figures:
clean flat vector-like scientific schematic, white background, restrained palette (one muted blue for
the agent/LLM layer, one muted orange for computational tools, grey for data, a single green accent for the
result), thin dark outlines, simple arrows, short sans-serif labels only (the exact label text is given
below; no other text), no logos, no people, no photographs, no decorative 3D rendering, no fake plots with
numbers, no numbers at all unless listed. Aspect ratio 16:9 unless stated. Output role: concept draft.

Every label listed under "Labels" must appear exactly as written (short, spelled exactly). Nothing else may be
written in the image. If a label does not fit, drop it rather than inventing another.

---

## Figure 1 — System architecture (replaces the current block diagram)

One-sentence message: a language model plans and explains; every number comes from computational tools
that read two databases.

Reading order: top to bottom, five horizontal bands connected by downward arrows; a thin return arrow on the
right from the bottom band back to the top band labelled "results".

Bands and labels (exactly these):
1. "User" — a chat bubble icon with the label "natural-language request" (web, terminal or MCP client are
   NOT to be written; just one chat bubble).
2. "LLM agent" — a rounded box containing three small tiles: "system prompt", "tool selection", "session memory".
3. "Tool registry" — a slim band with the label "16 tools, one schema" and three small tags: "Anthropic", "OpenAI", "MCP".
4. "Computational layer" — five tiles in a row: "property models", "inverse design", "buildability", "literature retrieval", "SQL (read-only)".
5. "Data" — two cylinders: "literature database" and "print-process database".

Focal element: band 2 (the agent) slightly larger. Exclude: product names, student bundle, environment
details, any numbers other than "16".

Aspect ratio 4:3. File name: fig1_architecture.

---

## Figure 2 — Print-planning conversation as tool calls (replaces the current sequence diagram)

One-sentence message: one conversation moves from a job description to a verdict, then to a mix design, then
to a report, each step being a tool call.

Reading order: left to right, three stages separated by light vertical dividers.

Stage A "Assess": left, a small printed wall icon with a nozzle above it and the labels "job" (height,
nozzle, speed, open time written as tiny icons, no text) and "material" (a small rheometer/vane icon).
Arrow to a tool box "assess_buildability". Output icons: a traffic-light style verdict with "verdict",
a small time-window bar with "cycle-time window".

Stage B "Design": arrow from stage A to a tool box "design_for_print_job"; inside or beside it a small
funnel icon with the label "required rheology" feeding a cloud of candidate dots with "candidates",
and a small re-check loop arrow back to the wall icon labelled "re-assess".

Stage C "Report": arrow to a tool box "save_report" with a document icon.

Along the top a thin bar labelled "LLM agent" spanning all stages with small downward arrows into each tool
box; along the bottom a thin bar "computational layer".

Exclude: numbers, chat text, logos. Aspect ratio 16:9. File name: fig2_workflow.

---

## Figure 3 (new) — Inverse mix design pipeline

One-sentence message: inverse design samples the composition space, predicts each target with an
interval, keeps candidates whose targets are likely satisfied, and refines them.

Reading order: left to right, six steps as rounded tiles connected by arrows, with a loop arrow from the last
step back to step 3 labelled "refine".

Steps and labels (exactly):
1. "targets + search space" — an icon of three sliders (bounds) and a small bar with lower/upper markers.
2. "Sobol sample" — a scatter of evenly spread points in a square.
3. "predict with intervals" — a small vertical bar with a central dot and whiskers (one interval), repeated
   three times for three targets, no numbers.
4. "probabilistic screening" — the same intervals against a shaded target band; points inside the band kept,
   outside greyed out; label "p(feasible)".
5. "non-dominated sort" — a small Pareto-front sketch (dots with a front line), labels "clinker" and "feasibility" on the two axes.
6. "DE refinement" — a few dots converging toward the front, label "candidates".
Right end: an output card with "ranked mixes", "analogues" (small stack of paper icons) and "applicability".

Below the pipeline, a thin second lane labelled "job-based variant" with two added tiles: "required τs at print time"
(use the exact text "required tau_s at print time") feeding step 1, and "re-assess against job" after step 6.

Exclude: numbers, chemical formulas, equations. Aspect ratio 16:9. File name: fig3_inverse_design.

---

## Figure 4 (new) — Buildability criteria

One-sentence message: a printed stack stands while the strength gained during printing outpaces the
self-weight added by each layer; slender walls can buckle first; the open time caps the schedule.

Composition: three panels side by side, labelled (a), (b), (c) in the top-left corners.

(a) "plastic collapse": a stack of printed layers (8–10 rounded rectangles), the bottom layer highlighted,
a downward block arrow on top labelled "self-weight", and to the right a small graph with time on the
x-axis (label "time") and a rising straight line labelled "yield stress grows" with a second line
"load grows" crossing it; mark the crossing with a small circle labelled "limit". No numbers.

(b) "elastic buckling": a tall slender wall shown in side view bowing sideways (slightly curved), base
clamped (hatched ground), label "slender wall", a small double-arrow for wall thickness labelled
"thickness".

(c) "open time": a horizontal time bar from "mixing" to "open time"; within it a shaded window labelled
"feasible cycle time"; left of the window a label "too fast: collapse", right of the window "too slow: open time".

Exclude: numbers, equations, logos. Aspect ratio 16:9. File name: fig4_buildability.

---

## Figure 5 (new) — Benchmark scoring

One-sentence message: each task is run in a fresh session and scored automatically on what the agent called,
what it extracted, whether database answers match the ground truth, and whether every reported number can be
traced to a tool result.

Reading order: left to right.

Left: a card "task" with a short prompt line icon (no text) and small tags "expected tools", "expected
arguments", "ground truth".
Centre: a box "fresh session" containing the LLM icon connected to tool icons; below it a recorder icon
"recorded calls + answer".
Right: four check tiles in a column, each with a check-mark box: "tool selection", "parameter checks",
"ground truth", "numeric fidelity". Beside the last tile a small diagram: numbers in the answer (small
circles) linked by thin lines to numbers in tool results (small squares); one unlinked circle marked with a
question mark; a label "chance-match control" with a dashed link to a different task's results.

Exclude: numbers, model names, logos. Aspect ratio 16:9. File name: fig5_benchmark.
