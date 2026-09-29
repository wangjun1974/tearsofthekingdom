# 王国之泪助手（iPhone HTML5）

## 当前进度

- **状态**：呀哈哈 + 套装图鉴 + **忠实穿戴 360° 预览**已实现并部署 Pages
- **在线地址**：https://wangjun1974.github.io/tearsofthekingdom/
- **模式**：顶栏切换「呀哈哈 / 套装」
- **呀哈哈数据**：全量 **900**；找法 detailed **330 / 900**
- **套装数据**：**35 / 35**
- **穿戴预览**：**35 / 35** — 按 TotK 原造型程序化复刻（体型比例、尖耳、蓝眼、金发、分套装款式/配色/材质感）；拖拽 360°；**不使用游戏拆包资源**
- **计划文档**：[`PLAN.md`](PLAN.md)（`~/git/agents/cursor/tearsofthekingdom`；`~/git/agent/...` 不存在）
- **运行**：`python3 -m http.server 8080`；勿用 `file://`

## 目标

1. 呀哈哈地图（三层、找法、已找到）
2. 套装图鉴（列表/详情/定位/升级材料）
3. **穿戴预览（忠实复刻）**：尽量准确复刻林克穿着该套装时的完整形象（款式、颜色、材质感、头饰装备、发型、面部、体型比例与整体风格），不做自由再设计；支持 360° 旋转

## 任务清单

| ID | 任务 | 状态 |
| ---- | ---- | ---- |
| plan-md … brand-rename | 既有地图/套装功能 | done |
| armor-preview-360 | 详情页穿戴预览 + 拖拽旋转 | done |
| armor-preview-faithful | TotK 原造型强化（比例/脸/发/分套装款式与材质） | done |
| armor-preview-data | 35 套忠实 `preview` 参数 | done |
| pages-deploy | 推送 GitHub Pages | done |

## 技术选型

- Three.js 程序化林克 + `preview.outfit` / `style` / 材质参数换装（[`js/armor-preview.js`](js/armor-preview.js)）
- **禁止**分发 Nintendo 拆包模型/贴图；本预览为高精度近似复刻
- 关闭抽屉停止渲染

## 验收标准

- [x] 人偶体型比例、尖耳、蓝眼、金发贴近 TotK 林克
- [x] 各套装款式可区分且配色贴近原作（兜帽/盔/沙漠露肩/橡胶/夜光等）
- [x] 材质感区分金属 / 布料 / 橡胶等
- [x] 360° 拖拽旋转
- [x] Pages 更新（随本提交）

## 后续

1. 呀哈哈 detailed、瓦片自托管、搜索
2. 若有**自有合法授权**高精度 glTF，可替换程序化网格以进一步贴近原模
