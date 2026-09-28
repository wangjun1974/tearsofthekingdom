# 王国之泪 · 呀哈哈地图

可在 iPhone Safari（或「添加到主屏幕」）使用的 HTML5 地图：在地表 / 天空 / 地底显示呀哈哈位置，点击查看坐标与中文找法。

## 本地运行

请用静态服务器打开（Safari 对 `file://` 加载 JSON 可能受限）：

```bash
cd tearsofthekingdom
python3 -m http.server 8080
```

手机与电脑同一局域网时，访问 `http://<电脑IP>:8080`。

## 重新生成数据

```bash
python3 scripts/build_koroks.py
```

数据源：`data/map_data_source.json`（来自社区 [lud99/totk-unexplored](https://github.com/lud99/totk-unexplored)）。

## 致谢

- 地图瓦片：[Zelda Dungeon TotK Interactive Map](https://www.zeldadungeon.net/tears-of-the-kingdom-interactive-map/)
- 坐标与类型：社区存档/地图研究（Marc Robledo 等）

本项目为非官方粉丝工具，与任天堂无关。

## 进度

见 [PLAN.md](PLAN.md)。
