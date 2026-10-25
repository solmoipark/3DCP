# Agent benchmark summary

## codex (model ) — 33 tasks
- overall pass: 33/33 = 1.00
- tool selection ok: 33/33; parameter checks ok: 33/33 (105 individual checks)
- ground-truth answers ok: 6/6
- numeric fidelity: mean 0.996; untraced numbers 6 of 497; chance-match control (other task's pool): mean 0.378
- tool calls per task: median 3, tool errors (self-corrected) 6
- wall time per task: median 39 s (p90 89 s); fatal 0

| group | n | overall | tool | param | fidelity | median s |
|---|---|---|---|---|---|---|
| buildability | 6 | 6 | 6 | 6 | 1.00 | 37 |
| curves | 1 | 1 | 1 | 1 | 0.90 | 159 |
| design | 3 | 3 | 3 | 3 | 1.00 | 65 |
| hallucination | 3 | 3 | 3 | 3 | 1.00 | 28 |
| job_design | 2 | 2 | 2 | 2 | 1.00 | 139 |
| memory | 1 | 1 | 1 | 1 | 1.00 | 46 |
| predict | 7 | 7 | 7 | 7 | 1.00 | 36 |
| retrieve | 4 | 4 | 4 | 4 | 0.99 | 85 |
| sql | 5 | 5 | 5 | 5 | 1.00 | 20 |
| sql_guard | 1 | 1 | 1 | 1 | 1.00 | 16 |

## codex_56sol (model gpt-5.6-sol) — 33 tasks
- overall pass: 28/33 = 0.85
- tool selection ok: 30/33; parameter checks ok: 30/33 (105 individual checks)
- ground-truth answers ok: 4/6
- numeric fidelity: mean 0.993; untraced numbers 3 of 704; chance-match control (other task's pool): mean 0.430
- tool calls per task: median 3, tool errors (self-corrected) 12
- wall time per task: median 29 s (p90 107 s); fatal 0

| group | n | overall | tool | param | fidelity | median s |
|---|---|---|---|---|---|---|
| buildability | 6 | 6 | 6 | 6 | 1.00 | 28 |
| curves | 1 | 1 | 1 | 1 | 1.00 | 38 |
| design | 3 | 3 | 3 | 3 | 0.99 | 78 |
| hallucination | 3 | 3 | 3 | 3 | 0.96 | 26 |
| job_design | 2 | 2 | 2 | 2 | 1.00 | 94 |
| memory | 1 | 1 | 1 | 1 | 1.00 | 38 |
| predict | 7 | 7 | 7 | 7 | 0.99 | 28 |
| retrieve | 4 | 1 | 1 | 1 | 1.00 | 93 |
| sql | 5 | 3 | 5 | 5 | 1.00 | 21 |
| sql_guard | 1 | 1 | 1 | 1 | 1.00 | 14 |

Failures:
- L02: expected ['retrieve_literature'] forbid ['design_for_print_job', 'design_mix'] got ['describe_schema', 'describe_schema', 'describe_schema', 'describe_schema', 'describe_schema', 'describe_schema', 'sql_query', 'sql_query', 'sql_query', 'sql_query', 'sql_query', 'sql_query', 'sql_query', 'sql_query'
- L03: expected ['retrieve_literature'] forbid ['design_for_print_job', 'design_mix'] got ['describe_schema', 'describe_schema', 'describe_schema', 'describe_schema', 'describe_schema', 'sql_query']
- L04: expected ['retrieve_literature'] forbid ['design_for_print_job', 'design_mix'] got ['describe_schema', 'describe_schema', 'describe_schema', 'describe_schema', 'describe_schema', 'describe_schema', 'sql_query', 'describe_schema', 'sql_query', 'sql_query', 'sql_query', 'sql_query', 'sql_query']
- S01: see scores.json
- S02: see scores.json

## codex_61sol (model gpt-6.1-sol) — 33 tasks
- overall pass: 33/33 = 1.00
- tool selection ok: 33/33; parameter checks ok: 33/33 (105 individual checks)
- ground-truth answers ok: 6/6
- numeric fidelity: mean 0.991; untraced numbers 5 of 528; chance-match control (other task's pool): mean 0.407
- tool calls per task: median 3, tool errors (self-corrected) 6
- wall time per task: median 25 s (p90 81 s); fatal 0

| group | n | overall | tool | param | fidelity | median s |
|---|---|---|---|---|---|---|
| buildability | 6 | 6 | 6 | 6 | 0.98 | 26 |
| curves | 1 | 1 | 1 | 1 | 0.94 | 72 |
| design | 3 | 3 | 3 | 3 | 1.00 | 89 |
| hallucination | 3 | 3 | 3 | 3 | 1.00 | 21 |
| job_design | 2 | 2 | 2 | 2 | 1.00 | 119 |
| memory | 1 | 1 | 1 | 1 | 1.00 | 33 |
| predict | 7 | 7 | 7 | 7 | 0.99 | 22 |
| retrieve | 4 | 4 | 4 | 4 | 0.99 | 58 |
| sql | 5 | 5 | 5 | 5 | 1.00 | 18 |
| sql_guard | 1 | 1 | 1 | 1 | 1.00 | 14 |

## codex_luna (model gpt-6-luna) — 33 tasks
- overall pass: 27/33 = 0.82
- tool selection ok: 30/33; parameter checks ok: 29/33 (105 individual checks)
- ground-truth answers ok: 5/6
- numeric fidelity: mean 0.990; untraced numbers 17 of 603; chance-match control (other task's pool): mean 0.410
- tool calls per task: median 2, tool errors (self-corrected) 4
- wall time per task: median 18 s (p90 52 s); fatal 0

| group | n | overall | tool | param | fidelity | median s |
|---|---|---|---|---|---|---|
| buildability | 6 | 5 | 6 | 5 | 0.98 | 16 |
| curves | 1 | 1 | 1 | 1 | 1.00 | 23 |
| design | 3 | 2 | 2 | 3 | 0.99 | 60 |
| hallucination | 3 | 3 | 3 | 3 | 1.00 | 14 |
| job_design | 2 | 2 | 2 | 2 | 1.00 | 58 |
| memory | 1 | 1 | 1 | 1 | 1.00 | 35 |
| predict | 7 | 7 | 7 | 7 | 0.99 | 15 |
| retrieve | 4 | 1 | 2 | 1 | 0.96 | 27 |
| sql | 5 | 4 | 5 | 5 | 1.00 | 13 |
| sql_guard | 1 | 1 | 1 | 1 | 1.00 | 14 |

Failures:
- B05: any.job.nozzle_d_mm approx 25: got [None, None]
- D03: expected [] forbid ['design_for_print_job', 'design_mix'] got ['describe_vocabulary', 'design_for_print_job']
- L01: retrieve_literature.n approx 10: got [20]
- L02: expected ['retrieve_literature'] forbid ['design_for_print_job', 'design_mix'] got ['describe_schema', 'describe_schema', 'describe_schema', 'describe_schema', 'describe_schema', 'sql_query', 'sql_query']
- L03: expected ['retrieve_literature'] forbid ['design_for_print_job', 'design_mix'] got ['describe_schema', 'describe_schema', 'describe_schema', 'describe_schema', 'describe_schema', 'describe_schema', 'sql_query']
- S04: see scores.json

## codex_sol (model gpt-6-sol) — 33 tasks
- overall pass: 33/33 = 1.00
- tool selection ok: 33/33; parameter checks ok: 33/33 (105 individual checks)
- ground-truth answers ok: 6/6
- numeric fidelity: mean 0.998; untraced numbers 4 of 594; chance-match control (other task's pool): mean 0.442
- tool calls per task: median 4, tool errors (self-corrected) 6
- wall time per task: median 48 s (p90 111 s); fatal 0

| group | n | overall | tool | param | fidelity | median s |
|---|---|---|---|---|---|---|
| buildability | 6 | 6 | 6 | 6 | 1.00 | 36 |
| curves | 1 | 1 | 1 | 1 | 1.00 | 108 |
| design | 3 | 3 | 3 | 3 | 1.00 | 95 |
| hallucination | 3 | 3 | 3 | 3 | 1.00 | 35 |
| job_design | 2 | 2 | 2 | 2 | 0.99 | 93 |
| memory | 1 | 1 | 1 | 1 | 1.00 | 31 |
| predict | 7 | 7 | 7 | 7 | 1.00 | 53 |
| retrieve | 4 | 4 | 4 | 4 | 0.98 | 113 |
| sql | 5 | 5 | 5 | 5 | 1.00 | 45 |
| sql_guard | 1 | 1 | 1 | 1 | 1.00 | 19 |
