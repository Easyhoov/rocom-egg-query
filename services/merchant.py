"""远行商人 - WeGame API 调用 + 缓存 + 轮次计算"""

import os
import json
import time
import asyncio
import re
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from typing import Optional

CST = timezone(timedelta(hours=8))

# ---------- 本地图标映射 ----------

def _load_item_mapping() -> dict:
    """加载 BWiki 道具图标映射表 (ID → 名称)"""
    mapping_path = os.path.join(os.path.dirname(__file__), "..", "static", "item_mapping.json")
    if os.path.exists(mapping_path):
        with open(mapping_path, encoding="utf-8") as f:
            return json.load(f)
    return {}

# 模块级图标索引缓存，启动时构建一次
_ICON_DIR = os.path.join(os.path.dirname(__file__), "..", "static", "item-icons")
_icon_index: list[str] = []
if os.path.isdir(_ICON_DIR):
    _icon_index = [f for f in os.listdir(_ICON_DIR) if f.endswith(".png")]

def _resolve_icon(icon_url: str, item_name: str) -> str:
    """将商品图标 URL 解析为本地路径"""
    static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
    icons_dir = os.path.join(static_dir, "item-icons")

    # 1) 精确匹配：道具名 + ".png"
    exact_path = os.path.join(icons_dir, f"{item_name}.png")
    if os.path.exists(exact_path):
        return f"/item-icons/{item_name}.png"

    # 2) 模糊匹配：道具名包含某图片名，或图片名包含道具名
    for fname in _icon_index:
        base = os.path.splitext(fname)[0]
        if item_name in base or base in item_name:
            return f"/item-icons/{fname}"

    # 2.5) 宽松匹配：取商品名和图片名的最长公共子串，够长才匹配
    def longest_common_substr(a: str, b: str) -> str:
        """返回 a 和 b 的最长公共子串"""
        m, n = len(a), len(b)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        lcs, end = 0, 0
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if a[i - 1] == b[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                    if dp[i][j] > lcs:
                        lcs = dp[i][j]
                        end = i
        return a[end - lcs:end]

    best_name, best_lcs = None, 0
    for fname in _icon_index:
        base = os.path.splitext(fname)[0]
        lcs = longest_common_substr(item_name, base)
        if len(lcs) > best_lcs and len(lcs) >= 4:
            # 公共子串至少占任一名长度的40%
            if len(lcs) >= len(item_name) * 0.4 and len(lcs) >= len(base) * 0.4:
                best_lcs = len(lcs)
                best_name = fname

    if best_name:
        return f"/item-icons/{best_name}"

    # 3) 从 URL 文件名提取数字 ID (如 100121_xxx.png -> 100121)
    m = re.search(r'/(\d{6,})[_\.]', icon_url)
    if m:
        item_id = m.group(1)
        if os.path.exists(os.path.join(icons_dir, f"{item_id}.png")):
            return f"/item-icons/{item_id}.png"

    # 4) 按名字查映射表
    mapping = _load_item_mapping()
    name_to_id = {v: k for k, v in mapping.items()}
    if item_name in name_to_id:
        item_id = name_to_id[item_name]
        if os.path.exists(os.path.join(icons_dir, f"{item_id}.png")):
            return f"/item-icons/{item_id}.png"

    # 5) 都没有则返回原 URL（兜底）
    return icon_url

WEGAME_API_KEY = os.getenv("WEGAME_API_KEY") or "sk-ff14f964051a5c966564e29b5bd3a768"
WEGAME_BASE_URL = "https://wegame.shallow.ink"

# 缓存
_cache: dict = {"data": None, "timestamp": 0, "lock": asyncio.Lock()}
CACHE_TTL = 1800  # 30 分钟

SHOP_ID = 3019

# ---------- 轮次计算 ----------

def compute_round() -> dict:
    """计算当前轮次信息"""
    now = datetime.now(CST)
    hour = now.hour
    minute = now.minute

    if hour < 8 or hour >= 24:
        return {
            "current": 0,
            "total": 4,
            "is_open": False,
            "countdown": "已打烊",
            "round_id": f"{now.strftime('%Y-%m-%d')}-0",
        }

    slot = (hour - 8) // 4  # 0,1,2,3
    current = slot + 1

    # 计算本轮结束时间
    slot_end_hour = 8 + (slot + 1) * 4
    end_dt = now.replace(hour=slot_end_hour, minute=0, second=0, microsecond=0)
    remaining = int((end_dt - now).total_seconds())

    if remaining <= 0:
        # 刚过整点，算下一轮
        if current < 4:
            current += 1
            slot_end_hour = 8 + current * 4
            end_dt = now.replace(hour=slot_end_hour, minute=0, second=0, microsecond=0)
            remaining = int((end_dt - now).total_seconds())
        else:
            return {
                "current": 4,
                "total": 4,
                "is_open": True,
                "countdown": "即将打烊",
                "round_id": f"{now.strftime('%Y-%m-%d')}-4",
            }

    hours = remaining // 3600
    mins = (remaining % 3600) // 60
    if hours > 0:
        countdown = f"{hours}小时{mins}分钟"
    else:
        countdown = f"{mins}分钟"

    return {
        "current": current,
        "total": 4,
        "is_open": True,
        "countdown": countdown,
        "round_id": f"{now.strftime('%Y-%m-%d')}-{current}",
    }

# ---------- API 调用 ----------

async def _fetch_merchant_data() -> Optional[dict]:
    """调用 WeGame API 获取远行商人数据"""
    url = f"{WEGAME_BASE_URL}/api/v1/games/rocom/merchant/info?refresh=true"
    headers = {
        "X-API-Key": WEGAME_API_KEY,
        "Accept": "application/json",
    }

    def _sync_fetch():
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
                return data
        except Exception as e:
            print(f"[Merchant] API 请求失败: {e}")
            return None

    return await asyncio.to_thread(_sync_fetch)


def _parse_goods(raw: dict) -> list[dict]:
    """解析 API 返回的商品列表"""
    activities = raw.get("data", {}).get("merchantActivities", [])
    if not activities:
        return []

    # 取第一个活动（远行商人）
    act = activities[0]
    props = act.get("get_props", [])

    goods = []
    for p in props:
        name = p.get("name", "")
        icon = p.get("icon_url", "")
        st = p.get("start_time", 0)
        et = p.get("end_time", 0)

        # 格式化时间标签
        st_dt = datetime.fromtimestamp(st / 1000, CST) if st else None
        et_dt = datetime.fromtimestamp(et / 1000, CST) if et else None
        time_label = ""
        if st_dt and et_dt:
            time_label = f"{st_dt.strftime('%H:%M')} ~ {et_dt.strftime('%H:%M')}"

        goods.append({
            "name": name,
            "icon": _resolve_icon(icon, name),
            "start_time": st,
            "end_time": et,
            "time_label": time_label,
        })

    return goods

# ---------- 缓存接口 ----------

async def get_merchant_info(force_refresh: bool = False) -> dict:
    """获取远行商人信息（带缓存）"""
    now = time.time()

    if not force_refresh and _cache["data"] and (now - _cache["timestamp"]) < CACHE_TTL:
        return _cache["data"]

    async with _cache["lock"]:
        # 双重检查
        if not force_refresh and _cache["data"] and (now - _cache["timestamp"]) < CACHE_TTL:
            return _cache["data"]

        raw = await _fetch_merchant_data()
        if raw is None:
            # 有缓存则返回旧数据
            if _cache["data"]:
                return _cache["data"]
            return {"success": False, "error": "获取远行商人数据失败"}

        goods = _parse_goods(raw)
        round_info = compute_round()

        result = {
            "success": True,
            "merchant": {
                "round": round_info,
                "goods": goods,
                "goods_count": len(goods),
            }
        }
        _cache["data"] = result
        _cache["timestamp"] = now
        return result
