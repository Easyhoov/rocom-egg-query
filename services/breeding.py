#!/usr/bin/env python3
"""孵蛋查询核心逻辑"""

import json
import sys
from pathlib import Path
from typing import Optional

DATA_DIR = Path(__file__).parent.parent / "data"
BREEDING_FILE = DATA_DIR / "breeding.json"

# ========== 蛋类型信息 ==========

EGG_TYPES = {
    0: {"name": "普通蛋", "icon": "🥚", "color": "#667eea"},
    1: {"name": "珍贵蛋", "icon": "💎", "color": "#e74c3c"},
    2: {"name": "异色蛋", "icon": "🌈", "color": "#e91e63"},
    4: {"name": "特殊蛋", "icon": "🎁", "color": "#ff9800"},
    5: {"name": "首领蛋", "icon": "👑", "color": "#9c27b0"},
    7: {"name": "速孵蛋", "icon": "⚡", "color": "#00bcd4"},
}


def get_egg_type_info(precious_type: int) -> dict:
    """获取蛋类型信息"""
    return EGG_TYPES.get(precious_type, {"name": "未知", "icon": "❓", "color": "#999"})


# ========== 数据加载 ==========

def load_breeding_data() -> list[dict]:
    """加载孵蛋数据"""
    if not BREEDING_FILE.exists():
        print(f"❌ 数据文件不存在: {BREEDING_FILE}")
        print("   请先运行: python3 download_data.py")
        sys.exit(1)

    with open(BREEDING_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    pets = data['pet_egg_conf']
    print(f"✅ 已加载 {len(pets)} 条孵蛋数据")
    return pets


PETS = load_breeding_data()


# ========== 匹配等级与概率 ==========

def calc_match_tier(r_diff: float) -> str:
    """根据 R 值差距计算匹配等级"""
    if r_diff == 0:
        return "exact"
    elif r_diff <= 0.1:
        return "tolerance1"
    elif r_diff <= 0.3:
        return "tolerance2"
    else:
        return "nearest"


def calc_probability(r_diff: float, tier: str) -> int:
    """根据 R 值差距和等级估算概率百分比"""
    if tier == "exact":
        return 100
    elif tier == "tolerance1":
        return max(80, int(99 - r_diff * 190))
    elif tier == "tolerance2":
        return max(50, int(79 - r_diff * 100))
    else:
        return max(1, min(49, int(50 - r_diff * 50)))


# ========== 查询逻辑 ==========

def query_egg(height_m: float, weight_kg: float, egg_filter: Optional[int] = None) -> tuple[list[dict], float]:
    """
    查询孵蛋结果
    egg_filter: 0=只神奇的蛋, 1=只炫彩蛋, None=不限
    返回: (结果列表, 用户R值)
    """
    from services.image import get_image_matcher

    height_cm = height_m * 100
    weight_g = weight_kg * 1000
    user_r = weight_kg / height_m if height_m > 0 else 0

    seen = set()
    results = []

    for pet in PETS:
        precious_type = pet.get('precious_egg_type', 0)

        # 蛋类型筛选
        if egg_filter == 0 and precious_type != 0:
            continue
        if egg_filter == 1 and precious_type == 0:
            continue

        # 身高体重匹配
        if not (pet['height_low'] <= height_cm <= pet['height_high']):
            continue
        if not (pet['weight_low'] <= weight_g <= pet['weight_high']):
            continue

        # 去重
        if egg_filter is None or egg_filter == 1:
            key = pet['name']
        else:
            key = f"{pet['name']}_{precious_type}"
        if key in seen:
            continue
        seen.add(key)

        egg_type_info = get_egg_type_info(precious_type)

        # R值 = 中位体重(kg) / 中位身高(m)
        h_mid = (pet['height_low'] + pet['height_high']) / 2 / 100
        w_mid = (pet['weight_low'] + pet['weight_high']) / 2 / 1000
        r_value = w_mid / h_mid if h_mid > 0 else 0
        r_diff = round(abs(r_value - user_r), 2)
        tier = calc_match_tier(r_diff)

        results.append({
            'name': pet['name'],
            'height_min': pet['height_low'] / 100,
            'height_max': pet['height_high'] / 100,
            'weight_min': pet['weight_low'] / 1000,
            'weight_max': pet['weight_high'] / 1000,
            'is_precious': precious_type > 0,
            'precious_type': precious_type,
            'egg_type_name': egg_type_info['name'],
            'egg_type_icon': egg_type_info['icon'],
            'egg_type_color': egg_type_info['color'],
            'r_value': round(r_value, 2),
            'r_diff': r_diff,
            'match_tier': tier,
            'probability': calc_probability(r_diff, tier),
        })

    # 按R值差距排序
    results.sort(key=lambda x: x['r_diff'])
    # 补充图片路径和图鉴链接
    from services.image import get_image_matcher
    from services.spirits import SPIRITS_BY_NAME
    matcher = get_image_matcher()
    for r in results:
        r['image'] = matcher.match(r['name'])
        spirit = SPIRITS_BY_NAME.get(r['name'])
        r['spirit_id'] = spirit['spirit_id'] if spirit else None

    return results, round(user_r, 2)
