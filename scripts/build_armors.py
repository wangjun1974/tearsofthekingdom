#!/usr/bin/env python3
"""Generate data/armors.json — curated Simplified Chinese armor-set guide."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "armors.json"

RUPEE_COSTS = {"star1": 10, "star2": 50, "star3": 200, "star4": 500}


def piece(pid, slot, name, defense, effect, how, loc=None):
    p = {
        "id": pid,
        "slot": slot,
        "name": name,
        "defense": defense,
        "effect": effect,
        "howToGet": how,
    }
    if loc:
        p["location"] = loc
    return p


def loc(layer, x, y, z, label):
    return {"layer": layer, "x": x, "y": y, "z": z, "label": label}


def ups(*stars):
    """stars: list of list of {item,count} for star1..star4"""
    keys = ["star1", "star2", "star3", "star4"]
    out = {}
    for i, mats in enumerate(stars):
        out[keys[i]] = mats
    out["rupees"] = RUPEE_COSTS
    return out


def m(item, count):
    return {"item": item, "count": count}


SETS = []


def add(s):
    SETS.append(s)


# --- climate / traversal ---
add(
    {
        "id": "hylian",
        "name": "海利亚套装",
        "category": "basic",
        "amiibo": False,
        "upgradable": True,
        "description": "经典旅行者装束，防御可靠、材料常见，适合开荒。完成哈特诺相关支线后可调整兜帽上下。",
        "setBonus": {"level2": None, "note": "无套装奖励"},
        "pieces": [
            piece(
                "hylian_hood",
                "head",
                "海利亚兜帽",
                [3, 5, 8, 12, 20],
                "无",
                "瞭望台防具店购买，70 卢比。",
                loc("surface", -254.0, 126.0, 46.0, "瞭望台防具店"),
            ),
            piece(
                "hylian_tunic",
                "body",
                "海利亚服",
                [3, 5, 8, 12, 20],
                "无",
                "瞭望台防具店购买，130 卢比。",
                loc("surface", -254.0, 126.0, 46.0, "瞭望台防具店"),
            ),
            piece(
                "hylian_trousers",
                "legs",
                "海利亚裤子",
                [3, 5, 8, 12, 20],
                "无",
                "瞭望台防具店购买，120 卢比。",
                loc("surface", -254.0, 126.0, 46.0, "瞭望台防具店"),
            ),
        ],
        "upgrades": ups(
            [m("波克布林的角", 5)],
            [m("波克布林的角", 8), m("波克布林的牙", 5)],
            [m("蓝波克布林的角", 5), m("波克布林的脏器", 5), m("蜥蜴战士的爪子", 5)],
            [m("黑波克布林的角", 5), m("波克布林的脏器", 8), m("琥珀", 15)],
        ),
    }
)

add(
    {
        "id": "snowquill",
        "name": "利特的防寒服",
        "category": "climate",
        "amiibo": False,
        "upgradable": True,
        "description": "利特村售卖的防寒装，单件提供耐寒；三件强化至 ★★ 后冻结无效。",
        "setBonus": {"level2": "冻结无效", "note": "需三件均强化至 ★★"},
        "pieces": [
            piece(
                "snowquill_headdress",
                "head",
                "防雪羽饰",
                [3, 5, 8, 12, 20],
                "耐寒防护",
                "利特村防具店购买，650 卢比。",
                loc("surface", -3615.0, 285.0, -1820.0, "利特村防具店"),
            ),
            piece(
                "snowquill_tunic",
                "body",
                "利特的羽绒服",
                [3, 5, 8, 12, 20],
                "耐寒防护",
                "利特村防具店购买，500 卢比。",
                loc("surface", -3615.0, 285.0, -1820.0, "利特村防具店"),
            ),
            piece(
                "snowquill_trousers",
                "legs",
                "利特的羽绒裤",
                [3, 5, 8, 12, 20],
                "耐寒防护",
                "利特村防具店购买，1000 卢比。",
                loc("surface", -3615.0, 285.0, -1820.0, "利特村防具店"),
            ),
        ],
        "upgrades": ups(
            [m("红雀的羽毛", 3)],
            [m("红雀的羽毛", 5), m("冰凯拉的翅膀", 5)],
            [m("红雀的羽毛", 8), m("冰凯拉的翅膀", 8), m("冰凯拉的脏器", 3)],
            [m("红雀的羽毛", 10), m("冰凯拉的脏器", 5), m("蓝宝石", 5)],
        ),
    }
)

add(
    {
        "id": "flamebreaker",
        "name": "防火石套装",
        "category": "climate",
        "amiibo": False,
        "upgradable": True,
        "description": "鼓隆城防具店出售。埃尔丁高热与岩浆区必备；全套 ★★ 后防火无效（不受火焰伤害）。",
        "setBonus": {"level2": "防火无效", "note": "需三件均强化至 ★★"},
        "pieces": [
            piece(
                "flamebreaker_helm",
                "head",
                "防火石盔",
                [3, 5, 8, 12, 20],
                "耐火防护",
                "鼓隆城防具店购买，1400 卢比。",
                loc("surface", 1680.0, 500.0, -1965.0, "鼓隆城防具店"),
            ),
            piece(
                "flamebreaker_armor",
                "body",
                "防火石铠",
                [3, 5, 8, 12, 20],
                "耐火防护",
                "鼓隆城防具店购买，700 卢比。也可在完成相关鼓隆剧情后于优诺波公司附近获取折扣机会。",
                loc("surface", 1680.0, 500.0, -1965.0, "鼓隆城防具店"),
            ),
            piece(
                "flamebreaker_boots",
                "legs",
                "防火石鞋",
                [3, 5, 8, 12, 20],
                "耐火防护",
                "鼓隆城防具店购买，1200 卢比。",
                loc("surface", 1680.0, 500.0, -1965.0, "鼓隆城防具店"),
            ),
        ],
        "upgrades": ups(
            [m("可燃石", 3), m("莫斯布林的牙", 3)],
            [m("可燃石", 5), m("火凯拉的翅膀", 5)],
            [m("可燃石", 8), m("火凯拉的翅膀", 8), m("火凯拉的脏器", 3)],
            [m("可燃石", 10), m("火凯拉的脏器", 5), m("红宝石", 5)],
        ),
    }
)

add(
    {
        "id": "desert_voe",
        "name": "格鲁德的沙漠服",
        "category": "climate",
        "amiibo": False,
        "upgradable": True,
        "description": "格鲁德地区耐热装。肩甲与裤子在格鲁德小镇时装店（需男扮女装入城），头带在卡拉卡拉集市可买。",
        "setBonus": {"level2": "电属性伤害减少", "note": "需三件均强化至 ★★"},
        "pieces": [
            piece(
                "desert_voe_headband",
                "head",
                "热沙头饰",
                [3, 5, 8, 12, 20],
                "耐热防护",
                "卡拉卡拉集市购买，450 卢比。",
                loc("surface", -3250.0, 140.0, 2580.0, "卡拉卡拉集市"),
            ),
            piece(
                "desert_voe_spaulder",
                "body",
                "热沙护肩",
                [3, 5, 8, 12, 20],
                "耐热防护",
                "格鲁德小镇时装店购买，1300 卢比（需进入小镇）。",
                loc("surface", -3885.0, 145.0, 2965.0, "格鲁德小镇时装店"),
            ),
            piece(
                "desert_voe_trousers",
                "legs",
                "热沙裤子",
                [3, 5, 8, 12, 20],
                "耐热防护",
                "格鲁德小镇时装店购买，650 卢比。",
                loc("surface", -3885.0, 145.0, 2965.0, "格鲁德小镇时装店"),
            ),
        ],
        "upgrades": ups(
            [m("白鸟的羽毛", 3)],
            [m("白鸟的羽毛", 5), m("电凯拉的翅膀", 5)],
            [m("白鸟的羽毛", 8), m("电凯拉的翅膀", 8), m("电凯拉的脏器", 3)],
            [m("白鸟的羽毛", 10), m("电凯拉的脏器", 5), m("黄玉", 5)],
        ),
    }
)

add(
    {
        "id": "zora",
        "name": "卓拉套装",
        "category": "traversal",
        "amiibo": False,
        "upgradable": True,
        "description": "卓拉领地剧情与任务相关装备。提升游泳速度；头盔可在瀑布中向上游。",
        "setBonus": {"level2": "水中冲刺耐力减少", "note": "需三件均强化至 ★★"},
        "pieces": [
            piece(
                "zora_helm",
                "head",
                "卓拉头盔",
                [3, 5, 8, 12, 20],
                "游泳速度提升；可游上瀑布",
                "浮游鳞片岛（天空）洞窟宝箱。",
                loc("sky", 3400.0, 1100.0, 500.0, "浮游鳞片岛"),
            ),
            piece(
                "zora_armor",
                "body",
                "卓拉铠甲",
                [3, 5, 8, 12, 20],
                "游泳速度提升",
                "卓拉主线「希多的请求」中由多雷丸打造赠予。",
                loc("surface", 3300.0, 270.0, 450.0, "卓拉领地"),
            ),
            piece(
                "zora_greaves",
                "legs",
                "卓拉胫甲",
                [3, 5, 8, 12, 20],
                "游泳速度提升",
                "完成卓拉支线「友情的证明」后获取。",
                loc("surface", 3300.0, 270.0, 450.0, "卓拉领地"),
            ),
        ],
        "upgrades": ups(
            [m("利扎尔弗斯的角", 3)],
            [m("利扎尔弗斯的角", 5), m("海拉鲁鲈鱼", 5)],
            [m("蓝利扎尔弗斯的角", 5), m("海拉鲁鲈鱼", 5), m("蜥蜴战士的尾巴", 5)],
            [m("黑利扎尔弗斯的角", 5), m("心心鲈鱼", 10), m("蛋白石", 15)],
        ),
    }
)

add(
    {
        "id": "climbing",
        "name": "攀登套装",
        "category": "traversal",
        "amiibo": False,
        "upgradable": True,
        "description": "提升攀爬速度；全套 ★★ 后攀爬跳跃更省耐力。部件分散在洞窟宝箱中。",
        "setBonus": {"level2": "攀爬跳跃耐力减少", "note": "需三件均强化至 ★★"},
        "pieces": [
            piece(
                "climber_bandana",
                "head",
                "攀登头巾",
                [3, 5, 8, 12, 20],
                "攀爬速度提升",
                "普莱姆斯山洞窟（卓拉领地附近）宝箱。",
                loc("surface", 3660.0, 320.0, 230.0, "普莱姆斯山洞窟"),
            ),
            piece(
                "climbing_gear",
                "body",
                "攀登护手",
                [3, 5, 8, 12, 20],
                "攀爬速度提升",
                "北海拉鲁平原洞窟宝箱。",
                loc("surface", -1200.0, 160.0, -650.0, "北海拉鲁平原洞窟"),
            ),
            piece(
                "climbing_boots",
                "legs",
                "攀登鞋",
                [3, 5, 8, 12, 20],
                "攀爬速度提升",
                "卓拉高地间道（Upland Zorana Byroad）洞窟宝箱。",
                loc("surface", 2850.0, 280.0, 300.0, "卓拉高地间道"),
            ),
        ],
        "upgrades": ups(
            [m("克洛格的叶子", 3), m("凯拉的翅膀", 3)],
            [m("电凯拉的翅膀", 5), m("黄色丘丘胶", 5)],
            [m("冰凯拉的翅膀", 5), m("白色丘丘胶", 5), m("青蛙", 10)],
            [m("火凯拉的翅膀", 5), m("红色丘丘胶", 10), m("钻石", 5)],
        ),
    }
)

add(
    {
        "id": "froggy",
        "name": "蛙之套装",
        "category": "traversal",
        "amiibo": False,
        "upgradable": True,
        "description": "提升防滑；全套 ★★ 后雨天攀爬不滑落。通过幸运草报社「疑似公主目击情报」系列驿站采访任务奖励获取。",
        "setBonus": {"level2": "雨天攀爬不滑落", "note": "需三件均强化至 ★★"},
        "pieces": [
            piece(
                "froggy_hood",
                "head",
                "蛙之兜帽",
                [3, 5, 8, 12, 20],
                "滑落防护",
                "完成幸运草报社驿站系列任务至对应进度后由特雷西奖励。起点：利特村东幸运草报社。",
                loc("surface", -3250.0, 200.0, -1780.0, "幸运草报社"),
            ),
            piece(
                "froggy_sleeve",
                "body",
                "蛙之袖套",
                [3, 5, 8, 12, 20],
                "滑落防护",
                "同上，驿站采访任务阶段性奖励。",
                loc("surface", -3250.0, 200.0, -1780.0, "幸运草报社"),
            ),
            piece(
                "froggy_leggings",
                "legs",
                "蛙之绑腿",
                [3, 5, 8, 12, 20],
                "滑落防护",
                "同上，完成全部相关驿站目击任务后凑齐。",
                loc("surface", -3250.0, 200.0, -1780.0, "幸运草报社"),
            ),
        ],
        "upgrades": ups(
            [m("Sticky Lizard", 3), m("Horriblin Horn", 3)],
            [m("Sticky Lizard", 5), m("Blue Horriblin Horn", 5)],
            [m("Sticky Lizard", 5), m("Black Horriblin Horn", 5), m("Horriblin Guts", 5)],
            [m("Sticky Lizard", 10), m("Silver Horriblin Horn", 5), m("Horriblin Guts", 10)],
        ),
    }
)

# Fix froggy materials to Chinese
SETS[-1]["upgrades"] = ups(
    [m("黏糊糊的蜥蜴", 3), m("霍拉布林的角", 3)],
    [m("黏糊糊的蜥蜴", 5), m("蓝霍拉布林的角", 5)],
    [m("黏糊糊的蜥蜴", 5), m("黑霍拉布林的角", 5), m("霍拉布林的脏器", 5)],
    [m("黏糊糊的蜥蜴", 10), m("银霍拉布林的角", 5), m("霍拉布林的脏器", 10)],
)

add(
    {
        "id": "glide",
        "name": "滑翔套装",
        "category": "traversal",
        "amiibo": False,
        "upgradable": True,
        "description": "天空岛跳水挑战奖励。提升滑翔稳定性；全套 ★★ 后落地伤害无效。",
        "setBonus": {"level2": "落地伤害无效", "note": "需三件均强化至 ★★"},
        "pieces": [
            piece(
                "glide_mask",
                "head",
                "滑翔面罩",
                [2, 4, 6, 9, 16],
                "滑翔时抗风",
                "勇气之岛（Valor Island）完成跳水挑战。",
                loc("sky", 4500.0, 1200.0, -800.0, "勇气之岛"),
            ),
            piece(
                "glide_shirt",
                "body",
                "滑翔紧身衣",
                [2, 4, 6, 9, 16],
                "滑翔时抗风",
                "刚毅之岛（Courage Island）完成跳水挑战。",
                loc("sky", -1300.0, 1100.0, 2200.0, "刚毅之岛"),
            ),
            piece(
                "glide_tights",
                "legs",
                "滑翔紧身裤",
                [2, 4, 6, 9, 16],
                "滑翔时抗风",
                "勇健之岛（Bravery Island）完成跳水挑战。",
                loc("sky", -800.0, 1000.0, -2200.0, "勇健之岛"),
            ),
        ],
        "upgrades": ups(
            [m("凯拉的翅膀", 3), m("云海蘑菇", 5)],
            [m("凯拉的翅膀", 5), m("云海蘑菇", 10)],
            [m("凯拉的脏器", 6), m("艾露迪诺蘑菇", 8)],
            [m("巨型艾露迪诺蘑菇", 8), m("凯拉的脏器", 8), m("钻石", 5)],
        ),
    }
)

add(
    {
        "id": "rubber",
        "name": "橡胶套装",
        "category": "climate",
        "amiibo": False,
        "upgradable": True,
        "description": "提升耐电；全套 ★★ 后落雷无效。部件在各区域洞窟宝箱中。",
        "setBonus": {"level2": "落雷无效", "note": "需三件均强化至 ★★"},
        "pieces": [
            piece(
                "rubber_helm",
                "head",
                "橡胶头盔",
                [3, 5, 8, 12, 20],
                "耐电防护",
                "萨琼树林洞窟（纳克罗达）宝箱。",
                loc("surface", 1200.0, 120.0, 2800.0, "萨琼树林洞窟"),
            ),
            piece(
                "rubber_armor",
                "body",
                "橡胶铠甲",
                [3, 5, 8, 12, 20],
                "耐电防护",
                "风鸣山丘洞窟（海拉鲁平原）宝箱；击败内部电击拉奇等后取得。",
                loc("surface", -50.0, 80.0, 900.0, "风鸣山丘洞窟"),
            ),
            piece(
                "rubber_tights",
                "legs",
                "橡胶紧身裤",
                [3, 5, 8, 12, 20],
                "耐电防护",
                "霍伦泻湖洞窟（拉聂尔）宝箱。",
                loc("surface", 4200.0, 100.0, 200.0, "霍伦泻湖洞窟"),
            ),
        ],
        "upgrades": ups(
            [m("黄色丘丘胶", 3), m("电凯拉的翅膀", 3)],
            [m("黄色丘丘胶", 5), m("电凯拉的翅膀", 5)],
            [m("黄色丘丘胶", 5), m("电凯拉的脏器", 5), m("电球果", 5)],
            [m("黄色丘丘胶", 10), m("电凯拉的脏器", 8), m("黄玉", 5)],
        ),
    }
)

add(
    {
        "id": "stealth",
        "name": "潜行套装",
        "category": "stealth",
        "amiibo": False,
        "upgradable": True,
        "description": "提升安静度，便于靠近动物与敌人。可在卡卡利科村防具店购买。",
        "setBonus": {"level2": "夜间移动速度提升", "note": "需三件均强化至 ★★"},
        "pieces": [
            piece(
                "stealth_mask",
                "head",
                "潜行面罩",
                [2, 4, 6, 9, 16],
                "安静度提升",
                "卡卡利科村防具店购买，500 卢比。",
                loc("surface", 1840.0, 220.0, 1000.0, "卡卡利科村防具店"),
            ),
            piece(
                "stealth_chest",
                "body",
                "潜行紧身衣",
                [2, 4, 6, 9, 16],
                "安静度提升",
                "卡卡利科村防具店购买，700 卢比。",
                loc("surface", 1840.0, 220.0, 1000.0, "卡卡利科村防具店"),
            ),
            piece(
                "stealth_tights",
                "legs",
                "潜行紧身裤",
                [2, 4, 6, 9, 16],
                "安静度提升",
                "卡卡利科村防具店购买，600 卢比。",
                loc("surface", 1840.0, 220.0, 1000.0, "卡卡利科村防具店"),
            ),
        ],
        "upgrades": ups(
            [m("蓝色夜光石", 3), m("日落萤火虫", 3)],
            [m("蓝色夜光石", 5), m("日落萤火虫", 5)],
            [m("夜光石", 5), m("静音公主", 5), m("斯塔尔的脏器", 3)],
            [m("夜光石", 5), m("静音公主", 10), m("斯塔尔的脏器", 5)],
        ),
    }
)

# --- combat / special ---
add(
    {
        "id": "barbarian",
        "name": "蛮族套装",
        "category": "combat",
        "amiibo": False,
        "upgradable": True,
        "description": "提升攻击力；全套 ★★ 后蓄力攻击更省耐力。地图上米斯科宝藏相关任务会标出位置。",
        "setBonus": {"level2": "蓄力攻击耐力减少", "note": "需三件均强化至 ★★"},
        "pieces": [
            piece(
                "barbarian_helm",
                "head",
                "蛮族头盔",
                [3, 5, 8, 12, 20],
                "攻击力提升",
                "罗布雷德断崖洞窟宝箱。",
                loc("surface", 2450.0, 180.0, 800.0, "罗布雷德断崖洞窟"),
            ),
            piece(
                "barbarian_armor",
                "body",
                "蛮族铠甲",
                [3, 5, 8, 12, 20],
                "攻击力提升",
                "克雷内尔山丘洞窟宝箱。",
                loc("surface", 800.0, 150.0, -400.0, "克雷内尔山丘洞窟"),
            ),
            piece(
                "barbarian_legwraps",
                "legs",
                "蛮族绑腿",
                [3, 5, 8, 12, 20],
                "攻击力提升",
                "瓦尔诺特山洞窟宝箱。",
                loc("surface", 3400.0, 250.0, 1800.0, "瓦尔诺特山洞窟"),
            ),
        ],
        "upgrades": ups(
            [m("莱尼尔的角", 3)],
            [m("蓝鬃莱尼尔的角", 3), m("莱尼尔的蹄", 2)],
            [m("白鬃莱尼尔的角", 3), m("莱尼尔的蹄", 3), m("莱尼尔的脏器", 1)],
            [m("银莱尼尔的角", 3), m("莱尼尔的脏器", 3), m("龙的碎片", 1)],
        ),
    }
)

add(
    {
        "id": "radiant",
        "name": "夜光套装",
        "category": "combat",
        "amiibo": False,
        "upgradable": True,
        "description": "卡卡利科村「蛊惑」防具店出售（完成「深暗带来的病」等支线后更易购入）。全套 ★★ 后骨武器伤害提升，骷髅敌不主动攻击。",
        "setBonus": {
            "level2": "骨武器伤害提升；骷髅类敌人不攻击",
            "note": "需三件均强化至 ★★",
        },
        "pieces": [
            piece(
                "radiant_mask",
                "head",
                "夜光面罩",
                [3, 5, 8, 12, 20],
                "无（套装相关）",
                "卡卡利科村蛊惑店购买，800 卢比。",
                loc("surface", 1840.0, 220.0, 1000.0, "卡卡利科村蛊惑店"),
            ),
            piece(
                "radiant_shirt",
                "body",
                "夜光衫",
                [3, 5, 8, 12, 20],
                "无（套装相关）",
                "卡卡利科村蛊惑店购买，800 卢比。",
                loc("surface", 1840.0, 220.0, 1000.0, "卡卡利科村蛊惑店"),
            ),
            piece(
                "radiant_tights",
                "legs",
                "夜光紧身裤",
                [3, 5, 8, 12, 20],
                "无（套装相关）",
                "卡卡利科村蛊惑店购买，800 卢比。",
                loc("surface", 1840.0, 220.0, 1000.0, "卡卡利科村蛊惑店"),
            ),
        ],
        "upgrades": ups(
            [m("夜光石", 5), m("波克布林的脏器", 3)],
            [m("夜光石", 8), m("莫力布林的脏器", 3)],
            [m("夜光石", 10), m("莱尼尔的脏器", 2), m("被诅咒的骷髅骨头", 3)],
            [m("夜光石", 20), m("莱尼尔的脏器", 3), m("钻石", 1)],
        ),
    }
)

add(
    {
        "id": "soldier",
        "name": "海利亚士兵套装",
        "category": "basic",
        "amiibo": False,
        "upgradable": True,
        "description": "高防御基础套，无特殊效果。位于瞭望台紧急避难所连通的王室隐秘通道。",
        "setBonus": {"level2": None, "note": "无套装奖励"},
        "pieces": [
            piece(
                "soldier_helm",
                "head",
                "海利亚士兵头盔",
                [4, 7, 12, 18, 28],
                "无",
                "王室隐秘通道（瞭望台紧急避难所地下）宝箱。",
                loc("surface", -250.0, 50.0, 50.0, "瞭望台紧急避难所入口"),
            ),
            piece(
                "soldier_armor",
                "body",
                "海利亚士兵铠甲",
                [4, 7, 12, 18, 28],
                "无",
                "王室隐秘通道深处宝箱，需炸开/打碎大量岩石。",
                loc("surface", -250.0, 50.0, 50.0, "瞭望台紧急避难所入口"),
            ),
            piece(
                "soldier_greaves",
                "legs",
                "海利亚士兵护胫",
                [4, 7, 12, 18, 28],
                "无",
                "王室隐秘通道宝箱。",
                loc("surface", -250.0, 50.0, 50.0, "瞭望台紧急避难所入口"),
            ),
        ],
        "upgrades": ups(
            [m("丘丘胶", 5), m("波克布林的脏器", 3)],
            [m("凯拉的翅膀", 5), m("莫力布林的脏器", 3)],
            [m("凯拉的脏器", 3), m("莱尼尔的脏器", 1), m("琥珀", 15)],
            [m("莱尼尔的脏器", 3), m("钻石", 2), m("星辰碎片", 1)],
        ),
    }
)

add(
    {
        "id": "royal_guard",
        "name": "近卫兵套装",
        "category": "combat",
        "amiibo": False,
        "upgradable": True,
        "description": "海拉鲁城堡内宝箱。单件减少蓄力攻击耐力消耗；全套强化后效果进一步加强。",
        "setBonus": {"level2": "蓄力攻击耐力大幅减少", "note": "需三件均强化至 ★★；与单件效果叠加"},
        "pieces": [
            piece(
                "royal_guard_cap",
                "head",
                "近卫兵帽子",
                [4, 7, 12, 18, 28],
                "蓄力攻击耐力减少",
                "海拉鲁城堡塞尔达房间相关区域宝箱。",
                loc("surface", -250.0, 280.0, -100.0, "海拉鲁城堡"),
            ),
            piece(
                "royal_guard_uniform",
                "body",
                "近卫兵制服",
                [4, 7, 12, 18, 28],
                "蓄力攻击耐力减少",
                "海拉鲁城堡卫兵室宝箱。",
                loc("surface", -250.0, 200.0, -80.0, "海拉鲁城堡卫兵室附近"),
            ),
            piece(
                "royal_guard_boots",
                "legs",
                "近卫兵靴子",
                [4, 7, 12, 18, 28],
                "蓄力攻击耐力减少",
                "海拉鲁城堡国王书房宝箱。",
                loc("surface", -230.0, 260.0, -120.0, "海拉鲁城堡国王书房附近"),
            ),
        ],
        "upgrades": ups(
            [m("首领波克布林的角", 3), m("波克布林的脏器", 3)],
            [m("首领波克布林的角", 5), m("莫力布林的脏器", 3)],
            [m("首领蓝波克布林的角", 3), m("莫尔德拉吉克的鳍", 3), m("莫尔德拉吉克的脏器", 1)],
            [m("首领黑波克布林的角", 3), m("古栗欧克的脏器", 3), m("星辰碎片", 1)],
        ),
    }
)

add(
    {
        "id": "yiga",
        "name": "依盖队套装",
        "category": "stealth",
        "amiibo": False,
        "upgradable": True,
        "description": "伪装成依盖队员，靠近据点内敌人时不易被识破。通过依盖队基地任务与兑换获取。",
        "setBonus": {"level2": "夜间移动速度提升", "note": "需三件均强化至 ★★"},
        "pieces": [
            piece(
                "yiga_mask",
                "head",
                "依盖队面罩",
                [1, 3, 5, 7, 12],
                "安静度提升；依盖伪装",
                "击败对应依盖队员后，在初始台地小屋取得。",
                loc("surface", -1000.0, 150.0, 1800.0, "初始台地小屋一带"),
            ),
            piece(
                "yiga_armor",
                "body",
                "依盖队紧身衣",
                [1, 3, 5, 7, 12],
                "安静度提升；依盖伪装",
                "击败对应依盖队员后，在阿卡莱古代研究所取得。",
                loc("surface", 4500.0, 180.0, -2100.0, "阿卡莱古代研究所"),
            ),
            piece(
                "yiga_tights",
                "legs",
                "依盖队紧身裤",
                [1, 3, 5, 7, 12],
                "安静度提升；依盖伪装",
                "击败对应依盖队员后，在马里塔支部（海拉鲁山脊）取得。",
                loc("surface", -2800.0, 180.0, -400.0, "依盖队马里塔支部"),
            ),
        ],
        "upgrades": ups(
            [m("奥克塔的眼球", 2), m("依盖队布片", 3)],
            [m("火焰奥克塔的眼球", 3), m("依盖队布片", 5)],
            [m("冰雪奥克塔的眼球", 5), m("凯拉的脏器", 3), m("依盖队布片", 5)],
            [m("电奥克塔的眼球", 5), m("凯拉的脏器", 5), m("钻石", 1)],
        ),
    }
)

add(
    {
        "id": "ember",
        "name": "火焰套装",
        "category": "elemental",
        "amiibo": False,
        "upgradable": True,
        "description": "炎热天气下提升攻击；全套 ★★ 后炎热时蓄力更快并附带火焰爆发。",
        "setBonus": {
            "level2": "炎热时蓄力加速，并产生火焰爆发",
            "note": "需三件均强化至 ★★",
        },
        "pieces": [
            piece(
                "ember_headdress",
                "head",
                "火焰头饰",
                [2, 4, 6, 9, 16],
                "炎热时攻击力提升",
                "优诺波公司本部南洞窟宝箱。",
                loc("surface", 1620.0, 520.0, -2100.0, "优诺波公司南洞窟"),
            ),
            piece(
                "ember_shirt",
                "body",
                "火焰衫",
                [2, 4, 6, 9, 16],
                "炎热时攻击力提升",
                "鼓隆比河洞窟宝箱。",
                loc("surface", 1400.0, 280.0, -1600.0, "鼓隆比河洞窟"),
            ),
            piece(
                "ember_trousers",
                "legs",
                "火焰裤",
                [2, 4, 6, 9, 16],
                "炎热时攻击力提升",
                "塞弗拉湖洞窟宝箱。",
                loc("surface", 2500.0, 220.0, -1400.0, "塞弗拉湖洞窟"),
            ),
        ],
        "upgrades": ups(
            [m("火凯拉的翅膀", 3), m("夏洛克蘑菇", 3)],
            [m("火凯拉的翅膀", 5), m("夏洛克蘑菇", 5)],
            [m("火凯拉的脏器", 5), m("大夏洛克蘑菇", 5), m("可燃石", 5)],
            [m("火凯拉的脏器", 8), m("大夏洛克蘑菇", 10), m("红宝石", 5)],
        ),
    }
)

add(
    {
        "id": "frostbite",
        "name": "暴风雪套装",
        "category": "elemental",
        "amiibo": False,
        "upgradable": True,
        "description": "寒冷天气下提升攻击；全套 ★★ 后寒冷时蓄力更快并附带冰冻爆发。",
        "setBonus": {
            "level2": "寒冷时蓄力加速，并产生冰属性爆发",
            "note": "需三件均强化至 ★★",
        },
        "pieces": [
            piece(
                "frostbite_headdress",
                "head",
                "暴风雪头饰",
                [2, 4, 6, 9, 16],
                "寒冷时攻击力提升",
                "基尔希湖洞窟（海布拉）宝箱。",
                loc("surface", -3800.0, 300.0, -2300.0, "基尔希湖洞窟"),
            ),
            piece(
                "frostbite_shirt",
                "body",
                "暴风雪衫",
                [2, 4, 6, 9, 16],
                "寒冷时攻击力提升",
                "光亮伞菇洞窟宝箱。",
                loc("surface", -3100.0, 280.0, -2100.0, "光亮伞菇洞窟"),
            ),
            piece(
                "frostbite_trousers",
                "legs",
                "暴风雪裤",
                [2, 4, 6, 9, 16],
                "寒冷时攻击力提升",
                "海布拉泉源洞窟宝箱。",
                loc("surface", -3600.0, 320.0, -2500.0, "海布拉泉源洞窟"),
            ),
        ],
        "upgrades": ups(
            [m("冰凯拉的翅膀", 3), m("冰蘑菇", 3)],
            [m("冰凯拉的翅膀", 5), m("冰蘑菇", 5)],
            [m("冰凯拉的脏器", 5), m("大冰蘑菇", 5), m("冰雪果", 5)],
            [m("冰凯拉的脏器", 8), m("大冰蘑菇", 10), m("蓝宝石", 5)],
        ),
    }
)

add(
    {
        "id": "charged",
        "name": "雷光套装",
        "category": "elemental",
        "amiibo": False,
        "upgradable": True,
        "description": "雷雨时提升攻击；全套 ★★ 后雷雨蓄力更快并附带电击爆发。分布在龙骨遗迹一带。",
        "setBonus": {
            "level2": "雷雨时蓄力加速，并产生电击爆发",
            "note": "需三件均强化至 ★★",
        },
        "pieces": [
            piece(
                "charged_headdress",
                "head",
                "雷光头饰",
                [2, 4, 6, 9, 16],
                "雷雨时攻击力提升",
                "德拉科祖河被藤蔓堵住的洞窟内。",
                loc("surface", 1400.0, 150.0, 2200.0, "德拉科祖河洞窟"),
            ),
            piece(
                "charged_shirt",
                "body",
                "雷光衫",
                [2, 4, 6, 9, 16],
                "雷雨时攻击力提升",
                "德拉科祖湖上游遗迹宝箱。",
                loc("surface", 1300.0, 160.0, 2400.0, "德拉科祖湖"),
            ),
            piece(
                "charged_trousers",
                "legs",
                "雷光裤",
                [2, 4, 6, 9, 16],
                "雷雨时攻击力提升",
                "达梅尔森林裂石后方宝箱。",
                loc("surface", 1100.0, 140.0, 2100.0, "达梅尔森林"),
            ),
        ],
        "upgrades": ups(
            [m("电凯拉的翅膀", 3), m("电球果", 3)],
            [m("电凯拉的翅膀", 5), m("电球果", 5)],
            [m("电凯拉的脏器", 5), m("大电球果", 5), m("黄色丘丘胶", 5)],
            [m("电凯拉的脏器", 8), m("大电球果", 10), m("黄玉", 5)],
        ),
    }
)

add(
    {
        "id": "depths",
        "name": "深暗套装",
        "category": "depths",
        "amiibo": False,
        "upgradable": True,
        "description": "地底讨价还价雕像用波用灵魂（Poe）兑换。提供深暗抗性；全套有额外抗性。",
        "setBonus": {"level2": "深暗抗性提升", "note": "需三件均强化至 ★★"},
        "pieces": [
            piece(
                "depths_hood",
                "head",
                "深暗兜帽",
                [3, 5, 8, 12, 20],
                "深暗抗性",
                "第 5 座讨价还价雕像处用 300 灵魂兑换。",
            ),
            piece(
                "depths_tunic",
                "body",
                "深暗服",
                [3, 5, 8, 12, 20],
                "深暗抗性",
                "第 1 座讨价还价雕像处用 150 灵魂兑换。",
                loc("depths", -800.0, -400.0, 500.0, "地底讨价还价雕像（其一）"),
            ),
            piece(
                "depths_gaiters",
                "legs",
                "深暗绑腿",
                [3, 5, 8, 12, 20],
                "深暗抗性",
                "第 3 座讨价还价雕像处用 200 灵魂兑换。",
            ),
        ],
        "upgrades": ups(
            [m("深暗块", 5)],
            [m("深暗块", 10)],
            [m("深暗块", 15), m("黑霍拉布林的角", 5)],
            [m("深暗块", 20), m("银霍拉布林的角", 5), m("星辰碎片", 1)],
        ),
    }
)

add(
    {
        "id": "miner",
        "name": "采矿套装",
        "category": "depths",
        "amiibo": False,
        "upgradable": True,
        "description": "地底废弃矿山宝箱。发光照明；全套 ★★ 后留下光轨，便于黑暗中探路。",
        "setBonus": {"level2": "留下发光轨迹", "note": "需三件均强化至 ★★"},
        "pieces": [
            piece(
                "miner_mask",
                "head",
                "采矿面罩",
                [3, 5, 8, 12, 20],
                "发光",
                "废弃卡拉卡拉矿（格鲁德沙漠地底）宝箱。",
                loc("depths", -3250.0, -400.0, 2580.0, "废弃卡拉卡拉矿"),
            ),
            piece(
                "miner_top",
                "body",
                "采矿上衣",
                [3, 5, 8, 12, 20],
                "发光",
                "达夫内斯峡谷矿（中央海拉鲁地底）宝箱。",
                loc("depths", -1000.0, -350.0, 200.0, "达夫内斯峡谷矿"),
            ),
            piece(
                "miner_trousers",
                "legs",
                "采矿裤",
                [3, 5, 8, 12, 20],
                "发光",
                "海利亚峡谷矿（中央海拉鲁地底）宝箱。",
                loc("depths", -200.0, -350.0, 400.0, "海利亚峡谷矿"),
            ),
        ],
        "upgrades": ups(
            [m("打火石", 5)],
            [m("打火石", 10)],
            [m("打火石", 15), m("发光石", 5)],
            [m("打火石", 20), m("钻石", 3), m("星辰碎片", 1)],
        ),
    }
)

add(
    {
        "id": "zonaite",
        "name": "左纳尼乌姆套装",
        "category": "zonaite",
        "amiibo": False,
        "upgradable": True,
        "description": "天空岛屿获取。提升左纳乌器械能源效率；全套 ★★ 后左纳乌能源回复速度翻倍。",
        "setBonus": {"level2": "左纳乌能源回复速度 ×2", "note": "需三件均强化至 ★★"},
        "pieces": [
            piece(
                "zonaite_helm",
                "head",
                "左纳尼乌姆头盔",
                [4, 7, 12, 18, 28],
                "左纳乌器械更省电",
                "光投射岛（塔班萨天空）宝箱。",
                loc("sky", -3500.0, 1400.0, -1500.0, "光投射岛"),
            ),
            piece(
                "zonaite_waistguard",
                "body",
                "左纳尼乌姆腰铠",
                [4, 7, 12, 18, 28],
                "左纳乌器械更省电",
                "东纳克罗达天空杨萨敏神庙后方宝箱。",
                loc("sky", 4500.0, 1400.0, 1200.0, "杨萨敏神庙附近"),
            ),
            piece(
                "zonaite_shin_guards",
                "legs",
                "左纳尼乌姆护胫",
                [4, 7, 12, 18, 28],
                "左纳乌器械更省电",
                "阿卡莱海天空矿山附近宝箱。",
                loc("sky", 4600.0, 1400.0, -1800.0, "阿卡莱海天空矿山"),
            ),
        ],
        "upgrades": ups(
            [m("左纳尼乌姆", 5)],
            [m("大的左纳尼乌姆", 5), m("左纳乌能源", 5)],
            [m("大的左纳尼乌姆", 8), m("大的左纳乌能源", 5), m("方块魔像的核心", 3)],
            [m("大的左纳尼乌姆", 12), m("大的左纳乌能源", 8), m("方块魔像的核心", 5)],
        ),
    }
)

add(
    {
        "id": "mystic",
        "name": "精灵套装",
        "category": "special",
        "amiibo": False,
        "upgradable": False,
        "description": "受伤时消耗卢比而非心心。用泡泡宝石在柯尔顿商店兑换；需先解锁并推进其商品列表。不可强化。",
        "setBonus": {"level2": None, "note": "无套装奖励；不可强化"},
        "pieces": [
            piece(
                "mystic_headpiece",
                "head",
                "精灵头饰",
                [3],
                "受伤时消耗卢比",
                "柯尔顿商店用 5 个泡泡宝石兑换（商品解锁后）。",
            ),
            piece(
                "mystic_robe",
                "body",
                "精灵长袍",
                [3],
                "受伤时消耗卢比",
                "柯尔顿商店用 3 个泡泡宝石兑换。",
            ),
            piece(
                "mystic_trousers",
                "legs",
                "精灵裤",
                [3],
                "受伤时消耗卢比",
                "柯尔顿商店用 4 个泡泡宝石兑换。",
            ),
        ],
    }
)

add(
    {
        "id": "dark",
        "name": "暗黑套装",
        "category": "special",
        "amiibo": False,
        "upgradable": True,
        "description": "地底讨价还价雕像用灵魂兑换。全套 ★★ 后夜间移动速度提升。",
        "setBonus": {"level2": "夜间移动速度提升", "note": "需三件均强化至 ★★"},
        "pieces": [
            piece(
                "dark_hood",
                "head",
                "暗黑兜帽",
                [3, 5, 8, 12, 20],
                "无（套装相关）",
                "第 4 座讨价还价雕像处用 300 灵魂兑换。",
            ),
            piece(
                "dark_tunic",
                "body",
                "暗黑服",
                [3, 5, 8, 12, 20],
                "无（套装相关）",
                "第 1 座讨价还价雕像处用 150 灵魂兑换。",
            ),
            piece(
                "dark_trousers",
                "legs",
                "暗黑裤",
                [3, 5, 8, 12, 20],
                "无（套装相关）",
                "第 2 座讨价还价雕像处用 200 灵魂兑换。",
            ),
        ],
        "upgrades": ups(
            [m("深暗块", 5)],
            [m("深暗块", 8), m("斯塔尔的脏器", 2)],
            [m("深暗块", 12), m("斯塔尔的脏器", 3)],
            [m("深暗块", 15), m("斯塔尔的脏器", 5), m("星辰碎片", 1)],
        ),
    }
)

# non-upgradable / amiibo-also-in-world
add(
    {
        "id": "archaic",
        "name": "残旧套装",
        "category": "basic",
        "amiibo": False,
        "upgradable": False,
        "description": "开场天空岛获得的破旧衣物。仅上衣与裤子，无头盔；防御很低，不可强化。开局耐寒可配合暖裤使用。",
        "setBonus": {"level2": None, "note": "无套装奖励；不可强化；无头盔部件"},
        "pieces": [
            piece(
                "archaic_tunic",
                "body",
                "残旧的衣服",
                [1],
                "无",
                "初始天空岛池畔洞窟等宝箱。",
                loc("sky", 450.0, 1500.0, -900.0, "初始天空岛"),
            ),
            piece(
                "archaic_legwear",
                "legs",
                "残旧的裤子",
                [2],
                "开局可提供耐寒（暖裤形态相关）",
                "苏醒之间附近宝箱。",
                loc("sky", 450.0, 1500.0, -950.0, "初始天空岛苏醒之间附近"),
            ),
        ],
    }
)

add(
    {
        "id": "evil_spirit",
        "name": "异次元恶灵套装",
        "category": "special",
        "amiibo": False,
        "upgradable": False,
        "description": "完成南／岛／北洛美迷宫预言支线后获得。提升安静度；套装效果类似夜光（骨武器与骷髅）。不可强化。",
        "setBonus": {
            "level2": "骨武器伤害提升；骷髅类敌人不攻击",
            "note": "穿齐三件即生效；不可强化",
        },
        "pieces": [
            piece(
                "evil_spirit_mask",
                "head",
                "异次元恶灵面具",
                [4],
                "安静度提升",
                "完成「南洛美预言」支线。",
                loc("surface", -1800.0, 150.0, 3200.0, "南洛美迷宫"),
            ),
            piece(
                "evil_spirit_armor",
                "body",
                "异次元恶灵铠甲",
                [4],
                "安静度提升",
                "完成「洛美迷宫岛预言」支线。",
                loc("surface", 4600.0, 100.0, -600.0, "洛美迷宫岛"),
            ),
            piece(
                "evil_spirit_greaves",
                "legs",
                "异次元恶灵护胫",
                [4],
                "安静度提升",
                "完成「北洛美预言」支线。",
                loc("surface", -1200.0, 280.0, -3400.0, "北洛美迷宫"),
            ),
        ],
    }
)

add(
    {
        "id": "phantom",
        "name": "幻影套装",
        "category": "combat",
        "amiibo": False,
        "upgradable": False,
        "description": "提升攻击力，无套装奖励，不可强化。部件在格鲁德与费罗尼相关洞窟。",
        "setBonus": {"level2": None, "note": "无套装奖励；不可强化"},
        "pieces": [
            piece(
                "phantom_helmet",
                "head",
                "幻影头盔",
                [8],
                "攻击力提升",
                "河豚海滩上方洞窟（费罗尼）宝箱。",
                loc("surface", 500.0, 80.0, 3400.0, "河豚海滩上方洞窟"),
            ),
            piece(
                "phantom_armor",
                "body",
                "幻影铠甲",
                [8],
                "攻击力提升",
                "塔米奥河下游洞窟（格鲁德高地）宝箱。",
                loc("surface", -2800.0, 220.0, 1800.0, "塔米奥河下游洞窟"),
            ),
            piece(
                "phantom_greaves",
                "legs",
                "幻影护胫",
                [8],
                "攻击力提升",
                "古代祭坛遗迹（格鲁德沙漠）宝箱。",
                loc("surface", -4200.0, 120.0, 3200.0, "古代祭坛遗迹"),
            ),
        ],
    }
)

add(
    {
        "id": "tingle",
        "name": "汀空套装",
        "category": "special",
        "amiibo": False,
        "upgradable": False,
        "description": "经典汀空装扮。提升安静度；穿齐有特殊演出效果。通过米斯科宝藏相关谜题获取，不可强化。",
        "setBonus": {"level2": None, "note": "穿齐有特殊效果；不可强化"},
        "pieces": [
            piece(
                "tingle_hood",
                "head",
                "汀空的头巾",
                [2],
                "安静度提升",
                "米斯科宝藏系列线索指向的宝箱之一。",
            ),
            piece(
                "tingle_shirt",
                "body",
                "汀空的衣服",
                [2],
                "安静度提升",
                "米斯科宝藏系列线索指向的宝箱之一。",
            ),
            piece(
                "tingle_tights",
                "legs",
                "汀空的紧身裤",
                [2],
                "安静度提升",
                "米斯科宝藏系列线索指向的宝箱之一。",
            ),
        ],
    }
)

# amiibo / depths hero sets
HERO_AMIIBO = [
    (
        "wild",
        "旷野之勇者套装",
        "旷野之勇者帽子",
        "旷野之勇者服",
        "旷野之勇者裤子",
        "地底巨型骷髅（海布拉／格鲁德／埃尔丁黑暗骷髅）宝箱；亦可用旷野之息林克 amiibo。",
        [
            loc("depths", -3600.0, -450.0, -2200.0, "海布拉黑暗骷髅"),
            loc("depths", -3800.0, -400.0, 2900.0, "格鲁德黑暗骷髅"),
            loc("depths", 1800.0, -400.0, -1900.0, "埃尔丁黑暗骷髅"),
        ],
        "攻击力提升",
    ),
    (
        "hero",
        "初始之勇者套装",
        "勇者的帽子",
        "勇者的衣服",
        "勇者的裤子",
        "地底废弃矿山等宝箱；亦可用初代林克 amiibo。",
        [
            loc("depths", 3000.0, -400.0, 2800.0, "废弃卢临矿一带"),
            loc("depths", 1800.0, -400.0, 1000.0, "废弃卡卡利科矿一带"),
            loc("depths", -3400.0, -400.0, -2000.0, "科瓦什峡谷矿一带"),
        ],
        "攻击力提升",
    ),
    (
        "time",
        "时之勇者套装",
        "时之勇者帽子",
        "时之勇者服",
        "时之勇者裤子",
        "地底宝箱；亦可用时之笛林克／大乱斗林克 amiibo。",
        [None, None, None],
        "攻击力提升",
    ),
    (
        "wind",
        "风之勇者套装",
        "风之勇者帽子",
        "风之勇者服",
        "风之勇者裤子",
        "地底宝箱；亦可用风之杖林克 amiibo。",
        [None, None, None],
        "攻击力提升",
    ),
    (
        "twilight",
        "黄昏之勇者套装",
        "黄昏之勇者帽子",
        "黄昏之勇者服",
        "黄昏之勇者裤子",
        "地底宝箱；亦可用黄昏公主林克 amiibo。",
        [None, None, None],
        "攻击力提升",
    ),
    (
        "sky",
        "天空之勇者套装",
        "天空之勇者帽子",
        "天空之勇者服",
        "天空之勇者裤子",
        "地底宝箱（如东纳克罗达／迷雾森林／克雷内尔峡谷矿一带）；亦可用天空之剑林克 amiibo。",
        [
            loc("depths", 3200.0, -400.0, 2600.0, "雷特索姆树林一带"),
            loc("depths", 400.0, -400.0, -900.0, "敏希树林一带"),
            loc("depths", 700.0, -400.0, -300.0, "克雷内尔峡谷矿一带"),
        ],
        "攻击力提升",
    ),
    (
        "awakening",
        "织梦之勇者套装",
        "织梦面具",
        "织梦之勇者服",
        "织梦之勇者裤子",
        "地表解谜宝箱；亦可用织梦林克 amiibo。面具：桑卓高原正午影子谜题；衣服：古代石柱秘密通路；裤子：竞技场遗迹雕像谜题。",
        [
            loc("surface", -2300.0, 160.0, -800.0, "桑卓高原"),
            loc("surface", -3500.0, 220.0, -1200.0, "古代石柱"),
            loc("surface", -1150.0, 140.0, 1100.0, "竞技场遗迹"),
        ],
        "攻击力提升",
    ),
    (
        "fierce_deity",
        "鬼神套装",
        "鬼神面具",
        "鬼神铠甲",
        "鬼神靴子",
        "地表宝箱或马约拉的面具林克 amiibo。面具：暴风雨谷；铠甲：阿卡莱城堡遗迹；靴子：达夫内斯山。",
        [
            loc("surface", 4200.0, 200.0, -2200.0, "暴风雨谷一带"),
            loc("surface", 3300.0, 180.0, -1500.0, "阿卡莱城堡遗迹"),
            loc("surface", -1000.0, 200.0, 100.0, "达夫内斯山"),
        ],
        "攻击力提升",
    ),
]

for sid, sname, hn, bn, ln, how_base, locs, bonus in HERO_AMIIBO:
    slots = [
        ("head", hn, locs[0]),
        ("body", bn, locs[1]),
        ("legs", ln, locs[2]),
    ]
    pieces = []
    for slot, pname, ploc in slots:
        pieces.append(
            piece(
                f"{sid}_{slot}",
                slot,
                pname,
                [3, 5, 8, 12, 20],
                "无（套装相关）" if sid != "fierce_deity" else "攻击力提升",
                how_base,
                ploc,
            )
        )
    add(
        {
            "id": sid,
            "name": sname,
            "category": "amiibo",
            "amiibo": True,
            "upgradable": True,
            "description": how_base + " 全套强化至 ★★ 后获得攻击力提升类套装奖励（鬼神套为蓄力耐力减少）。",
            "setBonus": {
                "level2": "蓄力攻击耐力减少" if sid == "fierce_deity" else bonus,
                "note": "需三件均强化至 ★★；amiibo 与地图宝箱二选一途径即可",
            },
            "pieces": pieces,
            "upgrades": ups(
                [m("古代核心", 3)] if False else [m("星辰碎片", 1), m("龙的鳞片", 2)],
                [m("星辰碎片", 1), m("龙的爪子", 2)],
                [m("星辰碎片", 1), m("龙的牙齿", 2)],
                [m("星辰碎片", 1), m("龙的角", 2)],
            ),
        }
    )

# Fix hero-set upgrades to more accurate shared pattern (many use silent princess / dragon parts differently)
# Keep simplified dragon-part ladder as placeholder note in description already.

assert len(SETS) == 35, f"expected 35 sets, got {len(SETS)}"

# Faithful TotK appearance approximation (colors/outfit from in-game look; no ripped assets).
PREVIEW = {
    "hylian": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#3f6b32", "body": "#4f7d3c", "legs": "#2f4f28", "accent": "#c4a35a",
        "undershirt": "#e8e0d0", "style": "hood", "outfit": "tunic",
        "hairVisible": True, "metalness": 0.04, "roughness": 0.82,
    },
    "snowquill": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#f2eee6", "body": "#ebe4d8", "legs": "#ddd4c4", "accent": "#c45c3a",
        "undershirt": "#f8f4ec", "style": "feather", "outfit": "tunic",
        "hairVisible": True, "metalness": 0.03, "roughness": 0.88,
    },
    "flamebreaker": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#6e7278", "body": "#7a7e86", "legs": "#5c6068", "accent": "#c45a2a",
        "undershirt": "#4a4e54", "style": "helm", "outfit": "armor",
        "hairVisible": False, "metalness": 0.55, "roughness": 0.38,
    },
    "desert_voe": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#e8c85a", "body": "#2a2a32", "legs": "#e0c050", "accent": "#f0d878",
        "undershirt": "#e8c4a0", "style": "band", "outfit": "open",
        "hairVisible": True, "metalness": 0.08, "roughness": 0.7,
    },
    "zora": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#5aa8c8", "body": "#4a98b8", "legs": "#3a7a98", "accent": "#e8f0f4",
        "undershirt": "#d0e8f0", "style": "helm", "outfit": "armor",
        "hairVisible": False, "metalness": 0.35, "roughness": 0.32,
    },
    "climbing": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#2a4a6a", "body": "#c45a3a", "legs": "#2a4a6a", "accent": "#e8a060",
        "undershirt": "#d8d0c0", "style": "band", "outfit": "suit",
        "hairVisible": True, "metalness": 0.05, "roughness": 0.75,
    },
    "froggy": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#5cb86a", "body": "#4aa85a", "legs": "#3a8a48", "accent": "#c8e878",
        "undershirt": "#d0e8c8", "style": "hood", "outfit": "suit",
        "hairVisible": False, "metalness": 0.06, "roughness": 0.55,
    },
    "glide": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#e8e0c8", "body": "#d8d0b8", "legs": "#c8c0a8", "accent": "#6a8aaa",
        "undershirt": "#f0ebe0", "style": "mask", "outfit": "suit",
        "hairVisible": False, "metalness": 0.04, "roughness": 0.8,
    },
    "rubber": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#1e1e22", "body": "#2a2a30", "legs": "#18181c", "accent": "#f0d040",
        "undershirt": "#222228", "style": "helm", "outfit": "suit",
        "hairVisible": False, "metalness": 0.02, "roughness": 0.35,
    },
    "stealth": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#5a3a6a", "body": "#4a2a5a", "legs": "#3a1a4a", "accent": "#c8a0d0",
        "undershirt": "#3a2a48", "style": "mask", "outfit": "suit",
        "hairVisible": False, "metalness": 0.05, "roughness": 0.7,
    },
    "barbarian": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#c45a2a", "body": "#a84820", "legs": "#8a3818", "accent": "#e8c060",
        "undershirt": "#e8c4a0", "style": "helm", "outfit": "barbarian",
        "hairVisible": False, "metalness": 0.12, "roughness": 0.65,
    },
    "radiant": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#1a1420", "body": "#120c18", "legs": "#0c0810", "accent": "#70e0a0",
        "undershirt": "#1a1420", "style": "mask", "outfit": "suit",
        "hairVisible": False, "metalness": 0.2, "roughness": 0.4,
    },
    "soldier": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#6a7080", "body": "#5a6070", "legs": "#4a5060", "accent": "#b0a060",
        "undershirt": "#4a5060", "style": "helm", "outfit": "armor",
        "hairVisible": False, "metalness": 0.62, "roughness": 0.35,
    },
    "royal_guard": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#14141c", "body": "#8a1a28", "legs": "#14141c", "accent": "#d0a040",
        "undershirt": "#2a1018", "style": "helm", "outfit": "armor",
        "hairVisible": False, "metalness": 0.45, "roughness": 0.4,
    },
    "yiga": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#f0f0f0", "body": "#d83030", "legs": "#f0f0f0", "accent": "#202020",
        "undershirt": "#d83030", "style": "mask", "outfit": "suit",
        "hairVisible": False, "metalness": 0.05, "roughness": 0.72,
    },
    "ember": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#e86020", "body": "#d05018", "legs": "#b04010", "accent": "#f0a040",
        "undershirt": "#e07030", "style": "crown", "outfit": "open",
        "hairVisible": True, "metalness": 0.08, "roughness": 0.7,
    },
    "frostbite": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#a0d8e8", "body": "#80c0d8", "legs": "#60a8c8", "accent": "#e8f8ff",
        "undershirt": "#c8e8f0", "style": "crown", "outfit": "open",
        "hairVisible": True, "metalness": 0.1, "roughness": 0.55,
    },
    "charged": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#f0d040", "body": "#e0c030", "legs": "#c0a020", "accent": "#60d0f0",
        "undershirt": "#f0e080", "style": "crown", "outfit": "open",
        "hairVisible": True, "metalness": 0.15, "roughness": 0.5,
    },
    "depths": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#3a2848", "body": "#2a1838", "legs": "#1a0828", "accent": "#9060c0",
        "undershirt": "#2a1838", "style": "hood", "outfit": "robe",
        "hairVisible": False, "cape": True, "metalness": 0.08, "roughness": 0.75,
    },
    "miner": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#c8a050", "body": "#8a7050", "legs": "#6a5040", "accent": "#f0e060",
        "undershirt": "#a08060", "style": "helm", "outfit": "armor",
        "hairVisible": False, "metalness": 0.4, "roughness": 0.45,
    },
    "zonaite": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#70b888", "body": "#509868", "legs": "#407858", "accent": "#c0f0a0",
        "undershirt": "#60a878", "style": "helm", "outfit": "armor",
        "hairVisible": False, "metalness": 0.5, "roughness": 0.35,
    },
    "mystic": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#e8b0d0", "body": "#d890c0", "legs": "#c870b0", "accent": "#f0e0f0",
        "undershirt": "#e8c0d8", "style": "crown", "outfit": "robe",
        "hairVisible": True, "metalness": 0.05, "roughness": 0.85,
    },
    "dark": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#101018", "body": "#181820", "legs": "#080810", "accent": "#404050",
        "undershirt": "#101018", "style": "hood", "outfit": "robe",
        "hairVisible": False, "cape": True, "metalness": 0.15, "roughness": 0.55,
    },
    "archaic": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#e8c4a0", "body": "#c4a070", "legs": "#a88858", "accent": "#8a7040",
        "undershirt": "#d4b890", "style": "none", "outfit": "tunic",
        "hairVisible": True, "metalness": 0.02, "roughness": 0.9,
    },
    "evil_spirit": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#c8d0d8", "body": "#a8b0b8", "legs": "#889098", "accent": "#60a0e0",
        "undershirt": "#b0b8c0", "style": "mask", "outfit": "armor",
        "hairVisible": False, "metalness": 0.55, "roughness": 0.3,
    },
    "phantom": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#4a6080", "body": "#3a5070", "legs": "#2a4060", "accent": "#90b0d0",
        "undershirt": "#3a5070", "style": "helm", "outfit": "armor",
        "hairVisible": False, "metalness": 0.65, "roughness": 0.28,
    },
    "tingle": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#3080d0", "body": "#2060b0", "legs": "#185098", "accent": "#f0d040",
        "undershirt": "#3080d0", "style": "hood", "outfit": "suit",
        "hairVisible": False, "metalness": 0.04, "roughness": 0.8,
    },
    "wild": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#2a6a38", "body": "#3a8a48", "legs": "#2a5a30", "accent": "#e8c060",
        "undershirt": "#e8e0d0", "style": "hood", "outfit": "tunic",
        "hairVisible": False, "metalness": 0.05, "roughness": 0.8,
    },
    "hero": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#2a6a38", "body": "#3a8a48", "legs": "#c84030", "accent": "#e8c060",
        "undershirt": "#e8e0d0", "style": "hood", "outfit": "tunic",
        "hairVisible": False, "metalness": 0.05, "roughness": 0.8,
    },
    "time": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#2a6a38", "body": "#3a8a48", "legs": "#c84030", "accent": "#e8d080",
        "undershirt": "#e8e0d0", "style": "hood", "outfit": "tunic",
        "hairVisible": False, "metalness": 0.05, "roughness": 0.8,
    },
    "wind": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#f0e8d0", "body": "#3a8a48", "legs": "#c84030", "accent": "#f0d040",
        "undershirt": "#e8e0d0", "style": "hood", "outfit": "tunic",
        "hairVisible": False, "metalness": 0.05, "roughness": 0.8,
    },
    "twilight": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#2a6a38", "body": "#3a8a48", "legs": "#c84030", "accent": "#60a0e0",
        "undershirt": "#e8e0d0", "style": "hood", "outfit": "tunic",
        "hairVisible": False, "metalness": 0.05, "roughness": 0.8,
    },
    "sky": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#e8e0c0", "body": "#d0c8a0", "legs": "#b8b088", "accent": "#60a0d0",
        "undershirt": "#f0ebe0", "style": "hood", "outfit": "tunic",
        "hairVisible": False, "metalness": 0.05, "roughness": 0.82,
    },
    "awakening": {
        "skin": "#e8c4a0", "hair": "#e8c84a", "eyes": "#3a6cb0",
        "head": "#e8d8a0", "body": "#3a8a48", "legs": "#c84030", "accent": "#f0e060",
        "undershirt": "#e8e0d0", "style": "mask", "outfit": "tunic",
        "hairVisible": False, "metalness": 0.05, "roughness": 0.8,
    },
    "fierce_deity": {
        "skin": "#e8e8f0", "hair": "#f0f0f8", "eyes": "#c02030",
        "head": "#e8e8f0", "body": "#f0f0f8", "legs": "#d8d8e8", "accent": "#c02030",
        "undershirt": "#e8e8f0", "style": "mask", "outfit": "armor",
        "hairVisible": False, "metalness": 0.25, "roughness": 0.4,
    },
}

DEFAULT_PREVIEW = {
    "skin": "#e8c4a0",
    "hair": "#e8c84a",
    "eyes": "#3a6cb0",
    "head": "#3f6b32",
    "body": "#4f7d3c",
    "legs": "#2f4f28",
    "accent": "#c4a35a",
    "undershirt": "#e8e0d0",
    "style": "hood",
    "outfit": "tunic",
    "hairVisible": True,
    "metalness": 0.05,
    "roughness": 0.78,
}

for s in SETS:
    s["preview"] = dict(PREVIEW.get(s["id"], DEFAULT_PREVIEW))


def main():
    payload = {
        "meta": {
            "totalSets": len(SETS),
            "upgradable": sum(1 for s in SETS if s.get("upgradable")),
            "amiibo": sum(1 for s in SETS if s.get("amiibo")),
            "previewReady": sum(1 for s in SETS if s.get("preview")),
            "previewMode": "faithful-procedural",
            "note": "preview 按 TotK 原造型做程序化近似复刻（非拆包资源）。",
        },
        "sets": SETS,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} ({len(SETS)} sets)")


if __name__ == "__main__":
    main()
