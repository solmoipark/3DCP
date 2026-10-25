# Manuscript versions

One folder per version; a folder is never edited after the next version starts. Each folder is self-contained
(main.tex, refs.bib, figures/, gen/, main.pdf). Shared across versions: eval/ (benchmark tasks, runs, scores).

| version | date | status | notes |
|---|---|---|---|
| v01 | 2026-10-16 | draft for PI review | first complete draft: 3DCP-Agent name, English tool figures, 33-task benchmark on gpt-6-astra and gpt-6-sol |
| v02 | 2026-10-17 | draft for PI review (figures: AI concept drafts, ~250 dpi) | reviewer/copy-editor pass by GPT-6-Astra (Codex CLI) under the CCR plain-style skill and the PI's comments: prose 6.5k -> 3.6k words, insider wording and self-promotion removed, related-work table and most transcripts dropped, backend reporting reduced to models and access, Fig. 1 simplified; author fixes: safety factor in Eq. (1), width default 1.18 d, training/validation settings added, AI declaration extended. Memo: v02/review/astra_review.md |

v02 figure note: Figures 1, 2 and the new inverse-design, buildability-criteria and benchmark-scoring schematics were generated with the Codex CLI built-in image tool (GPT-6-Astra driving it) from paper/v02/figures/ai/BRIEF.md; prompts and QA in figures/ai/PROVENANCE.md. Elsevier permits AI-assisted explanatory schematics with caption disclosure (policy checked 2026-10-17). Native sizes 1448x1086 and 1672x941 px; vector redraws recommended before production.
| v03 | 2026-10-17 | draft for PI review | vector (TikZ) redraws of all schematics with more detail in Figs 1-2, benchmark-scoring schematic dropped, journal-style data figures (Arial 7 pt, 90/190 mm, Okabe-Ito, panel letters), benchmark extended to five OpenAI models (gpt-6-astra, gpt-6-sol, gpt-6-luna, gpt-6.1-sol, gpt-5.6-sol) with per-model and per-group tables |
| v04 | 2026-10-25 | in review | second GPT-6-Astra pass: remove remaining insider content, process narrative and instruction echoes (PI comment of 2026-10-25); memo in v04/review/astra_review2.md |
