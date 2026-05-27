#!/usr/bin/env python3
"""
洛克王国：世界 - 孵蛋查询 API
基于 FastAPI + 开源数据 (github.com/jiluoQAQ/RocomUID)
"""

import os
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from static_serve import register_static_routes, register_spa_fallback

# ========== App 创建 ==========

app = FastAPI(
    title="洛克王国：世界 - 孵蛋查询 API",
    description="根据身高体重查询可能孵化的精灵",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:2026",
        "http://127.0.0.1:2026",
        "http://localhost:20204",
        "http://127.0.0.1:20204",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== 静态资源和 SPA 路由（必须在 API 路由之前） ==========
register_static_routes(app)

# ========== API 路由注册 ==========

from api.query import router as query_router
from api.spirits import router as spirits_router
from api.pets import router as pets_router
from api.stats import router as stats_router
from api.garden import router as garden_router
from api.merchant import router as merchant_router
from models import HealthResponse
from services.breeding import PETS
from services.image import get_image_matcher

app.include_router(query_router)
app.include_router(spirits_router)
app.include_router(pets_router)
app.include_router(stats_router)
app.include_router(garden_router)
app.include_router(merchant_router)

# 测试路由
@app.get("/api/test")
async def test_route():
    return {"success": True, "message": "测试路由正常"}


@app.get("/api/health", response_model=HealthResponse, tags=["系统"])
async def health_check():
    """健康检查"""
    return HealthResponse(status="ok", total_pets=len(PETS), version="2.0.0")

@app.get("/api/test2")
async def test2():
    return {"success": True, "message": "test2正常"}

@app.get("/api/gardenhealth")
async def garden_health():
    return {"success": True, "message": "家园炼金健康检查正常"}

@app.get("/api/refresh-image-cache", tags=["系统"])
async def refresh_image_cache(authorization: str = Header(None)):
    """刷新图片缓存（需要管理员密钥）"""
    admin_key = os.getenv("ROCOM_ADMIN_KEY")
    if not admin_key:
        raise HTTPException(status_code=403, detail="管理员密钥未配置，此接口不可用")
    if not authorization or authorization != f"Bearer {admin_key}":
        raise HTTPException(status_code=403, detail="密钥无效或未提供")
    matcher = get_image_matcher()
    matcher.refresh_cache()
    return {"success": True, "message": "缓存已刷新"}


# ========== 生命周期 ==========

@app.on_event("startup")
async def startup_event():
    get_image_matcher()
    print("[FastAPI] 图片匹配器已加载")

# ========== SPA fallback（必须放在所有路由最后面） ==========
register_spa_fallback(app)

# ========== 启动 ==========

if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("🎮 洛克王国：世界 - 孵蛋查询 API v2.0")
    print("=" * 50)
    print(f"📡 API文档: http://localhost:2026/docs")
    print("=" * 50 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=2026, log_level="info")
