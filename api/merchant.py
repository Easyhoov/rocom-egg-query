"""远行商人 API 路由"""

from fastapi import APIRouter, Query
from services.merchant import get_merchant_info

router = APIRouter(prefix="/api", tags=["远行商人"])


@router.get("/merchant/info")
async def merchant_info(refresh: bool = Query(False, description="强制刷新")):
    """获取远行商人当前商品信息"""
    return await get_merchant_info(force_refresh=refresh)
