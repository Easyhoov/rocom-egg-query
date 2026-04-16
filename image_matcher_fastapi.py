#!/usr/bin/env python3
"""
洛克王国孵蛋查询工具 - 后端图片匹配模块
可直接集成到FastAPI应用中
"""

import requests
import json
import re
from typing import Dict, Optional, Tuple, List
from pathlib import Path
from functools import lru_cache


class ImageMatcher:
    """图片匹配器（单例模式）"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        
        # rocomegg数据源
        self.rocomegg_url = "https://raw.githubusercontent.com/mfskys/rocomegg/main/public/data/creatures-master-list.json"
        
        # 映射表
        self.name_to_id: Dict[str, str] = {}
        self.id_to_images: Dict[str, dict] = {}
        
        # 加载数据
        self._load_data()
    
    def _load_data(self):
        """加载rocomegg数据"""
        try:
            # 尝试从本地缓存加载
            cache_file = Path(__file__).parent / "rocomegg_cache.json"
            if cache_file.exists():
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                self.name_to_id = cache_data.get('name_to_id', {})
                self.id_to_images = cache_data.get('id_to_images', {})
                print(f"[ImageMatcher] 从缓存加载: {len(self.name_to_id)} 个映射")
            else:
                # 从远程获取
                self._fetch_remote_data()
                # 保存缓存
                self._save_cache()
        except Exception as e:
            print(f"[ImageMatcher] 加载数据失败: {e}")
            # 使用空数据
            self.name_to_id = {}
            self.id_to_images = {}
    
    def _fetch_remote_data(self):
        """从远程获取数据"""
        print(f"[ImageMatcher] 正在获取rocomegg数据...")
        resp = requests.get(self.rocomegg_url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        creatures = data.get('creatures', [])
        for creature in creatures:
            creature_id = creature.get('id')
            creature_name = creature.get('name')
            images = creature.get('images', {})
            
            if creature_id and creature_name:
                self.name_to_id[creature_name] = creature_id
                self.id_to_images[creature_id] = images
        
        print(f"[ImageMatcher] 获取完成: {len(self.name_to_id)} 个映射")
    
    def _save_cache(self):
        """保存缓存"""
        try:
            cache_file = Path(__file__).parent / "rocomegg_cache.json"
            cache_data = {
                'name_to_id': self.name_to_id,
                'id_to_images': self.id_to_images
            }
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            print(f"[ImageMatcher] 缓存已保存")
        except Exception as e:
            print(f"[ImageMatcher] 保存缓存失败: {e}")
    
    def refresh_cache(self):
        """刷新缓存（手动调用）"""
        self._fetch_remote_data()
        self._save_cache()
    
    def _extract_base_name(self, name: str) -> str:
        """提取基础名称"""
        # 去掉括号内容
        base_name = re.sub(r'（.*?）', '', name)
        base_name = re.sub(r'\(.*?\)', '', base_name)
        
        # 去掉特殊前缀
        prefixes = ['异色', '首领', '闪光']
        for prefix in prefixes:
            if base_name.startswith(prefix):
                base_name = base_name[len(prefix):]
        
        return base_name.strip()
    
    @lru_cache(maxsize=1024)
    def match(self, name: str) -> Optional[str]:
        """
        匹配精灵名称，返回图片路径
        返回格式: /creature-atlas/{id}-base.webp 或 None
        """
        if not name:
            return None
        
        # 1. 精确匹配
        creature_id = self.name_to_id.get(name)
        
        # 2. 模糊匹配
        if not creature_id:
            base_name = self._extract_base_name(name)
            if base_name and base_name != name:
                creature_id = self.name_to_id.get(base_name)
        
        if not creature_id:
            return None
        
        # 获取图片路径
        images = self.id_to_images.get(creature_id, {})
        
        # 优先使用base图片（且不为空）
        if images.get('base'):
            return f"/creature-atlas/{images['base']}"
        
        # 回退到default
        if images.get('default'):
            return f"/creature-atlas/{images['default']}"
        
        # 如果有forms，使用第一个form
        forms = images.get('forms', {})
        if forms:
            first_form = next(iter(forms.values()))
            if first_form:
                return f"/creature-atlas/{first_form}"
        
        # 构造默认路径
        return f"/creature-atlas/{creature_id}-base.webp"
    
    def enrich_pet(self, pet: dict) -> dict:
        """
        丰富精灵数据，补充图片路径
        如果已有image字段且非空，则跳过
        """
        if not pet.get('image'):
            image_path = self.match(pet.get('name', ''))
            if image_path:
                pet['image'] = image_path
        return pet
    
    def enrich_pets(self, pets: List[dict]) -> List[dict]:
        """批量丰富精灵数据"""
        return [self.enrich_pet(pet) for pet in pets]


# 全局实例
_image_matcher = None


def get_image_matcher() -> ImageMatcher:
    """获取图片匹配器实例"""
    global _image_matcher
    if _image_matcher is None:
        _image_matcher = ImageMatcher()
    return _image_matcher


# FastAPI集成示例
def integrate_with_fastapi(app):
    """
    集成到FastAPI应用
    示例用法:
    
    from image_matcher_fastapi import integrate_with_fastapi, get_image_matcher
    
    # 在应用启动时
    integrate_with_fastapi(app)
    
    # 在API端点中使用
    @app.get("/api/query")
    async def query(height: float, weight: float):
        results = [...]  # 查询结果
        matcher = get_image_matcher()
        enriched_results = matcher.enrich_pets(results)
        return {"results": enriched_results}
    """
    
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


# 独立测试
if __name__ == '__main__':
    matcher = ImageMatcher()
    
    test_names = [
        '喵喵',
        '迪莫（光系血脉）',
        '异色恶魔狼',
        '恶魔叮（完美无暇）',
        '雪豆丁',
        '赤毛鸡仔',
        '黑炎宝宝'
    ]
    
    print("\n匹配测试:")
    for name in test_names:
        image = matcher.match(name)
        if image:
            print(f"  {name} -> {image}")
        else:
            print(f"  {name} -> 未匹配")
