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

# ========== 静态资源 必须放在所有路由最前面！ ==========
if (STATIC_DIR / "creature-atlas").exists():
    app.mount("/creature-atlas", StaticFiles(directory=STATIC_DIR / "creature-atlas"), name="creature-atlas")

ASSETS_DIR = STATIC_DIR / "assets"
if ASSETS_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")

ATTR_ICONS_DIR = STATIC_DIR / "attr-icons"
if ATTR_ICONS_DIR.exists():
    app.mount("/attr-icons", StaticFiles(directory=str(ATTR_ICONS_DIR)), name="attr-icons")

GARDEN_ICONS_DIR = STATIC_DIR / "garden-icons"
if GARDEN_ICONS_DIR.exists():
    app.mount("/garden-icons", StaticFiles(directory=str(GARDEN_ICONS_DIR)), name="garden-icons")

# ========== 页面路由 ==========
@app.get("/")
async def serve_home():
    """首页"""
    return FileResponse(INDEX_HTML)

@app.get("/garden")
@app.get("/garden/{path:path}")
async def serve_garden(path: str = ""):
    """家园炼金页面"""
    return FileResponse(INDEX_HTML)

@app.get("/egg-group")
@app.get("/egg-group/{path:path}")
async def serve_egg_group(path: str = ""):
    """蛋组配对页面"""
    return FileResponse(INDEX_HTML)

@app.get("/egg-query")
@app.get("/egg-query/{path:path}")
async def serve_egg_query(path: str = ""):
    """孵蛋查询页面 (Vue SPA)"""
    return FileResponse(INDEX_HTML)

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
from api.garden import router as garden_router
from models import HealthResponse
from services.breeding import PETS
from services.image import get_image_matcher

app.include_router(query_router)
app.include_router(spirits_router)
app.include_router(pets_router)
app.include_router(stats_router)
app.include_router(garden_router)

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

# ========== 启动 ==========

if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("🎮 洛克王国：世界 - 孵蛋查询 API v2.0")
    print("=" * 50)
    print(f"📡 API文档: http://localhost:2026/docs")
    print("=" * 50 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=2026, log_level="info")

# SPA fallback 必须放在所有路由最后面
@app.get("/{full_path:path}")
async def spa_fallback(full_path: str):
    return FileResponse(INDEX_HTML)
