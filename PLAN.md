# 王国之泪助手（iPhone HTML5）

## 当前进度

- **状态**：呀哈哈地图 + 套装图鉴已实现；已托管于 GitHub Pages（部署后可见最新套装功能）
- **在线地址**：https://wangjun1974.github.io/tearsofthekingdom/
- **模式**：顶栏切换「呀哈哈 / 套装」
- **呀哈哈数据**：全量 **900**（地表 842 / 天空 58 / 地底 0）
- **找法补全**：**330** 条 `detailed`（约 **36.7%**），其余 **570** 条为类型中文模板
- **套装数据**：**35 / 35**（全部可成套防具，含 8 套 amiibo 亦可地图获取；含说明、获取、套装效果、升级材料）
- **运行**：`python3 -m http.server 8080` 后访问；勿用 `file://`

## 目标

可在 iPhone（Safari / 添加到主屏幕）使用的单页 HTML5 应用：

1. **呀哈哈**：在王国之泪地图上显示呀哈哈图标；点击后展示游戏坐标与「如何找到」中文说明。覆盖地表、天空、地底三层。
2. **套装图鉴**：列表浏览全部可成套防具；详情含说明、各件获取方式、套装效果、大妖精升级材料；有坐标的部件可地图定位。

## 任务清单

| ID | 任务 | 状态 |
| ---- | ---- | ---- |
| plan-md | 创建 PLAN.md 与项目脚手架 | done |
| map-layers | Leaflet CRS、三层瓦片与层切换 | done |
| markers-ui | 图标、聚合、底部抽屉 | done |
| korok-data | 全量坐标/类型 + 中文模板 | done |
| guides-detail | 按区域补全 detailed 找法（首批中央海拉鲁等） | done（持续可扩） |
| iphone-qa | iPhone meta / 主屏幕 / manifest 收尾 | done |
| found-check | 「已找到」勾选 + localStorage | done |
| mode-switch | 顶栏「呀哈哈 / 套装」模式切换 | done |
| armor-ui | 套装列表、搜索、详情抽屉、已拥有 | done |
| armor-locate | 部件坐标切层定位 + 临时标记 | done |
| armor-data | 全量 35 套成套防具 JSON（含 amiibo） | done |
| plan-tracking | 随推进更新本文件进度计数 | done |
| brand-rename | manifest / apple title 改为「王国之泪助手」 | done |

## 技术选型

- 纯前端：[`index.html`](index.html) + [`css/app.css`](css/app.css) + [`js/`](js/)
- Leaflet + Zelda Dungeon 对齐 CRS（`mapSizeCoords=12032`，`tileSize=564`，`maxZoom=6`）
- 瓦片：`raw.githubusercontent.com/zeldadungeon/maps/develop/public/totk/tiles/{surface|sky|depths}/{z}/{x}_{y}.jpg`
- 呀哈哈数据：[`data/koroks.json`](data/koroks.json)，由 [`scripts/build_koroks.py`](scripts/build_koroks.py) 生成
- 套装数据：[`data/armors.json`](data/armors.json)，由 [`scripts/build_armors.py`](scripts/build_armors.py) 生成
- 聚合：Leaflet.markercluster（仅呀哈哈模式）
- PWA：[`manifest.webmanifest`](manifest.webmanifest)、`apple-mobile-web-app-*`
- 持久化：呀哈哈 `totk-korok-found-v1`；套装部件 `totk-armor-owned-v1`

## 结构

```
tearsofthekingdom/
  PLAN.md
  README.md
  index.html
  manifest.webmanifest
  css/app.css
  js/app.js map.js markers.js ui.js found.js owned.js armors.js
  data/koroks.json
  data/armors.json
  data/map_data_source.json
  assets/korok.png apple-touch-icon.png
  scripts/build_koroks.py
  scripts/build_armors.py
```

## 验收标准

- [x] 三层地图可切换（地底无呀哈哈属正常）
- [x] 呀哈哈图标 + 聚合；点击底部抽屉显示坐标与中文找法
- [x] 全量点位有至少模板级找法；本文件追踪详述进度
- [x] iPhone 相关 viewport / 主屏幕 meta / manifest
- [x] 「已找到」勾选 + 隐藏已找到（localStorage）
- [x] 顶栏可切换呀哈哈 / 套装，互不破坏现有功能
- [x] 套装列表可浏览、可搜索；详情含说明、获取、套装效果、升级材料（或标明不可升级）
- [x] 有坐标的部件可定位到地图正确层级
- [x] 已拥有状态刷新后仍保留
- [ ] 真机手势与瓦片加载（需手机最终确认）

## 后续可继续

1. 继续扩大呀哈哈 `detailed` 找法覆盖
2. 自托管瓦片以防 GitHub raw 限速
3. 呀哈哈搜索
4. 套装数据坐标细化、商店价格与升级材料校对
