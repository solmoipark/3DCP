# pmpredict — student setup guide (Windows)

pmpredict is a chat assistant for cement paste / mortar mix design for 3D concrete printing (3DCP). You describe a mix,
a target performance, or a print job in plain English; the assistant calls prediction models trained on a literature
database (3,274 papers), an inverse-design engine, a buildability calculator, literature retrieval and read-only SQL,
and quotes every number from those tool results with an 80 % interval.

Everything you need is in this folder: code, trained models, the literature database and the print-run database.
For the language model you use **one** of: your ChatGPT subscription (Plus/Pro/Team), an OpenAI API key, a Claude
subscription, or an Anthropic API key.

## 0. Prerequisites

| Item | Where | Notes |
|---|---|---|
| Python 3.11 or 3.12 | https://www.python.org/downloads/windows/ | tick **"Add python.exe to PATH"** in the installer |
| Node.js LTS | https://nodejs.org | only for the ChatGPT-subscription backend (installs the Codex CLI) |
| ChatGPT subscription **or** an API key | — | one of them |

## 1. Install (once)

1. Unzip the archive into a path **without spaces or non-ASCII characters**, e.g. `C:\pmpredict`.
2. Double-click **`setup.bat`**. It creates a virtual environment (`.venv`) and installs the packages (5–10 min, needs internet).
3. Wait for `setup finished`.

## 2. Choose a language-model backend (one of A–D)

### A. ChatGPT subscription (recommended)
1. Double-click **`codex_login.bat`**. It installs the OpenAI Codex CLI (`npm i -g @openai/codex`) and opens a browser:
   sign in with **your own ChatGPT account**.
2. Run **`check_backend.bat`** and confirm the `codex` line says `ok`:
   ```
   ok  codex      ChatGPT subscription (Codex CLI)   codex CLI (...)
   chosen: codex
   ```
   - The model is Codex's default. To change it, uncomment the `PMPREDICT_CODEX_MODEL` line in `start_app.bat`.
   - Usage is charged against the limits of the ChatGPT account you logged in with.

### B. OpenAI API key
1. Copy `secrets.example.json` to **`secrets.json`** (same folder) and paste your key into `"openai_api_key"`.
2. `check_backend.bat` should show the `openai` line as `ok`. Default model `gpt-5` (`PMPREDICT_OPENAI_MODEL` to change).

### C. Anthropic API key
Put the key into `"anthropic_api_key"` in `secrets.json`.

### D. Claude Pro/Max subscription
`check_backend.bat` prints the exact `claude.exe auth login` command; run it in PowerShell (the path needs a leading `&`).

If several backends are available the app picks them in the order **API key → Claude subscription → ChatGPT subscription**;
you can switch at any time in the sidebar of the web app.

## 3. Run

- Double-click **`start_app.bat`** → the browser opens http://localhost:8501.
- Left sidebar: backend, model, session, example questions. Type your question in the box at the bottom.
- Terminal use: `.venv\Scripts\activate`, then `python -m pmpredict.cli agent` (commands `/new /sessions /artifacts /quit`).

How to phrase mixes, targets and print jobs, how to read the results, and the full tool list: **`docs/AGENT_GUIDE_EN.md`**.

```
Predict the 28-day compressive strength and flow of an OPC mortar, w/b 0.40, s/b 2.0, PCE 0.5 %
Find 10 published mixes with 28-day compressive strength >= 40 MPa and static yield stress 1-4 kPa (prefer 3DCP)
25 mm nozzle, 600 mm high, 1.5 m long wall (2 filaments), 50 mm/s. Is a material with tau_s 3 kPa and Athix 1 Pa/s printable? Give the cycle-time window.
```

## 4. Folder layout

```
setup.bat / start_app.bat / check_backend.bat / codex_login.bat   scripts
secrets.example.json      API-key template (copy to secrets.json; never share it)
app/                      web UI (Streamlit)
pmpredict/                prediction, inverse design, buildability, agent
artifacts/models/         trained models (27 targets)
data/                     feature/target caches, master.db.xz (literature DB, unpacked on first use), print_process.db
docs/AGENT_GUIDE_EN.md    user guide
```

Files produced by the tools (tables, figures, reports) are written to `artifacts/reports/agent/<session>/` and offered as
download buttons in the web app. Sessions and notes you asked it to remember live in `C:\Users\<you>\.pmpredict\agent\`.

## 5. Troubleshooting

| Symptom | What to do |
|---|---|
| `python` is not recognized | reinstall Python with "Add to PATH" ticked, or open a new terminal |
| `setup.bat` fails on lightgbm / pyarrow | you are probably on Python 3.13+; install 3.12 |
| `setup.bat` fails with `WinError 206` (file name too long) | the folder path is too long; move the folder to a short path such as `C:\pmpredict` and run `setup.bat` again |
| `check_backend.bat` shows `chosen: none` | finish one of the options in section 2; for ChatGPT run `codex login` again |
| `codex` is not recognized | install Node.js, open a new terminal, `npm i -g @openai/codex` |
| the browser does not open | go to http://localhost:8501 yourself; if port 8501 is busy change it in `start_app.bat` |
| the first question is slow | models and data load once (20–40 s) and `master.db.xz` is unpacked once |
| inverse design takes > 2 min | normal (up to ~2.5 min); the input box is locked meanwhile |
| the answer comes back in Korean | `start_app.bat` sets `PMPREDICT_LANG=en`; if you start Streamlit by hand, set that variable first |

## 6. Please note

- Predictions are correlations learned from published data. Always read them with the `q50 [q10, q90]` interval and verify
  the final mix experimentally.
- `secrets.json`, the `.pmpredict` folder and session transcripts are personal; do not share them.
- Subscription logins (ChatGPT / Claude) are for personal use on your own PC. For a shared server use an API key.
