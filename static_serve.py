"""
静态资源挂载 + SPA 页面路由
从 main.py 抽取，保持 main.py 只关注 API 路由和生命周期管理
"""
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

PROJECT_DIR = Path(__file__).parent
STATIC_DIR = PROJECT_DIR / "static"
INDEX_HTML = STATIC_DIR / "index.html"
PREVIEW_HTML = STATIC_DIR / "preview" / "index.html"


def register_static_routes(app: FastAPI):
    """注册所有静态资源挂载和 SPA 页面路由（必须在 API 路由之前调用静态挂载）"""

    # ========== 静态资源目录挂载 ==========
    static_subdirs = [
        ("creature-atlas", "/creature-atlas"),
        ("assets", "/assets"),
        ("attr-icons", "/attr-icons"),
        ("garden-icons", "/garden-icons"),
        ("skill-icons", "/skill-icons"),
        ("item-icons", "/item-icons"),
    ]
    for dirname, mount_path in static_subdirs:
        dirpath = STATIC_DIR / dirname
        if dirpath.exists():
            app.mount(mount_path, StaticFiles(directory=str(dirpath)), name=dirname)

    # ========== SPA 页面路由 ==========
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

    @app.get("/index.html")
    async def serve_index_html():
        return FileResponse(INDEX_HTML)

    # ========== 特殊文件路由 ==========
    ca_crt_file = STATIC_DIR / "ca.crt"

    @app.get("/ca.crt")
    async def serve_ca_crt():
        """提供 UnblockNeteaseMusic CA 证书下载"""
        if ca_crt_file.exists():
            return FileResponse(ca_crt_file, media_type="application/x-x509-ca-cert", filename="ca.crt")
        return {"error": "证书文件不存在"}

    pac_file = STATIC_DIR / "proxy.pac"

    @app.get("/proxy.pac")
    async def serve_pac():
        """提供代理自动配置 PAC 文件"""
        if pac_file.exists():
            return FileResponse(pac_file, media_type="application/x-ns-proxy-autoconfig")
        return {"error": "PAC 文件不存在"}


def register_spa_fallback(app: FastAPI):
    """注册 SPA fallback 路由（必须在所有其他路由之后调用）"""

    @app.get("/{full_path:path}")
    async def spa_fallback(full_path: str):
        return FileResponse(INDEX_HTML)
