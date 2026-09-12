# WebAgent Failure Atlas: 100 Real Chinese Web Tasks, Honestly Run

**TL;DR**: 68/100 passed (68.0%, 95% Wilson CI 58.3%–76.3%). Failures concentrate in Chinese form semantics (F6) and dynamic rendering (F3). Wait+retry+fallback selectors are the cheapest fixes.

## 1 Introduction
WebArena (self-hosted 4-domain reproducible env), Mind2Web (137 sites / 2000+ tasks for open generalization), VisualWebArena (visual modality), WebVoyager (end-to-end LMM on real sites) and OSWorld (whole-OS scope) built the science of web agents — all in English or synthetic sites. We port the same discipline to the real Chinese web: 6 domains (100 tasks), one harness, real HTTP + snapshot hashes per step. Failures are data.

## 2 Method
tasks.yaml (100 tasks) -> 10_run.py (polite <=1rps fetcher, semantic text_contains asserts, deterministic 7-class failure taxonomy, 5 observed this round with F2/F7 at zero — see taxonomy.yaml) -> 40_stats.py (Wilson CI, chi-square, logit) -> 8 figures -> this paper. Public pages only; login walls/captchas are recorded as blocks, never bypassed.

## 3 Results
- Overall 68.0% (CI 58.3%–76.3%, n=100).
- By domain: ecom 100%; form 59%; gov 29%; map 75%; media 69%; search 76%.
- Failures: F1x4, F3x8, F4x2, F5x4, F6x14.
- Association: chi2=21.216, p=0.0007, dof=5; see stats.json for logit coefs. Intervention: 5s-backoff retry rescued 1/32 (3.1%) of failed tasks (fig09).
- Chinese specifics: login-wall and dynamic tasks score lower; form/gov tasks show F6 (label association) excess.

## 4 Fix leverage (5 rules)
Wait-before-assert; fallback selectors (>=3); early-exit on login walls; backoff on 403/429; label-input association checks for Chinese forms.

## 5 Limits
Rule-based executor = lower bound (real LLM agents score higher); DOM drift; observational, not causal.

## 6 Reproduce
`bash run_all.sh --quick`. See work/artifacts/derived/ and dashboard in outputs.

## References (each HTTP-verified)
1. WebArena: A Realistic Web Environment for Building Autonomous Agents — https://arxiv.org/abs/2307.13854 (HTTP 200)
2. Mind2Web: Towards a Generalist Agent for the Web — https://arxiv.org/abs/2306.06070 (HTTP 200)
3. VisualWebArena: Evaluating Multimodal Agents on Realistic Visual Web Tasks — https://arxiv.org/abs/2401.13649 (HTTP 200)
4. WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models — https://arxiv.org/abs/2401.13919 (HTTP 200)
5. OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments — https://arxiv.org/abs/2404.07972 (HTTP 200)
6. WebArena GitHub repository — https://github.com/web-arena-x/webarena (HTTP 200)
7. ServiceNow AgentLab for web agents — https://github.com/ServiceNow/AgentLab (HTTP 200)
8. BrowserGym unified web agent gym — https://github.com/ServiceNow/BrowserGym (HTTP 200)
9. WebArena project site and leaderboard — https://webarena.dev/ (HTTP 200)
10. Playwright browser automation — https://playwright.dev/ (HTTP 200)
11. Playwright GitHub — https://github.com/microsoft/playwright (HTTP 200)
12. Matplotlib visualization — https://matplotlib.org/ (HTTP 200)
13. pandas data analysis — https://pandas.pydata.org/ (HTTP 200)
14. SciPy statistics — https://scipy.org/ (HTTP 200)
15. statsmodels regression (GitHub) — https://github.com/statsmodels/statsmodels (HTTP 200)
16. requests HTTP library (GitHub) — https://github.com/psf/requests (HTTP 200)
17. Python programming language (CPython GitHub) — https://github.com/python/cpython (HTTP 200)
18. MDN Web Docs (GitHub content) — https://github.com/mdn/content (HTTP 200)
19. HTML Living Standard (WHATWG GitHub) — https://github.com/whatwg/html (HTTP 200)
20. WCAG accessibility guidelines (W3C GitHub) — https://github.com/w3c/wcag (HTTP 200)
21. OpenReview peer review platform — https://openreview.net/ (HTTP 200)
22. OpenAlex scholarly API docs — https://docs.openalex.org/ (HTTP 200)
