#!/usr/bin/env python3
"""Pydantic 数据模型"""

from typing import Optional
from pydantic import BaseModel


class EggQueryRequest(BaseModel):
    """孵蛋查询请求"""
    height: float  # 身高 (米)
    weight: float  # 体重 (千克)
    egg_filter: Optional[int] = None  # 0=神奇的蛋, 1=炫彩蛋, None=不限


class PetResult(BaseModel):
    """精灵结果"""
    name: str
    height_min: float
    height_max: float
    weight_min: float
    weight_max: float
    is_precious: bool
    precious_type: int
    egg_type_name: str
    egg_type_icon: str
    egg_type_color: str
    r_value: float = 0
    r_diff: float = 0
    match_tier: str = "nearest"  # exact / tolerance1 / tolerance2 / nearest
    probability: int = 0  # 0-100
    image: Optional[str] = None


class EggQueryResponse(BaseModel):
    """孵蛋查询响应"""
    success: bool
    query: dict
    total: int
    normal_count: int
    precious_count: int
    user_r: float = 0
    results: list[PetResult]


class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str
    total_pets: int
    version: str
