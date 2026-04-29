#!/usr/bin/env python3
"""图鉴 API"""

import json
import math
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from services.spirits import SPIRITS, SPIRITS_BY_ID, OFFICIAL_EGG_GROUPS
from services.image import get_spirit_image

# 加载技能数据和克制数据
DATA_DIR = Path(__file__).parent.parent / "data"
SKILLS_DICT: dict[str, dict] = {}
SPIRIT_SKILLS: dict[int, list[dict]] = {}
SPIRIT_MATCHUPS: dict[int, dict] = {}
SKILL_ICONS_MAP: dict[str, str] = {}

_skills_file = DATA_DIR / "skills_dict.json"
_spirit_skills_file = DATA_DIR / "spirit_skills.json"
_spirit_matchups_file = DATA_DIR / "spirit_matchups.json"
_skills_icons_file = DATA_DIR / "skills_icons.json"

if _skills_file.exists():
    SKILLS_DICT = json.loads(_skills_file.read_text(encoding="utf-8"))
if _spirit_skills_file.exists():
    raw = json.loads(_spirit_skills_file.read_text(encoding="utf-8"))
    SPIRIT_SKILLS = {int(k): v for k, v in raw.items()}
if _spirit_matchups_file.exists():
    raw = json.loads(_spirit_matchups_file.read_text(encoding="utf-8"))
    SPIRIT_MATCHUPS = {int(k): v for k, v in raw.items()}
if _skills_icons_file.exists():
    raw = json.loads(_skills_icons_file.read_text(encoding="utf-8"))
    SKILL_ICONS_MAP = {k: f"/skill-icons/{k.replace(chr(47), chr(95)).replace(chr(92), chr(95)).replace(chr(63), chr(95))}.png" for k in raw}

router = APIRouter(prefix="/api", tags=["图鉴"])


@router.get("/spirits")
async def list_spirits(
    q: Optional[str] = Query(None, description="搜索（名称/编号）"),
    attribute: Optional[str] = Query(None, description="属性筛选"),
    egg_group: Optional[str] = Query(None, description="蛋组筛选"),
    shiny: Optional[str] = Query(None, description="异色筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(24, ge=1, le=100, description="每页数量"),
):
    """图鉴列表（搜索+筛选+分页）"""
    filtered = SPIRITS

    if q:
        q_lower = q.lower().strip()
        filtered = [
            s for s in filtered
            if q_lower in s['base_name'].lower()
            or q_lower in s.get('display_name', '').lower()
            or q_lower in s.get('spirit_no', '').lower()
            or (q.isdigit() and s['spirit_no_number'] == int(q))
        ]

    if attribute:
        filtered = [
            s for s in filtered
            if s.get('primary_attribute') == attribute
            or s.get('secondary_attribute') == attribute
        ]

    if egg_group:
        filtered = [
            s for s in filtered
            if egg_group in s.get('egg_groups', [])
        ]

    if shiny == 'true':
        filtered = [
            s for s in filtered
            if s.get('has_shiny_variant', False)
        ]

    filtered.sort(key=lambda s: s['spirit_no_number'])

    total = len(filtered)
    total_pages = math.ceil(total / page_size) if total > 0 else 1
    start = (page - 1) * page_size
    end = start + page_size
    items = filtered[start:end]

    return {
        "success": True,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "items": [_format_spirit_card(s) for s in items],
    }


@router.get("/spirits/{spirit_id}")
async def get_spirit(spirit_id: int):
    """精灵详情"""
    spirit = SPIRITS_BY_ID.get(spirit_id)
    if not spirit:
        raise HTTPException(status_code=404, detail=f"精灵 ID {spirit_id} 不存在")
    return {
        "success": True,
        "spirit": _format_spirit_detail(spirit),
    }


@router.get("/official-egg-groups")
async def list_official_egg_groups():
    """官方蛋组列表"""
    groups_with_count = []
    for g in OFFICIAL_EGG_GROUPS:
        name = g['egg_group_name']
        count = sum(1 for s in SPIRITS if name in s.get('egg_groups', []))
        groups_with_count.append({**g, "spirit_count": count})
    return {"success": True, "groups": groups_with_count}


@router.get("/spirits/{spirit_id}/skills")
async def get_spirit_skills(spirit_id: int):
    """获取精灵的技能列表"""
    skills = SPIRIT_SKILLS.get(spirit_id)
    if skills is None:
        return {"success": True, "skills": [], "total": 0}
    # 附上图标 URL
    enriched = []
    for s in skills:
        enriched.append({
            **s,
            "icon_url": SKILL_ICONS_MAP.get(s["name"], ""),
        })
    return {
        "success": True,
        "skills": enriched,
        "total": len(enriched),
    }


@router.get("/spirits/{spirit_id}/type-matchups")
async def get_spirit_matchups(spirit_id: int):
    """获取精灵的属性克制关系"""
    spirit = SPIRITS_BY_ID.get(spirit_id)
    if not spirit:
        raise HTTPException(status_code=404, detail=f"精灵 ID {spirit_id} 不存在")
    matchups = SPIRIT_MATCHUPS.get(spirit_id, {})
    return {
        "success": True,
        "spirit_id": spirit_id,
        "strong_against": matchups.get("strong_against", []),
        "weak_to": matchups.get("weak_to", []),
        "resists": matchups.get("resists", []),
        "resisted_by": matchups.get("resisted_by", []),
    }


def _format_spirit_card(s: dict) -> dict:
    """格式化精灵卡片（列表用）"""
    return {
        "spirit_id": s['spirit_id'],
        "spirit_no": s['spirit_no'],
        "base_name": s['base_name'],
        "display_name": s.get('display_name', s['base_name']),
        "form_name": s.get('form_name'),
        "primary_attribute": s.get('primary_attribute'),
        "egg_groups": s.get('egg_groups', []),
        "can_breed": s.get('can_breed', False),
        "image": get_spirit_image(s['spirit_no_number']),
        "shiny_image": s.get('shiny_image_url'),
        "race_total": s.get('race_total', 0),
        "has_shiny_variant": s.get('has_shiny_variant', False),
    }


def _format_spirit_detail(s: dict) -> dict:
    """格式化精灵详情"""
    evolution = []
    for e in s.get('evolution_chain', []):
        evolution.append({
            "spirit_id": e['spirit_id'],
            "spirit_no": e['spirit_no'],
            "base_name": e['base_name'],
            "display_name": e.get('display_name', e['base_name']),
            "form_name": e.get('form_name'),
            "stage_name": e.get('stage_name'),
            "evolution_level": e.get('evolution_level'),
            "evolution_level_text": e.get('evolution_level_text'),
            "image": get_spirit_image(e['spirit_no_number']),
        })

    forms = []
    for f in s.get('forms', []):
        forms.append({
            "spirit_id": f['spirit_id'],
            "spirit_no": f['spirit_no'],
            "base_name": f['base_name'],
            "display_name": f.get('display_name', f['base_name']),
            "form_name": f.get('form_name'),
            "image": get_spirit_image(f['spirit_no_number']),
        })

    return {
        "spirit_id": s['spirit_id'],
        "spirit_no": s['spirit_no'],
        "base_name": s['base_name'],
        "display_name": s.get('display_name', s['base_name']),
        "form_name": s.get('form_name'),
        "stage_name": s.get('stage_name'),
        "primary_attribute": s.get('primary_attribute'),
        "secondary_attribute": s.get('secondary_attribute'),
        "trait_name": s.get('trait_name'),
        "trait_effect": s.get('trait_effect'),
        "description": s.get('description'),
        "height_text": s.get('height_text'),
        "weight_text": s.get('weight_text'),
        "location_text": s.get('location_text'),
        "locations": s.get('locations', []),
        "egg_groups": s.get('egg_groups', []),
        "can_breed": s.get('can_breed', False),
        "race_total": s.get('race_total', 0),
        "hp": s.get('hp', 0),
        "attack": s.get('attack', 0),
        "magic_attack": s.get('magic_attack', 0),
        "defense": s.get('defense', 0),
        "magic_defense": s.get('magic_defense', 0),
        "speed": s.get('speed', 0),
        "image": get_spirit_image(s['spirit_no_number']),
        "has_shiny_variant": s.get('has_shiny_variant', False),
        "shiny_image": s.get('shiny_image_url'),
        "evolution_chain": evolution,
        "forms": forms,
    }
