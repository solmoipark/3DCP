# Review and revision brief for the manuscript in this folder (v02)

You are acting as a senior reviewer and copy editor for a manuscript to be submitted to *Automation in Construction*.
Work directly on the files in this folder. Your deliverables are listed at the end.

## Files

- `main.tex` — the manuscript (elsarticle). Edit this file in place.
- `figures/architecture.tex`, `figures/sequence.tex` — TikZ figures. You may simplify `architecture.tex` (see comment 5 below).
- `gen/*.tex` — machine-generated inputs (transcripts of real agent runs, tables, `numbers.tex` macros). Do **not** edit these. You may decide which of them `main.tex` includes.
- `refs.bib` — verified references. Do not add references that you cannot verify; do not change existing entries.
- `review/ccr-style-SKILL.md` — the house-style rules you must apply to all prose you write or rewrite.

## The principal investigator's comments (verbatim, Korean, followed by an English rendering)

> 논문으로써 가치가 있는 것만 보고하도록 하고, 더 strict한 논문 스타일로 다듬어줘. 클로드 너는 특유의 스스로를 높이 평가하고, 사람이었으면 대단한 것도 아닌데 혼자 대단한 것처럼 반복적으로 강조하는 특징이 있어. 그런 걸 버려. 그리고 모든 걸 기계적으로 처음부터 끝까지 모든 숫자를 아주 상세히 다 보고하려는 특징이 있어. 'in our previous work with an LLM-assisted', 'frozen machine validator' 등 너 혼자만 아는 걸 아직도 많이 사용하고 있어. 필요치 않다면 언급을 안해도 되는 부분도 포함. Student bundle이라든지 그림 1에서 너무 불필요한게 많이 들어가있네. LLM backend 부분도 구독버젼을 사용했다거나 하는게 중요한 부분은 아니지 않나? 그냥 어떤 모델을 썼는지라든지, 아니면 프론티어 모델이 아닌 다른 모델로만 테스트해서 범용성을 보여준다든가? 일반적으로 이 필드에서 하는 방식을 따라가줘. 그림 3에 general model에 대한 건 다른 부분에서 언급되는 게 있나?

1. Report only what has value as a paper. Make the style stricter and plainer, as in a journal paper.
2. Remove the self-congratulatory tone. The current draft repeatedly presents ordinary engineering as remarkable. A human author would not do that. Drop every such emphasis.
3. Stop reporting every number mechanically from beginning to end. Keep the numbers that a reader needs to judge the work. Everything else goes.
4. Remove insider phrases that only the author's own workflow explains, such as "in our previous work with an LLM-assisted ...", "frozen machine validator", "settlement", internal script names, folder names, and similar. If a detail is not needed, leave it out.
5. Remove unnecessary content such as the "student bundle". Figure 1 (architecture) has far too much in it; reduce it to what a reader needs.
6. The LLM-backend discussion over-emphasises subscriptions versus API keys. That is not what matters. State which models were used, how they were accessed, and the settings. If a second, non-frontier or smaller model was used, present it as a check of generality. Follow the conventions of this field (see how recent Automation in Construction LLM papers report their models).
7. Figure 3 distinguishes "general" and "3DCP-specific" models. Check whether this distinction is explained where it should be, and make the text and figure consistent (explain it once, where the models are introduced, or drop it from the figure).

## What to do

1. Read `main.tex` completely, then `review/ccr-style-SKILL.md`.
2. Write `review/astra_review.md`: a concise reviewer memo (no more than two pages) with (a) the parts that do not earn their place in a journal paper and why, (b) insider wording found, (c) self-promotion found, (d) inconsistencies (including the Figure 3 question), (e) how the model/backend reporting should be framed in this field, (f) anything else a referee at Automation in Construction would raise.
3. Revise `main.tex` accordingly, in place. Apply the style skill to every sentence you keep or write. Specifically:
   - Delete content rather than compress it when it has no value for the paper (e.g. the student bundle, launcher scripts, environment variables, internal folder or script names, the benchmark's first-run bug-hunt narrative unless you can state it in two neutral sentences, repeated statements of what the system "does not" do).
   - Keep the methods complete enough to reproduce: data sources and sizes, model type and validation, the buildability criteria with their equations and calibration basis, the tool registry idea, the agent rules, the benchmark design and metrics.
   - Keep numbers that support a claim; drop the rest. Numbers that stay must stay exactly as they are (they come from `gen/numbers.tex` macros or from the generated tables; do not retype them).
   - Reframe the backend paragraph and the benchmark "Backends" paragraph: name the models (gpt-6-astra and gpt-6-sol, accessed through the OpenAI Codex command-line interface with tools served over MCP; default reasoning settings), present the second model as a generality check, and drop the subscription/API-key/login narrative. The sentence about the Claude backend not being available can be dropped or reduced to one neutral clause in the limitations.
   - Remove self-praise and meta-commentary ("the honest answer", "what the benchmark caught", "is what a machine-checkable task set is for", "notably", "remarkably", etc.). State findings and let them stand.
   - Resolve the Figure 3 point (comment 7). The variant mechanism is currently described in the "Property models" paragraph; make sure the figure legend terms match the text, or remove the variant series from the figure if the paper never uses it.
   - Simplify `figures/architecture.tex`: four or five rows (interfaces, agent core, tool registry, computational layer, data layer) with short labels, no product names of third-party clients, no "student bundle", no environment details.
   - Keep LaTeX compiling: keep every `\input{gen/...}` whose figure or table you still reference, remove the `\casefigure`/figure blocks you drop together with all `\ref`s to them, keep the `\n...` macros (they are defined in `gen/numbers.tex`), keep the preamble.
   - Keep the abstract under 250 words, plain, with the same claims as the body.
   - Do not invent results, references, or numbers.
4. Run the style skill's inventory and residual scans on `main.tex` (em dashes, semicolons in prose, colon openers, bold lead-ins, banned words) and report the counts in the memo.
5. Finish `review/astra_review.md` with a short change log (what was removed, what was reframed, what was kept and why) and any sentences you left alone to protect meaning.

Do not run LaTeX; the author will compile. Do not modify anything outside this folder.
