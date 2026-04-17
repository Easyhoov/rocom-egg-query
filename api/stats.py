#!/usr/bin/env python3
"""数据统计 API"""

from fastapi import APIRouter
from services.breeding import PETS

router = APIRouter(prefix="/api", tags=["统计"])


@router.get("/stats")
async def get_stats():
    """获取数据统计"""
    normal = sum(1 for p in PETS if p.get('precious_egg_type', 0) == 0)
    precious = sum(1 for p in PETS if p.get('precious_egg_type', 0) > 0)
    unique_names = len(set(p['name'] for p in PETS))

    return {
        "success": True,
        "stats": {
            "total_records": len(PETS),
            "unique_pets": unique_names,
            "normal_eggs": normal,
            "precious_eggs": precious,
        },
    }
