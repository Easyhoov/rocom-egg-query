#!/usr/bin/env python3
"""
从 BWiki 批量下载技能图标。
每个技能有唯一的图标 URL，跨精灵页面一致。
方法：用 spirit_skills.json 中有数据的精灵，从它们的 BWiki 页面爬技能图标URL，
去重存储到 skills_icons.json（映射 技能名 → URL），
然后下载图片到 static/skill-icons/ 目录。
"""
import json
import os
import re
import sys
import time
import urllib.request
import urllib.parse
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
DATA_DIR = PROJECT_DIR / "data"
STATIC_DIR = PROJECT_DIR / "static"
SKILL_ICONS_DIR = STATIC_DIR / "skill-icons"

# URL 编码映射：精灵名 → BWiki URL 路径
NAME_TO_URL = {
    '迪莫': '迪莫', '喵喵': '喵喵', '喵呜': '喵呜', '魔力猫': '魔力猫',
    '火花': '火花', '焰火': '焰火', '火神': '火神', '水蓝蓝': '水蓝蓝',
    '波波拉': '波波拉', '水灵': '水灵', '板板壳': '板板壳',
    '咔咔壳': '咔咔壳', '水泡壳': '水泡壳',
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

# 已有技能名 → URL 映射持久化文件
ICON_MAP_FILE = DATA_DIR / "skills_icons.json"

def load_existing_icons() -> dict:
    if ICON_MAP_FILE.exists():
        return json.loads(ICON_MAP_FILE.read_text(encoding="utf-8"))
    return {}

def save_icons(icons: dict):
    ICON_MAP_FILE.write_text(json.dumps(icons, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[✓] 保存 {len(icons)} 个图标映射到 {ICON_MAP_FILE.name}")

def download_image(url: str, filename: str) -> bool:
    """下载图片到 skill-icons/ 目录"""
    filepath = SKILL_ICONS_DIR / filename
    if filepath.exists():
        return True  # 已存在
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
        filepath.write_bytes(data)
        return True
    except Exception as e:
        print(f"  [✗] 下载失败 {filename}: {e}")
        return False

def process_spirit(name: str, existing: dict) -> dict:
    """爬取一只精灵的技能图标URL"""
    # URL encode
    encoded = urllib.parse.quote(name)
    url = f"https://wiki.biligame.com/rocom/{encoded}"
    
    new_icons = {}
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8")
        
        # 找到所有技能图标
        # 格式: alt="技能图标 闪光.png", src="https://patchwiki.biligame.com/..."
        pattern = r'<img[^>]*alt="技能图标\s+([^"]+?)\.png"[^>]*src="([^"]+)"'
        matches = re.findall(pattern, html)
        
        # 另一种格式（可能 src 在 alt 前面）
        if not matches:
            pattern2 = r'<img[^>]*src="([^"]+)"[^>]*alt="技能图标\s+([^"]+?)\.png"[^>]*>'
            matches = [(b, a) for a, b in re.findall(pattern2, html)]
        
        for skill_name, src_url in matches:
            if skill_name not in existing and skill_name not in new_icons:
                new_icons[skill_name] = src_url
                print(f"  + {skill_name}")
        
        print(f"  {name}: 新增 {len(new_icons)} 个新技能图标")
    except Exception as e:
        print(f"  [✗] {name} 页面获取失败: {e}")
    
    return new_icons

def main():
    os.makedirs(SKILL_ICONS_DIR, exist_ok=True)
    
    # 加载已有映射
    existing = load_existing_icons()
    print(f"[*] 已有 {len(existing)} 个技能图标映射")
    
    # 加载精灵技能数据，找出哪些精灵技能覆盖最广
    with open(DATA_DIR / "spirit_skills.json") as f:
        spirit_skills = json.load(f)
    with open(DATA_DIR / "spirits.json") as f:
        spirits = json.load(f)
    
    # 创建 spirit_id → 精灵名映射
    id_to_name = {}
    for s in spirits:
        base = s.get("display_name") or s.get("base_name", "")
        # 跳过有form的（鸭吉吉·蓬松的样子这类）
        if not s.get("form_name"):
            id_to_name[s["spirit_id"]] = base
    
    # 按技能覆盖量排序，挑覆盖面最广的
    spirit_coverage = []
    for sid_str, skills in spirit_skills.items():
        sid = int(sid_str)
        if sid in id_to_name:
            new_count = sum(1 for s in skills if s["name"] not in existing)
            spirit_coverage.append((new_count, sid, id_to_name[sid]))
    
    spirit_coverage.sort(reverse=True)
    
    print(f"[*] 有图鉴数据的精灵: {len(spirit_coverage)} 只")
    
    # 只爬前 N 只精灵直到覆盖所有技能
    total_new = 0
    target = len(json.loads((DATA_DIR / "skills_dict.json").read_text()))  # 488
    crawled = 0
    
    for new_count, sid, name in spirit_coverage:
        if len(existing) >= target:
            break
        if new_count == 0:
            continue
        
        print(f"\n[{crawled+1}] {name} (预计新增 ~{new_count} 个)")
        new_icons = process_spirit(name, existing)
        if new_icons:
            existing.update(new_icons)
            total_new += len(new_icons)
            save_icons(existing)
        crawled += 1
        
        # BWiki礼貌间隔
        time.sleep(1.5)
    
    print(f"\n=== 完成 ===")
    print(f"爬取 {crawled} 个精灵页面")
    print(f"共 {len(existing)} 个技能图标映射 (目标 {target})")
    print(f"本次新增 {total_new} 个")
    
    # 第二步：下载所有未下载的图片
    print(f"\n[*] 开始下载图片...")
    downloaded = 0
    failed = 0
    for skill_name, icon_url in existing.items():
        # 用技能名做文件名
        safe_name = skill_name.replace('/', '_').replace('\\', '_').replace('?', '_')
        filename = f"{safe_name}.png"
        if download_image(icon_url, filename):
            downloaded += 1
        else:
            failed += 1
    
    print(f"\n=== 下载完成 ===")
    print(f"成功: {downloaded} | 失败: {failed}")
    print(f"图片位置: {SKILL_ICONS_DIR}")

if __name__ == "__main__":
    main()
