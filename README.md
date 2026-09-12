# WebAgent Failure Atlas — 100 Real Chinese Web Tasks, Honestly Run

> **68/100 passed (68.0%, 95% Wilson CI 58.3%–76.3%)** · n=100 · 6 domains · Failures: F6×14, F3×8, F1×4, F5×4, F4×2 · Retry rescued 1/32 (3.1%) · chi²=21.216 p=0.0007

English benchmarks (WebArena/Mind2Web/VisualWebArena/WebVoyager/OSWorld) are English/synthetic. This ports the discipline to the real Chinese web: search/ecom/form/gov/map/media, one polite harness (≤1rps), semantic asserts, deterministic 7-class taxonomy. Failures are data.

## One-click reproduce
```bash
python reproduce.py
# expected: PASS — n=100 pass=68 rate=0.680 CI=[0.5834,0.7633]  retry 1/32
# or full pipeline:
bash run_all.sh --quick   # rebuilds stats + 9 figs + papers + dashboard
```

## What's inside
- `runs.jsonl` — 100 trajectories (http/final_url/bytes/hash/snapshot_sha)
- `stats.json` — single source of truth (injected into papers/dashboard)
- `assets/figures/` — fig01..fig09 (overall/by_domain/failure/steps/login/dynamic/bytes/heatmap/retry)
- `../outputs/webagent-failure-atlas/paper-{cn,en}.md` — papers (22 refs HTTP-verified)
- `../outputs/webagent-failure-atlas/dashboard.html` — interactive dashboard (100 rows)

## Key numbers (must stay consistent across all channels)
- Overall 68.0% (68/100, CI 58.3%–76.3%)
- By domain: ecom 17/17 (100%) · search 13/17 (76%) · map 12/16 (75%) · media 11/16 (69%) · form 10/17 (59%) · gov 5/17 (29%)
- Failures: F1 4, F3 8, F4 2, F5 4, F6 14 (F2/F7 0)
- Intervention: 5s-backoff retry 1/32 (3.1%, search-01 F3), proof soft walls need structural fixes

## Honest limits
- Rule-based executor = **lower bound** (real LLM agents score higher)
- DOM drift (snapshot 2026-09-11), single run
- Observational association, not causal

## AI disclosure
Code/analysis/drafting had AI assistance; scientific judgments and responsibility are human authors'.

## Citation
See `CITATION.cff`. License: `LICENSE` (MIT).

## Links (filled after publish)
See `PUBLISHED.md` for landing page / GitHub / Zhihu / X permalinks.
