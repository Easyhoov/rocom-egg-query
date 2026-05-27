#!/usr/bin/env python3
"""
洛克王国：世界 - 孵蛋查询 API
基于 FastAPI + 开源数据 (github.com/jiluoQAQ/RocomUID)
"""

import os
from pathlib import Path
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 路径
PROJECT_DIR = Path(__file__).parent
STATIC_DIR = PROJECT_DIR / "static"
INDEX_HTML = STATIC_DIR / "index.html"

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
    allow_origins=["http://localhost:2026", "http://localhost:20204"],
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

SKILL_ICONS_DIR = STATIC_DIR / "skill-icons"
if SKILL_ICONS_DIR.exists():
    app.mount("/skill-icons", StaticFiles(directory=str(SKILL_ICONS_DIR)), name="skill-icons")

IMG_DIR = STATIC_DIR / "img"
if IMG_DIR.exists():
    app.mount("/img", StaticFiles(directory=str(IMG_DIR)), name="img")

ITEM_ICONS_DIR = STATIC_DIR / "item-icons"
if ITEM_ICONS_DIR.exists():
    app.mount("/item-icons", StaticFiles(directory=str(ITEM_ICONS_DIR)), name="item-icons")

PREVIEW_HTML = STATIC_DIR / "preview" / "index.html"

# ========== 页面路由 ==========
@app.get("/")
async def serve_home():
    """首页"""
    return FileResponse(INDEX_HTML)

@app.get("/merchant-preview")
async def serve_merchant_preview():
    """远行商人模板预览"""
    return FileResponse(PREVIEW_HTML)

@app.get("/garden")
@app.get("/garden/{path:path}")
async def serve_garden(path: str = ""):
    """家园炼金页面"""
    return FileResponse(INDEX_HTML)

@app.get("/merchant")
@app.get("/merchant/{path:path}")
async def serve_merchant(path: str = ""):
    """远行商人页面"""
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

@app.get("/favicon.png")
async def serve_favicon():
    """favicon - 神奇的蛋"""
    fav = STATIC_DIR / "favicon.png"
    if fav.exists():
        return FileResponse(fav, media_type="image/png")
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
@app.get("/{full_path:path}")
async def spa_fallback(full_path: str):
    return FileResponse(INDEX_HTML)

@app.get("/design-template")
async def serve_design_template():
    """前端设计模板预览"""
    return FileResponse(STATIC_DIR / "design-template.html")

@app.get("/asset-template")
async def serve_asset_template():
    """素材组合模板演示"""
    return FileResponse(STATIC_DIR / "asset-template.html")

# ========== 启动 ==========

if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("🎮 洛克王国：世界 - 孵蛋查询 API v2.0")
    print("=" * 50)
    print(f"📡 API文档: http://localhost:2026/docs")
    print("=" * 50 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=2026, log_level="info")
