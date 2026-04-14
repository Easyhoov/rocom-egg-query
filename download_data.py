#!/usr/bin/env python3
"""下载孵蛋数据"""

import os
import urllib.request
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

URLS = {
    "breeding.json": "https://raw.githubusercontent.com/jiluoQAQ/RocomUID/main/RocomUID/utils/map/breeding.json",
    "rocom_map.py": "https://raw.githubusercontent.com/jiluoQAQ/RocomUID/main/RocomUID/utils/map/rocom_map.py",
    "name-map.json": "https://raw.githubusercontent.com/jiluoQAQ/RocomUID/main/RocomUID/utils/map/name-map.json",
}

def download_file(url, dest):
    print(f"  下载: {url}")
    urllib.request.urlretrieve(url, dest)
    size = os.path.getsize(dest)
    print(f"  ✅ 已保存: {dest} ({size} bytes)")

if __name__ == '__main__':
    print("📥 下载孵蛋数据...\n")
    
    for filename, url in URLS.items():
        dest = DATA_DIR / filename
        try:
            download_file(url, dest)
        except Exception as e:
            print(f"  ❌ 下载失败: {e}")
    
    # 验证数据
    breeding_file = DATA_DIR / "breeding.json"
    if breeding_file.exists():
        with open(breeding_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"\n✅ 数据验证通过: {len(data['pet_egg_conf'])} 条记录")
    else:
        print("\n❌ 数据文件缺失")
