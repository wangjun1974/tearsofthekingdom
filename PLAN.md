# 王国之泪助手（iPhone HTML5）

## 当前进度

- **状态**：呀哈哈地图 + 套装图鉴（文字详情）；**已取消套装图形展示**
- **在线地址**：https://wangjun1974.github.io/tearsofthekingdom/
- **计划文档**：[`PLAN.md`](PLAN.md)（`~/git/agents/cursor/tearsofthekingdom`；`~/git/agent/...` 不存在）
- **呀哈哈**：全量 **900**；detailed **330 / 900**
- **套装**：**35 / 35**（说明、获取、套装效果、升级材料、地图定位、已拥有）
- **穿戴图形**：**已移除**（不再展示 2D/3D 林克形象）
- **运行**：`python3 -m http.server 8080`；勿用 `file://`

## 目标

1. **呀哈哈**：三层地图、找法、已找到勾选
2. **套装图鉴**：列表 / 搜索 / 文字详情（获取、效果、升级材料）/ 有坐标则地图定位；**不包含套装图形展示**

## 任务清单

| ID | 任务 | 状态 |
| ---- | ---- | ---- |
| map-korok-armor | 呀哈哈地图 + 套装文字图鉴 | done |
| armor-preview-* | 林克穿戴图形预览（2D/3D） | **cancelled** |
| remove-armor-graphic | 取消套装图形展示并清理相关代码 | done |
| pages-deploy | 推送 GitHub Pages | done |

## 技术选型

- 纯前端：Leaflet 地图 + [`data/koroks.json`](data/koroks.json) / [`data/armors.json`](data/armors.json)
- 套装详情仅文字与定位；无 `armor-preview.js` / Three.js

## 验收标准

- [x] 套装详情无图形/人偶预览
- [x] 文字说明、获取、升级材料、定位、已拥有仍可用
- [x] Pages 已更新

## 后续可继续

1. 呀哈哈 detailed 补全
2. 自托管瓦片
3. 呀哈哈搜索
