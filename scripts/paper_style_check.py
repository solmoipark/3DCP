# -*- coding: utf-8 -*-
"""Style inventory and numeric-integrity check for a manuscript version (CCR plain-style rules).

  python scripts/paper_style_check.py paper/v02/main.tex [--before paper/v01/main.tex]

Scans prose (outside comments, preamble, listings, tabular and TikZ) for: em dashes, en dashes used as punctuation, semicolons,
colon-label sentence openers, bold lead-in pseudo-headings, banned vocabulary. With --before, prints the digit sequences that
disappeared or appeared between the two versions (numbers must either be unchanged or deliberately removed).
"""
from __future__ import annotations

import argparse
import collections
import re
import sys
from pathlib import Path

BANNED = ["notably", "importantly", "interestingly", "strikingly", "remarkably", "crucially", "it is worth noting", "we emphasise", "we emphasize",
          "of note", "dissolves", "collapses the", "striking", "powerful", "dramatic", "headline", "the picture that emerges", "tells a story",
          "novel", "comprehensive", "state-of-the-art", "seamless", "elegant", "not only", "rather than", "highlighting", "underscoring",
          "demonstrating the potential", "it is widely recognised", "it should be mentioned", "in order to", "honest", "what the benchmark caught",
          "is what a", "cheaply", "frozen", "settlement", "in our previous work", "subscription", "login", "logged in", "student bundle", "launcher",
          "pmpredict", "\\texttt{paper/", "environment variable"]


def prose_lines(tex: str) -> list[tuple[int, str]]:
    out, skip = [], 0
    begin_skip = re.compile(r"\\begin\{(lstlisting|tabular|tikzpicture|verbatim|equation|align|thebibliography)")
    end_skip = re.compile(r"\\end\{(lstlisting|tabular|tikzpicture|verbatim|equation|align|thebibliography)")
    in_doc = False
    for i, ln in enumerate(tex.split("\n"), 1):
        s = ln.split("%")[0] if not ln.strip().startswith("\\%") else ln
        if "\\begin{document}" in s:
            in_doc = True; continue
        if not in_doc:
            continue
        if begin_skip.search(s):
            skip += 1
        if skip == 0 and s.strip() and not s.strip().startswith("\\"):
            out.append((i, s))
        elif skip == 0 and s.strip().startswith(("\\paragraph", "\\caption", "\\section", "\\subsection", "\\casefigure", "\\item")):
            out.append((i, s))
        if end_skip.search(s):
            skip = max(0, skip - 1)
    return out


def inventory(path: Path) -> dict:
    tex = path.read_text(encoding="utf-8")
    lines = prose_lines(tex)
    rep = collections.OrderedDict()
    rep["em dash"] = [(i, s.strip()[:90]) for i, s in lines if "—" in s or "---" in s]
    rep["en dash as punctuation"] = [(i, s.strip()[:90]) for i, s in lines if re.search(r"(?<!\d)\s--\s|[a-zA-Z]–[a-zA-Z ]|\s–\s", s)]
    rep["semicolon"] = [(i, s.strip()[:90]) for i, s in lines if re.search(r";(?![^{]*\})", re.sub(r"\\cite\{[^}]*\}|\\ref\{[^}]*\}|\\label\{[^}]*\}|\\texttt\{[^}]*\}", "", s))]
    rep["colon opener / colon in heading"] = [(i, s.strip()[:90]) for i, s in lines
                                              if re.match(r"^\s*(\\paragraph\{[^}]*\}\s*)?[A-Z][^.:]{0,40}:\s", s) or re.match(r"^\s*\\(sub)?section\{[^}]*:", s)]
    rep["bold lead-in"] = [(i, s.strip()[:90]) for i, s in lines if re.match(r"^\s*\\textbf\{[^}]{2,60}\}[.:]?\s", s)]
    low = [(i, s.lower()) for i, s in lines]
    rep["banned words"] = [(i, f"{w!r}: " + s.strip()[:70]) for i, s in low for w in BANNED if w in s]
    words = len(re.findall(r"\b[A-Za-z][A-Za-z'-]+\b", " ".join(s for _, s in lines)))
    rep["_words"] = words
    return rep


def numbers(path: Path) -> collections.Counter:
    tex = path.read_text(encoding="utf-8")
    body = tex.split("\\begin{document}")[-1]
    body = re.sub(r"\\(cite|ref|label|input|includegraphics|n[A-Za-z]+)\{[^}]*\}", " ", body)
    body = re.sub(r"\\n[A-Za-z]+", " ", body)                        # macros carry the numbers that come from the data
    return collections.Counter(re.findall(r"\d+(?:[.,]\d+)*", body))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("tex"); ap.add_argument("--before", default=None)
    a = ap.parse_args()
    rep = inventory(Path(a.tex))
    print(f"# style inventory: {a.tex} ({rep.pop('_words')} prose words)")
    for k, v in rep.items():
        print(f"\n## {k}: {len(v)}")
        for i, s in v[:25]:
            print(f"  L{i}: {s}")
    if a.before:
        b, c = numbers(Path(a.before)), numbers(Path(a.tex))
        gone = sorted((b - c).items(), key=lambda kv: -kv[1]); new = sorted((c - b).items(), key=lambda kv: -kv[1])
        print(f"\n# numbers typed in prose: before {sum(b.values())}, after {sum(c.values())}")
        print("removed:", ", ".join(f"{k}×{v}" if v > 1 else k for k, v in gone[:60]))
        print("added:", ", ".join(f"{k}×{v}" if v > 1 else k for k, v in new[:60]) or "none")
    return 0


if __name__ == "__main__":
    sys.exit(main())
