#!/usr/bin/env python3
"""
从 BWiki 道具图鉴页抓取道具 ID → 名称映射，下载图标到本地

道具图片结构：
  <a href="/rocom/名称" title="名称">
    <img alt="ID.png" src="缩略图URL"></a>
  
道具名在 <a> 的 title 属性中，ID 在 <img> 的 alt 属性中。
"""

import os, re, json, sys, time
import urllib.request, urllib.error

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(SCRIPT_DIR, "static")
ITEM_ICONS_DIR = os.path.join(STATIC_DIR, "item-icons")
MAPPING_FILE = os.path.join(STATIC_DIR, "item_mapping.json")

def ensure_dirs():
    os.makedirs(ITEM_ICONS_DIR, exist_ok=True)

def fetch_page(url: str) -> str:
    """获取页面 HTML"""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")

def parse_items(html: str) -> dict:
    """
    提取 {道具ID: 道具名} 映射
    
    结构:
    <a href="/rocom/道具名" title="道具名">
      <img alt="100002.png" src="..."></a>
    """
    items = {}
    
    # 定位到主内容区域
    main_match = re.search(r'class="mw-parser-output">(.*?)<div\s+class="printfooter"', html, re.DOTALL)
    content = main_match.group(1) if main_match else html
    
    # 找所有 img alt="数字.png" 的标签
    # 正则匹配: <a href="/rocom/名称" title="名称"><img alt="ID.png" src="..."></a>
    pattern = r'<a\s+href="/rocom/[^"]*"\s+title="([^"]+)"[^>]*>\s*<img[^>]*alt="(\d+)\.png"[^>]*src="([^"]+)"[^>]*>'
    matches = re.findall(pattern, content)
    
    for name, item_id, src in matches:
        # 排除特殊道具和背景图
        if item_id not in items:
            items[item_id] = name
    
    # 如果上面的匹配不到，试试更宽松的
    if not items:
        # 找所有 alt="数字.png" 的位置，往前找 title
        pattern2 = r'<a\s+href="(/rocom/[^"]*)"\s+title="([^"]+)"[^>]*>.*?alt="(\d+)\.png"'
        matches2 = re.findall(pattern2, content)
        for href, name, item_id in matches2:
            if '文件' not in href and '物品' not in href and item_id not in items:
                items[item_id] = name
    
    return items

def get_original_image_url(img_src: str) -> str:
    """
    从缩略图URL获取原图URL
    缩略图: .../thumb/.../100px-100002.png
    原图:   .../.../hash.png
    """
    # 如果已经是原图（没有 /thumb/）
    if '/thumb/' not in img_src:
        return img_src
    
    # 对于BWiki缩略图，原图是去掉 /thumb/ 和最后的 /100px-xxx.png
    # 例如: .../thumb/e/e1/hash.png/100px-100002.png
    # 原图: .../e/e1/hash.png
    m = re.match(r'(https?://[^/]+/images/rocom)/thumb(/[^/]+/[^/]+/[^/]+)/\d+px-.+', img_src)
    if m:
        return m.group(1) + m.group(2)
    
    # 兜底
    return img_src

def download_icon(item_id: str, name: str, html: str) -> bool:
    """从页面HTML中提取图片URL并下载"""
    # 找道具图片的 src
    # <a href="/rocom/名称" title="名称">
    #   <img alt="ID.png" src="..."></a>
    pattern = r'alt="' + item_id + r'\.png"[^>]*src="([^"]+)"'
    m = re.search(pattern, html)
    if not m:
        print(f"  [SKIP] {item_id} ({name}): 找不到图片URL")
        return False
    
    thumb_url = m.group(1)
    if thumb_url.startswith('//'):
        thumb_url = 'https:' + thumb_url
    
    # 获取原图
    img_url = get_original_image_url(thumb_url)
    
    local_path = os.path.join(ITEM_ICONS_DIR, f"{item_id}.png")
    if os.path.exists(local_path):
        return True
    
    try:
        req = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
        with open(local_path, 'wb') as f:
            f.write(data)
        print(f"  [OK] {item_id} ({name}) - {len(data)} bytes")
        return True
    except Exception as e:
        # 尝试下载原图失败时，试试缩略图
        try:
            req = urllib.request.Request(thumb_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
            with open(local_path, 'wb') as f:
                f.write(data)
            print(f"  [OK-THUMB] {item_id} ({name}) - {len(data)} bytes (缩略图)")
            return True
        except Exception as e2:
            print(f"  [FAIL] {item_id} ({name}): {e2}")
            return False

def main():
    ensure_dirs()
    
    print("=" * 50)
    print("   抓取 BWiki 道具图标")
    print("=" * 50)
    
    url = "https://wiki.biligame.com/rocom/%E9%81%93%E5%85%B7%E5%9B%BE%E9%89%B4"
    print(f"\n[1/3] 获取页面: {url}")
    html = fetch_page(url)
    print(f"       HTML 大小: {len(html)} bytes")
    
    print(f"\n[2/3] 解析道具 ID → 名称映射")
    items = parse_items(html)
    print(f"       解析到 {len(items)} 个道具")
    
    if not items:
        print("       [ERROR] 没有解析到任何道具，检查页面结构")
        sys.exit(1)
    
    # 排序
    mapping = dict(sorted(items.items(), key=lambda x: int(x[0])))
    
    print(f"\n       映射样本 (前15):")
    for i, (item_id, name) in enumerate(list(mapping.items())[:15]):
        print(f"         {item_id} → {name}")
    print(f"       ... 共 {len(mapping)} 个")
    
    with open(MAPPING_FILE, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    print(f"\n       映射已保存到 {MAPPING_FILE}")
    
    print(f"\n[3/3] 下载图标 ({len(mapping)} 个)")
    existing = len([f for f in os.listdir(ITEM_ICONS_DIR) if f.endswith('.png')])
    
    success = 0
    fail = 0
    for item_id, name in mapping.items():
        if download_icon(item_id, name, html):
            success += 1
        else:
            fail += 1
        time.sleep(0.05)  # 礼貌间隔
    
    print(f"\n{'=' * 50}")
    print(f"   完成: {success} 成功, {fail} 失败")
    print(f"   图标目录: {ITEM_ICONS_DIR} ({len(os.listdir(ITEM_ICONS_DIR))} 文件)")
    print(f"   映射文件: {MAPPING_FILE}")
    print(f"{'=' * 50}")

if __name__ == '__main__':
    main()
