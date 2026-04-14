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
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

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

def load_json_file(filename):
    """加载 JSON 数据文件"""
    filepath = DATA_DIR / filename
    if not filepath.exists():
        print(f"⚠️ 数据文件不存在: {filepath}")
        return {}
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

EGG_GROUPS = load_json_file('egg_groups.json')  # {蛋组名: [精灵列表]}
EVOLUTION_CHAINS = load_json_file('evolution_chains.json')  # {count, chains}
CONFIG = load_json_file('config.json')  # {no_breed_pets, shiny_seed_pets}

# 构建反向索引: 精灵名 -> [蛋组列表]
PET_TO_GROUPS = {}
for group_name, members in EGG_GROUPS.items():
    for pet_name in members:
        PET_TO_GROUPS.setdefault(pet_name, []).append(group_name)

# 构建进化链索引: 精灵名 -> [自身名]（进化链数据暂不可用，后续补充）
PET_TO_CHAIN = {}
# TODO: 从外部数据源补充进化链
# for chain in EVOLUTION_CHAINS.get('chains', []):
#     names = [c['name'] for c in chain if isinstance(c, dict) and 'name' in c]
#     if len(names) >= 2 and len(set(names)) > 1:  # 至少两个不同名字才有效
#         for c in chain:
#             PET_TO_CHAIN[c['name']] = names

NO_BREED_PETS = set(CONFIG.get('no_breed_pets', []))
SHINY_SEED_PETS = set(CONFIG.get('shiny_seed_pets', []))

print(f"✅ 已加载 {len(EGG_GROUPS)} 个蛋组, {len(PET_TO_GROUPS)} 只精灵有蛋组信息")
print(f"✅ 已加载 {EVOLUTION_CHAINS.get('count', 0)} 条进化链")

# ========== API 定义 ==========

app = FastAPI(
    title="洛克王国：世界 - 孵蛋查询 API",
    description="根据身高体重查询可能孵化的精灵",
    version="1.0.0",
    docs_url="/docs",       # Swagger UI
    redoc_url="/redoc",     # ReDoc
)

# 允许跨域 (小程序需要)
# 静态文件 - 首页
@app.get("/index.html")
async def serve_index():
    from pathlib import Path
    return FileResponse(Path(__file__).parent / "index.html")

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
    match_tier: str = "range"  # exact / tolerance1 / tolerance2 / range / nearest
    probability: float = 0  # 匹配概率 0-100


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



def classify_match_tier(pet: dict, height_cm: float, weight_g: float) -> tuple[str, float]:
    """
    分层命中判定
    返回: (match_tier, probability)
    
    精准: 身高体重完全在范围内 → 高概率
    容差1: 身高 ±0.01m / 体重 ±0.1kg → 中高概率
    容差2: 身高 ±0.02m / 体重 ±0.2kg → 中概率
    范围: 在原始范围内 → 低概率
    """
    hl, hh = pet['height_low'], pet['height_high']
    wl, wh = pet['weight_low'], pet['weight_high']
    
    # 精准命中: 输入值在记录范围内
    if hl <= height_cm <= hh and wl <= weight_g <= wh:
        # 计算精确度: 越接近中位值概率越高
        h_mid = (hl + hh) / 2
        w_mid = (wl + wh) / 2
        h_range = (hh - hl) / 2 if hh > hl else 1
        w_range = (wh - wl) / 2 if wh > wl else 1
        h_closeness = max(0, 1 - abs(height_cm - h_mid) / h_range)
        w_closeness = max(0, 1 - abs(weight_g - w_mid) / w_range)
        prob = round(60 + (h_closeness + w_closeness) / 2 * 40, 1)
        return "exact", prob
    
    # 容差1: ±0.01m / ±0.1kg
    if (hl - 1 <= height_cm <= hh + 1) and (wl - 100 <= weight_g <= wh + 100):
        # 超出范围的距离
        h_over = max(0, hl - height_cm, height_cm - hh)
        w_over = max(0, wl - weight_g, weight_g - wh)
        prob = round(max(20, 50 - (h_over / 1 * 15 + w_over / 100 * 15)), 1)
        return "tolerance1", prob
    
    # 容差2: ±0.02m / ±0.2kg
    if (hl - 2 <= height_cm <= hh + 2) and (wl - 200 <= weight_g <= wh + 200):
        h_over = max(0, hl - height_cm, height_cm - hh)
        w_over = max(0, wl - weight_g, weight_g - wh)
        prob = round(max(5, 30 - (h_over / 2 * 10 + w_over / 200 * 10)), 1)
        return "tolerance2", prob
    
    return "range", 0


def query_egg(height_m: float, weight_kg: float, egg_filter: Optional[int] = None, 
              include_nearest: bool = True) -> tuple[list[dict], float, dict]:
    """
    查询孵蛋结果（分层命中）
    egg_filter: 0=只神奇的蛋, 1=只炫彩蛋, None=不限
    返回: (结果列表, 用户R值, 分层统计)
    """
    height_cm = height_m * 100
    weight_g = weight_kg * 1000
    user_r = weight_kg / height_m if height_m > 0 else 0
    
    seen = set()
    exact_results = []    # 精准 + 容差命中
    nearest_candidates = []  # 近似候选（都不匹配时的兜底）
    tier_counts = {"exact": 0, "tolerance1": 0, "tolerance2": 0, "range": 0, "nearest": 0}
    
    for pet in PETS:
        precious_type = pet.get('precious_egg_type', 0)
        
        # 蛋类型筛选
        if egg_filter == 0 and precious_type != 0:
            continue
        if egg_filter == 1 and precious_type == 0:
            continue
        
        # 分层命中判定
        match_tier, probability = classify_match_tier(pet, height_cm, weight_g)
        
        # R值 = 中位体重(kg) / 中位身高(m)
        h_mid = (pet['height_low'] + pet['height_high']) / 2 / 100
        w_mid = (pet['weight_low'] + pet['weight_high']) / 2 / 1000
        r_value = w_mid / h_mid if h_mid > 0 else 0
        
        # 去重
        if egg_filter is None or egg_filter == 1:
            key = pet['name']
        else:
            key = f"{pet['name']}_{precious_type}"
        if key in seen:
            continue
        seen.add(key)
        
        egg_type_info = get_egg_type_info(precious_type)
        
        item = {
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
            'match_tier': match_tier,
            'probability': probability,
        }
        
        if match_tier in ("exact", "tolerance1", "tolerance2"):
            exact_results.append(item)
            tier_counts[match_tier] += 1
        else:
            # 计算距离用于近似候选排序
            h_dist = min(abs(height_cm - pet['height_low']), abs(height_cm - pet['height_high']))
            w_dist = min(abs(weight_g - pet['weight_low']), abs(weight_g - pet['weight_high']))
            item['_distance'] = h_dist * 10 + w_dist  # 加权距离
            nearest_candidates.append(item)
    
    # 按概率降序排列精准/容差结果
    exact_results.sort(key=lambda x: (-x['probability'], x['r_diff']))
    
    # 近似候选: 取距离最近的前10个
    if include_nearest and not exact_results:
        nearest_candidates.sort(key=lambda x: x['_distance'])
        for item in nearest_candidates[:10]:
            item['match_tier'] = 'nearest'
            h_mid = (item['height_min'] + item['height_max']) / 2
            w_mid = (item['weight_min'] + item['weight_max']) / 2
            item['probability'] = round(max(1, 10 - item['_distance'] / 100), 1)
            del item['_distance']
            tier_counts['nearest'] += 1
        results = nearest_candidates[:10]
    else:
        # 清理 _distance 字段
        for item in nearest_candidates:
            item.pop('_distance', None)
        results = exact_results
    
    return results, round(user_r, 2), tier_counts


# ========== API 路由 ==========

@app.get("/", response_model=HealthResponse)
async def health_check():
    """健康检查"""
    return HealthResponse(
        status="ok",
        total_pets=len(PETS),
        version="1.0.0"
    )


@app.get("/api/query")
async def query_egg_get(
    height: float = Query(..., description="身高 (米), 如 0.24"),
    weight: float = Query(..., description="体重 (千克), 如 1.60"),
    precious: Optional[int] = Query(None, description="蛋类型筛选: 0=神奇的蛋, 1=炫彩蛋, 不传=不限"),
):
    """
    GET 方式查询孵蛋结果（分层命中）
    precious: 0=神奇的蛋(precious_egg_type=0), 1=炫彩蛋(precious_egg_type>0), 不传=不限
    
    返回结果含 match_tier 字段:
    - exact: 精准命中 (probability 60-100)
    - tolerance1: 容差命中1 (身高±0.01m/体重±0.1kg, probability 20-50)
    - tolerance2: 容差命中2 (身高±0.02m/体重±0.2kg, probability 5-30)
    - nearest: 近似候选 (无精确匹配时的兜底)
    """
    if height <= 0 or weight <= 0:
        raise HTTPException(status_code=400, detail="身高和体重必须大于0")
    
    results, user_r, tier_counts = query_egg(height, weight, precious)
    normal = [r for r in results if not r['is_precious']]
    precious_list = [r for r in results if r['is_precious']]
    
    return {
        "success": True,
        "query": {"height": height, "weight": weight, "egg_filter": precious},
        "total": len(results),
        "normal_count": len(normal),
        "precious_count": len(precious_list),
        "user_r": user_r,
        "tier_counts": tier_counts,
        "results": results,
    }


@app.post("/api/query")
async def query_egg_post(req: EggQueryRequest):
    """
    POST 方式查询孵蛋结果（分层命中）
    """
    if req.height <= 0 or req.weight <= 0:
        raise HTTPException(status_code=400, detail="身高和体重必须大于0")
    
    results, user_r, tier_counts = query_egg(req.height, req.weight, req.egg_filter)
    normal = [r for r in results if not r['is_precious']]
    precious_list = [r for r in results if r['is_precious']]
    
    return {
        "success": True,
        "query": {"height": req.height, "weight": req.weight, "egg_filter": req.egg_filter},
        "total": len(results),
        "normal_count": len(normal),
        "precious_count": len(precious_list),
        "user_r": user_r,
        "tier_counts": tier_counts,
        "results": results,
    }


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
            "egg_groups": len(EGG_GROUPS),
            "evolution_chains": EVOLUTION_CHAINS.get('count', 0),
        }
    }


# ========== 蛋组 & 繁殖 API ==========

@app.get("/api/egg-group")
async def query_egg_group(
    name: Optional[str] = Query(None, description="精灵名称，查该精灵所属蛋组"),
    group: Optional[str] = Query(None, description="蛋组名称，查该蛋组所有成员"),
):
    """
    蛋组查询
    - 传 name: 返回该精灵的蛋组列表、进化链、是否可繁殖
    - 传 group: 返回该蛋组所有成员
    - 两个都传: 检查该精灵是否属于该蛋组
    """
    if not name and not group:
        raise HTTPException(status_code=400, detail="请至少传入 name 或 group 参数")
    
    # 按蛋组名查成员
    if group and not name:
        if group not in EGG_GROUPS:
            return {"success": False, "message": f"蛋组 '{group}' 不存在", "available_groups": list(EGG_GROUPS.keys())}
        members = EGG_GROUPS[group]
        return {
            "success": True,
            "group": group,
            "member_count": len(members),
            "members": [
                {
                    "name": m,
                    "groups": PET_TO_GROUPS.get(m, []),
                    "evolution_chain": PET_TO_CHAIN.get(m, [m]),
                    "can_breed": m not in NO_BREED_PETS,
                }
                for m in members
            ]
        }
    
    # 按精灵名查蛋组
    if name and not group:
        if name not in PET_TO_GROUPS:
            # 模糊搜索
            fuzzy = [n for n in PET_TO_GROUPS if name in n]
            if not fuzzy:
                return {"success": False, "message": f"精灵 '{name}' 未找到蛋组信息", "suggestion": "请检查名称是否正确"}
            return {"success": False, "message": f"未精确匹配 '{name}'", "fuzzy_matches": fuzzy[:10]}
        
        return {
            "success": True,
            "pet": name,
            "groups": PET_TO_GROUPS[name],
            "evolution_chain": PET_TO_CHAIN.get(name, [name]),
            "can_breed": name not in NO_BREED_PETS,
        }
    
    # name + group: 检查归属
    if name and group:
        in_group = name in EGG_GROUPS.get(group, [])
        return {
            "success": True,
            "pet": name,
            "group": group,
            "belongs": in_group,
            "groups": PET_TO_GROUPS.get(name, []),
        }


@app.get("/api/breeding")
async def query_breeding(
    target: str = Query(..., description="目标精灵名称（母系）"),
):
    """
    繁殖匹配查询
    输入目标精灵（母系），返回所有可配对的父系候选
    规则：需要同蛋组精灵，且一公一母；孵化出来的为母系精灵
    """
    if target not in PET_TO_GROUPS:
        fuzzy = [n for n in PET_TO_GROUPS if target in n]
        if fuzzy:
            return {"success": False, "message": f"未精确匹配 '{target}'", "fuzzy_matches": fuzzy[:10]}
        return {"success": False, "message": f"精灵 '{target}' 未找到"}
    
    if target in NO_BREED_PETS:
        return {
            "success": True,
            "target": target,
            "can_breed": False,
            "message": f"{target} 不可繁殖",
            "fathers": []
        }
    
    my_groups = PET_TO_GROUPS[target]
    my_chain = PET_TO_CHAIN.get(target, [target])
    
    # Find all potential fathers (same egg group, different pet)
    fathers = set()
    for g in my_groups:
        for member in EGG_GROUPS.get(g, []):
            if member != target:
                fathers.add(member)
    
    father_list = []
    for f in sorted(fathers):
        f_groups = PET_TO_GROUPS.get(f, [])
        f_chain = PET_TO_CHAIN.get(f, [f])
        shared_groups = set(my_groups) & set(f_groups)
        same_chain = bool(set(my_chain) & set(f_chain))
        father_list.append({
            "name": f,
            "shared_groups": sorted(shared_groups),
            "evolution_chain": f_chain,
            "same_evolution_chain": same_chain,
            "can_breed": f not in NO_BREED_PETS,
        })
    
    # Sort: same evolution chain first, then by name
    father_list.sort(key=lambda x: (not x["same_evolution_chain"], x["name"]))
    
    return {
        "success": True,
        "target": target,
        "can_breed": True,
        "target_groups": my_groups,
        "target_evolution_chain": my_chain,
        "father_count": len(father_list),
        "fathers": father_list,
    }


@app.get("/api/groups")
async def list_groups():
    """列出所有蛋组"""
    return {
        "success": True,
        "group_count": len(EGG_GROUPS),
        "groups": [
            {"name": name, "member_count": len(members)}
            for name, members in sorted(EGG_GROUPS.items())
        ]
    }


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
