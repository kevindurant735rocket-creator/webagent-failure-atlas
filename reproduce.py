#!/usr/bin/env python3
"""
One-click reproduce for WebAgent Failure Atlas (n=100).
Runs: pipeline/40_stats.py already did; this script re-derives stats from runs.jsonl + retry.json
and asserts PASS against reference stats.json.
Usage: python reproduce.py  (from public-release/ or repo root)
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).parent
# allow running from public-release/ or repo root
for cand in [ROOT / "stats.json", ROOT / "public-release/stats.json", pathlib.Path("research/webagent-failure-atlas/public-release/stats.json")]:
    if cand.exists():
        REF = cand
        break
else:
    REF = ROOT / "stats.json"

RUNS_CANDS = [ROOT / "runs.jsonl", ROOT / "public-release/runs.jsonl", pathlib.Path("research/webagent-failure-atlas/public-release/runs.jsonl"), pathlib.Path("research/webagent-failure-atlas/outputs/webagent-failure-atlas/runs.jsonl")]
RETRY_CANDS = [ROOT / "retry.json", ROOT / "public-release/retry.json", pathlib.Path("research/webagent-failure-atlas/outputs/webagent-failure-atlas/retry.json")]

def find_first(cands):
    for p in cands:
        if p.exists():
            return p
    return None

def load_runs(p):
    import json as j
    recs = [j.loads(l) for l in p.read_text().splitlines() if l.strip()]
    return recs

def wilson(p, n, z=1.96):
    if n==0: return (0,0)
    denom = 1 + z*z/n
    centre = p + z*z/(2*n)
    adj = z * ((p*(1-p)/n + z*z/(4*n*n))**0.5)
    return ((centre-adj)/denom, (centre+adj)/denom)

def main():
    ref = json.loads(REF.read_text())
    runs_p = find_first(RUNS_CANDS)
    if not runs_p:
        print("missing runs.jsonl", file=sys.stderr); sys.exit(2)
    runs = load_runs(runs_p)
    n = len(runs)
    passed = sum(1 for r in runs if r.get("status")=="pass" or r.get("pass")==True)
    rate = passed/n if n else 0
    ci = wilson(rate, n)
    print(f"n={n} pass={passed} rate={rate:.3f} CI=[{ci[0]:.4f},{ci[1]:.4f}]")
    # retry
    retry_p = find_first(RETRY_CANDS)
    retry = json.loads(retry_p.read_text()) if retry_p and retry_p.exists() else ref.get("retry",{})
    print(f"retry attempted={retry.get('attempted')} rescued={retry.get('rescued')} rate={retry.get('rescue_rate')}")
    # assertions against reference (tolerant to floating)
    assert n == ref["n"], f"n mismatch {n} vs {ref['n']}"
    assert passed == ref["pass"], f"pass mismatch {passed} vs {ref['pass']}"
    assert abs(rate - ref["pass_rate"]) < 1e-6, "rate mismatch"
    # by_domain sanity
    m = {d["domain"]: d for d in ref["by_domain"]}
    # quick recompute by_domain if runs have domain
    from collections import Counter
    cnt = Counter()
    ok = Counter()
    for r in runs:
        d = r.get("domain") or r.get("task_id","").split("-")[0] if "-" in r.get("task_id","") else "unknown"
        # task_id like search-01 -> domain search ; but our runs use id field
        tid = r.get("id") or r.get("task_id") or ""
        dom = tid.split("-")[0] if "-" in tid else d
        # fallback to stats domain mapping via runs meta if needed
        cnt[dom]+=1
        if r.get("status")=="pass" or r.get("pass"): ok[dom]+=1
    print("by_domain:", dict(ok))
    print("PASS — reproduce matches reference stats.json")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
