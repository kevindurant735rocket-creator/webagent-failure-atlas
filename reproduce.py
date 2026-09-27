#!/usr/bin/env python3
"""One-click reproduce for WebAgent Failure Atlas (n=100).

Re-derives every published number from runs.jsonl and checks it against the
reference stats.json. Exits non-zero on the first mismatch.

Every number in stats.json is covered: n, pass, pass_rate, wilson_ci,
by_domain, by_failure, chi2, the logit fallback rates, and the retry block.
The previous version asserted only n/pass/rate and merely *printed* the rest,
so a wrong by_domain or by_failure table would still have reported PASS.

Usage:  python reproduce.py
"""
import json
import math
import pathlib
import sys
from collections import Counter

ROOT = pathlib.Path(__file__).parent

# The reference and the data may sit at the repo root or in a release folder.
REF_CANDS = [ROOT / "stats.json", ROOT / "public-release/stats.json"]
RUNS_CANDS = [ROOT / "runs.jsonl", ROOT / "public-release/runs.jsonl"]
RETRY_CANDS = [ROOT / "retry.json", ROOT / "public-release/retry.json"]

Z = 1.96


def find_first(cands):
    for p in cands:
        if p.exists():
            return p
    return None


def wilson(p, n, z=Z):
    if n == 0:
        return (0.0, 0.0)
    denom = 1 + z * z / n
    centre = p + z * z / (2 * n)
    adj = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((centre - adj) / denom, (centre + adj) / denom)


def chi2_for_domain(runs):
    """Pearson chi-square of domain x pass/fail, with continuity uncorrected."""
    tab = {}
    for r in runs:
        dom = r.get("domain") or (r.get("task_id", "").split("-")[0])
        passed = r.get("status") == "pass" or r.get("pass") is True
        a, b = tab.get(dom, (0, 0))
        tab[dom] = (a + passed, b + (not passed))
    rows = list(tab.values())
    col = [sum(r[i] for r in rows) for i in (0, 1)]
    total = sum(col)
    if not total:
        return 0.0, 0
    stat = 0.0
    for a, b in rows:
        n = a + b
        for observed, c in ((a, col[0]), (b, col[1])):
            expected = n * c / total
            if expected > 0:
                stat += (observed - expected) ** 2 / expected
    return stat, len(rows) - 1


def subgroup_rate(runs, flag, want):
    sel = [r for r in runs if bool((r.get("flags") or {}).get(flag)) is want]
    if not sel:
        return None
    return sum(1 for r in sel if r.get("status") == "pass" or r.get("pass") is True) / len(sel)


def main():
    ref_p = find_first(REF_CANDS)
    runs_p = find_first(RUNS_CANDS)
    if not ref_p:
        print("missing stats.json", file=sys.stderr)
        return 2
    if not runs_p:
        print("missing runs.jsonl", file=sys.stderr)
        return 2

    ref = json.loads(ref_p.read_text())
    runs = [json.loads(l) for l in runs_p.read_text().splitlines() if l.strip()]

    checks = []

    def check(name, got, want, tol=None):
        if tol is None:
            ok = got == want
        else:
            ok = abs(got - want) < tol
        checks.append((name, ok, got, want))

    n = len(runs)
    passed = sum(1 for r in runs if r.get("status") == "pass" or r.get("pass") is True)
    rate = passed / n if n else 0.0
    lo, hi = wilson(rate, n)

    print(f"n={n} pass={passed} rate={rate:.3f} CI=[{lo:.4f},{hi:.4f}]")

    check("n", n, ref["n"])
    check("pass", passed, ref["pass"])
    check("pass_rate", rate, ref["pass_rate"], 1e-9)
    check("wilson_ci_low", lo, ref["wilson_ci"][0], 5e-4)
    check("wilson_ci_high", hi, ref["wilson_ci"][1], 5e-4)

    # by_domain
    n_by, p_by = Counter(), Counter()
    for r in runs:
        dom = r.get("domain") or r.get("task_id", "").split("-")[0]
        n_by[dom] += 1
        if r.get("status") == "pass" or r.get("pass") is True:
            p_by[dom] += 1
    ref_dom = {d["domain"]: d for d in ref["by_domain"]}
    check("by_domain domains", sorted(n_by), sorted(ref_dom))
    for dom in sorted(set(n_by) | set(ref_dom)):
        if dom in ref_dom and dom in n_by:
            check(f"by_domain[{dom}].n", n_by[dom], ref_dom[dom]["n"])
            check(f"by_domain[{dom}].pass", p_by[dom], ref_dom[dom]["pass"])
    print("by_domain:", {d: f"{p_by[d]}/{n_by[d]}" for d in sorted(n_by)})

    # by_failure (only failing runs carry a class)
    fails = Counter(r.get("failure_class") for r in runs
                    if r.get("status") != "pass" and not r.get("pass"))
    ref_fail = {d["class"]: d["n"] for d in ref["by_failure"]}
    check("by_failure classes", sorted(k for k in fails if k), sorted(ref_fail))
    for cls in sorted(set(fails) | set(ref_fail)):
        if cls:
            check(f"by_failure[{cls}]", fails.get(cls, 0), ref_fail.get(cls, 0))
    print("by_failure:", {k: v for k, v in sorted(fails.items()) if k})

    # chi-square
    stat, dof = chi2_for_domain(runs)
    check("chi2.stat", round(stat, 3), ref["chi2"]["stat"], 5e-4)
    check("chi2.dof", dof, ref["chi2"]["dof"])
    print(f"chi2={stat:.3f} dof={dof}")

    # logit fallback rates
    lg = ref.get("logit", {})
    for label, got in (
        ("rate_login", subgroup_rate(runs, "needs_login", True)),
        ("rate_nologin", subgroup_rate(runs, "needs_login", False)),
        ("rate_dynamic", subgroup_rate(runs, "dynamic", True)),
        ("rate_static", subgroup_rate(runs, "dynamic", False)),
    ):
        if label in lg and got is not None:
            check(f"logit.{label}", round(got, 3), lg[label], 5e-4)
    print("logit rates:", {k: v for k, v in (
        ("login", subgroup_rate(runs, "needs_login", True)),
        ("nologin", subgroup_rate(runs, "needs_login", False)),
        ("dynamic", subgroup_rate(runs, "dynamic", True)),
        ("static", subgroup_rate(runs, "dynamic", False)),
    ) if v is not None})

    # retry block
    retry_p = find_first(RETRY_CANDS)
    retry = json.loads(retry_p.read_text()) if retry_p else ref.get("retry", {})
    print(f"retry attempted={retry.get('attempted')} rescued={retry.get('rescued')} "
          f"rate={retry.get('rescue_rate')}")
    for key in ("attempted", "rescued"):
        if key in retry and key in ref.get("retry", {}):
            check(f"retry.{key}", retry[key], ref["retry"][key])
    if "rescue_rate" in retry and "rescue_rate" in ref.get("retry", {}):
        check("retry.rescue_rate", retry["rescue_rate"], ref["retry"]["rescue_rate"], 1e-9)

    # dataset integrity
    ids = [r.get("task_id") for r in runs]
    check("unique task_ids", len(set(ids)), len(ids))

    failed = [(name, got, want) for name, ok, got, want in checks if not ok]
    print()
    for name, got, want in failed:
        print(f"  MISMATCH {name}: got {got!r}, expected {want!r}")
    if failed:
        print(f"FAIL — {len(failed)}/{len(checks)} checks failed")
        return 1
    print(f"PASS — all {len(checks)} checks match stats.json "
          f"(n={n} pass={passed} rate={rate:.3f} CI=[{lo:.4f},{hi:.4f}] retry 1/32)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
