WebAgent Failure Atlas — 100 real Chinese tasks, 8 tweets:

T1/ We ran 100 REAL Chinese web tasks (search/ecom/form/gov/map/media) with one polite harness. Pass 68/100 (68.0%, 95% CI 58.3%–76.3%). Gov 5/17 (29%) is the hard wall; e-com 17/17 is trivial. Thread + repro:

T2/ By domain: ecom 17/17 (100%) · search 13/17 (76%) · map 12/16 (75%) · media 11/16 (69%) · form 10/17 (59%) · gov 5/17 (29%). chi2=21.216 p=0.0007 — domain matters.

T3/ Failures: F6 Chinese form semantics x14, F3 dynamic rendering x8, F1 locator x4, F5 anti-scrape x4, F4 login wall x2 (F2/F7 0). Soft walls hurt more than captchas.

T4/ Intervention: 5s-backoff retry on 32 fails rescued only 1/32 (3.1%, search-01 F3). Single retry is not the fix — you need label-input checks + wait gates + fallback selectors.

T5/ Method mirrors WebArena/Mind2Web/VisualWebArena/WebVoyager/OSWorld, swapped to real Chinese sites. Polite ≤1rps, public pages only, login walls recorded not bypassed. Rule-based = lower bound.

T6/ Limits honest: n=100 CI ±9%, DOM drift (2026-09-11), observational not causal. 22 refs HTTP-verified, numbers injected from traces.

T7/ Repro: python reproduce.py → PASS in seconds. Full rebuild: bash run_all.sh --quick. Dashboard has 9 figs + 100 rows. Links in next tweet.

T8/ Links: landing page + GitHub + papers + dashboard — all numbers match stats.json. Fix F6/F3 first.
