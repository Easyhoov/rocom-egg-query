#!/usr/bin/env python3
"""
洛克王国：世界 - 孵蛋查询 API
基于 FastAPI + 开源数据 (github.com/jiluoQAQ/RocomUID)
"""

from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 路径
PROJECT_DIR = Path(__file__).parent
STATIC_DIR = PROJECT_DIR / "static"
INDEX_HTML = STATIC_DIR / "index.html"
COMPENDIUM_HTML = STATIC_DIR / "index.html"  # Vue SPA (同一入口，由路由区分)

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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== 静态文件 ==========

if (STATIC_DIR / "creature-atlas").exists():
    app.mount("/creature-atlas", StaticFiles(directory=STATIC_DIR / "creature-atlas"), name="creature-atlas")

ASSETS_DIR = STATIC_DIR / "assets"
if ASSETS_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")


# ========== 页面路由 ==========

@app.get("/egg-query")
async def serve_egg_query():
    """旧版孵蛋查询页面"""
    return FileResponse(PROJECT_DIR / "index.html")

@app.get("/compendium")
@app.get("/compendium/{path:path}")
async def serve_compendium(path: str = ""):
    """Vue 图鉴页面"""
    return FileResponse(INDEX_HTML)

@app.get("/index.html")
async def serve_index_html():
    return FileResponse(INDEX_HTML)


# ========== API 路由注册 ==========

from api.query import router as query_router
from api.spirits import router as spirits_router
from api.pets import router as pets_router
from api.stats import router as stats_router
from models import HealthResponse
from services.breeding import PETS
from services.image import get_image_matcher

app.include_router(query_router)
app.include_router(spirits_router)
app.include_router(pets_router)
app.include_router(stats_router)


@app.get("/api/health", response_model=HealthResponse, tags=["系统"])
async def health_check():
    """健康检查"""
    return HealthResponse(status="ok", total_pets=len(PETS), version="2.0.0")


@app.get("/api/refresh-image-cache", tags=["系统"])
async def refresh_image_cache():
    """刷新图片缓存"""
    matcher = get_image_matcher()
    matcher.refresh_cache()
    return {"success": True, "message": "缓存已刷新"}


# ========== 生命周期 ==========

@app.on_event("startup")
async def startup_event():
    get_image_matcher()
    print("[FastAPI] 图片匹配器已加载")


# SPA fallback
@app.get("/{full_path:path}")
async def spa_fallback(full_path: str):
    return FileResponse(INDEX_HTML)


# ========== 启动 ==========

if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("🎮 洛克王国：世界 - 孵蛋查询 API v2.0")
    print("=" * 50)
    print(f"📡 API文档: http://localhost:2026/docs")
    print("=" * 50 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=2026, log_level="info")
