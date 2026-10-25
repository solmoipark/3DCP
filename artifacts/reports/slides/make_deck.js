const pptxgen = require("pptxgenjs");
const path = require("path");
const ROOT = "C:/Users/User/3D Printing Concrete Prediction";
const OUT = path.join(ROOT, "artifacts/reports/slides/pmpredict_progress_review.pptx");

const C = { ink: "1F2A2E", muted: "5B6B70", teal: "0E6B6B", tealDark: "0A4F4F", tealSoft: "E3F0EF", sand: "F3F4F1",
            line: "D3D9D6", terra: "B85042", terraSoft: "F6E4E1", ok: "2E6E3E", okSoft: "E6F1E7", amber: "8A5A00", amberSoft: "FBF1DD", white: "FFFFFF" };
const HF = "Cambria", BF = "Calibri";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.author = "Solmoi Park";
pres.title = "pmpredict — literature-driven mix design for 3DCP";

function title(slide, text, sub) {
  slide.addText(text, { x: 0.6, y: 0.35, w: 12.1, h: 0.7, fontFace: HF, fontSize: 30, bold: true, color: C.ink, isTextBox: true, margin: 0 });
  if (sub) slide.addText(sub, { x: 0.6, y: 1.02, w: 12.1, h: 0.4, fontFace: BF, fontSize: 14, color: C.muted, isTextBox: true, margin: 0 });
}
function footer(slide, n) {
  slide.addText(`pmpredict · progress review · 2026-09-30`, { x: 0.6, y: 7.05, w: 8, h: 0.3, fontFace: BF, fontSize: 9, color: C.muted, isTextBox: true, margin: 0 });
  slide.addText(String(n), { x: 12.2, y: 7.05, w: 0.5, h: 0.3, fontFace: BF, fontSize: 9, color: C.muted, align: "right", isTextBox: true, margin: 0 });
}
function stat(slide, x, y, w, big, small, color) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: 1.05, fill: { color: C.white }, line: { color: C.line, width: 0.75 }, rectRadius: 0.08 });
  slide.addText(big, { x: x + 0.15, y: y + 0.08, w: w - 0.3, h: 0.55, fontFace: HF, fontSize: 24, bold: true, color: color || C.teal, isTextBox: true, margin: 0 });
  slide.addText(small, { x: x + 0.15, y: y + 0.6, w: w - 0.3, h: 0.4, fontFace: BF, fontSize: 10.5, color: C.muted, isTextBox: true, margin: 0 });
}
function callout(slide, x, y, w, h, text, tone) {
  const fill = tone === "warn" ? C.amberSoft : tone === "bad" ? C.terraSoft : C.tealSoft;
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { color: fill }, rectRadius: 0.08 });
  slide.addText(text, { x: x + 0.15, y: y + 0.05, w: w - 0.3, h: h - 0.1, fontFace: BF, fontSize: 11.5, color: C.ink, valign: "middle", isTextBox: true, margin: 0 });
}
function bullets(slide, x, y, w, h, items, size) {
  slide.addText(items.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < items.length - 1, paraSpaceAfter: 6 } })),
    { x, y, w, h, fontFace: BF, fontSize: size || 13, color: C.ink, valign: "top", isTextBox: true, margin: 0 });
}

// ---------------------------------------------------------------- 1 title
{
  const s = pres.addSlide();
  s.background = { color: C.tealDark };
  s.addText("pmpredict", { x: 0.8, y: 1.3, w: 11, h: 0.6, fontFace: BF, fontSize: 16, color: "9FD3CF", isTextBox: true, margin: 0, charSpacing: 4 });
  s.addText("Literature-driven mix design for 3D concrete printing", { x: 0.8, y: 1.9, w: 11.5, h: 1.3, fontFace: HF, fontSize: 40, bold: true, color: C.white, isTextBox: true, margin: 0 });
  s.addText("Prediction · inverse design · buildability · AI agent", { x: 0.8, y: 3.25, w: 11, h: 0.5, fontFace: BF, fontSize: 20, color: "CFE6E4", isTextBox: true, margin: 0 });
  s.addText("Three questions the framework answers from 3,274 published studies:\nHow many layers will this mix stand?  ·  Which mix fits this nozzle and height?  ·  What layer cycle time?",
    { x: 0.8, y: 4.2, w: 11.5, h: 0.9, fontFace: BF, fontSize: 14, color: "CFE6E4", isTextBox: true, margin: 0 });
  s.addText("Solmoi Park · Sungkyunkwan University · Project progress review · 30 Sep 2026", { x: 0.8, y: 6.3, w: 11.5, h: 0.4, fontFace: BF, fontSize: 13, color: "9FD3CF", isTextBox: true, margin: 0 });
  s.addText("github.com/solmoipark/3DCP_ERC", { x: 0.8, y: 6.7, w: 11.5, h: 0.35, fontFace: BF, fontSize: 11, color: "9FD3CF", isTextBox: true, margin: 0 });
}

// ---------------------------------------------------------------- 2 pipeline + data
{
  const s = pres.addSlide();
  title(s, "One pipeline from papers to print schedule", "Every block is data the next block consumes; numbers are the current state of the database");
  const blocks = [["Corpus & extraction", "3,274 papers\n1,176 on 3DCP"], ["Normalised DB", "29,626 mixes\n236,199 measurements"], ["Forward models", "19 targets\n+17 3DCP variants"],
                  ["Inverse design", "targets → Pareto\n+ literature analogues"], ["Print labels (print01)", "1,014 papers\n7,420 print runs"], ["Buildability + agent", "physics layer\n16 tools, chat UI"]];
  const bw = 1.85, gap = 0.2, x0 = 0.6, y0 = 1.65;
  blocks.forEach((b, i) => {
    const x = x0 + i * (bw + gap);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: y0, w: bw, h: 1.35, fill: { color: i === 5 ? C.teal : C.white }, line: { color: i === 5 ? C.teal : C.line, width: 0.75 }, rectRadius: 0.08 });
    s.addText(b[0], { x: x + 0.12, y: y0 + 0.1, w: bw - 0.24, h: 0.45, fontFace: BF, fontSize: 12, bold: true, color: i === 5 ? C.white : C.ink, isTextBox: true, margin: 0 });
    s.addText(b[1], { x: x + 0.12, y: y0 + 0.55, w: bw - 0.24, h: 0.7, fontFace: BF, fontSize: 11, color: i === 5 ? "DDEFEE" : C.muted, isTextBox: true, margin: 0 });
    if (i < 5) s.addShape(pres.shapes.RIGHT_ARROW, { x: x + bw + 0.02, y: y0 + 0.55, w: 0.16, h: 0.25, fill: { color: C.line }, line: { color: C.line } });
  });
  // chart: papers per year
  const years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026];
  const all = [34, 47, 86, 109, 158, 211, 293, 366, 407, 478, 553, 412];
  const p3 = [2, 2, 1, 19, 40, 58, 106, 150, 170, 179, 242, 207];
  s.addChart(pres.ChartType.bar, [{ name: "All papers", labels: years.map(String), values: all }, { name: "3DCP papers", labels: years.map(String), values: p3 }],
    { x: 0.6, y: 3.3, w: 6.6, h: 3.5, barDir: "col", barGrouping: "clustered", chartColors: [C.line, C.teal], showLegend: true, legendPos: "t", legendFontSize: 10, legendFontFace: BF,
      showTitle: true, title: "Papers in the database by publication year (2026 partial)", titleFontSize: 11, titleFontFace: BF, titleColor: C.ink,
      catAxisLabelFontSize: 9, valAxisLabelFontSize: 9, catAxisLabelColor: C.muted, valAxisLabelColor: C.muted, valGridLine: { color: "E6EAE8", size: 0.5 }, catGridLine: { style: "none" },
      showValue: false, dataLabelFontSize: 8 });
  bullets(s, 7.6, 3.4, 5.1, 3.4, [
    "Extraction by LLM sub-agents with evidence sentences, machine validation and adjudication; frozen record schema (v1.2.2).",
    "The hard part is normalisation: kg/m³, % of binder, parts, molarity, solution vs solid — all mapped to mass ratios relative to the binder. 28,001 of 29,626 mixes (94 %) normalise.",
    "Rheology pitfalls kept as data, not averaged away: 69 % of static-yield rows lack a rest time; text-vs-table conflicts stored as discrepancies.",
    "print01 adds the missing link: what was actually printed, with what nozzle and speed, and whether it stood."], 12.5);
  footer(s, 2);
  s.addNotes("Walk left to right. Emphasise that the print labels are new since the last review and are what makes the buildability layer calibratable.");
}

// ---------------------------------------------------------------- 3 prediction + inverse design
{
  const s = pres.addSlide();
  title(s, "Forward models and inverse design", "LightGBM per target, cross-validated by paper (GroupKFold), 80 % prediction intervals from split-conformal calibration");
  const rows = [
    [{ text: "Target", options: { bold: true } }, { text: "n (papers)", options: { bold: true } }, { text: "R² log", options: { bold: true } }, { text: "Spearman", options: { bold: true } }, { text: "PI cover.", options: { bold: true } }],
    ["Compressive strength", "47,125 (1,634)", "0.45", "0.69", "80 %"],
    ["Flexural strength", "6,148 (452)", "0.29", "0.46", "80 %"],
    ["Static yield stress", "1,728 (241)", "0.40", "0.62", "80 %"],
    ["Plastic viscosity", "1,817 (274)", "0.40", "0.65", "80 %"],
    ["Dynamic yield stress", "2,032 (294)", "0.25", "0.54", "80 %"],
    ["Initial setting time", "1,747 (348)", "0.34", "0.53", "80 %"],
    ["Athix (structuration)", "692 (124)", "0.04  weak", "0.22", "80 %"],
    ["Flow table spread", "1,693 (290)", "−0.03  weak", "0.08", "80 %"],
  ];
  s.addTable(rows.map((r, i) => r.map(c => (typeof c === "string" ? { text: c, options: { color: i === 0 ? C.ink : (c.includes("weak") ? C.terra : C.ink) } } : c))),
    { x: 0.6, y: 1.6, w: 6.4, colW: [2.2, 1.4, 1.0, 0.9, 0.9], fontFace: BF, fontSize: 11, border: { type: "solid", color: C.line, pt: 0.5 }, fill: { color: C.white }, rowH: 0.3, margin: 0.04 });
  s.addText("Per-model quality (out-of-fold, log scale for skewed targets). 36 models incl. 3DCP-specific variants chosen automatically when better.",
    { x: 0.6, y: 4.4, w: 6.4, h: 0.5, fontFace: BF, fontSize: 10, color: C.muted, isTextBox: true, margin: 0 });
  s.addImage({ path: path.join(ROOT, "artifacts/reports/agent/20260915-133838-44d7/design_clinker_min_3dcp/pareto.png"), x: 7.4, y: 1.55, w: 5.3, h: 3.35 });
  s.addText("Inverse design: fc,28 ≥ 40 MPa and τs 1–4 kPa, minimise clinker. Sobol sweep → probabilistic screening → refinement; 170 of 4,096 samples feasible; each candidate paired with its nearest published mix.",
    { x: 7.4, y: 4.92, w: 5.3, h: 0.7, fontFace: BF, fontSize: 10, color: C.muted, isTextBox: true, margin: 0 });
  callout(s, 0.6, 5.1, 6.4, 1.7,
    "Honest limit. Rheology models are order-of-magnitude tools: on 20 lab pastes (Kim et al.) the 3DCP-flagged static-yield model over-predicted 32×, the general model 1.9×. The flag had learned the rest-time protocol, not the material. Rule adopted everywhere downstream: quote q50 [q10, q90], flag weak models, treat retrieved literature mixes as the primary evidence.", "warn");
  bullets(s, 7.4, 5.75, 5.3, 1.1, ["Applicability-domain score blocks extrapolation.", "Objectives: clinker fraction, CO₂, cost (placeholder tables, user-replaceable)."], 11.5);
  footer(s, 3);
  s.addNotes("Table values are from artifacts/manifest.json. The Kim comparison is artifacts/reports/external/kim2026_ppt_comparison.md.");
}

// ---------------------------------------------------------------- 4 print01
{
  const s = pres.addSlide();
  title(s, "print01: turning printed evidence into labels", "1,014 3DCP papers read for what was printed — nozzle, layer height, speed, cycle time, height reached, failure mode, the authors' verdict and the sentence that says so");
  stat(s, 0.6, 1.6, 2.9, "7,420", "print runs labelled (928 papers with ≥1 run)");
  stat(s, 3.7, 1.6, 2.9, "841", "stack-until-failure tests (height at collapse)");
  stat(s, 6.8, 1.6, 2.9, "7,053", "runs keyed to a normalised mix (95 %)");
  stat(s, 9.9, 1.6, 2.85, "29 → 1,014", "papers with structured buildability data, before → after", C.terra);
  const t = [
    [{ text: "outcome \\ label", options: { bold: true } }, { text: "printable", options: { bold: true } }, { text: "borderline", options: { bold: true } }, { text: "non-printable", options: { bold: true } }],
    ["printable", "5,286", "513", "11"], ["collapsed", "297 *", "193", "451"], ["extrusion failure", "0", "73", "316"], ["tearing / segregation", "0", "84", "67"], ["unclear / not printed", "3", "69", "57"]];
  s.addTable(t, { x: 0.6, y: 2.95, w: 6.2, colW: [2.3, 1.3, 1.3, 1.3], fontFace: BF, fontSize: 11, border: { type: "solid", color: C.line, pt: 0.5 }, rowH: 0.32, margin: 0.04, align: "left" });
  s.addText("* collapse inside a stack-until-failure test can still be 'printable' when the authors call the mix buildable — the label follows the authors, the outcome follows the geometry.",
    { x: 0.6, y: 5.0, w: 6.2, h: 0.6, fontFace: BF, fontSize: 10, color: C.muted, isTextBox: true, margin: 0 });
  s.addChart(pres.ChartType.bar, [{ name: "filled", labels: ["mix linked", "print speed", "layer height", "layers reached", "height reached", "cycle time", "open time"], values: [95.1, 69.9, 60.6, 43.5, 26.6, 17.6, 5.2] }],
    { x: 7.2, y: 2.9, w: 5.5, h: 2.9, barDir: "bar", chartColors: [C.teal], showLegend: false, showTitle: true, title: "Field fill rate across 7,420 runs (%)", titleFontSize: 11, titleFontFace: BF, titleColor: C.ink,
      showValue: true, dataLabelPosition: "outEnd", dataLabelFontSize: 9, dataLabelColor: C.ink, catAxisLabelFontSize: 10, valAxisLabelFontSize: 9, catAxisLabelColor: C.ink, valAxisLabelColor: C.muted,
      valAxisMinVal: 0, valAxisMaxVal: 100, valGridLine: { color: "E6EAE8", size: 0.5 }, catGridLine: { style: "none" } });
  bullets(s, 0.6, 5.9, 12.1, 1.1, [
    "Side table beside the frozen record schema; every value carries a verbatim quote and locator; 1,507 rheology-protocol rows (test class, rest time) captured in the same pass.",
    "Sparse fields are the honest picture of the literature: only 349 runs state both a cycle time and a rest-time protocol, so the physics layer must carry structuration itself."], 12);
  footer(s, 4);
  s.addNotes("Numbers from master/print_process.db merge (2026-09-14). Printer statistics: 721 papers state nozzle size (median 20 mm), 539 gantry, 148 robot arm.");
}

// ---------------------------------------------------------------- 5 buildability
{
  const s = pres.addSlide();
  title(s, "Buildability: physics first, literature-calibrated", "A print job (nozzle, geometry, speed, open time) × a fresh state (τs(0), Athix) → verdict, maximum layers, feasible cycle-time window, required rheology");
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 1.6, w: 5.9, h: 2.25, fill: { color: C.sand }, line: { color: C.sand }, rectRadius: 0.08 });
  s.addText([
    { text: "Plastic collapse (Roussel)  ", options: { bold: true } }, { text: "ρ g h n ≤ √3 · [τs(0) + Athix · n · tc]  →  n_max, critical cycle time tc* = ρ g h / (√3 Athix)", options: { breakLine: true } },
    { text: "Elastic buckling (Suiker)  ", options: { bold: true } }, { text: "l_cr = (7.84 · E · t_w² / 12 ρ g)^(1/3), E = k · τs(t) for a free straight wall", options: { breakLine: true } },
    { text: "Open time  ", options: { bold: true } }, { text: "start + n · tc ≤ open time  →  upper bound of the cycle-time window", options: { breakLine: true } },
    { text: "Inverse  ", options: { bold: true } }, { text: "requirement becomes a target 'τs at rest = print duration ≥ SF · ρ g H / √3' for the existing design engine" }],
    { x: 0.8, y: 1.7, w: 5.5, h: 2.05, fontFace: BF, fontSize: 11.5, color: C.ink, paraSpaceAfter: 6, isTextBox: true, margin: 0 });
  s.addImage({ path: path.join(ROOT, "artifacts/reports/slides/cycle_sweep_en.png"), x: 0.6, y: 3.95, w: 4.2, h: 2.55 });
  s.addText("Cycle-time sweep, 600 mm two-filament wall, τs 3 kPa, Athix 1 Pa/s: stability needs ≥160 s per layer, the 60 min open time allows ≤75 s — the window is empty. The tool then reports the τs(0) or Athix that would open it (7.8 kPa or 2.7 Pa/s).",
    { x: 4.9, y: 4.0, w: 1.6, h: 2.5, fontFace: BF, fontSize: 9.5, color: C.muted, isTextBox: true, margin: 0 });
  s.addImage({ path: path.join(ROOT, "artifacts/reports/slides/R_fail_hist.png"), x: 7.0, y: 1.6, w: 5.7, h: 3.65 });
  callout(s, 7.0, 5.35, 5.7, 1.4,
    "Calibration on 146 stack-until-failure collapses (37 papers): stacks fail at a median 1.39× the static Roussel height (IQR 0.64–2.87) — the structuration gained during the print. τs alone separates collapse from success with AUC 0.59 only, so the physics route with Athix is the primary verdict and the empirical distribution is shown as a probability band.", "warn");
  footer(s, 5);
  s.addNotes("Extrudability windows from printable runs: static yield p10/50/90 = 273/1186/4920 Pa, viscosity 2.7/12/57 Pa·s; failed extrusions median 67 Pa·s. Layer height median 0.5× nozzle, width 1.2× nozzle.");
}

// ---------------------------------------------------------------- 6 agent
{
  const s = pres.addSlide();
  title(s, "The AI agent: one conversation instead of seven forms", "Natural-language requests → tool calls into the package → every number quoted from a tool result with its 80 % interval");
  // architecture column
  const arch = [["Tool registry", "16 tools: predict, curves, literature, inverse design, buildability, schedule, SQL (read-only), report, memory"],
                ["LLM backends", "Anthropic API · OpenAI API · Claude subscription (Agent SDK) · ChatGPT subscription (Codex CLI) — auto-detected"],
                ["Guardrails", "no invented numbers · weak-model flags · extrapolation flags · slow tools confirmed once · SQL SELECT-only"],
                ["Memory", "sessions resume; durable notes; every artifact (CSV, PNG, report) downloadable"]];
  arch.forEach((a, i) => {
    const y = 1.6 + i * 1.3;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y, w: 4.3, h: 1.15, fill: { color: C.white }, line: { color: C.line, width: 0.75 }, rectRadius: 0.08 });
    s.addText(a[0], { x: 0.75, y: y + 0.08, w: 4.0, h: 0.32, fontFace: BF, fontSize: 12.5, bold: true, color: C.teal, isTextBox: true, margin: 0 });
    s.addText(a[1], { x: 0.75, y: y + 0.42, w: 4.0, h: 0.7, fontFace: BF, fontSize: 10.5, color: C.ink, isTextBox: true, margin: 0 });
  });
  // chat mock (verbatim from a live run on 30 Sep 2026)
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 5.2, y: 1.6, w: 7.5, h: 4.55, fill: { color: C.sand }, line: { color: C.line, width: 0.75 }, rectRadius: 0.1 });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 5.45, y: 1.8, w: 7.0, h: 0.75, fill: { color: C.white }, line: { color: C.line, width: 0.5 }, rectRadius: 0.1 });
  s.addText("25 mm nozzle, 600 mm tall wall, 1.5 m long, 2 filaments, 50 mm/s, open time 60 min. Material: static yield 3 kPa, Athix 1 Pa/s. Is it buildable? Give the layer cycle time window and the closest published prints.",
    { x: 5.6, y: 1.85, w: 6.7, h: 0.65, fontFace: BF, fontSize: 10, color: C.ink, isTextBox: true, margin: 0 });
  const tools = ["assess_buildability — non_printable (elastic_buckling); n_max 34 / target 48", "print_schedule — no feasible window", "similar_prints — 8 published prints"];
  tools.forEach((t, i) => {
    s.addShape(pres.shapes.OVAL, { x: 5.6, y: 2.72 + i * 0.3, w: 0.16, h: 0.16, fill: { color: C.ok }, line: { color: C.ok } });
    s.addText(t, { x: 5.85, y: 2.65 + i * 0.3, w: 6.5, h: 0.3, fontFace: "Courier New", fontSize: 9.5, color: C.muted, isTextBox: true, margin: 0 });
  });
  s.addText([
    { text: "Verdict: non-printable as specified. ", options: { bold: true, color: C.terra } },
    { text: "Governing mode: elastic buckling of the free 2-filament wall at layer 17 (~213 mm); plastic collapse would follow at layer 34 (~423 mm). Empirical collapse probability ≈ 0.70.", options: { breakLine: true } },
    { text: "Cycle-time window: ", options: { bold: true } }, { text: "stability needs tc ≥ 160 s, open time allows ≤ 75 s → empty. Required τs(0) ≈ 7.8 kPa at a 60 s cycle, or Athix ≥ 2.7 Pa/s (vs 1.0).", options: { breakLine: true } },
    { text: "Options: ", options: { bold: true } }, { text: "raise Athix (accelerator, lower w/b, thixotropy enhancer); thicker or braced wall removes buckling; slow to 19–40 mm/s.", options: { breakLine: true } },
    { text: "Closest prints: ", options: { bold: true } }, { text: "straight walls with 30 mm nozzle, τs 3.0–3.6 kPa, Athix 1.6–2.0 Pa/s reached 450 mm and were printable (Cem. Concr. Res. 2026); 25 mm hollow cylinders at Athix 0.5–0.6 collapsed at 590–740 mm." }],
    { x: 5.6, y: 3.65, w: 6.85, h: 2.4, fontFace: BF, fontSize: 10.5, color: C.ink, paraSpaceAfter: 5, valign: "top", isTextBox: true, margin: 0 });
  s.addText("Live run, Claude subscription backend, 30 Sep 2026 — text abridged, numbers verbatim.", { x: 5.2, y: 6.2, w: 7.5, h: 0.25, fontFace: BF, fontSize: 8.5, color: C.muted, italic: true, isTextBox: true, margin: 0 });
  footer(s, 6);
  s.addNotes("Lab members run it locally on their own Claude/ChatGPT subscription (no API key); the public web deployment uses an API key in Streamlit Secrets. Guide: docs/AGENT_GUIDE.md.");
}

// ---------------------------------------------------------------- 7 validation / limits / next
{
  const s = pres.addSlide();
  title(s, "Where it stands, what it cannot do yet, what comes next");
  const cols = [
    ["Verified", C.okSoft, C.ok, ["39 unit tests: schema consistency, SQL guard, form-rule parity, secrets handling, end-to-end with a scripted backend",
      "7 live scenarios with the real model: prediction, buildability, DB query, retrieval, session resume + report, inverse design (34 s), web chat",
      "External checks: Kim et al. rheology data; 146 published stack-to-failure collapses",
      "Typical turn 10–35 s; $0.03–0.21 API-equivalent per turn"]],
    ["Limits", C.amberSoft, C.amber, ["Rheology intervals span a decade: literature static yield mixes rest-time protocols",
      "Linear structuration law over-predicts beyond ~90 min prints",
      "Free-wall buckling is the most conservative case; closed or braced paths need the toggle",
      "No trial-print validation of the buildability verdict yet; cost/CO₂ tables are placeholders"]],
    ["Next", C.tealSoft, C.teal, ["Normalise static-yield protocols (rest time, device) to tighten the rheology models",
      "Calibrate the collapse ratio with our own trial prints and feed lab data into the DB",
      "Lab roll-out: clone and run on personal subscriptions; public web app on an API key with viewer restriction",
      "Experimental validation of agent-proposed mixes for one target geometry"]]];
  cols.forEach((c, i) => {
    const x = 0.6 + i * 4.1;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.5, w: 3.9, h: 4.9, fill: { color: c[1] }, line: { color: c[1] }, rectRadius: 0.1 });
    s.addText(c[0], { x: x + 0.25, y: 1.65, w: 3.4, h: 0.45, fontFace: HF, fontSize: 20, bold: true, color: c[2], isTextBox: true, margin: 0 });
    bullets(s, x + 0.25, 2.25, 3.4, 4.0, c[3], 13);
  });
  footer(s, 7);
  s.addNotes("Close with the ask: trial-print campaign for one geometry (e.g. 300 mm hollow cylinder, 20 mm nozzle) to calibrate R and validate one agent-designed mix.");
}

pres.writeFile({ fileName: OUT }).then(f => console.log("wrote", f));
