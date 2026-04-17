#!/usr/bin/env python3
"""
洛克王国：世界 - 孵蛋查询 API
基于 FastAPI + 开源数据 (github.com/jiluoQAQ/RocomUID)
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import math

# 图片匹配模块
from image_matcher_fastapi import get_image_matcher

# ========== 数据加载 ==========

DATA_DIR = Path(__file__).parent / "data"
BREEDING_FILE = DATA_DIR / "breeding.json"

def load_breeding_data():
    """加载孵蛋数据"""
    if not BREEDING_FILE.exists():
        print(f"❌ 数据文件不存在: {BREEDING_FILE}")
        print("   请先运行: python3 download_data.py")
        sys.exit(1)
    
    with open(BREEDING_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    pets = data['pet_egg_conf']
    print(f"✅ 已加载 {len(pets)} 条孵蛋数据")
    return pets

# 全局数据
PETS = load_breeding_data()

# ========== 图鉴数据加载 ==========

SPIRITS_FILE = DATA_DIR / "spirits.json"
OFFICIAL_EGG_GROUPS_FILE = DATA_DIR / "official_egg_groups.json"

def load_spirits_data():
    """加载图鉴数据"""
    if not SPIRITS_FILE.exists():
        print(f"⚠️ 图鉴数据不存在: {SPIRITS_FILE}")
        return [], {}, {}
    
    with open(SPIRITS_FILE, 'r', encoding='utf-8') as f:
        spirits = json.load(f)
    
    # 按 spirit_id 建索引
    by_id = {s['spirit_id']: s for s in spirits}
    
    # 按名字建索引（用于孵蛋结果关联）
    by_name = {}
    for s in spirits:
        name = s['base_name']
        if name not in by_name or s.get('form_name') is None:
            by_name[name] = s
    
    print(f"✅ 已加载 {len(spirits)} 只精灵图鉴数据")
    return spirits, by_id, by_name

def load_official_egg_groups():
    """加载官方蛋组数据"""
    if not OFFICIAL_EGG_GROUPS_FILE.exists():
        return []
    with open(OFFICIAL_EGG_GROUPS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

SPIRITS, SPIRITS_BY_ID, SPIRITS_BY_NAME = load_spirits_data()
OFFICIAL_EGG_GROUPS = load_official_egg_groups()

# 本地图片文件索引（按编号）
STATIC_DIR = Path(__file__).parent / "static"
ATLAS_DIR = STATIC_DIR / "creature-atlas"
_local_image_cache: dict[int, str] = {}

def _build_image_index():
    """构建本地图片索引"""
    if not ATLAS_DIR.exists():
        return
    # 按编号收集所有可用图片
    by_number: dict[int, list[str]] = {}
    for p in ATLAS_DIR.glob("*.webp"):
        stem = p.stem  # e.g. "001-base", "011-form-02"
        try:
            num = int(stem.split("-")[0])
            by_number.setdefault(num, []).append(stem)
        except ValueError:
            continue
    
    # 优先 base → form-01 → 第一个
    for num, files in by_number.items():
        base = f"{num:03d}-base"
        if base in files:
            _local_image_cache[num] = f"/creature-atlas/{base}.webp"
        else:
            # 找 form-01
            form01 = [f for f in files if "form-01" in f]
            if form01:
                _local_image_cache[num] = f"/creature-atlas/{form01[0]}.webp"
            else:
                _local_image_cache[num] = f"/creature-atlas/{files[0]}.webp"

_build_image_index()

def get_spirit_image(spirit_no_number: int) -> Optional[str]:
    """获取精灵本地图片路径"""
    return _local_image_cache.get(spirit_no_number)

# ========== API 定义 ==========

app = FastAPI(
    title="洛克王国：世界 - 孵蛋查询 API",
    description="根据身高体重查询可能孵化的精灵",
    version="1.0.0",
    docs_url="/docs",       # Swagger UI
    redoc_url="/redoc",     # ReDoc
)

# 允许跨域 (小程序需要)
# 静态文件 - 图片资源
STATIC_DIR = Path(__file__).parent / "static"
if (STATIC_DIR / "creature-atlas").exists():
    app.mount("/creature-atlas", StaticFiles(directory=STATIC_DIR / "creature-atlas"), name="creature-atlas")

# 静态文件 - 首页
INDEX_HTML = Path(__file__).parent / "static" / "index.html"

@app.get("/index.html")
async def serve_index():
    return FileResponse(INDEX_HTML)

# 静态资源 (Vite 构建产物)
ASSETS_DIR = Path(__file__).parent / "static" / "assets"
if ASSETS_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========== 数据模型 ==========

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


# ========== 工具函数 ==========

def get_egg_type_info(precious_type: int) -> dict:
    """获取蛋类型信息"""
    types = {
        0: {"name": "普通蛋", "icon": "🥚", "color": "#667eea"},
        1: {"name": "珍贵蛋", "icon": "💎", "color": "#e74c3c"},
        2: {"name": "异色蛋", "icon": "🌈", "color": "#e91e63"},
        4: {"name": "特殊蛋", "icon": "🎁", "color": "#ff9800"},
        5: {"name": "首领蛋", "icon": "👑", "color": "#9c27b0"},
        7: {"name": "速孵蛋", "icon": "⚡", "color": "#00bcd4"},
    }
    return types.get(precious_type, {"name": "未知", "icon": "❓", "color": "#999"})



def query_egg(height_m: float, weight_kg: float, egg_filter: Optional[int] = None) -> tuple[list[dict], float]:
    """
    查询孵蛋结果
    egg_filter: 0=只神奇的蛋, 1=只炫彩蛋, None=不限
    返回: (结果列表, 用户R值)
    """
    height_cm = height_m * 100
    weight_g = weight_kg * 1000
    user_r = weight_kg / height_m if height_m > 0 else 0
    
    seen = set()
    results = []
    
    for pet in PETS:
        precious_type = pet.get('precious_egg_type', 0)
        
        # 蛋类型筛选
        if egg_filter == 0 and precious_type != 0:
            continue
        if egg_filter == 1 and precious_type == 0:
            continue
        
        # 身高体重匹配
        if not (pet['height_low'] <= height_cm <= pet['height_high']):
            continue
        if not (pet['weight_low'] <= weight_g <= pet['weight_high']):
            continue
        
        # 去重: 炫彩蛋/不限类型按名字去重, 神奇的蛋按名字+类型去重
        if egg_filter is None or egg_filter == 1:
            key = pet['name']
        else:
            key = f"{pet['name']}_{precious_type}"
        if key in seen:
            continue
        seen.add(key)
        
        egg_type_info = get_egg_type_info(precious_type)
        
        # R值 = 中位体重(kg) / 中位身高(m)
        h_mid = (pet['height_low'] + pet['height_high']) / 2 / 100
        w_mid = (pet['weight_low'] + pet['weight_high']) / 2 / 1000
        r_value = w_mid / h_mid if h_mid > 0 else 0

        results.append({
            'name': pet['name'],
            'height_min': pet['height_low'] / 100,
            'height_max': pet['height_high'] / 100,
            'weight_min': pet['weight_low'] / 1000,
            'weight_max': pet['weight_high'] / 1000,
            'is_precious': precious_type > 0,
            'precious_type': precious_type,
            'egg_type_name': egg_type_info['name'],
            'egg_type_icon': egg_type_info['icon'],
            'egg_type_color': egg_type_info['color'],
            'r_value': round(r_value, 2),
            'r_diff': round(abs(r_value - user_r), 2),
        })
    
    # 按R值差距排序
    results.sort(key=lambda x: x['r_diff'])
    
    # 补充图片路径
    matcher = get_image_matcher()
    for r in results:
        r['image'] = matcher.match(r['name'])
    
    return results, round(user_r, 2)


# ========== API 路由 ==========

@app.get("/")
async def serve_root():
    """返回旧版孵蛋查询页面"""
    return FileResponse(Path(__file__).parent / "index.html")

@app.get("/compendium")
@app.get("/compendium/{path:path}")
async def serve_compendium(path: str = ""):
    """返回 Vue 图鉴页面"""
    return FileResponse(INDEX_HTML)


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """健康检查"""
    return HealthResponse(
        status="ok",
        total_pets=len(PETS),
        version="1.0.0"
    )


@app.get("/api/query", response_model=EggQueryResponse)
async def query_egg_get(
    height: float = Query(..., description="身高 (米), 如 0.24"),
    weight: float = Query(..., description="体重 (千克), 如 1.60"),
    precious: Optional[int] = Query(None, description="蛋类型筛选: 0=神奇的蛋, 1=炫彩蛋, 不传=不限"),
):
    """
    GET 方式查询孵蛋结果
    precious: 0=神奇的蛋(precious_egg_type=0), 1=炫彩蛋(precious_egg_type>0), 不传=不限
    """
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


@app.post("/api/query", response_model=EggQueryResponse)
async def query_egg_post(req: EggQueryRequest):
    """
    POST 方式查询孵蛋结果
    """
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


@app.get("/api/pets")
async def list_pets(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
    precious: Optional[bool] = Query(None, description="过滤珍贵蛋"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
):
    """
    分页获取精灵列表
    """
    filtered = PETS
    
    # 珍贵蛋过滤
    if precious is not None:
        if precious:
            filtered = [p for p in filtered if p.get('precious_egg_type', 0) > 0]
        else:
            filtered = [p for p in filtered if p.get('precious_egg_type', 0) == 0]
    
    # 关键词搜索
    if keyword:
        filtered = [p for p in filtered if keyword in p['name']]
    
    # 分页
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
        ]
    }


@app.get("/api/stats")
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
        }
    }


# ========== 图鉴 API ==========

@app.get("/api/spirits")
async def list_spirits(
    q: Optional[str] = Query(None, description="搜索（名称/编号）"),
    attribute: Optional[str] = Query(None, description="属性筛选"),
    egg_group: Optional[str] = Query(None, description="蛋组筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(24, ge=1, le=100, description="每页数量"),
):
    """图鉴列表（搜索+筛选+分页）"""
    filtered = SPIRITS
    
    # 搜索
    if q:
        q_lower = q.lower().strip()
        filtered = [
            s for s in filtered
            if q_lower in s['base_name'].lower()
            or q_lower in s.get('display_name', '').lower()
            or q_lower in s.get('spirit_no', '').lower()
            or (q.isdigit() and s['spirit_no_number'] == int(q))
        ]
    
    # 属性筛选
    if attribute:
        filtered = [
            s for s in filtered
            if s.get('primary_attribute') == attribute
            or s.get('secondary_attribute') == attribute
        ]
    
    # 蛋组筛选
    if egg_group:
        filtered = [
            s for s in filtered
            if egg_group in s.get('egg_groups', [])
        ]
    
    # 排序：按编号
    filtered.sort(key=lambda s: s['spirit_no_number'])
    
    # 分页
    total = len(filtered)
    total_pages = math.ceil(total / page_size) if total > 0 else 1
    start = (page - 1) * page_size
    end = start + page_size
    items = filtered[start:end]
    
    return {
        "success": True,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "items": [_format_spirit_card(s) for s in items],
    }


@app.get("/api/spirits/{spirit_id}")
async def get_spirit(spirit_id: int):
    """精灵详情"""
    spirit = SPIRITS_BY_ID.get(spirit_id)
    if not spirit:
        raise HTTPException(status_code=404, detail=f"精灵 ID {spirit_id} 不存在")
    return {
        "success": True,
        "spirit": _format_spirit_detail(spirit),
    }


@app.get("/api/official-egg-groups")
async def list_official_egg_groups():
    """官方蛋组列表"""
    groups_with_count = []
    for g in OFFICIAL_EGG_GROUPS:
        name = g['egg_group_name']
        count = sum(1 for s in SPIRITS if name in s.get('egg_groups', []))
        groups_with_count.append({**g, "spirit_count": count})
    return {"success": True, "groups": groups_with_count}


def _format_spirit_card(s: dict) -> dict:
    """格式化精灵卡片（列表用）"""
    return {
        "spirit_id": s['spirit_id'],
        "spirit_no": s['spirit_no'],
        "base_name": s['base_name'],
        "display_name": s.get('display_name', s['base_name']),
        "form_name": s.get('form_name'),
        "primary_attribute": s.get('primary_attribute'),
        "egg_groups": s.get('egg_groups', []),
        "can_breed": s.get('can_breed', False),
        "image": get_spirit_image(s['spirit_no_number']),
        "race_total": s.get('race_total', 0),
    }


def _format_spirit_detail(s: dict) -> dict:
    """格式化精灵详情"""
    # 进化链附带图片
    evolution = []
    for e in s.get('evolution_chain', []):
        evolution.append({
            "spirit_id": e['spirit_id'],
            "spirit_no": e['spirit_no'],
            "base_name": e['base_name'],
            "display_name": e.get('display_name', e['base_name']),
            "form_name": e.get('form_name'),
            "stage_name": e.get('stage_name'),
            "evolution_level": e.get('evolution_level'),
            "evolution_level_text": e.get('evolution_level_text'),
            "image": get_spirit_image(e['spirit_no_number']),
        })
    
    # 形态
    forms = []
    for f in s.get('forms', []):
        forms.append({
            "spirit_id": f['spirit_id'],
            "spirit_no": f['spirit_no'],
            "base_name": f['base_name'],
            "display_name": f.get('display_name', f['base_name']),
            "form_name": f.get('form_name'),
            "image": get_spirit_image(f['spirit_no_number']),
        })
    
    return {
        "spirit_id": s['spirit_id'],
        "spirit_no": s['spirit_no'],
        "base_name": s['base_name'],
        "display_name": s.get('display_name', s['base_name']),
        "form_name": s.get('form_name'),
        "stage_name": s.get('stage_name'),
        "primary_attribute": s.get('primary_attribute'),
        "secondary_attribute": s.get('secondary_attribute'),
        "trait_name": s.get('trait_name'),
        "trait_effect": s.get('trait_effect'),
        "description": s.get('description'),
        "height_text": s.get('height_text'),
        "weight_text": s.get('weight_text'),
        "location_text": s.get('location_text'),
        "locations": s.get('locations', []),
        "egg_groups": s.get('egg_groups', []),
        "can_breed": s.get('can_breed', False),
        "race_total": s.get('race_total', 0),
        "hp": s.get('hp', 0),
        "attack": s.get('attack', 0),
        "magic_attack": s.get('magic_attack', 0),
        "defense": s.get('defense', 0),
        "magic_defense": s.get('magic_defense', 0),
        "speed": s.get('speed', 0),
        "image": get_spirit_image(s['spirit_no_number']),
        "has_shiny_variant": s.get('has_shiny_variant', False),
        "evolution_chain": evolution,
        "forms": forms,
    }


# ========== 图鉴 API (CDN 图片版) ==========

@app.on_event("startup")
async def startup_event():
    """应用启动时加载图片匹配器"""
    get_image_matcher()
    print("[FastAPI] 图片匹配器已加载")


@app.get("/api/refresh-image-cache")
async def refresh_image_cache():
    """刷新图片缓存（管理接口）"""
    matcher = get_image_matcher()
    matcher.refresh_cache()
    return {"success": True, "message": "缓存已刷新"}


# SPA fallback — 所有非 API 路由返回 index.html
@app.get("/{full_path:path}")
async def spa_fallback(full_path: str):
    return FileResponse(INDEX_HTML)


# ========== 启动 ==========

if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("🎮 洛克王国：世界 - 孵蛋查询 API")
    print("=" * 50)
    print(f"📡 API文档: http://localhost:8000/docs")
    print(f"📡 ReDoc文档: http://localhost:8000/redoc")
    print("=" * 50 + "\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=2026,
        log_level="info",
    )
