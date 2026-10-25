# Second reviewer and copy-editor pass

The revision removes internal development history and editorial instructions while retaining the scientific method, observed failures and limitations. It follows review/brief.md and review/ccr-style-SKILL.md. The deliverables are the revised main.tex and this memo. Section and paragraph order was retained.

## Passage classification and action

Locations refer to both the supplied and revised main.tex, whose line numbering is unchanged. Each row identifies a changed passage by its original opening. Repeated disclosures are consolidated as indicated.

| No. | Passage | Classification | Action and reason |
| --- | --- | --- | --- |
| 1 | `main.tex:39`, `\newcommand{\sessionsep}[1]{\par\medskip\noindent{\footnotesize\bfseries --- #1 ---}\par\smallskip}` | Style | Deleted decorative TeX em dashes in the session separator; retained the macro and its label. |
| 2 | `main.tex:42`, `\newcommand{\aidisclosure}{Vector schematic drawn with AI assistance (Claude, Anthropic) from the...` | Instruction echo | Shortened the shared disclosure for all four schematic captions. Full attribution and author responsibility remain in the declaration. |
| 3 | `main.tex:57`, `Five OpenAI models were run through the Codex command-line interface. Three passed all tasks under the...` | Process narrative / tooling detail | Removed access detail and scoring-history wording from the abstract; retained model count and failure finding. |
| 4 | `main.tex:121`, `Conditions include age, specimen group, curing, rest time and the 3DCP flag.` | Insider wording | Replaced the database flag noun with its meaning. |
| 5 | `main.tex:125`, `LightGBM hyperparameters are set by data-size tier, with learning rates of 0.03 to 0.05, 7 to 31 leaves...` | Instruction echo / style | Recast weak-model instructions as the purpose of the methodological thresholds; split the training and validation sentences without changing values. |
| 6 | `main.tex:139`, `\caption{Inverse mix design. Candidates are sampled from the search space, each target is predicted with...` | Style | Split the long pipeline caption while retaining all computational steps. |
| 7 | `main.tex:143`, `The agent is required to report the defaults used.` | Instruction echo | Expressed default disclosure as part of the assessment output. |
| 8 | `main.tex:181`, `Literature retrieval ranks published mixes against the design targets. The exact tier contains mixes...` | Tooling detail / insider wording | Replaced exact/near tier names with their meaning. Removed SQL-filter implementation, timeout, row limits, response-digest and CSV details; kept the read-only constraint relevant to the write test. |
| 9 | `main.tex:185`, `Each tool is registered with its name, description, argument schema, executable function and access or...` | Tooling detail | Removed access/runtime flags and artifact-handling detail; retained schemas, registry interoperability and scientific output types. |
| 10 | `main.tex:191`, `\caption{Tool registry. Slow tools perform design searches. All tools are read-only with respect to the...` | Insider wording | Explained table labels in reader-facing terms and retained the database-write boundary. |
| 11 | `main.tex:198`, `The system prompt is assembled for each turn from the current model information and session context. It...` | Tooling detail / insider wording | Removed per-turn assembly and session-summary implementation; retained prompt information needed to interpret the experiment. |
| 12 | `main.tex:200`, `The agent rules require quantitative predictions to come from tool results and to include units....` | Instruction echo | Converted an imperative checklist into a description of the prompt design. These are configured behaviours, not claims that every evaluated model complied. |
| 13 | `main.tex:202`, `For an unsuccessful buildability assessment, the agent must report available schedule or material...` | Instruction echo | Retained scientifically relevant response requirements and the retry limit as method, removing must-report wording. |
| 14 | `main.tex:204`, `The tool loop ends when the model stops requesting tools or reaches twelve iterations. Session...` | Tooling detail | Removed transcript/rolling-summary implementation and the 40,000-character threshold. Retained the iteration bound and the persistence function tested by the benchmark. |
| 15 | `main.tex:208`, `Five OpenAI models were evaluated through the Codex command-line interface (version 0.163) with the...` | Tooling detail / unsupported interpretation | Removed CLI version, interface-default status, generation/size framing and repeated client architecture. Retained access route, model identifiers, reasoning settings and common prompt. |
| 16 | `main.tex:214`, `The case-study excerpts were recorded with \nbenchCxModel{} through the Codex command-line interface....` | Process narrative / instruction echo | Removed naming-edit workflow, otherwise-retained wording and plot-regeneration instructions. Kept concise provenance and naming standardisation, so the excerpts are not falsely described as wholly verbatim. |
| 17 | `main.tex:237`, `The benchmark contains \nbenchCxN{} tasks in ten groups (Table~\ref{tab:bench}). Tasks cover forward...` | Insider wording | Removed the released-evaluation-package reference; availability is stated once in the data-availability section. |
| 18 | `main.tex:239`, `Each task specifies required and prohibited tool calls and checks on recorded arguments. These include...` | Instruction echo / tooling detail | Retained actual scoring criteria as method, replaced slow-tool shorthand and removed separate-storage implementation. |
| 19 | `main.tex:243`, `The same task set was run once per model from fresh sessions. Reported wall times include tool execution...` | Process narrative / tooling detail | Consolidated evaluation scope, response-informed scoring limitation and timing definition here. Did not invent a claim that criteria had been fixed before all final runs. |
| 20 | `main.tex:247`, `\caption{Benchmark results under the final scoring rules after integration fixes and wording-rule...` | Process narrative | Deleted integration-fix and wording-revision history from Table 2 caption. |
| 21 | `main.tex:254`, `\caption{Tasks passed per task group and model under the final scoring rules.}` | Process narrative | Deleted final-scoring-rules qualifier from Table 3 caption. |
| 22 | `main.tex:259`, `Tables~\ref{tab:bench} and \ref{tab:benchgroups} give the results per model and per task group. The...` | Process narrative / insider wording / style | Deleted defect/rerun chronology and model-order narrative. Retained reported failures, including counts, and split the long failure catalogue into interpretable sentences. Replaced internal call shorthand with task descriptions. |
| 23 | `main.tex:261`, `Mean numeric fidelity ranged from \nbenchCuFidelity{} (\nbenchCuModel{}) to \nbenchCsFidelity{}...` | Tooling detail / style | Replaced recorded-response-digest jargon with the limitation relevant to automatic matching. Retained manual inspection and all unmatched-value categories. |
| 24 | `main.tex:263`, `Tool errors were corrected within the same turn in every case. Their number per model is listed in...` | Unsupported interpretation / style | Removed the claim linking faster models, preparatory schema calls and failure concentration, which Tables 2 and 3 do not establish. Retained errors and measured ranges. |
| 25 | `main.tex:268`, `\caption{Benchmark timing and tool use per model. (a) Median wall time per task group. (b) Distribution...` | Tooling detail | Removed repeated MCP server-startup implementation; timing scope remains in benchmark design. |
| 26 | `main.tex:276`, `Numeric fidelity measures whether reported numbers occur in the available inputs and outputs. It does...` | Tooling detail / instruction echo | Retained the substantive traceability-versus-correctness and record-completeness limitations. Removed a development prescription for future logging. |
| 27 | `main.tex:282`, `The benchmark evaluates specified tool calls and answer checks. It does not measure engineering adequacy...` | Process narrative / unsupported interpretation | Moved the response-informed scoring limitation to benchmark design. Replaced weaker-model rhetoric and the causal attribution to tool descriptions/schema guidance with the observed failure groups and an explicit inference limit. Kept language mismatch and generalisation limits. |
| 28 | `main.tex:288`, `3DCP-Agent connects natural-language requests to \nnModels{} property models, inverse mix design,...` | Process narrative / style | Removed final-scoring-rules language and split the model-result sentence; retained all conclusions and limitations. |
| 29 | `main.tex:291`, `During the preparation of this work the author used Claude (Anthropic) to assist in software...` | Tooling detail / style | Retained full AI-use attribution and author responsibility once; removed CLI routing and split the long declaration. |
| 30 | `main.tex:294`, `The package, trained models, both databases (compressed), the benchmark tasks, the harness and the...` | Insider wording / tooling detail | Replaced package and harness with software and evaluation code; removed compression detail and retained the existing availability claim and URL. |
| 31 | `main.tex:306`, `\caption{Benchmark tasks with abridged prompts. Full prompts, checks and ground-truth values are...` | Insider wording | Removed repeated released-evaluation-package language while retaining the meaning of the checks column. |

The following passages were deliberately retained or retained in rewritten form.

| Passage | Classification | Decision |
| --- | --- | --- |
| Computational layer, inverse-design constraints and buildability criteria | Scientific method | Kept. These define the calculation and its applicability. Equations, material defaults, weak-model thresholds and uncertainty levels are unchanged. |
| Agent core, prompt contents and response requirements | Instruction echo rewritten as method | Kept as configured prompt behaviour, not as proof that every model complied. Removing prompt design would obscure the evaluated intervention. |
| Agent core, retry and tool-iteration limits | Relevant tooling detail | Kept the two-retry and twelve-iteration bounds because they constrain agent behaviour and recovery. Removed the character-count memory threshold. |
| Benchmark, required/prohibited tools, argument tolerances, clarification, write and memory checks | Evaluation criteria | Kept. These define a pass and explain why using SQL in a retrieval task can fail even if it produces an answer. |
| Benchmark, response-informed wording criteria | Process history with a validation consequence | Rewritten once in benchmark design. The limitation remains explicit. No claim was added that criteria were fixed before all final runs. |
| Benchmark and Discussion, shortened tool-response records | Tooling detail with a measurement consequence | Rewritten in plain terms. Incomplete records affect automatic numerical matching and explain manual verification. |
| Case studies, standardised system naming | Editorial transformation relevant to provenance | Kept as one short qualification. The excerpts are not called wholly verbatim because the supplied manuscript says naming was changed. |
| Schematic captions and AI declaration | Disclosure | Short clause in each of four captions, full attribution and responsibility once in the declaration. |
| Scientific variables, model identifiers, MCP and SQL | Necessary technical terminology | Kept. Tool names remain in typewriter font in the protected registry and transcripts. |

No student-bundle passage was present in main.tex. Author identity and affiliation were retained as publication metadata.

## Style inventory before and after

Counts are pattern occurrences from the abstract through the end of main.tex, including its captions. They exclude imported gen files, vector-source text, bibliography entries and preamble definitions. LaTeX label identifiers and the URL colon are not prose-colon violations. Vocabulary matching is case-insensitive. Sentence structure, substantive lists, stacked hedges and parenthetical length were also reviewed manually.

| Pattern | Before | After |
| --- | ---: | ---: |
| Unicode em dash | 0 | 0 |
| TeX em dash | 0 | 0 |
| Unicode en dash | 0 | 0 |
| TeX en dash ranges | 5 | 5 |
| Semicolon | 0 | 0 |
| Colon followed by space | 1 | 0 |
| Colon headings | 0 | 0 |
| Bold lead-in candidates | 0 | 0 |
| Bracket numeric CI | 0 | 0 |
| Banned vocabulary | 1 | 1 |
| Negative parallelism | 0 | 0 |
| Implication tails | 0 | 0 |
| Final scoring qualifiers | 4 | 0 |
| Directive echoes | 6 | 0 |
| Insider phrases | 14 | 0 |

The vocabulary scan covers the full banned-word and stock-phrase list in the supplied skill. The directive-echo scan counts "is instructed to," "is required to," "agent rules require," "must be identified," "must be stated" and "agent must report." The insider scan counts integration defects/fixes, wording-rule revisions/changes, fresh-session reruns, recorded response digest, released evaluation package, the harness, separate storage, MCP server startup, internal package name, "Transcript wording was otherwise retained" and "regenerated by executing." These counts are not a substitute for the paragraph-by-paragraph review.

Preamble checks supplement the body inventory. The session-separator macro contained two decorative TeX em dashes, now zero. The shared AI-caption disclosure was reduced to "Schematic drawn with AI assistance, see the declaration." All four calls to that macro remain.

Intentional survivors and scope boundaries are as follows.

- The five TeX en dashes in the body express the interquartile range, the 10th to 90th percentiles and the three measured-property ranges. All remain unchanged. The Unicode en dash in the listings character-conversion definition also remains because it maps an input character rather than punctuating prose.
- The one raw banned-word hit is "stack-to-failure collapses." It describes physical failure, not rhetorical drama. The substantive banned-vocabulary violation count is zero before and after.
- Technical enumerations were retained when each member specifies a material feature, tool function, scoring criterion or distinct limitation. They were not deleted merely because they contain three items.
- The property-model appendix caption retains its parenthetical list of validation metrics. It is a technical key to the table, not an extended aside.
- Imported transcripts retain original response punctuation and bold labels, including semicolons in gen/case_P05.tex, gen/case_B01.tex and gen/case_J01.tex. Those outputs are outside the authorised edit scope and are excluded from the edited-prose counts. This memo does not claim zero style violations throughout a compiled document.

Four representative changes illustrate the approach.

1. "The agent is required to report the defaults used." became "The assessment reports the defaults used." The intended reporting function remains without a development instruction.
2. The Table 2 caption opening about "integration fixes and wording-rule revisions" became "Benchmark results." The response-informed scoring limitation now appears once in benchmark design.
3. "The cycle-time plot was regenerated by executing the recorded tool call with the same arguments and English labels" was deleted. Plot-production instructions do not help interpret the physical result.
4. The Discussion attribution of model differences to tool descriptions and schema guidance was replaced by the table-supported concentration of failures in retrieval and database questions. The next sentence states that the results do not isolate the causes of model differences.

## Evidence check against Tables 2 and 3

The tables were read directly from gen/benchmark_table.tex and gen/benchmark_groups.tex. Model names and unrounded quantities were checked against gen/numbers.tex.

- gpt-6-astra, gpt-6-sol and gpt-6.1-sol each passed 33/33 tasks. gpt-6-luna passed 27/33 and gpt-5.6-sol passed 28/33, consistent with six and five failures.
- For gpt-6-luna, Table 3 shows three retrieval failures and one failure each in inverse design, buildability/schedule and database questions. For gpt-5.6-sol, it shows three retrieval and two database failures. These groups support the revised Discussion statement.
- The macro-based mean-fidelity range remains 0.990 to 0.998. The chance-match range remains 0.378 to 0.442. Median wall times remain 18 to 48 s, and median calls remain two to four. Table 2 rounds some values. The existing manuscript precision was retained.
- Aggregate timing and call counts cannot establish that reduced preparatory schema/vocabulary calls caused failures. The model with the second-shortest median time passed every task. The causal explanation was removed.
- Detailed failure mechanisms, recovery of every tool error within the same turn and the finding that no fabricated quantity was identified are observations reported in the supplied manuscript. They are not independently demonstrated by the aggregate tables. They were retained without strengthening them. This pass did not rerun the benchmark or audit its response logs.

## Numerical and source-integrity checks

The required digit-sequence multiset comparison found only authorised deletions of operational details. No digit sequence was added. The complete multiset delta (after minus before) is as follows.

| Digit sequence | Delta | Deleted detail |
| --- | ---: | --- |
| 0 | -1 | CLI version 0.163 |
| 163 | -1 | CLI version 0.163 |
| 20 | -2 | SQL timeout of 20 s and digest threshold of 20 rows |
| 200 | -1 | Query row limit |
| 40 | -1 | 40,000-character session threshold |
| 000 | -1 | 40,000-character session threshold |

The retained request/result counts of 20 and 10 mixes were not changed. Spelled-out counts associated solely with integration defects, wording-list revisions and run order were removed with that process history. No scientific numerical value was substituted.

Static checks passed for the following items.

- All 34 distinct generated numerical/model-name macros used by the supplied main.tex remain in use. gen/numbers.tex is unchanged. One duplicate occurrence each of 
benchCxModel and 
benchCsModel was removed only with the rerun-history sentence; the macros and model names remain throughout the manuscript.
- All original input commands, graphic inclusions, case-study input paths, label definitions, citations and section headings were retained. Every cited bibliography key and referenced label resolves in the supplied sources. All directly included files exist.
- Inline mathematical expressions have identical multisets, and both displayed equations are unchanged. Braces and LaTeX begin/end environments are balanced. Original LF line endings were retained.
- SHA-256 checks confirm that all 66 protected files comprising the gen/ and figures/ contents and refs.bib are unchanged.

LaTeX was not run, as instructed. These are source-level checks, not a compilation or rendered-layout claim. External references and the repository availability statement were not independently re-verified on the web.

## Items left for the author

1. **Protected generated text.** The included gen/tools_table.tex still describes report output as "markdown / xlsx." The included case-study outputs retain semicolons, colon lead-ins and bold labels. These were left intact under the explicit prohibition on editing gen/*.tex. Applying house style inside quoted outputs or the registry requires a separate authorised revision that preserves transcript provenance. Unused generated MCP examples also contain local paths, but main.tex does not include them.
2. **Benchmark provenance.** Retain the response-informed-scoring limitation. Independently fixed evaluation would require new evidence, not a wording change. The detailed failure mechanisms, recovery claim and numerical-inspection finding should remain traceable to the original evaluation records before submission.
3. **Uncertainty-method terminology.** The manuscript retains both "split-conformal calibration" and estimation of the scale factor from out-of-fold residuals. Confirm that these descriptions match the actual calibration and evaluation partitions. No method or coverage result was inferred or altered here.
4. **Availability.** The supplied repository URL and availability statement remain. Confirm that the software, models, databases, evaluation code and transcripts are accessible in the intended release.

Both requested deliverables are complete. These author decisions do not leave any authorised edit in this pass unfinished.
