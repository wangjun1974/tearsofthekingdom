# 王国之泪呀哈哈地图（iPhone HTML5）

## 当前进度

- **状态**：已托管于 GitHub Pages；已支持「已找到」勾选（localStorage）
- **在线地址**：https://wangjun1974.github.io/tearsofthekingdom/
- **数据**：全量 **900** 个呀哈哈（地表 842 / 天空 58 / 地底 0）
- **找法补全**：**330** 条 `detailed`（约 **36.7%**），其余 **570** 条为类型中文模板
- **详述范围（本批）**：
  - 全部「呀哈哈朋友」运输线 + 全部赛跑（含起终点坐标）
  - 地表近中央区域（|X| < 2000 且 |Z| < 2000）常见谜题类型的逐点中文说明
- **运行**：`python3 -m http.server 8080` 后访问；勿用 `file://`

## 目标

可在 iPhone（Safari / 添加到主屏幕）使用的单页 HTML5 应用：在王国之泪地图上显示呀哈哈图标；点击后展示游戏坐标与「如何找到」中文说明。覆盖地表、天空、地底三层。

## 任务清单

| ID | 任务 | 状态 |
| ---- | ---- | ---- |
| plan-md | 创建 PLAN.md 与项目脚手架 | done |
| map-layers | Leaflet CRS、三层瓦片与层切换 | done |
| markers-ui | 图标、聚合、底部抽屉 | done |
| korok-data | 全量坐标/类型 + 中文模板 | done |
| guides-detail | 按区域补全 detailed 找法（首批中央海拉鲁等） | done（持续可扩） |
| iphone-qa | iPhone meta / 主屏幕 / manifest 收尾 | done |

## 技术选型

- 纯前端：[`index.html`](index.html) + [`css/app.css`](css/app.css) + [`js/`](js/)
- Leaflet + Zelda Dungeon 对齐 CRS（`mapSizeCoords=12032`，`tileSize=564`，`maxZoom=6`）
- 瓦片：`raw.githubusercontent.com/zeldadungeon/maps/develop/public/totk/tiles/{surface\|sky\|depths}/{z}/{x}_{y}.jpg`
- 数据：[`data/koroks.json`](data/koroks.json)，由 [`scripts/build_koroks.py`](scripts/build_koroks.py) 从 [`data/map_data_source.json`](data/map_data_source.json) 生成
- 聚合：Leaflet.markercluster
- PWA 元数据：[`manifest.webmanifest`](manifest.webmanifest)、`apple-mobile-web-app-*`

## 结构

```
tearsofthekingdom/
  PLAN.md
  README.md
  index.html
  manifest.webmanifest
  css/app.css
  js/app.js map.js markers.js ui.js
  data/koroks.json
  data/map_data_source.json
  assets/korok.png apple-touch-icon.png
  scripts/build_koroks.py
```

## 验收标准

- [x] 三层地图可切换（地底无呀哈哈属正常）
- [x] 呀哈哈图标 + 聚合；点击底部抽屉显示坐标与中文找法
- [x] 全量点位有至少模板级找法；本文件追踪详述进度
- [x] iPhone 相关 viewport / 主屏幕 meta / manifest
- [ ] 真机手势与瓦片加载（需你在手机上访问局域网服务器最终确认）

## 后续可继续

1. 继续扩大 `in_central` 或按区域把更多 `template` 改为 `detailed`
2. 自托管瓦片以防 GitHub raw 限速
3. 增加搜索 / 已找到勾选（localStorage）
