# Image-generation provenance

These five files are AI-generated concept drafts requested in BRIEF.md. They were checked visually after every generation. Three attempts were made per figure (15 calls total); the third attempt was selected for each figure. No raster retouching, text replacement, resizing or drawing-code substitution was performed. This task did not edit main.tex or write project files outside figures/ai/.

Workspace observation: main.tex changed during generation outside this task's write operations. Its initial SHA-256 was 971BFCF4C18AD8B26E8335B18178196D782259FEF4594F15F930B0E7DE72C8EE, and its final observed SHA-256 was 5F68B3199FEB0DD3C66D65D0611D5BFF5FD28D322CCF517324B79B2F16C02665. No attempt was made to modify or revert it.

## Tool disclosure and common limitations

- Callable tool: `image_gen.imagegen` (exposed in orchestration as `image_gen__imagegen`), built-in image generation.
- Image model name/version: **not reported by the tool**. Tool version: **not reported**. The response supplies only `image_url` and `output_hint`; it does not identify the underlying model. No model/version has been inferred from skill documentation.
- Generation date for all attempts: **2026-10-17, Asia/Seoul (UTC+09:00)**.
- Requested quality: high quality, 2K, opaque white background. The tool interface has no explicit size or quality parameter; these requirements were sent in the prompt. All calls used `transparent_background: false`, without reference images.
- **The 2K requirement was not met by the tool after three attempts per figure.** Native delivered sizes are 1448 x 1086 for Figure 1, and 1672 x 941 for Figures 2–5. The latter ratio differs slightly from exact 16:9 (about 0.053%). These are the original generated PNGs, not upscaled 2K files.
- Strict flat-color styling was not fully met: mild gradient/texture shading remains. Other remaining limitations are listed individually below.
- QA was direct visual inspection against the brief, including label-by-label comparison, exclusion checks and arrow/panel order. It is not an OCR certificate or experimental/scientific validation. Line wraps at spaces were accepted; literal underscores and punctuation were checked.

## Figure 1: fig1_architecture.png

- Tool name: `image_gen.imagegen`.
- Underlying image model and version: not reported. Tool version: not reported.
- Generation date: 2026-10-17 (Asia/Seoul).
- Attempts: **3**. Selected attempt: **3**.
- Dimensions: **1448 x 1086 pixels**.
- Source artifact: `C:\Users\User\.codex\generated_images\01a1457a-7821-7ca0-8350-3d8f43612018\exec-86a21bc2-89bd-4a2e-accd-dea32f89f19f.png`.
- Attempt review: Attempt 1: complete labels; gradients and sub-2K resolution. Attempt 2: complete labels, but registry too tall; gradients and sub-2K resolution. Attempt 3 selected: improved band proportions and palette assignment; remaining issues below.
- QA note: All 21 required labels are present and visually spelled exactly. Only allowed numeric text '16' appears. Five bands read top to bottom; the enlarged agent band, five computational tiles, two databases and upward results return are present. No extra text, logos, people, photographs or decorative 3D rendering observed. Remaining deviations: slight gradient/texture shading instead of strictly flat fills; native output 1448 x 1086 is exact 4:3 but below requested 2K.

### Final prompt used for the selected image

```text
Use case: scientific-educational. Create a high-quality 2K PNG concept schematic for a civil-engineering journal manuscript. Clean flat vector-like scientific schematic, pure white background, restrained palette: one muted blue for agent/LLM, one muted orange for computational tools, grey for data, a single muted green accent for result. Thin dark outlines, simple arrows, short crisp sans-serif labels. No logos, people, photographs, decorative 3D, shadows, gradients, watermark, figure title, caption or extra text. Render all listed labels verbatim, including capitalization, spaces, hyphens and underscores. Only listed labels may appear. Do not write step numbers. Graphs are conceptual icons without numeric ticks. Give all labels enough space; do not omit them. Canvas exactly 2048 x 1536 pixels, aspect ratio 4:3.
Message: a language model plans and explains; every number comes from computational tools reading two databases.
Composition: top to bottom, five full horizontal bands linked by downward arrows. Band 2 slightly larger and the focal element. A thin return arrow on far right starts at the bottom Data band, travels upward, and points into the top User band, labelled "results".
Top band: label "User", one chat bubble icon and label "natural-language request".
Second band: large muted-blue rounded rectangle labelled "LLM agent", containing three small tiles "system prompt", "tool selection", "session memory".
Third band: slim band labelled "Tool registry", the label "16 tools, one schema", and three small tags "Anthropic", "OpenAI", "MCP". These three plain-text tags are explicitly required; no brand logos.
Fourth band: label "Computational layer"; five muted-orange tiles in ONE horizontal row, each wide enough for readable text: "property models", "inverse design", "buildability", "literature retrieval", "SQL (read-only)".
Fifth band: label "Data" and two grey database cylinders labelled "literature database" and "print-process database".
Only text allowed: User; natural-language request; LLM agent; system prompt; tool selection; session memory; Tool registry; 16 tools, one schema; Anthropic; OpenAI; MCP; Computational layer; property models; inverse design; buildability; literature retrieval; SQL (read-only); Data; literature database; print-process database; results.
No numbers except the single 16 within its specified label. No other product names, environment details, student bundle, web, terminal, or MCP client text.
Regenerate this composition at native 2K resolution: exactly 2048 pixels wide by 1536 pixels high. The previous output was only 1448 by 1086; output must be larger. Remove all gradient shading and textures; use solid uniform fills only. Preserve every exact label and the five-band order with right-hand return arrow.
FINAL OUTPUT REQUIREMENTS: HIGH QUALITY, 2K resolution, 2048x1536 (4:3). This is the third and final generation attempt. Produce actual native pixel dimensions as requested, not merely a label saying 2K. Do not print these instructions. Ensure every allowed label is present and spelled exactly, no other text or numbers. Use plain uniform solid color areas with no visible gradient, gloss, or texture.
Keep the Tool registry band distinctly slim and make the LLM agent band the tallest band. Use grey for User, registry and data, muted blue for LLM agent, muted orange for computation. Keep return arrow thin.
```

## Figure 2: fig2_workflow.png

- Tool name: `image_gen.imagegen`.
- Underlying image model and version: not reported. Tool version: not reported.
- Generation date: 2026-10-17 (Asia/Seoul).
- Attempts: **3**. Selected attempt: **3**.
- Dimensions: **1672 x 941 pixels**.
- Source artifact: `C:\Users\User\.codex\generated_images\01a1457a-7821-7ca0-8350-3d8f43612018\exec-35148c9b-2e44-4a69-bd5f-546bdb7b8602.png`.
- Attempt review: Attempt 1: left agent arrow stopped at Assess heading; sub-2K resolution. Attempt 2: agent arrow corrected. Attempt 3 selected: clear connected tool flow and integrated report icon; remaining issues below.
- QA note: All 15 required labels are present and visually spelled exactly, including underscores. Assess -> Design -> Report order, stage dividers, all three downward agent-to-tool arrows, output icons, funnel-to-candidates link, return to wall and lower computational bar are present. No extra text, numbers, logos or people observed. Remaining deviations: slight gradient shading and relatively saturated orange instead of uniformly flat muted fills; native 1672 x 941 is below 2K and only approximately 16:9.

### Final prompt used for the selected image

```text
Use case: scientific-educational. Create a high-quality 2K PNG concept schematic for a civil-engineering journal manuscript. Clean flat vector-like scientific schematic, pure white background, restrained palette: one muted blue for agent/LLM, one muted orange for computational tools, grey for data, a single muted green accent for result. Thin dark outlines, simple arrows, short crisp sans-serif labels. No logos, people, photographs, decorative 3D, shadows, gradients, watermark, figure title, caption or extra text. Render all listed labels verbatim, including capitalization, spaces, hyphens and underscores. Only listed labels may appear. Do not write step numbers. Graphs are conceptual icons without numeric ticks. Give all labels enough space; do not omit them. Canvas exactly 2048 x 1152 pixels, aspect ratio 16:9.
Print-planning conversation as tool calls. Left-to-right THREE stages separated by light vertical dividers. Top thin muted-blue bar spans all stages labelled "LLM agent", small downward arrows from this bar terminate in each of the three tool boxes. Bottom thin muted-orange bar labelled "computational layer".
Left stage heading "Assess": small printed wall icon with nozzle above it, label "job". Tiny icons ONLY for height, nozzle, speed and open time (no words for those). Beside it label "material" with a small rheometer/vane icon. An arrow from these inputs to muted-orange tool box "assess_buildability". Downstream output icons a traffic-light style verdict (grey lights and green active light; no extra colors) labelled "verdict", and a small time-window bar labelled "cycle-time window".
Middle stage heading "Design": a rightward flow arrow from left stage outputs to muted-orange tool box "design_for_print_job". Below this tool box a funnel icon labelled "required rheology" feeds a cloud of candidate dots labelled "candidates". Small re-check loop, routed cleanly below the main flow, goes back from these candidates into the wall icon in the left stage, arrowhead on the wall end, labelled "re-assess".
Right stage heading "Report": arrow from the Design stage to a muted-orange tool box labelled "save_report" with a document icon.
Keep tool function names in one line; preserve literal underscores. No A/B/C or other panel letters. No numbers. No chat text or other text.
Exact allowed labels, each present: "Assess", "job", "material", "assess_buildability", "verdict", "cycle-time window", "Design", "design_for_print_job", "required rheology", "candidates", "re-assess", "Report", "save_report", "LLM agent", "computational layer".
Use flat fills without gradient shading. White background with generous empty space and readable typography.
Correction requirement: all THREE blue downward agent arrows must actually connect to and end with an arrowhead ON their tool boxes, including assess_buildability. In the Assess stage route the agent arrow down a clear narrow channel beside the icons if necessary, then into assess_buildability. Do not stop any arrow at the stage heading. Use ONLY uniform solid flat fills, absolutely no gradient or texture shading. Preserve all required labels, icons, three-stage left-to-right structure and the candidates-to-wall re-assess loop.
Regenerate at native 2K resolution: exactly 2048 pixels wide by 1152 pixels high; previous output was only 1672 by 941. Output must be larger.
FINAL OUTPUT REQUIREMENTS: HIGH QUALITY, 2K resolution, 2048x1152 (16:9). This is the third and final generation attempt. Produce actual native pixel dimensions as requested, not merely a label saying 2K. Do not print these instructions. Ensure every allowed label is present and spelled exactly, no other text or numbers. Use plain uniform solid color areas with no visible gradient, gloss, or texture.
```

## Figure 3: fig3_inverse_design.png

- Tool name: `image_gen.imagegen`.
- Underlying image model and version: not reported. Tool version: not reported.
- Generation date: 2026-10-17 (Asia/Seoul).
- Attempts: **3**. Selected attempt: **3**.
- Dimensions: **1672 x 941 pixels**.
- Source artifact: `C:\Users\User\.codex\generated_images\01a1457a-7821-7ca0-8350-3d8f43612018\exec-4edcb75c-b94f-4b36-9f56-36d346a22fd8.png`.
- Attempt review: Attempt 1: five screening intervals instead of three and an extra lower-lane shortcut arrow. Attempt 2: three intervals, but all dots within target band despite greying, and shortcut arrow remained. Attempt 3 selected: screening positions and lower-lane connections corrected; remaining issues below.
- QA note: All 17 required labels are present and visually spelled exactly, including literal tau_s, p(feasible), and hyphens. Six steps read left to right; refine returns from DE refinement to prediction; requirements feed the first step and re-assessment follows the sixth. Three prediction intervals and three screening intervals are present, with outside points greyed. No extra text, digits, chemical formulas, equations, logos or people observed. Remaining deviations: slight gradient shading; blue is also used for computational markers and arrows; native 1672 x 941 is below 2K and only approximately 16:9. Scientific limitation: the descending front icon is illustrative and is not a mathematically validated non-dominated front for lower-clinker/higher-feasibility objectives; plotted points and Sobol-like scatter are generated icons, not computed data. Interval positions are not pixel-identical between prediction and screening tiles.

### Final prompt used for the selected image

```text
Use case: scientific-educational. Create a high-quality 2K PNG concept schematic for a civil-engineering journal manuscript. Clean flat vector-like scientific schematic, pure white background, restrained palette: one muted blue for agent/LLM, one muted orange for computational tools, grey for data, a single muted green accent for result. Thin dark outlines, simple arrows, short crisp sans-serif labels. No logos, people, photographs, decorative 3D, shadows, gradients, watermark, figure title, caption or extra text. Render all listed labels verbatim, including capitalization, spaces, hyphens and underscores. Only listed labels may appear. Do not write step numbers. Graphs are conceptual icons without numeric ticks. Give all labels enough space; do not omit them. Canvas exactly 2048 x 1152 pixels, aspect ratio 16:9. High quality.
Inverse mix design pipeline: a single left-to-right row of SIX rounded muted-orange tiles connected sequentially with rightward arrows, followed by a separate green-accent output card on far right. Do not number the steps. Six steps in this order:
First tile "targets + search space": icon of three bound sliders and a small bar with lower/upper endpoint markers, no words on markers.
Second tile "Sobol sample": evenly spread scatter points in a square.
Third tile "predict with intervals": THREE small vertical interval bars, each with central dot and whisker caps.
Fourth tile "probabilistic screening": intervals against a shaded target band; inside points kept, outside points greyed out. Include label "p(feasible)".
Fifth tile "non-dominated sort": small Pareto-front sketch with dots and a front line, with x-axis label "clinker" and y-axis label "feasibility"; no numeric axes, no ticks.
Sixth tile "DE refinement": few dots converging toward a front, label "candidates".
Output card right of step six: "ranked mixes", "analogues" beside small stack of paper icons, and "applicability".
Above the row, a loop arrow travels FROM the sixth tile back TO the third tile, arrowhead enters third tile. Label that loop "refine".
Below the main pipeline, a thin separate lane labelled "job-based variant" contains two added tiles: left tile labelled "required tau_s at print time", with UPWARD arrow feeding the first main tile. Right tile "re-assess against job", connected downstream after the sixth main tile. Keep the lane connections distinct from the refine loop. Do not use Greek tau or subscript formatting; literal tau_s with underscore.
Every allowed label: targets + search space; Sobol sample; predict with intervals; probabilistic screening; p(feasible); non-dominated sort; clinker; feasibility; DE refinement; candidates; ranked mixes; analogues; applicability; refine; job-based variant; required tau_s at print time; re-assess against job.
No numbers, chemical formulas, equations, extra axis labels, extra titles or other text. Exact labels may wrap at spaces within a tile without changing characters. Flat fills with no gradients; ample white space above and below pipeline, crisp scientific diagram.
Regenerate at native 2K resolution: exactly 2048 pixels wide by 1152 pixels high; previous output was only 1672 by 941. Output must be larger. Remove gradient and texture shading; all fills solid and uniform. Preserve every required label, reading order and arrow connection.
In probabilistic screening show exactly THREE interval marks, corresponding to the three intervals in the previous tile. Do not draw five interval marks. Keep the bottom lane as a thin lane, not an independent direct shortcut arrow bypassing computation.
FINAL OUTPUT REQUIREMENTS: HIGH QUALITY, 2K resolution, 2048x1152 (16:9). This is the third and final generation attempt. Produce actual native pixel dimensions as requested, not merely a label saying 2K. Do not print these instructions. Ensure every allowed label is present and spelled exactly, no other text or numbers. Use plain uniform solid color areas with no visible gradient, gloss, or texture.
Critical screening correction: draw three intervals at three horizontal positions. First central dot ABOVE target band, grey. Second central dot INSIDE target band, highlighted. Third central dot BELOW target band, grey. Shade only the central horizontal target band. Use the identical positions in the preceding prediction tile, but without the band and greying. Bottom job-based variant is a non-directional pale-grey thin BACKGROUND LANE, not a direct bypass arrow; only connect its left requirements tile UP to first main step, and connect sixth main step DOWN into its right re-assessment tile. In Pareto icon, higher feasibility and lower clinker are favorable; front should form the upper-left envelope of dominated grey dots.
```

## Figure 4: fig4_buildability.png

- Tool name: `image_gen.imagegen`.
- Underlying image model and version: not reported. Tool version: not reported.
- Generation date: 2026-10-17 (Asia/Seoul).
- Attempts: **3**. Selected attempt: **3**.
- Dimensions: **1672 x 941 pixels**.
- Source artifact: `C:\Users\User\.codex\generated_images\01a1457a-7821-7ca0-8350-3d8f43612018\exec-55f5ed10-71c4-49f5-9a3e-9c638739328c.png`.
- Attempt review: Attempt 1: load line slightly kinked; sub-2K resolution. Attempt 2: straight lines, but feasible cycle time label placed below window. Attempt 3 selected: straight lines and label inside window; remaining issues below.
- QA note: All 17 distinct required text strings are present and visually spelled exactly (open time also appears at the bar end and within too slow: open time). Panels (a), (b), (c) read left to right. Nine printed layers, highlighted bottom layer, downward self-weight arrow, straight crossing lines and circled limit, slender bowed wall with hatched clamp and thickness double-arrow, and central feasible cycle time window are present. No extra text, numeric digits, equations, logos or people observed. Remaining deviations: slight gradient shading; native 1672 x 941 is below 2K and only approximately 16:9. Lines and geometry are conceptual, not measured or calculated results.

### Final prompt used for the selected image

```text
Use case: scientific-educational. Create a high-quality 2K PNG concept schematic for a civil-engineering journal manuscript. Clean flat vector-like scientific schematic, pure white background, restrained palette: one muted blue for agent/LLM, one muted orange for computational tools, grey for data, a single muted green accent for result. Thin dark outlines, simple arrows, short crisp sans-serif labels. No logos, people, photographs, decorative 3D, shadows, gradients, watermark, figure title, caption or extra text. Render all listed labels verbatim, including capitalization, spaces, hyphens and underscores. Only listed labels may appear. Do not write step numbers. Graphs are conceptual icons without numeric ticks. Give all labels enough space; do not omit them. Canvas exactly 2048 x 1152 pixels, aspect ratio 16:9. Render at full 2K native output resolution, high quality.
Three scientific panels side by side with subtle light-grey vertical separators. Give panel (a) enough width for a layer stack AND graph side by side; panel (b) narrower, panel (c) sufficiently wide for its timeline. Panel labels "(a)", "(b)", "(c)" in their respective top-left corners, followed by their titles.
Panel (a) title "plastic collapse": left a flat front-view stack of nine horizontal rounded rectangles representing printed layers; bottom layer highlighted orange. A downward block arrow above the stack labelled "self-weight". To RIGHT of stack, a small graph, x-axis labelled "time"; two rising STRAIGHT lines: one has positive starting intercept and modest slope labelled "yield stress grows"; other starts lower and rises faster, labelled "load grows". The second overtakes the first at their intersection; mark intersection with a small outlined circle and label "limit". No numeric ticks or axis quantities.
Panel (b) title "elastic buckling": tall slender wall in SIDE VIEW bowing slightly sideways, base clamped in hatched ground. Label "slender wall". Small horizontal double-arrow ACROSS the thin wall width, with extension guides and label "thickness". Not a height measurement, no extra symbol.
Panel (c) title "open time": horizontal time bar from left label "mixing" to right label "open time"; inside bar a central shaded muted-green feasible window labelled "feasible cycle time". Outside that central window, left label "too fast: collapse", right label "too slow: open time". Allow these labels to wrap at spaces, with enough room to remain fully inside panel. No invented timing values.
Exact allowed text: (a); plastic collapse; self-weight; time; yield stress grows; load grows; limit; (b); elastic buckling; slender wall; thickness; (c); open time; mixing; feasible cycle time; too fast: collapse; too slow: open time.
No numbers, equations, logos, people, extra words. Do not depict numerical data. Clean thin consistent outlines and uniform solid flat fills without gradients, scientific restraint.
Regenerate at native 2K resolution: exactly 2048 pixels wide by 1152 pixels high; previous output was only 1672 by 941. Output must be larger. Remove gradient and texture shading; all fills solid and uniform. Preserve every required label, reading order and arrow connection.
FINAL OUTPUT REQUIREMENTS: HIGH QUALITY, 2K resolution, 2048x1152 (16:9). This is the third and final generation attempt. Produce actual native pixel dimensions as requested, not merely a label saying 2K. Do not print these instructions. Ensure every allowed label is present and spelled exactly, no other text or numbers. Use plain uniform solid color areas with no visible gradient, gloss, or texture.
Keep feasible cycle time label INSIDE the green shaded window. Show two truly straight crossing lines in panel (a). Use nine printed layers. Use grey for the wall and stack, muted orange for bottom layer and load line, muted blue for yield line, one green feasible-window accent.
```

## Figure 5: fig5_benchmark.png

- Tool name: `image_gen.imagegen`.
- Underlying image model and version: not reported. Tool version: not reported.
- Generation date: 2026-10-17 (Asia/Seoul).
- Attempts: **3**. Selected attempt: **3**.
- Dimensions: **1672 x 941 pixels**.
- Source artifact: `C:\Users\User\.codex\generated_images\01a1457a-7821-7ca0-8350-3d8f43612018\exec-42383517-18f3-4151-8d36-222700c0221e.png`.
- Attempt review: Attempt 1: unmatched question-mark circle had a dashed link. Attempt 2: circle isolated, but traceability diagram below the check stack. Attempt 3 selected: isolated circle and diagram beside numeric fidelity; remaining issues below.
- QA note: All 10 distinct required word labels are present and visually spelled exactly; ground truth appears in both required locations. The required question mark is present in an isolated, unlinked circle. Left-to-right task -> fresh session -> four scoring checks is clear; recorder is below session; circle-to-square traceability is beside numeric fidelity; dashed chance-match link reaches a separate results card. No extra words, numeric digits, model names, logos or people observed. Remaining deviations: light gradient/texture shading instead of strictly flat fills; native 1672 x 941 is below 2K and only approximately 16:9. Chance-match dashed link originates at a tool-result square; the brief does not specify that endpoint, but the diagram should not be read as an exact implementation trace.

### Final prompt used for the selected image

```text
Use case: scientific-educational. Create a high-quality 2K PNG concept schematic for a civil-engineering journal manuscript. Clean flat vector-like scientific schematic, pure white background, restrained palette: one muted blue for agent/LLM, one muted orange for computational tools, grey for data, a single muted green accent for result. Thin dark outlines, simple arrows, short crisp sans-serif labels. No logos, people, photographs, decorative 3D, shadows, gradients, watermark, figure title, caption or extra text. Render all listed labels verbatim, including capitalization, spaces, hyphens and underscores. Only listed labels may appear. Do not write step numbers. Graphs are conceptual icons without numeric ticks. Give all labels enough space; do not omit them. Canvas exactly 2048 x 1152 pixels, aspect ratio 16:9. Render full 2K native PNG, high quality.
Benchmark scoring concept. Read LEFT to RIGHT.
Left: grey card labelled "task", containing a short prompt-line icon consisting of abstract horizontal strokes only (no actual words), plus three small tags labelled "expected tools", "expected arguments", "ground truth".
Arrow from task card to centre.
Centre: muted-blue rounded box labelled "fresh session". Inside, a simple abstract language-model network/chip icon (no label, no face) connected to small muted-orange tool icons. Below this box, a recorder icon labelled "recorded calls + answer", connected downward from session.
Arrow from recorder/session to right-hand scoring stack.
Right: FOUR check tiles stacked VERTICALLY, each with a check-mark box, top-to-bottom labels "tool selection", "parameter checks", "ground truth", "numeric fidelity".
BESIDE the bottom numeric fidelity tile, leave space for a small traceability diagram: three small hollow circles representing answer numbers linked by thin solid lines to three small squares representing tool-result numbers; a fourth separate circle unlinked to all squares contains a question mark. All circles and squares otherwise EMPTY, absolutely no digits or text in them. A nearby label "chance-match control" with a dashed link to a separate grey mini-card of small empty squares representing a DIFFERENT task's results. This miniature alternative-results card is unlabelled.
Exact allowed words: task; expected tools; expected arguments; ground truth (appears on left card and scoring tile); fresh session; recorded calls + answer; tool selection; parameter checks; numeric fidelity; chance-match control. The single question mark inside the unmatched circle is explicitly required and allowed.
No numbers, model names, logos, people, added headings, legends, or labels. Uniform flat fills, no gradient shading, pure white background, thin outlines and readable sans-serif labels.
Regenerate at native 2K resolution: exactly 2048 pixels wide by 1152 pixels high; previous output was only 1672 by 941. Output must be larger. Remove gradient and texture shading; all fills solid and uniform. Preserve every required label, reading order and arrow connection.
The unmatched circle containing ? must remain isolated with NO link of any kind. Place the dashed chance-match link from the group of answer circles to the alternate-results card instead of from the ? circle. Use grey for data recorder.
FINAL OUTPUT REQUIREMENTS: HIGH QUALITY, 2K resolution, 2048x1152 (16:9). This is the third and final generation attempt. Produce actual native pixel dimensions as requested, not merely a label saying 2K. Do not print these instructions. Ensure every allowed label is present and spelled exactly, no other text or numbers. Use plain uniform solid color areas with no visible gradient, gloss, or texture.
Place circle-square traceability diagram immediately to the RIGHT of numeric fidelity tile, not underneath it, while maintaining adequate space. Keep isolated ? circle unlinked. All tiles and diagrams fully inside canvas.
```


