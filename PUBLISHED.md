# PUBLISHED — WebAgent Failure Atlas 发布台账

> 单一事实源 `stats.json`：n=100 pass=68 rate=0.68 CI[0.5834,0.7633] chi²=21.216 p=0.0007 F6×14 F3×8 F1×4 F5×4 F4×2 retry 1/32 (3.1%)。四渠道数字必须完全一致。

## 四件套状态
| 渠道 | 链接 | 特征文本 | 状态 |
|------|------|----------|------|
| 落地页 | `index.html`（GitHub Pages 未启用） | 68.0% / F6×14 / 1/32 | 仓库内就绪，未上线 |
| GitHub | https://github.com/kevindurant735rocket-creator/webagent-failure-atlas | reproduce.py PASS (34) | **已发布** |
| 知乎 | — | 68.0% / 政务5/17 / F6×14 | 未发布 |
| X | — | 68/100 / F6×14 / 1/32 | 未发布 |

## 各渠道要点
- 落地页：OG 卡 + 4 KPI 卡 + 分域表 + 失败表 + 9 图 + 诚实边界 + 一键复现
- GitHub：`reproduce.py` 秒级 PASS（34 项断言），`verify.sh` 复核全部文档数字
- 知乎：结构【一句话结论→你能带走什么→三步自查法】，剥 markdown 后 `keyboard.paste`，两步发布（发布→更新）
- X：T1..T8 逐条 ≤280（URL计23）已校验，最长205字符，首条含落地页/GitHub链接

## 未做清单
- [x] GitHub 公开仓库 + push（已完成）
- [x] `reproduce.py` 覆盖全部 stats.json 字段（34 项断言）
- [x] 修正指向不存在的 `run_all.sh` 的 11 处引用 → `verify.sh`
- [ ] 落地页发布为公开 URL（需开启 GitHub Pages）
- [ ] 知乎 / X 发布（需本人账号授权）
- [ ] 知乎/X 定时重发/置顶

## 诚实边界（随文必带）
- 不指控具体论文造假，结论是"中文软墙（动态+表单）比硬墙更致命"
- 统计局限如实标注（CI ±9%、logit 分离降级为率差、DOM 漂移）
- AI 使用声明：代码/分析/文稿有 AI 辅助，责任人类作者承担
- 本科级可复现审计定位，非领域突破；单 harness、观察性非因果

## 验证
- `python reproduce.py` → PASS (n=100 pass=68 rate=0.680 CI=[0.5834,0.7633])
- X 线程 8 条均 ≤280，最长 T1 205字符
- 落地页 `python build_public_site.py` → 8372 bytes

## 时间
- 2026-09-12 stage A 完成，GitHub 已发布
- 2026-09-27 复核：34 项断言全通过；修正失效引用与占位符
