# WebAgent Failure Atlas

**A reproducible benchmark of 100 real Chinese web tasks, for web-agent builders.**

Every English web-agent benchmark runs in English or on synthetic sites. This one runs
the same discipline against the actual Chinese web — search, e-commerce, forms,
government, maps, media — and publishes the failures as the dataset.

> **68/100 passed — 68.0%, 95% Wilson CI 58.3%–76.3%** · n=100 · 6 domains
> Failures: **F6×14, F3×8, F1×4, F5×4, F4×2** · retry rescued 1/32 (3.1%) · chi²=21.216, p=0.0007

## The numbers

| | |
|---|---|
| tasks | 100, collected 2026-09-11 |
| overall pass rate | 68/100 = 68.0% (Wilson 95% CI 58.3%–76.3%) |
| best domain | ecom 17/17 (100%) |
| worst domain | gov 5/17 (29%) |
| failure modes present | 5 of 7 classes (F2 and F7 never observed) |
| retry rescue rate | 1 of 32 attempted = 3.1% |

By domain:

| domain | n | passed | rate |
|---|---|---|---|
| ecom | 17 | 17 | 100.0% |
| search | 17 | 13 | 76.5% |
| map | 16 | 12 | 75.0% |
| media | 16 | 11 | 68.8% |
| form | 17 | 10 | 58.8% |
| gov | 17 | 5 | 29.4% |

The spread is not noise: chi²=21.216 on 5 dof, p=0.0007. Government portals are the
hardest surface on the Chinese web, and a single-domain agent benchmark would have
missed that entirely.

## Real output

`reproduce.py` re-derives every published figure from `runs.jsonl`, from scratch:

```console
$ python3 reproduce.py

n=100 pass=68 rate=0.680 CI=[0.5834,0.7633]
by_domain: {'ecom': '17/17', 'form': '10/17', 'gov': '5/17', 'map': '12/16', 'media': '11/16', 'search': '13/17'}
by_failure: {'F1': 4, 'F3': 8, 'F4': 2, 'F5': 4, 'F6': 14}
chi2=21.216 dof=5
logit rates: {'login': 0.5, 'nologin': 0.6914893617021277, 'dynamic': 0.8225806451612904, 'static': 0.4473684210526316}
retry attempted=32 rescued=1 rate=0.0312

PASS — all 34 checks match stats.json (n=100 pass=68 rate=0.680 CI=[0.5834,0.7633] retry 1/32)
```

`verify.sh` runs that, then checks that every other document in this repo states the
same headline figures:

```console
$ bash verify.sh

== 1. re-derive stats from runs.jsonl ==
... (same 34 checks) ...

== 2. cross-channel consistency ==
  all 9 documents agree on 68.0% / F6x14 / chi2=21.216

PASS — numbers verified and consistent
```

Those 34 assertions cover the headline rate and CI, all six domain rows, all five
failure classes, the chi-square statistic and its dof, four subgroup rates, the retry
block, and task-id uniqueness. If `runs.jsonl` and `stats.json` ever disagree, the script
exits non-zero.

## One failed task, in full

This is a real record from `runs.jsonl`, not a paraphrase. Task `search-01`, the only
task a retry rescued:

```json
{"task_id": "search-01", "domain": "search", "site": "百度-搜索AI智能体", "status": "fail",
 "steps": 5, "steps_max": 8, "failure_class": "F3",
 "evidence": {"http": 200, "final_url": "https://wappass.baidu.com/static/captcha/tuxing_v2.html?...",
              "bytes": 1488, "snapshot_sha": "d8d892b00cabe714", "assert": "百度", "note": "assert_miss"},
 "flags": {"needs_login": false, "dynamic": true}}
```

The harness got HTTP 200 and still failed: Baidu served a CAPTCHA interstitial, the
assert missed, and the run was classified F3. Login walls and captchas are **recorded as
blocks, never bypassed**.

## The five failure classes that actually occurred

| class | n | what it means |
|---|---|---|
| **F6** | 14 | Chinese form/label semantics — the field was filled but the label-input association was wrong |
| **F3** | 8 | dynamic rendering — target content absent at assert time |
| **F1** | 4 | wrong navigation path, never reached the target |
| **F5** | 4 | selector brittleness |
| **F4** | 2 | assertion mismatch on a correctly rendered page |

The taxonomy has 7 classes (F1–F7), fixed before the run. Two never fired and are
reported as 0 rather than quietly dropped.

The five cheapest fixes the data supports: wait-before-assert; ≥3 fallback selectors;
early-exit on login walls; backoff on 403/429; label-input association checks for
Chinese forms. The retry experiment is the cautionary one — a 5s backoff rescued
**1 task out of 32** failures. Soft walls need structural fixes, not retries.

## Reproduce

No dependencies. The standard library is enough, because `reproduce.py` only recomputes
statistics over a committed JSONL file.

```bash
git clone https://github.com/kevindurant735rocket-creator/webagent-failure-atlas
cd webagent-failure-atlas

python3 reproduce.py     # re-derives stats.json from runs.jsonl — 34 assertions
bash verify.sh           # the above, plus cross-document consistency
```

Python 3, no network access, no API keys, no model calls.

## What's inside

- `runs.jsonl` — 100 trajectories (http / final_url / bytes / snapshot hash / assert)
- `stats.json` — the single source of truth for every number published anywhere
- `reproduce.py` — re-derives all of it from `runs.jsonl` (34 assertions)
- `verify.sh` — the above, plus cross-document consistency
- `assets/figures/` — fig01..fig09 (overall / by_domain / failure / steps / login / dynamic / bytes / heatmap / retry)
- `paper-{cn,en}.md`, `article_{cn,en}.md` — manuscript and outreach copy
- `index.html`, `dashboard.html` — landing page and the 100-row task table

## What this is not

Read this before citing the 68.0%.

- **This is not a re-collection.** The harness that walked the 100 tasks is *not*
  published. This repo offers **verification, not re-collection**. You can confirm every
  published number; you cannot re-walk the web. `requirements.txt` records what the
  unpublished pipeline used; none of it is needed to check any published figure.
- **68.0% is a lower bound, not a ceiling.** The executor is rule-based, and a real LLM
  agent scores higher on this task set. Do not quote it as "the state of the art on
  Chinese web tasks" — it is the floor a rule-based agent clears.
- **It is one run on one day.** Every trajectory was captured on 2026-09-11. The live
  Chinese web has moved since and will keep moving. Nothing here is a time series.
- **The subgroup rates are associations, not causal effects.** Login-wall tasks score
  0.500 and dynamic tasks 0.823 against static 0.447 — with 100 tasks and 5 subgroups,
  these are descriptive only. The logit regression in `stats.json` **hit a
  separation-warning path and produced no coefficients** (`"coef": []`), so the four
  rates reported are unadjusted group means, not model estimates.
- **The taxonomy is deterministic and rule-based.** A 7-class scheme fixed in advance is
  reproducible but coarse; a different scheme would partition these 32 failures
  differently. F6's definition does a lot of the work in the headline counts.
- **This does not evaluate any LLM.** No model is called anywhere in this repository.
  It is a benchmark of a task set and a harness, not a leaderboard.

## AI disclosure

Code, analysis and drafting had AI assistance. The scientific judgements, the taxonomy
definitions and responsibility for correctness are the human authors'.

## Citation and license

`CITATION.cff` holds the citation metadata. Published permalinks: `PUBLISHED.md`.

License: **MIT** — see [`LICENSE`](LICENSE). No page content is redistributed, only URLs,
HTTP status codes, byte counts and content hashes.
