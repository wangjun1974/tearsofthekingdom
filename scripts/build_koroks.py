#!/usr/bin/env python3
"""Build data/koroks.json from lud99 map_data.json with Chinese guides."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "map_data_source.json"
OUT = ROOT / "data" / "koroks.json"

# English type -> (type_id, typeLabel, template Chinese how-to)
TYPE_INFO = {
    "Rock Lift": (
        "lift_rock",
        "搬起石头",
        "在标记附近寻找可疑的石头，搬起后呀哈哈会出现。",
    ),
    "Korok Friends": (
        "korok_friends",
        "呀哈哈朋友",
        "找到迷路的呀哈哈，用乌尔波扎之力把它送到朋友身边（地图上常有两点连线）。完成后通常获得两颗种子。",
    ),
    "Stationary Lights": (
        "stationary_lights",
        "静止光点",
        "靠近并查看闪烁的光点/花，或站到光点上触发呀哈哈。",
    ),
    "Puzzle Blocks": (
        "puzzle_blocks",
        "拼方块",
        "用乌尔波扎之力把金属方块拼成与旁边图案一致的形状。",
    ),
    "Rock Pattern": (
        "rock_pattern",
        "石头拼图",
        "把散落的石头摆进缺口，拼成完整图案（圆圈、箭头等）。",
    ),
    "Flower Trail": (
        "flower_trail",
        "追花",
        "按顺序触摸/靠近依次出现的黄色小花，跟到终点即可。",
    ),
    "Pinwheel Balloons": (
        "pinwheel_balloons",
        "风车气球",
        "站到风车旁，气球出现后用弓箭射破所有气球。",
    ),
    "Moving Lights": (
        "moving_lights",
        "移动光点",
        "追上移动的光点（可用冲刺或马），碰到后呀哈哈出现。",
    ),
    "Hanging Acorn": (
        "hanging_acorn",
        "悬挂橡果",
        "用弓箭射下树或结构上悬挂的橡果。",
    ),
    "Goal Ring (Race)": (
        "race",
        "赛跑",
        "检查标记旁的树桩/起点，限时穿过光环到达终点。",
    ),
    "Through the Roof": (
        "through_roof",
        "从屋顶落下",
        "把物体（常是石头或果子）从上方开口投进下方容器。",
    ),
    "Catch the Seed": (
        "catch_seed",
        "接种子",
        "接住呀哈哈抛出的种子，或在种子落地前接到它。",
    ),
    "Land on Target": (
        "land_target",
        "落点标靶",
        "从高处滑翔/落下，准确落在目标圆圈内。",
    ),
    "Boulder Stand": (
        "boulder_stand",
        "滚石归位",
        "把附近的大圆石推/搬到凹槽或台座上。",
    ),
    "Pull the Plug": (
        "pull_plug",
        "拔塞子",
        "用乌尔波扎之力拔起木塞或堵塞物，让水流/机关触发。",
    ),
    "Dive": (
        "dive",
        "跳水",
        "从高处跳入水中的目标区域（常有光圈提示）。",
    ),
    "Stationary Balloon": (
        "stationary_balloon",
        "固定气球",
        "用弓箭射破固定位置的气球。",
    ),
    "Offering Plate": (
        "offering",
        "供品盘",
        "在石盘/祭坛上放置指定物品（水果、武器等）作为供品。",
    ),
    "Acorn in a Hole": (
        "acorn_hole",
        "橡果入洞",
        "把橡果投进树洞、洞口或容器中。",
    ),
    "Catch the Light": (
        "catch_light",
        "接住光点",
        "在光点消失前追上并触碰它（可能需要攀爬或滑翔）。",
    ),
    "Repair Roof": (
        "repair_roof",
        "修屋顶",
        "用木板等材料补上屋顶破洞。",
    ),
    "Provide Shelter": (
        "provide_shelter",
        "搭庇护所",
        "用材料为呀哈哈搭一个能挡住雨/提供遮挡的棚子。",
    ),
    "Touch the Target": (
        "touch_target",
        "碰到目标",
        "碰到指定目标（木板、旗帜等），有时需借助弹射或融合。",
    ),
    "Ring the Bell": (
        "ring_bell",
        "敲钟",
        "想办法敲响附近的钟（投掷、箭矢或物理撞击）。",
    ),
}


def layer_for_y(y: float) -> str:
    if y > 750:
        return "sky"
    if y < -300:
        return "depths"
    return "surface"


def region_name(x: float, z: float, layer: str) -> str:
    if layer == "sky":
        return "天空岛屿"
    if layer == "depths":
        return "地底"

    # Approximate surface regions by game X (E/W) and Z (N/S)
    if z > 2500:
        lat = "北"
    elif z > 800:
        lat = "中北"
    elif z > -800:
        lat = "中央"
    elif z > -2500:
        lat = "中南"
    else:
        lat = "南"

    if x < -2500:
        lon = "西"
    elif x < -800:
        lon = "中西"
    elif x < 800:
        lon = "中"
    elif x < 2500:
        lon = "中东"
    else:
        lon = "东"

    key = f"{lat}{lon}"
    names = {
        "北中": "奥尔丁山地区",
        "北中西": "海布拉西部地区",
        "北中东": "奥尔丁东侧",
        "北西": "海布拉山脉",
        "北东": "阿卡莱湖地区",
        "中北中": "海拉鲁平原北侧",
        "中北中西": "塔邦挞雪原一带",
        "中北中东": "拉聂尔湿地一带",
        "中北西": "塔邦挞前线阵地一带",
        "中北東": "阿卡莱地区",
        "中央中": "海拉鲁平原",
        "中央中西": "海拉鲁丘陵/平原西侧",
        "中央中东": "拉聂尔地区西侧",
        "中央西": "格鲁德峡谷北侧",
        "中央东": "拉聂尔地区",
        "中南中": "菲罗尼草原北侧",
        "中南中西": "格鲁德地区北侧",
        "中南中东": "哈特诺一带",
        "中南西": "格鲁德沙漠北缘",
        "中南东": "尼克林/东海岸一带",
        "南中": "菲罗尼草原",
        "南中西": "格鲁德沙漠",
        "南中东": "拉露托湖以南/海岸",
        "南西": "格鲁德沙漠南缘",
        "南東": "东南海岸与群岛",
    }
    return names.get(key, f"海拉鲁（{lat}·{lon}）")


def detailed_howto(entry: dict, type_id: str, type_label: str, template: str) -> tuple[str, str]:
    """Return (howToFind, guideStatus). Mark central Hyrule common types as detailed."""
    p = entry["position"]
    x, y, z = p["x"], p["y"], p["z"]
    layer = layer_for_y(y)
    region = region_name(x, z, layer)

    # Central / near-central Hyrule batch: detailed guides
    in_central = layer == "surface" and abs(x) < 2000 and abs(z) < 2000
    path = entry.get("path")

    if in_central and type_id == "lift_rock":
        text = (
            f"位于{region}附近（约 X:{x:.0f}, Z:{z:.0f}, 高度:{y:.0f}）。"
            f"在标记点周围仔细查看地面、草丛或废墟旁的可搬起石块，搬起后即可发现呀哈哈。"
        )
        return text, "detailed"

    if in_central and type_id == "flower_trail":
        flower_n = ""
        if path and path.get("flowers"):
            flower_n = f"共约 {len(path['flowers'])} 朵花。"
        elif path and path.get("flowerCount"):
            flower_n = f"共约 {path['flowerCount']} 朵花。"
        text = (
            f"位于{region}（约 X:{x:.0f}, Z:{z:.0f}）。"
            f"从第一朵黄花开始，按出现顺序依次触碰后续花朵，跟完整条花径后呀哈哈会出现。"
            f"{flower_n}"
        )
        return text, "detailed"

    if in_central and type_id == "pinwheel_balloons":
        text = (
            f"位于{region}（约 X:{x:.0f}, Z:{z:.0f}）。"
            f"站到风车旁激活气球，用弓箭在时限内射破全部气球。"
        )
        return text, "detailed"

    if in_central and type_id == "puzzle_blocks":
        text = (
            f"位于{region}（约 X:{x:.0f}, Z:{z:.0f}）。"
            f"用乌尔波扎之力把金属块拼成与地面/墙上图案一致的形状。"
        )
        return text, "detailed"

    if in_central and type_id == "rock_pattern":
        text = (
            f"位于{region}（约 X:{x:.0f}, Z:{z:.0f}）。"
            f"把周围散落的小石块填进图案缺口，拼出完整图形。"
        )
        return text, "detailed"

    if in_central and type_id in {
        "stationary_lights",
        "moving_lights",
        "hanging_acorn",
        "offering",
        "dive",
        "land_target",
        "catch_seed",
        "pull_plug",
        "boulder_stand",
        "stationary_balloon",
        "through_roof",
        "acorn_hole",
    }:
        extras = {
            "stationary_lights": "寻找地面或建筑旁闪烁的光点，靠近或站上去触发。",
            "moving_lights": "追上移动的光点并触碰（可骑马或滑翔抄近路）。",
            "hanging_acorn": "用弓箭射下附近树或梁上悬挂的橡果。",
            "offering": "在石盘上放置所需供品（常见为水果）。",
            "dive": "从高处跳入下方水中光圈。",
            "land_target": "滑翔后准确落在地面目标圈内。",
            "catch_seed": "接住呀哈哈抛出的种子。",
            "pull_plug": "拔起木塞或堵塞物触发机关。",
            "boulder_stand": "把大圆石推/搬到凹槽台座上。",
            "stationary_balloon": "用箭射破固定气球。",
            "through_roof": "从上方开口把物体投入下方容器。",
            "acorn_hole": "把橡果投入树洞或容器。",
        }
        text = (
            f"位于{region}（约 X:{x:.0f}, Z:{z:.0f}, 高度:{y:.0f}）。"
            f"{extras[type_id]}类型：{type_label}。"
        )
        return text, "detailed"

    if type_id == "korok_friends" and path and "start" in path and "end" in path:
        sx, sy, sz = path["start"]["x"], path["start"]["y"], path["start"]["z"]
        ex, ey, ez = path["end"]["x"], path["end"]["y"], path["end"]["z"]
        text = (
            f"迷路的呀哈哈大约在起点 (X:{sx:.0f}, Z:{sz:.0f}, 高:{sy:.0f})，"
            f"需要送到终点朋友处 (X:{ex:.0f}, Z:{ez:.0f}, 高:{ey:.0f})。"
            f"用乌尔波扎之力抓住并运输（可搭载载具）。完成后通常获得两颗种子。"
        )
        return text, "detailed"

    if type_id == "race" and path and "start" in path and "end" in path:
        sx, sz = path["start"]["x"], path["start"]["z"]
        ex, ez = path["end"]["x"], path["end"]["z"]
        text = (
            f"赛跑型呀哈哈：在起点附近 (X:{sx:.0f}, Z:{sz:.0f}) 检查树桩开始挑战，"
            f"限时穿过光环抵达终点 (X:{ex:.0f}, Z:{ez:.0f})。"
        )
        return text, "detailed"

    if layer == "sky":
        text = f"【天空】{template} 坐标约 X:{x:.0f}, Z:{z:.0f}, 高度:{y:.0f}（注意落点与滑翔路径）。"
        return text, "template"

    return template, "template"


def convert_one(entry: dict, kind: str, index: int) -> dict:
    p = entry["position"]
    x, y, z = float(p["x"]), float(p["y"]), float(p["z"])
    layer = layer_for_y(y)
    eng_type = entry.get("type") or "Rock Lift"
    type_id, type_label, template = TYPE_INFO.get(
        eng_type,
        ("unknown", eng_type, f"在标记附近探索并完成谜题（类型：{eng_type}）。"),
    )
    how, status = detailed_howto(entry, type_id, type_label, template)
    prefix = "C" if kind == "carry" else "H"
    rec = {
        "id": f"{prefix}-{index:04d}",
        "layer": layer,
        "x": round(x, 2),
        "y": round(y, 2),
        "z": round(z, 2),
        "region": region_name(x, z, layer),
        "type": type_id,
        "typeLabel": type_label,
        "typeEn": eng_type,
        "howToFind": how,
        "guideStatus": status,
        "kind": kind,
        "internalHash": entry.get("internalHash"),
    }
    path = entry.get("path") or {}
    if "start" in path and "end" in path:
        rec["path"] = {
            "start": {
                "x": round(path["start"]["x"], 2),
                "y": round(path["start"]["y"], 2),
                "z": round(path["start"]["z"], 2),
            },
            "end": {
                "x": round(path["end"]["x"], 2),
                "y": round(path["end"]["y"], 2),
                "z": round(path["end"]["z"], 2),
            },
        }
    elif "flowers" in path and path["flowers"]:
        first = path["flowers"][0]["position"]
        last = path["flowers"][-1]["position"]
        rec["path"] = {
            "start": {
                "x": round(first["x"], 2),
                "y": round(first["y"], 2),
                "z": round(first["z"], 2),
            },
            "end": {
                "x": round(last["x"], 2),
                "y": round(last["y"], 2),
                "z": round(last["z"], 2),
            },
            "flowerCount": len(path["flowers"]),
        }
    return rec


def main() -> None:
    src = json.loads(SRC.read_text(encoding="utf-8"))
    out = []
    for i, e in enumerate(src["hidden_koroks"], 1):
        out.append(convert_one(e, "hidden", i))
    for i, e in enumerate(src["carry_koroks"], 1):
        out.append(convert_one(e, "carry", i))

    detailed = sum(1 for k in out if k["guideStatus"] == "detailed")
    by_layer = {}
    for k in out:
        by_layer[k["layer"]] = by_layer.get(k["layer"], 0) + 1

    payload = {
        "meta": {
            "total": len(out),
            "detailed": detailed,
            "template": len(out) - detailed,
            "byLayer": by_layer,
            "source": "lud99/totk-unexplored map_data.json (community coordinates)",
            "coordNote": "游戏坐标：x 东西、y 高度、z 南北；地图标记使用 Leaflet lat=-z, lng=x",
        },
        "koroks": out,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT} total={len(out)} detailed={detailed} layers={by_layer}")


if __name__ == "__main__":
    main()
