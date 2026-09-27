# Executive Summary — WebAgent Failure Atlas (1-page)

**One-liner**: 100 real Chinese web tasks, honestly run: **68/100 (68.0%, CI 58.3%–76.3%)** passed. Gov services are the hard wall (5/17), e-com is trivial (17/17). Failures cluster in Chinese form semantics (F6×14) and dynamic rendering (F3×8). Single retry rescues only 1/32 (3.1%) — soft walls need structural fixes.

**Why this matters**: WebArena/Mind2Web/VisualWebArena/WebVoyager/OSWorld established the science, but all English/synthetic. This is the Chinese real-web counterpart, same discipline, different site morphology.

**What to take away (5 fixes, cheapest first)**:
1. Wait-before-assert + <20KB JS-shell gate (kills most F3)
2. Fallback selectors ≥3 per semantic (text/role/URL)
3. Early-exit on login-wall keywords (save steps, tag F4)
4. Backoff on 403/429, never bypass
5. Label→input association check for Chinese forms (kills F6)

**Limits**: Rule-based executor = lower bound; DOM drift (2026-09-11); observational not causal; n=100 CI still ±9%.

**Reproduce**: `python reproduce.py` → PASS in seconds (34 checks); `bash verify.sh` also cross-checks every document.
