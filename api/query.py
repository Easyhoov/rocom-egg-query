#!/usr/bin/env python3
"""孵蛋查询 API"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from models import EggQueryRequest, PetResult, EggQueryResponse
from services.breeding import query_egg, PETS

router = APIRouter(prefix="/api", tags=["孵蛋查询"])


@router.get("/query", response_model=EggQueryResponse)
async def query_egg_get(
    height: float = Query(..., description="身高 (米), 如 0.24"),
    weight: float = Query(..., description="体重 (千克), 如 1.60"),
    precious: Optional[int] = Query(None, description="蛋类型筛选: 0=神奇的蛋, 1=炫彩蛋, 不传=不限"),
):
    """GET 方式查询孵蛋结果"""
    if height <= 0 or weight <= 0:
        raise HTTPException(status_code=400, detail="身高和体重必须大于0")

    results, user_r = query_egg(height, weight, precious)
    normal = [r for r in results if not r['is_precious']]
    precious_list = [r for r in results if r['is_precious']]

    return EggQueryResponse(
        success=True,
        query={"height": height, "weight": weight, "egg_filter": precious},
        total=len(results),
        normal_count=len(normal),
        precious_count=len(precious_list),
        user_r=user_r,
        results=[PetResult(**r) for r in results],
    )


@router.post("/query", response_model=EggQueryResponse)
async def query_egg_post(req: EggQueryRequest):
    """POST 方式查询孵蛋结果"""
    if req.height <= 0 or req.weight <= 0:
        raise HTTPException(status_code=400, detail="身高和体重必须大于0")

    results, user_r = query_egg(req.height, req.weight, req.egg_filter)
    normal = [r for r in results if not r['is_precious']]
    precious_list = [r for r in results if r['is_precious']]

    return EggQueryResponse(
        success=True,
        query={"height": req.height, "weight": req.weight, "egg_filter": req.egg_filter},
        total=len(results),
        normal_count=len(normal),
        precious_count=len(precious_list),
        user_r=user_r,
        results=[PetResult(**r) for r in results],
    )
