# 王国之泪助手（iPhone HTML5）

## 当前进度

- **状态**：穿戴预览已改为 **2D 正面忠实复刻**（已取消 360°）；Pages 随本提交更新
- **在线地址**：https://wangjun1974.github.io/tearsofthekingdom/
- **计划文档**：[`PLAN.md`](PLAN.md)（`~/git/agents/cursor/tearsofthekingdom`；`~/git/agent/...` 不存在）
- **呀哈哈**：900 点；detailed 330
- **套装**：**35 / 35**
- **穿戴预览**：**35 / 35** — 2D SVG 正面；按 TotK 原设定匹配服装款式、配件、关联兵器（如有）、发型、面部、比例、配色与材质倾向；无改款/现代化/原创元素；不内嵌拆包素材

## 目标

1. 呀哈哈地图
2. 套装图鉴
3. **2D 穿戴复刻**：严格按游戏原设定展示；静态 2D，不要求旋转

## 任务清单

| ID | 任务 | 状态 |
| ---- | ---- | ---- |
| …既有… | 地图 / 套装图鉴 | done |
| armor-preview-2d | 2D SVG 正面复刻替换 Three.js 360° | done |
| pages-deploy | 推送 GitHub Pages | done |

## 技术说明

- [`js/armor-preview.js`](js/armor-preview.js) + `data/armors.json` 的 `preview`
- 已移除 Three.js
- 版权：不使用 Nintendo 拆包精灵图/截图

## 验收

- [x] 详情为 2D 静态正面图，无 360°
- [x] 套装款式/配色/头饰按原设定参数切换
- [x] Pages 更新（本提交）

## 后续

1. 呀哈哈 detailed、瓦片自托管、搜索
2. 若有合法授权官方立绘/精灵，可替换 SVG 层以进一步贴图级一致
