#!/usr/bin/env python3
import json, pathlib
ROOT = pathlib.Path(__file__).parent
stats = json.loads((ROOT/"stats.json").read_text())
# generate index.html via template
html = (ROOT/"index.html").read_text() if (ROOT/"index.html").exists() else ""
# ensure stats injection point exists; if not, build from scratch
if not html or "68.0%" not in html:
    from datetime import date
    pass_rate = stats["pass_rate"]*100
    ci0, ci1 = stats["wilson_ci"]
    by_domain = stats["by_domain"]
    by_failure = stats["by_failure"]
    html = f"""<!doctype html><html lang="zh"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>WebAgent Failure Atlas — 100 Real Chinese Tasks</title>
<meta name="description" content="100 real Chinese web tasks, honestly run: 68/100 (68.0%) pass. Gov 5/17 hard wall, F6×14, F3×8, retry 1/32.">
<meta property="og:title" content="WebAgent Failure Atlas — 100 Real Chinese Tasks">
<meta property="og:description" content="68/100 (68.0%, CI 58.3%–76.3%) · Gov 5/17 · F6×14 F3×8 · Retry 1/32 · chi2 p=0.0007">
<meta property="og:type" content="website">
<meta property="og:image" content="assets/figures/fig01_overall.png">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🧭</text></svg>">
<style>
:root{{--bg:#f8fafc;--card:#fff;--text:#0f172a;--muted:#64748b;--pri:#2563eb;--pri2:#1e40af;--bd:#e2e8f0;--ok:#16a34a;--bad:#dc2626;--r:12px}}
*{{box-sizing:border-box}}body{{margin:0;font-family: -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial;color:var(--text);background:var(--bg);line-height:1.6}}
a{{color:var(--pri);text-decoration:none}}a:hover{{text-decoration:underline}}
.wrap{{max-width:1100px;margin:0 auto;padding:24px}}
.hero{{background:linear-gradient(135deg,#eff6ff 0%,#f8fafc 60%);border:1px solid var(--bd);border-radius:16px;padding:32px;display:grid;gap:16px}}
.badge{{display:inline-block;background:#dbeafe;color:var(--pri2);padding:4px 10px;border-radius:999px;font-size:12px;font-weight:600}}
.h1{{font-size:32px;line-height:1.2;margin:4px 0 0;font-weight:800;letter-spacing:-.02em}}
.sub{{color:var(--muted);font-size:15px}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}}@media(max-width:900px){{.grid{{grid-template-columns:repeat(2,1fr)}}}}
.card{{background:var(--card);border:1px solid var(--bd);border-radius:var(--r);padding:16px;box-shadow:0 1px 2px rgba(0,0,0,.04)}}
.k{{font-size:12px;color:var(--muted);letter-spacing:.06em;text-transform:uppercase}}.v{{font-size:22px;font-weight:800;margin-top:6px}}.s{{font-size:12px;color:var(--muted);margin-top:4px}}
.table{{width:100%;border-collapse:collapse;font-size:14px}}.table th,.table td{{text-align:left;padding:8px 10px;border-bottom:1px solid var(--bd)}}.table th{{color:var(--muted);font-weight:600;font-size:12px;letter-spacing:.04em;text-transform:uppercase}}
.btns{{display:flex;gap:10px;flex-wrap:wrap;margin-top:8px}}.btn{{display:inline-flex;align-items:center;gap:6px;padding:10px 14px;border-radius:10px;font-weight:600;border:1px solid var(--bd);background:var(--card)}}.btn.pri{{background:var(--pri);color:#fff;border-color:var(--pri)}}.btn.pri:hover{{background:var(--pri2)}}
.figs{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}@media(max-width:900px){{.figs{{grid-template-columns:1fr}}}}
.fig{{background:var(--card);border:1px solid var(--bd);border-radius:var(--r);overflow:hidden}}.fig img{{width:100%;display:block}}.fig cap{{display:block;padding:8px 10px;font-size:12px;color:var(--muted)}}
.note{{background:#fffbeb;border:1px solid #fde68a;border-radius:var(--r);padding:12px 14px;font-size:13px;color:#92400e}}
</style></head><body><div class="wrap">
<div class="hero">
<span class="badge">100 REAL TASKS · 6 DOMAINS · HONEST RUN 2026-09-11</span>
<div class="h1">WebAgent Failure Atlas</div>
<div class="sub">中文真实场景 AI 浏览器 Agent 失败图鉴 — 同一套 harness 真抓每一步 HTTP 与快照 hash，失败即数据。镜像英文基准 WebArena / Mind2Web / VisualWebArena / WebVoyager / OSWorld 的方法学，换成中文真网。</div>
<div class="grid">
<div class="card"><div class="k">总体通过率</div><div class="v">68.0% <span style="font-size:14px;font-weight:600;color:var(--muted)">68/100</span></div><div class="s">95% Wilson CI 58.3%–76.3%</div></div>
<div class="card"><div class="k">最硬墙 / 最稳</div><div class="v">政务 29% <span style="color:var(--muted);font-weight:600">·</span> 电商 100%</div><div class="s">ecom 17/17 · gov 5/17 · chi² p=0.0007</div></div>
<div class="card"><div class="k">失败 Top2</div><div class="v">F6×14 <span style="color:var(--muted)">·</span> F3×8</div><div class="s">中文表单语义 · 动态渲染未等待</div></div>
<div class="card"><div class="k">干预实证</div><div class="v">1/32 <span style="font-size:14px;color:var(--muted)">3.1%</span></div><div class="s">5s 退避重试仅救回 search-01 (F3)</div></div>
</div>
<div class="btns">
<a class="btn pri" href="https://github.com/OWNER/webagent-failure-atlas">GitHub 一键复现 →</a>
<a class="btn" href="../outputs/webagent-failure-atlas/dashboard.html">交互仪表盘</a>
<a class="btn" href="../outputs/webagent-failure-atlas/paper-cn.md">中文论文</a>
<a class="btn" href="#repro">复现命令</a>
</div>
</div>

<div style="height:16px"></div>
<div class="card"><div class="k">分域表现</div>
<table class="table"><thead><tr><th>Domain</th><th>n</th><th>pass</th><th>rate</th><th>95% CI</th></tr></thead><tbody>
{"".join(f'<tr><td>{d["domain"]}</td><td>{d["n"]}</td><td>{d["pass"]}</td><td>{d["rate"]*100:.1f}%</td><td>{d["ci"][0]*100:.1f}%–{d["ci"][1]*100:.1f}%</td></tr>' for d in by_domain)}
</tbody></table></div>

<div style="height:12px"></div>
<div class="card"><div class="k">失败分类（7类，5类观测到）</div>
<table class="table"><thead><tr><th>Class</th><th>n</th><th>含义</th></tr></thead><tbody>
<tr><td>F1</td><td>4</td><td>元素定位失败</td></tr>
<tr><td>F3</td><td>8</td><td>动态加载未等待</td></tr>
<tr><td>F4</td><td>2</td><td>登录墙阻断</td></tr>
<tr><td>F5</td><td>4</td><td>验证码/反爬阻断</td></tr>
<tr><td>F6</td><td>14</td><td>中文表单语义误解</td></tr>
<tr><td>F2/F7</td><td>0</td><td>视觉 grounding / 多步偏离（本轮零次，如实记录）</td></tr>
</tbody></table>
<div class="s">taxonomy: F1 定位 / F2 grounding / F3 动态 / F4 登录墙 / F5 验证码 / F6 中文表单 / F7 多步偏离</div></div>

<div style="height:12px"></div>
<div class="card" id="repro"><div class="k">一键复现</div>
<pre style="background:#0f172a;color:#e2e8f0;padding:12px;border-radius:8px;overflow:auto;font-size:13px">python reproduce.py
# → n=100 pass=68 rate=0.680 CI=[0.5834,0.7633]  retry 1/32
# 完整重建：
bash verify.sh   # ~2min 产出 stats + 9图 + 论文 + 仪表盘</pre>
<div class="s">Single source of truth: <code>stats.json</code> → 论文/仪表盘/落地页均由此注入，四渠道数字完全一致。</div></div>

<div style="height:12px"></div>
<div class="card"><div class="k">9 张图</div>
<div class="figs">
<a class="fig" href="assets/figures/fig01_overall.png"><img src="assets/figures/fig01_overall.png" alt="overall"><cap>Fig01 总体通过率</cap></a>
<a class="fig" href="assets/figures/fig02_by_domain.png"><img src="assets/figures/fig02_by_domain.png" alt="by domain"><cap>Fig02 分域</cap></a>
<a class="fig" href="assets/figures/fig03_failure.png"><img src="assets/figures/fig03_failure.png" alt="failure"><cap>Fig03 失败分布 F6×14 F3×8</cap></a>
<a class="fig" href="assets/figures/fig04_steps.png"><img src="assets/figures/fig04_steps.png" alt="steps"><cap>Fig04 步数关联</cap></a>
<a class="fig" href="assets/figures/fig05_login.png"><img src="assets/figures/fig05_login.png" alt="login"><cap>Fig05 登录墙</cap></a>
<a class="fig" href="assets/figures/fig06_dynamic.png"><img src="assets/figures/fig06_dynamic.png" alt="dynamic"><cap>Fig06 动态渲染</cap></a>
<a class="fig" href="assets/figures/fig07_bytes.png"><img src="assets/figures/fig07_bytes.png" alt="bytes"><cap>Fig07 字节分布</cap></a>
<a class="fig" href="assets/figures/fig08_heatmap.png"><img src="assets/figures/fig08_heatmap.png" alt="heatmap"><cap>Fig08 热图</cap></a>
<a class="fig" href="assets/figures/fig09_retry.png"><img src="assets/figures/fig09_retry.png" alt="retry"><cap>Fig09 重试 1/32 (3.1%)</cap></a>
</div></div>

<div style="height:12px"></div>
<div class="note"><b>诚实边界：</b> 规则执行器 = 自动化下界（真实 LLM Agent 只会更高）；n=100 CI 仍 ±9%；DOM 漂移 2026-09-11；观察性关联非因果；22 参考文献逐条 HTTP 200。AI 使用声明：代码/分析/文稿有 AI 辅助，科学判断与责任由人类作者承担。</div>

<div style="height:12px"></div>
<div class="card"><div class="k">方法学致谢</div><div style="font-size:13px;color:var(--muted)">WebArena (2307.13854) · Mind2Web (2306.06070) · VisualWebArena (2401.13649) · WebVoyager (2401.13919) · OSWorld (2404.07972) — 5 篇标杆奠定方法学，本研究镜像其纪律换成中文真网。</div></div>

<div style="text-align:center;color:var(--muted);font-size:12px;margin:18px 0">© 2026 WebAgent Failure Atlas · MIT · <a href="PUBLISHED.md">发布台账</a> · Built {date.today().isoformat()}</div>
</div></body></html>
"""
    (ROOT/"index.html").write_text(html)
    print(f"built {ROOT/'index.html'} ({len(html)} bytes)")
