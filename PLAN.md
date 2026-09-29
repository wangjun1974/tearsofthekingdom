# 王国之泪助手（iPhone HTML5）

## 当前进度

- **状态**：呀哈哈 + 套装图鉴 + **穿戴 360° 预览**已实现
- **在线地址**：https://wangjun1974.github.io/tearsofthekingdom/（需推送后更新）
- **模式**：顶栏切换「呀哈哈 / 套装」
- **呀哈哈数据**：全量 **900**（地表 842 / 天空 58 / 地底 0）
- **找法补全**：**330** 条 `detailed`（约 **36.7%**），其余 **570** 条为类型中文模板
- **套装数据**：**35 / 35**（含 amiibo；说明 / 获取 / 效果 / 升级材料）
- **穿戴预览**：**35 / 35** 套装详情含风格化林克人偶，支持拖拽 360° 旋转
- **运行**：`python3 -m http.server 8080` 后访问；勿用 `file://`
- **计划文档**：[`PLAN.md`](PLAN.md)（路径：`~/git/agents/cursor/tearsofthekingdom`；`~/git/agent/...` 不存在）

## 目标

可在 iPhone（Safari / 添加到主屏幕）使用的单页 HTML5 应用：

1. **呀哈哈**：地图显示呀哈哈；点击展示坐标与中文找法；三层地表/天空/地底。
2. **套装图鉴**：列表 + 详情（获取、套装效果、升级材料）；有坐标可地图定位。
3. **穿戴预览**：套装详情页展示林克穿戴该套效果，支持手指拖拽 **360°** 水平旋转。

## 任务清单

| ID | 任务 | 状态 |
| ---- | ---- | ---- |
| plan-md | 创建 PLAN.md 与项目脚手架 | done |
| map-layers | Leaflet CRS、三层瓦片与层切换 | done |
| markers-ui | 图标、聚合、底部抽屉 | done |
| korok-data | 全量坐标/类型 + 中文模板 | done |
| guides-detail | 按区域补全 detailed 找法 | done（持续可扩） |
| iphone-qa | iPhone meta / 主屏幕 / manifest | done |
| found-check | 「已找到」勾选 + localStorage | done |
| mode-switch | 顶栏「呀哈哈 / 套装」模式切换 | done |
| armor-ui | 套装列表、搜索、详情抽屉、已拥有 | done |
| armor-locate | 部件坐标切层定位 + 临时标记 | done |
| armor-data | 全量 35 套成套防具 JSON | done |
| plan-tracking | 随推进更新本文件 | done |
| brand-rename | manifest / apple title「王国之泪助手」 | done |
| armor-preview-360 | 详情页林克穿戴效果 + 拖拽 360° 旋转 | done |

## 技术选型

- 纯前端 + Leaflet 地图 + 套装 JSON
- **穿戴预览**：Three.js CDN + [`js/armor-preview.js`](js/armor-preview.js) 程序化林克人偶；[`data/armors.json`](data/armors.json) 的 `preview` 配色换装；触摸/鼠标拖拽绕 Y 轴 360°，闲置慢速自转；关闭抽屉停止渲染
- **版权**：不使用游戏拆包模型/贴图，为可交互风格化预览
- 持久化：`totk-korok-found-v1` / `totk-armor-owned-v1`

## 结构

```
tearsofthekingdom/
  PLAN.md
  README.md
  index.html
  css/app.css
  js/… armor-preview.js armors.js …
  data/koroks.json armors.json
  scripts/build_koroks.py build_armors.py
```

## 验收标准

- [x] 呀哈哈三层地图、找法、已找到、套装列表/详情/定位/已拥有
- [x] 套装详情页可见林克穿戴该套的预览人偶
- [x] 支持触摸/鼠标拖拽水平 360° 旋转；松手后可恢复轻量自转
- [x] 切换套装时预览配色/头饰样式同步；关闭抽屉停止渲染
- [ ] 真机手势与瓦片加载（需手机最终确认）

## 后续可继续

1. 继续扩大呀哈哈 `detailed` 找法覆盖
2. 自托管瓦片
3. 呀哈哈搜索
4. 套装坐标/材料校对；若有合法自制 glTF 可替换人偶精度
