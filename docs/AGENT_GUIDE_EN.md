# pmpredict agent — user guide

A mix-design assistant for the 3DCP (3D concrete printing) laboratory. Ask in plain English; the agent answers using
prediction models trained on the literature database, an inverse-design engine, a buildability calculator, literature
retrieval and read-only SQL. Every number comes from a tool result, and predictions are always written as
`q50 [q10, q90]` (80 % interval) with units.

Installation and backend setup: see `STUDENT_README.md` in the root folder.

---

## 1. At a glance

| What you want | Ask for example | Tools the agent uses |
|---|---|---|
| mix → properties | "28-day compressive strength and static yield stress of a mortar with w/b 0.35, OPC 85 % + SF 15 %, PCE 0.3 %" | `predict_properties`, `flow_curve`, `structuration_curve` |
| targets → mix design | "28-day compressive >= 40 MPa, static yield 1–4 kPa, minimum clinker" | `design_mix` (+ `retrieve_literature`) |
| nozzle / structure → buildability, schedule | "25 mm nozzle, 600 mm wall, is tau_s 3 kPa enough? cycle time?" | `assess_buildability`, `print_schedule`, `similar_prints`, `design_for_print_job` |
| published mixes | "10 3DCP mixes with static yield stress above 2 kPa" | `retrieve_literature` |
| database statistics | "How many 3DCP papers use a VMA?" | `describe_schema` → `sql_query` |
| summarise, save, remember | "save this as a report", "remember that our default specimen is prism40" | `save_report`, `remember` |

Data: literature DB 3,274 papers / 29,626 mixes (28,001 normalised); print-label DB 1,014 papers / 7,420 print runs.
Model metrics are paper-grouped cross-validation (GroupKFold).

---

## 2. Getting started

### Web app (recommended)
`start_app.bat` (or `streamlit run app/streamlit_app.py`) → http://localhost:8501. Choose backend, model and session in the
left sidebar and type in the box at the bottom. The example buttons run immediately. The legacy form pages (Korean) are
behind the sidebar toggle **"Direct mode (legacy forms)"**.

### Terminal
```bash
python -m pmpredict.cli agent            # interactive (commands: /new /sessions /artifacts /quit)
python -m pmpredict.cli agent -p "question"   # one question, then exit
python -m pmpredict.cli agent --check    # which backend will be used and why
```
Set `PMPREDICT_LANG=en` before starting (the launcher scripts do it) so the agent answers in English.

### Backends
Detected in the order **API key → logged-in subscription**; override in the sidebar or with `--provider`.

| Backend | Needs | Notes |
|---|---|---|
| Anthropic API | `ANTHROPIC_API_KEY` or `anthropic_api_key` in `secrets.json` | default model claude-sonnet-5, option claude-opus-5 |
| OpenAI API | `OPENAI_API_KEY` or `openai_api_key` in `secrets.json` | model via `PMPREDICT_OPENAI_MODEL` |
| Claude subscription | one-time login of the bundled CLI (`--check` prints the command) | personal local use only; never on a public server |
| ChatGPT subscription | `npm i -g @openai/codex` + `codex login` (`codex_login.bat`) | tools are passed to Codex over MCP; model via `PMPREDICT_CODEX_MODEL` |

Key values are never written to the screen, logs or the repository.

---

## 3. How to ask

A good question contains the items below. Missing values get **defaults, and the answer says which defaults were used**.

- **Mix**: system (paste/mortar), w/b, s/b, binder composition (fractions), admixtures (% of binder), fibres (vol %).
- **Conditions**: age (default 28 d), compressive specimen (default 50 mm cube), curing (default moist 20 °C), whether it is a 3DCP mix.
- **Targets** (inverse design / retrieval): for each target one of ">= / <= / range / goal", with unit.
- **Print job**: object type, target height, wall length or cylinder diameter, nozzle size, speed, open time, material (static yield stress and Athix, or a mix).

Examples:
- "28-day compressive strength and flow of an OPC mortar with w/b 0.40, s/b 2.0, PCE 0.5 %"
- "Also give the flow curve and the structuration curve (60 min) of that mix and compare with measured curves from the literature"
- "10 published mixes with 28-day compressive >= 40 MPa and static yield 1–4 kPa (rest 0 s), 3DCP preferred"
- "Same targets, minimise clinker. OPC required 0.5–1.0, SF 0–0.15, limestone 0–0.3, w/b 0.28–0.45. Run without asking"
- "25 mm nozzle, 600 mm high, 1.5 m wall (2 filaments), 50 mm/s, open time 60 min. tau_s 3 kPa, Athix 1 Pa/s: printable? cycle-time window"
- "Inverse-design a mix for this print job (design_for_print_job)"
- "Number of 3DCP papers that use a VMA, and the median static yield stress of their mixes"
- "Save everything so far as a report (md + xlsx)"
- "Remember: our lab's default specimen is comp_prism40"

Slow tools (`design_mix`, `design_for_print_job`, 30–150 s) run immediately when targets and search space are given;
otherwise the agent asks once. Write "run without asking" to skip the question.

---

## 4. Describing a mix

The agent converts your text into the dict below and passes it to the tools. You can also give the JSON yourself.

```json
{"system_type": "mortar", "w_b": 0.35, "s_b": 1.5,
 "binder": {"portland_cement": 0.85, "silica_fume": 0.15},
 "admixtures_pct": {"superplasticiser_pce": 0.5, "vma_cellulose": 0.2},
 "fibres_vol_pct": {}, "nano_pct": {},
 "conditions": {"age_d": 28, "comparability_group": "comp_cube50", "curing": "moist", "rest_time_s": 0, "is_3dcp": true},
 "name": "my_mix"}
```

| Field | Meaning | Convention |
|---|---|---|
| `binder` | binder (powder) class → mass fraction | renormalised automatically if the sum is not 1 (with a warning) |
| `s_b` | fine aggregate / binder mass ratio | mortar only; ignored for paste |
| `admixtures_pct` | admixture → % of binder mass | product dosage, not solids |
| `fibres_vol_pct` | fibre → vol % of the mixture | |
| `nano_pct` | nano material → % of binder | |
| `activators` | activator → {amount (mass ratio to binder), molarity} | alkali-activated systems |
| `material_props` | oxides, Blaine, specific gravity, d50 per class | class medians are imputed when absent |
| `conditions.curing` | curing | `water` / `moist` / `sealed` / `ambient` / `steam` or a preset name |
| `conditions.is_3dcp` | 3DCP mix | if true the 3DCP-specific model is used when its quality is higher |

Material class names are a fixed vocabulary (e.g. `portland_cement`, `fly_ash_class_F`, `ggbfs`, `silica_fume`,
`limestone_powder`, `metakaolin`, `superplasticiser_pce`, `vma_cellulose`, `accelerator_setting`, `nano_clay`).
Ask "show me the binder classes" and the agent calls `describe_vocabulary`. A wrong name returns an error with the closest candidates.

---

## 5. Describing targets

| kind | meaning | values | example |
|---|---|---|---|
| `ge` | at least | `lo` | compressive >= 40 MPa → `lo: 40` |
| `le` | at most | `hi` | plastic viscosity <= 50 Pa·s → `hi: 50` |
| `range` | between | `lo`, `hi` | static yield 1–4 kPa → `lo: 1, hi: 4, unit: kPa` |
| `goal` | close to | `goal` | flow about 180 mm |

- Units (`unit`) are converted automatically (kPa→Pa, h→min, ...).
- Conditions: `age_d`, `comparability_group` (strength), `rest_time_s` (static yield), `shear_rate_1s` (flow-curve point).
- Derived targets: `shear_stress_at_rate` (given shear rate), `static_yield_stress_at_rest` (given rest time; the "tau_s at the end of the print" in buildability).
- `p_min`: minimum probability of meeting the target. 0.6–0.7 for strength, 0.3–0.4 for weak targets such as rheology and flow.

Search space (`space`): `w_b`, `s_b` ranges, binder classes with `{lo, hi, required}`, admixture ranges (%), maximum number of
binder components, curing. Objectives: `clinker_fraction`, `co2`, `cost`, `co2_per_mpa`, `cost_per_mpa` (the cost and CO₂
tables are placeholders; replace them with your own values).

---

## 6. Describing a print job

| Field | Meaning | Default |
|---|---|---|
| `object_type` | wall / hollow_cylinder / column / other | wall |
| `target_height_mm` | target height | required |
| `footprint_mm` | wall length or cylinder diameter → path length per layer | — |
| `wall_filaments` | filaments across the wall thickness | 1 |
| `nozzle_d_mm` or `nozzle_w_mm` + `nozzle_h_mm` | nozzle | — |
| `layer_height_mm`, `layer_width_mm` | layer height / width | 0.5·nozzle, 1.2·nozzle (medians of printable runs) |
| `print_speed_mm_s` | speed | 40 |
| `layer_cycle_time_s` | layer cycle time | path / speed + dwell |
| `open_time_min`, `start_time_after_mixing_min` | open time, start time | — / 0 |
| `safety_factor` | load safety factor | 1.5 |
| `check_buckling` | free-wall buckling check (walls only) | true |

The material is given as measurements (`tau_s0_Pa`, `athix_Pa_s`, density, E/tau_s) or as a mix (→ pmpredict prediction).
Without Athix the literature ratio (median 0.0007 s⁻¹ × tau_s) is used and reported.

---

## 7. Reading the results

- **Prediction** `q50 [q10, q90]`: median and 80 % interval. An interval wider than an order of magnitude is guidance only.
- **weak_model**: few training samples or poor interval coverage / ranking (most rheology and flow models). Published analogue mixes are then the primary evidence.
- **n_range_violations**: number of features outside the training range; non-zero means extrapolation.
- **Retrieval tier**: `exact` = all targets met by measured values, `near` = close.
- **Design candidates**: `p_feasible` (product of per-target probabilities), `ad_max` (applicability-domain distance, <= 1 is interpolation), objective values, DOIs of similar papers. P around 0.3 is normal when rheology targets are involved.
- **Buildability**: `printable / borderline / non_printable` and the governing mode (plastic_collapse, elastic_buckling, open_time). `n_max` is given with and without the safety factor. `R = ρgH/(√3·tau_s)` and the empirical collapse probability (distribution of 146 stack-to-failure tests) are secondary indicators. The cycle-time window is feasible only when min (stability) <= max (open time); when it is closed the required tau_s(0)/Athix and alternatives are reported.

---

## 8. Tool reference

`*` = required input. Slow tools are marked ★.

| Tool | Purpose | Input | Outputs |
|---|---|---|---|
| `list_models` | predictable targets and model quality | variant | model table |
| `describe_vocabulary` | material classes, specimens, curing, target names | family, query | list + mix example |
| `build_mix_spec` | validate a mix dict | mix* | MixSpec JSON |
| `predict_properties` | property prediction | mix*, targets | CSV table, interval PNG |
| `flow_curve` | Bingham flow curve + measured literature curves | mix*, max_rate_1s, n_analogues | PNG, CSV |
| `structuration_curve` | tau_s(t) structuration curve + literature | mix*, max_rest_min, n_analogues | PNG, CSV |
| `retrieve_literature` | published mixes near targets | targets*, system_type, prefer_3dcp, n | literature.csv |
| `design_mix` ★ | inverse design | targets*, space, objectives, budget, top_n | report.md, candidates.csv, pareto.png … |
| `assess_buildability` | verdict + schedule + similar prints | job*, material or mix | assessment.md, sweep PNG/CSV |
| `print_schedule` | cycle-time / speed window only | job*, material or mix | sweep PNG |
| `similar_prints` | similar published prints | job*, material, k | CSV |
| `design_for_print_job` ★ | job → required rheology → mix candidates → verdict per candidate | job*, space, extra_targets, budget | candidates_buildability.csv + design outputs |
| `describe_schema` | DB tables, columns, samples | db, table | — |
| `sql_query` | read-only SELECT (200 rows, 20 s) | sql*, db, max_rows | CSV when > 20 rows |
| `save_report` | save a report | title*, markdown*, tables, include_artifacts, format | .md, .xlsx |
| `remember` | notes that persist across sessions | note*, kind | notes.md |

---

## 9. Sessions, memory, files

- Sessions are stored in `~/.pmpredict/agent/sessions/<id>/` (transcript, metadata, summary). Continue one from the sidebar or with `--session <id>`. Long conversations are summarised automatically.
- Notes left with "remember" accumulate in `~/.pmpredict/agent/notes.md` and enter the system prompt of every session.
- Files created by tools are in `artifacts/reports/agent/<session id>/` (download buttons in the web app). `save_report` writes md and xlsx under `reports/` there.
- Large tool results show 20 rows to the model; the full table is kept as CSV.

---

## 10. Limitations

- The models are correlations in published data. They do not replace experiments; the final mix needs experimental verification.
- Static yield stress, Athix and flow models have 80 % intervals wider than an order of magnitude. Literature static yield stresses mix test protocols (rest time, device).
- Free-wall buckling is the most conservative boundary condition. For closed paths or braced walls use `check_buckling=false` or more filaments. The linear structuration law can overestimate for prints longer than 90 min.
- The cost and CO₂ tables are placeholders.
- While a slow tool runs the web input is locked and there is no cancel button (up to about 2.5 min).
- Subscription backends are for personal use on your own PC. Use an API key for a shared deployment.

---

## 11. Troubleshooting

| Symptom | Action |
|---|---|
| `--check` says chosen: none | add an API key or log in to a subscription (section 2 of STUDENT_README) |
| PowerShell path error | put `&` in front of a quoted path |
| "Not logged in · Please run /login" | the bundled Claude CLI login is separate from the desktop app; run the `auth login` command from `--check` |
| Codex: "MCP tool call requires approval" | update the Codex CLI (`npm i -g @openai/codex`); the app pre-approves its own tools |
| tool error `SpecValidationError` / `NormaliseError` | the agent fixes the input and retries (twice); if it keeps failing, give class names, units and kind explicitly |
| answers too long | add "briefly" or "table only" |
| it forgot the earlier conversation | check the session (`/sessions`); in a new session repeat the summary |
| answers in Korean | start with `PMPREDICT_LANG=en` (the .bat launchers set it) |

---

## 12. Code layout

```
pmpredict/agent/
  tools/registry.py      tool definitions (name, description, JSON schema, function) → Anthropic / OpenAI / MCP projections
  tools/normalise.py     natural-language dict → MixSpec / DesignSpec / PrintJob
  tools/*_tools.py       the 16 tools
  providers/             anthropic_api · openai_api · claude_sdk · codex_cli · fake
  core.py                Agent (prompt, history, tool loop)
  memory.py, prompt.py   session store, system prompt (ko / en)
  i18n.py                UI strings and English prompt
  mcp_server.py          stdio MCP server (pmpredict agent-mcp)
  cli.py                 pmpredict agent
app/streamlit_app.py     chat UI · app/legacy_pages.py legacy forms (Korean)
```
