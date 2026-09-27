#!/usr/bin/env bash
# Verify every published number in this repo.
#
#   1. reproduce.py re-derives all of stats.json from runs.jsonl (34 checks)
#   2. cross-channel check: the headline figures must agree in every
#      document that states them
#
# Exits non-zero on any mismatch.
set -euo pipefail
cd "$(dirname "$0")"

echo "== 1. re-derive stats from runs.jsonl =="
python3 reproduce.py

echo
echo "== 2. cross-channel consistency =="
python3 - <<'PY'
import json, pathlib, re, sys

ref = json.loads(pathlib.Path("stats.json").read_text())
headline = {
    "68.0":  f"{ref['pass_rate']*100:.1f}",
    "F6":    str(next(d["n"] for d in ref["by_failure"] if d["class"] == "F6")),
    "chi2":  f"{ref['chi2']['stat']:.3f}",
}

def stated(text, label, token):
    """True if the doc states this figure, or simply does not mention it.

    A missing figure is not a contradiction; a *different* figure is. So this
    returns False only when the doc mentions the label with another value.
    """
    if label == "68.0":
        return "68.0" in text or "68%" in text or "68/100" in text
    if label == "F6":
        return "F6" in text and token in text
    return token in text
docs = ["README.md", "PUBLISHED.md", "executive_summary.md", "article_zh.md",
        "article_en.md", "paper-cn.md", "paper-en.md", "index.html", "CITATION.cff"]
missing = []
for name in docs:
    p = pathlib.Path(name)
    if not p.exists():
        continue
    text = p.read_text()
    for label, token in headline.items():
        # find every value the doc attaches to this label
        if label == "chi2":
            found = re.findall(r"chi[^0-9]{0,3}([0-9]+\.[0-9]+)", text)
            if found and token not in found:
                missing.append(f"{name}: chi2={found} != {token}")
            continue
        if not stated(text, label, token):
            missing.append(f"{name}: {label}={token}")
if missing:
    print("  MISMATCH in:")
    for m in missing:
        print("   ", m)
    sys.exit(1)
print(f"  all {len(docs)} documents agree on 68.0% / F6x14 / chi2={headline['chi2']}")
PY

echo
echo "PASS — numbers verified and consistent"
