"""Build the self-contained student archive: git-tracked files + the bundled databases + setup scripts.

  python scripts/build_student_bundle.py [--out DIR]

Excluded: anything git-ignored (secrets.json, .venv, caches, logs), claude-memory/, artifacts/reports/external/ (third-party
material), internal scripts. Included on top of the tracked files: data/print_process.db, secrets.example.json, the *.bat
launchers and STUDENT_README.md. The archive root is a single folder pmpredict/.
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE_PREFIXES = ("claude-memory/", "artifacts/reports/external/", "artifacts/reports/slides/", "scripts/kim2026", ".claude/", "%TEMP%")
EXTRA = ["data/print_process.db", "secrets.example.json", "STUDENT_README.md", "setup.bat", "start_app.bat", "check_backend.bat",
         "codex_login.bat", "docs/AGENT_GUIDE_EN.md"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT.parent / "pmpredict_student_bundle"))
    a = ap.parse_args()
    # tracked + untracked-but-not-ignored files, so a new module is never left out (the i18n module was, once)
    tracked = subprocess.check_output(["git", "ls-files", "--cached", "--others", "--exclude-standard"], cwd=ROOT, text=True,
                                      encoding="utf-8").split("\n")
    files = [f for f in tracked if f and not f.startswith(EXCLUDE_PREFIXES) and (ROOT / f).is_file()]
    for e in EXTRA:
        if e not in files:
            if not (ROOT / e).is_file():
                print("missing extra file:", e, file=sys.stderr); return 1
            files.append(e)
    out_dir = Path(a.out); out_dir.mkdir(parents=True, exist_ok=True)
    name = f"pmpredict_student_{dt.date.today().isoformat()}.zip"
    out = out_dir / name
    total = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for f in sorted(files):
            p = ROOT / f
            total += p.stat().st_size
            z.write(p, "pmpredict/" + f)
    print(f"{out}  files={len(files)}  uncompressed={total/1e6:.1f} MB  zip={out.stat().st_size/1e6:.1f} MB")
    return 0


if __name__ == "__main__":
    os.chdir(ROOT)
    sys.exit(main())
