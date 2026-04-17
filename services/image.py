#!/usr/bin/env python3
"""图片匹配与本地图片索引"""

from pathlib import Path
from typing import Optional

STATIC_DIR = Path(__file__).parent.parent / "static"
ATLAS_DIR = STATIC_DIR / "creature-atlas"

_local_image_cache: dict[int, str] = {}


def _build_image_index():
    """构建本地图片索引"""
    if not ATLAS_DIR.exists():
        return
    by_number: dict[int, list[str]] = {}
    for p in ATLAS_DIR.glob("*.webp"):
        stem = p.stem  # e.g. "001-base", "011-form-02"
        try:
            num = int(stem.split("-")[0])
            by_number.setdefault(num, []).append(stem)
        except ValueError:
            continue

    for num, files in by_number.items():
        base = f"{num:03d}-base"
        if base in files:
            _local_image_cache[num] = f"/creature-atlas/{base}.webp"
        else:
            form01 = [f for f in files if "form-01" in f]
            if form01:
                _local_image_cache[num] = f"/creature-atlas/{form01[0]}.webp"
            else:
                _local_image_cache[num] = f"/creature-atlas/{files[0]}.webp"


_build_image_index()


def get_spirit_image(spirit_no_number: int) -> Optional[str]:
    """获取精灵本地图片路径"""
    return _local_image_cache.get(spirit_no_number)


# ========== Image Matcher (基于缓存的名字→图片映射) ==========

_matcher_instance = None


def get_image_matcher():
    """获取图片匹配器单例"""
    global _matcher_instance
    if _matcher_instance is None:
        from image_matcher_fastapi import get_image_matcher as _load
        _matcher_instance = _load()
    return _matcher_instance
