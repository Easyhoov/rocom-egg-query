"""
家园炼金查询 API
数据来源: 洛克工具箱 (roco.gptvip.chat)
"""
import json
import re
from pathlib import Path
from fastapi import APIRouter, Query

router = APIRouter(prefix="/api/garden", tags=["家园炼金"])

GARDEN_DATA_FILE = Path(__file__).parent.parent / "data" / "garden_data.json"

# CDN -> local icon URL mapping
CDN_PATTERNS = [
    (re.compile(r'https://rococdn\.gptvip\.chat/webp/home_garden/seeds/(\d+)\.webp\S*'), r'/garden-icons/seeds/\1.webp'),
    (re.compile(r'https://rococdn\.gptvip\.chat/webp/home_garden/materials/(\d+)\.webp\S*'), r'/garden-icons/materials/\1.webp'),
    (re.compile(r'https://rococdn\.gptvip\.chat/webp/home_garden/foods/(\d+)\.webp\S*'), r'/garden-icons/foods/\1.webp'),
    (re.compile(r'https://rococdn\.gptvip\.chat/webp/balls/(\d+)\.webp\S*'), r'/garden-icons/balls/\1.webp'),
]

def _localize_icon_urls(obj):
    """Recursively replace CDN icon URLs with local paths."""
    if isinstance(obj, dict):
        return {k: _localize_icon_urls(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_localize_icon_urls(v) for v in obj]
    elif isinstance(obj, str):
        for pat, repl in CDN_PATTERNS:
            if pat.search(obj):
                return pat.sub(repl, obj)
        return obj
    return obj

def load_garden_data():
    with open(GARDEN_DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


@router.get("/query")
async def query_garden(level: int = Query(16, ge=1, le=25), target_ball: str = Query(None)):
    """查询家园炼金推荐方案"""
    data = load_garden_data()
    available_cards = [c for c in data.get("cards", []) if c.get("unlock_level") <= level]
    if not available_cards:
        return _localize_icon_urls({
            "success": True,
            "level": level,
            "available_count": 0,
            "best_recommendation": None,
            "available_balls": [],
            "ball_cards": [],
            "summary": None
        })
    all_balls_map = {}
    for card in available_cards:
        for ball in card.get("direct_craft_balls", []):
            if ball["name"] not in all_balls_map:
                all_balls_map[ball["name"]] = {
                    "name": ball["name"],
                    "icon_url": ball["icon_url"],
                    "description": ball["description"],
                    "usage": ball.get("usage", ""),
                    "item_id": ball.get("item_id")
                }
    available_balls = list(all_balls_map.values())
    sorted_cards = sorted(available_cards, key=lambda x: x.get("exp_per_hour", 0), reverse=True)
    best_card = sorted_cards[0]
    best_recommendation = {
        "seed": {
            "name": best_card.get("seed_name"),
            "icon_url": best_card.get("seed_icon_url")
        },
        "material": {
            "name": best_card.get("material_name"),
            "icon_url": best_card.get("material_icon_url")
        },
        "food": {
            "name": best_card.get("food_name"),
            "icon_url": best_card.get("food_icon_url"),
            "duration_minutes": best_card.get("food_duration_minutes"),
            "duration_label": best_card.get("food_duration_label"),
            "exp": best_card.get("food_home_exp"),
            "recipe_count": best_card.get("food_recipe_count"),
            "formula": f"{best_card.get('material_name')} x{best_card.get('food_recipe_count', 1)}"
        },
        "exp_per_hour": best_card.get("exp_per_hour"),
        "unlock_level": best_card.get("unlock_level")
    }
    ball_cards = []
    if target_ball:
        for card in sorted_cards:
            for ball in card.get("direct_craft_balls", []):
                if ball["name"] == target_ball:
                    ball_cards.append({
                        "seed": {
                            "name": card.get("seed_name"),
                            "icon_url": card.get("seed_icon_url")
                        },
                        "material": {
                            "name": card.get("material_name"),
                            "icon_url": card.get("material_icon_url")
                        },
                        "food": {
                            "name": card.get("food_name"),
                            "icon_url": card.get("food_icon_url"),
                            "duration_minutes": card.get("food_duration_minutes"),
                            "duration_label": card.get("food_duration_label"),
                            "exp": card.get("food_home_exp"),
                            "recipe_count": card.get("food_recipe_count"),
                            "formula": f"{card.get('material_name')} x{card.get('food_recipe_count', 1)}"
                        },
                        "exp_per_hour": card.get("exp_per_hour"),
                        "unlock_level": card.get("unlock_level"),
                        "ball": {
                            "name": ball["name"],
                            "icon_url": ball["icon_url"],
                            "group_label": ball.get("group_label", ""),
                            "formula_label": ball.get("formula_label", "")
                        }
                    })
                    break
    summary = {
        "available_count": len(available_cards),
        "max_level": max(c.get("unlock_level", 0) for c in available_cards),
        "best_food": best_card.get("food_name"),
        "best_exp_per_hour": best_card.get("exp_per_hour"),
        "available_ball_count": len(available_balls),
        "ball_names": [b["name"] for b in available_balls]
    }
    return _localize_icon_urls({
        "success": True,
        "level": level,
        "target_ball": target_ball,
        "available_count": len(available_cards),
        "best_recommendation": best_recommendation,
        "available_balls": available_balls,
        "ball_cards": ball_cards if target_ball else None,
        "summary": summary
    })


@router.get("/balls")
async def get_ball_options():
    """获取所有球的列表"""
    data = load_garden_data()
    return _localize_icon_urls({
        "success": True,
        "balls": data.get("ball_options", [])
    })


@router.get("/levels")
async def get_all_levels():
    """获取所有等级链数据"""
    data = load_garden_data()
    cards = data.get("cards", [])
    levels = {}
    for card in cards:
        level = card.get("unlock_level")
        if level not in levels:
            levels[level] = []
        levels[level].append(card)
    level_chain = []
    for level in sorted(levels.keys()):
        for card in levels[level]:
            ball_names = [b["name"] for b in card.get("direct_craft_balls", [])]
            level_chain.append({
                "level": level,
                "seed": {
                    "name": card.get("seed_name"),
                    "icon_url": card.get("seed_icon_url")
                },
                "material": {
                    "name": card.get("material_name"),
                    "icon_url": card.get("material_icon_url")
                },
                "food": {
                    "name": card.get("food_name"),
                    "icon_url": card.get("food_icon_url"),
                    "duration_minutes": card.get("food_duration_minutes"),
                    "duration_label": card.get("food_duration_label"),
                    "exp": card.get("food_home_exp"),
                    "recipe_count": card.get("food_recipe_count"),
                    "formula": f"{card.get('material_name')} x{card.get('food_recipe_count', 1)}"
                },
                "exp_per_hour": card.get("exp_per_hour"),
                "balls": ball_names
            })
    return _localize_icon_urls({
        "success": True,
        "levels": level_chain
    })
