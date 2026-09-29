# 王国之泪助手

可在 iPhone Safari（或「添加到主屏幕」）使用的 HTML5 应用：

- **呀哈哈地图**：地表 / 天空 / 地底显示呀哈哈位置，点击查看坐标与中文找法，「已找到」本地勾选
- **套装图鉴**：全部可成套防具（含 amiibo）的说明、获取方式、套装效果与升级材料；有坐标可地图定位（无套装图形展示）

进度与任务见 [PLAN.md](PLAN.md)。

## 在线访问

**GitHub Pages：** https://wangjun1974.github.io/tearsofthekingdom/

仓库：https://github.com/wangjun1974/tearsofthekingdom

## 本地运行

请用静态服务器打开（Safari 对 `file://` 加载 JSON 可能受限）：

```bash
cd tearsofthekingdom
python3 -m http.server 8080
```

## 重新生成数据

```bash
python3 scripts/build_koroks.py
python3 scripts/build_armors.py
```

- 呀哈哈数据源：`data/map_data_source.json`（来自社区 [lud99/totk-unexplored](https://github.com/lud99/totk-unexplored)）
- 套装数据：`data/armors.json`（自维护简体中文，由 `scripts/build_armors.py` 生成）

## 致谢

- 地图瓦片：[Zelda Dungeon TotK Interactive Map](https://www.zeldadungeon.net/tears-of-the-kingdom-interactive-map/)
- 坐标与类型：社区存档/地图研究（Marc Robledo 等）

本项目为非官方粉丝工具，与任天堂无关。
