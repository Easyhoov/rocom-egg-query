#!/usr/bin/env python3
"""精灵列表 API"""

from typing import Optional
from fastapi import APIRouter, Query
from services.breeding import PETS

router = APIRouter(prefix="/api", tags=["精灵列表"])


@router.get("/pets")
async def list_pets(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
    precious: Optional[bool] = Query(None, description="过滤珍贵蛋"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
):
    """分页获取精灵列表"""
    filtered = PETS

    if precious is not None:
        if precious:
            filtered = [p for p in filtered if p.get('precious_egg_type', 0) > 0]
        else:
            filtered = [p for p in filtered if p.get('precious_egg_type', 0) == 0]

    if keyword:
        filtered = [p for p in filtered if keyword in p['name']]

    total = len(filtered)
    start = (page - 1) * size
    end = start + size
    items = filtered[start:end]

    return {
        "success": True,
        "total": total,
        "page": page,
        "size": size,
        "items": [
            {
                "name": p['name'],
                "height_range": f"{p['height_low']/100:.2f}-{p['height_high']/100:.2f}m",
                "weight_range": f"{p['weight_low']/1000:.3f}-{p['weight_high']/1000:.3f}kg",
                "is_precious": p.get('precious_egg_type', 0) > 0,
            }
            for p in items
        ],
    }
