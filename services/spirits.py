#!/usr/bin/env python3
"""图鉴数据加载"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
SPIRITS_FILE = DATA_DIR / "spirits.json"
OFFICIAL_EGG_GROUPS_FILE = DATA_DIR / "official_egg_groups.json"


def load_spirits_data() -> tuple[list, dict, dict]:
    """加载图鉴数据，返回 (列表, 按ID索引, 按名字索引)"""
    if not SPIRITS_FILE.exists():
        print(f"⚠️ 图鉴数据不存在: {SPIRITS_FILE}")
        return [], {}, {}

    with open(SPIRITS_FILE, 'r', encoding='utf-8') as f:
        spirits = json.load(f)

    by_id = {s['spirit_id']: s for s in spirits}

    by_name = {}
    for s in spirits:
        name = s['base_name']
        if name not in by_name or s.get('form_name') is None:
            by_name[name] = s

    print(f"✅ 已加载 {len(spirits)} 只精灵图鉴数据")
    return spirits, by_id, by_name


def load_official_egg_groups() -> list[dict]:
    """加载官方蛋组数据"""
    if not OFFICIAL_EGG_GROUPS_FILE.exists():
        return []
    with open(OFFICIAL_EGG_GROUPS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


SPIRITS, SPIRITS_BY_ID, SPIRITS_BY_NAME = load_spirits_data()
OFFICIAL_EGG_GROUPS = load_official_egg_groups()
