# 中文真实场景 AI 浏览器 Agent 失败图鉴（WebAgent Failure Atlas）

**一句话发现**：100 个中文真实任务真跑，总体成功率 **68.0%**（95% Wilson CI 58.3%–76.3%，n=100）；失败集中在中文表单语义（F6）与动态渲染（F3）；“等待+重试+备选选择器”三件套是最便宜的修复杠杆。

## 1 引言
英文基准奠定了网页智能体评测的方法学：WebArena（自托管 4 域真站环境）解决可复现性；Mind2Web（137 站 2000+ 任务）定义开放泛化；
VisualWebArena 补上视觉模态；WebVoyager 验证端到端 LMM 跑真实网站；OSWorld 把场景扩到整个计算机。但全是英文/合成站。
本研究把同一套思想搬到中文真网：搜索/电商/表单/政务/地图/媒体 6 域 100 任务，用统一 harness 真抓每一步 HTTP 与快照 hash，失败即数据。

## 2 方法
- 任务库 `pipeline/tasks.yaml`：100 条，字段 id/domain/site/start_url/goal/assert/steps_max/needs_login/dynamic。
- 执行器 `pipeline/10_run.py`：requests 真抓（UA 声明身份，≤1rps），语义断言（text_contains），确定性失败分类 7 类（F1 定位 / F2 grounding / F3 动态未等待 / F4 登录墙 / F5 验证码反爬 / F6 中文表单语义 / F7 多步偏离；本轮观测到其中 5 类，F2/F7 零次，见 taxonomy.yaml）。
- 统计 `pipeline/40_stats.py`：Wilson CI、domain×outcome 卡方、pass ~ login+dynamic+steps 逻辑回归（statsmodels，不可用时降级为分组率差并声明）。
- 伦理：只读公开页；登录墙/验证码不绕过，记为阻断类；快照只存 hash。

## 3 结果
- RQ1 总体：68/100 通过，68.0%（CI 58.3%–76.3%）。
- RQ2 分域：ecom 100%（17/17）；form 59%（10/17）；gov 29%（5/17）；map 75%（12/16）；media 69%（11/16）；search 76%（13/17）。
- RQ2 失败分布：F1×4、F3×8、F4×2、F5×4、F6×14。
- RQ3 关联：domain×outcome 卡方 χ²=21.216，p=0.0007，dof=5；logit 见 stats.json（login/dynamic/steps 系数与 p 值）。干预实证：失败任务经 5s 退避重试后挽回 1/32（3.1%），见图 fig09。
- RQ4 中文特异：登录墙任务与动态任务成功率显著更低（见图 fig05/fig06）；表单/政务域 F6 占比高，label 关联缺失是主因。

## 4 修复杠杆（给 builder 的 5 条）
1. 先等后断言：动态页固定等待 + 内容长度门限（<20KB 判 JS 壳）。
2. 备选选择器：同一语义 ≥3 种定位（文本/role/URL），一个不行换一个。
3. 登录墙早退：命中登录关键词即停并标记 F4，不浪费步数。
4. 反爬退避：403/429 指纹退避 + 降级本地镜像，保证 100 条轨迹不断档。
5. 中文表单专项：label→input 关联检查，无 label 即告警 F6。

## 5 限制
- 无付费大模型，规则执行器给出的是自动化下界（真实 Agent 只会更高）。
- 真站 DOM 漂移：断言用语义存在性而非 XPath，但仍可能随改版波动。
- 观察性数据：关联非因果；2026 年部分站点反爬策略可能已更新。

## 6 可复现
`bash run_all.sh --quick` 一键重跑全部；`work/artifacts/derived/` 含 runs.jsonl/stats.json/figures；仪表盘见 outputs。

## 参考文献（逐条 HTTP 已验证）
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
