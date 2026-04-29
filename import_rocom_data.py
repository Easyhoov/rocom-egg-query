#!/usr/bin/env python3
"""
导入 rocom-data 的技能数据和属性克制关系到 rocom-egg-query 项目。

数据来源: /root/.hermes/projects/rocom-data/data/
  - sprites.csv: 469 只精灵（含技能列表 + 克制关系）
  - skills_all.csv: 488 个技能（含效果描述）
"""
import csv
import json
import re
import os
from pathlib import Path

ROCOM_DATA_DIR = Path("/root/.hermes/projects/rocom-data/data")
TARGET_DIR = Path("/root/.hermes/projects/rocom-egg-query/data")

# ==================== 1. 读取 skills_all.csv ====================
# 技能全量字典: skill_name -> {attribute, type, power, cost, effect}
SKILLS_DICT: dict[str, dict] = {}

with open(ROCOM_DATA_DIR / "skills_all.csv", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row["技能名"].strip()
        if not name:
            continue
        # 解析威力: 数字或0/""
        power_raw = row.get("威力", "0").strip()
        try:
            power = int(power_raw) if power_raw else 0
        except ValueError:
            power = 0
        # 解析耗能
        cost_raw = row.get("耗能", "0").strip()
        try:
            cost = int(cost_raw) if cost_raw else 0
        except ValueError:
            cost = 0

        skill_type_map = {
            "物攻": "物理",
            "魔攻": "魔法",
            "防御": "防御",
            "变化": "状态",
        }
        skill_type = skill_type_map.get(row.get("类型", "").strip(), "状态")

        SKILLS_DICT[name] = {
            "name": name,
            "attribute": row.get("属性", "").strip(),
            "type": skill_type,
            "power": power,
            "cost": cost,
            "effect": row.get("效果描述", "").strip(),
            "source": row.get("数据来源", "").strip(),
        }

print(f"[✓] 读取技能字典: {len(SKILLS_DICT)} 个技能")

# ==================== 2. 读取 sprites.csv ====================
# 构建精灵→技能映射 和 属性克制映射
# 名称匹配策略: sprites.csv 的 name 与 spirits.json 的 base_name 匹配
# 先用 spirit_no_number 做匹配

SPRITE_SKILLS: dict[int, list[str]] = {}  # spirit_no_number -> [skill_name, ...]
SPRITE_MATCHUPS: dict[int, dict] = {}     # spirit_no_number -> {strong_against, weak_to, resists, resisted_by}

with open(ROCOM_DATA_DIR / "sprites.csv", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            no = int(row["no"])
        except ValueError:
            continue

        # 解析技能列表 - skills 字段是分号分隔的
        skills_raw = row.get("skills", "").strip()
        skill_names = []
        if skills_raw:
            for skill_entry in skills_raw.split(";"):
                # 格式: "技能名(属性/类型/威力/耗能/效果描述)"
                skill_name = skill_entry.split("(")[0].strip()
                if skill_name:
                    skill_names.append(skill_name)
        SPRITE_SKILLS[no] = skill_names

        # 解析克制关系
        def parse_type_list(val: str) -> list[str]:
            """解析 '\\"恶,幽\\"' → ['恶', '幽']"""
            # 去掉可能的引号
            val = val.strip().strip('"').strip("'")
            if not val:
                return []
            return [t.strip() for t in val.split(",") if t.strip()]

        SPRITE_MATCHUPS[no] = {
            "strong_against": parse_type_list(row.get("strong_against", "")),
            "weak_to": parse_type_list(row.get("weak_to", "")),
            "resists": parse_type_list(row.get("resists", "")),
            "resisted_by": parse_type_list(row.get("resisted_by", "")),
        }

print(f"[✓] 读取精灵技能映射: {len(SPRITE_SKILLS)} 只")
print(f"[✓] 读取属性克制映射: {len(SPRITE_MATCHUPS)} 只")

# ==================== 3. 匹配到我们的 spirits.json ====================
# 通过 spirit_no_number (NO.xxx) 来关联
with open(TARGET_DIR / "spirits.json", encoding="utf-8") as f:
    spirits: list[dict] = json.load(f)

spirit_no_to_id = {}
for s in spirits:
    no = s["spirit_no_number"]
    spirit_no_to_id[no] = s["spirit_id"]

# ==================== 4. 构建精灵技能关联（合并 skills_all 的详细信息） ====================
SPIRIT_SKILL_DETAILS: dict[int, list] = {}  # spirit_id -> [skill_detail, ...]

for no, skill_names in SPRITE_SKILLS.items():
    spirit_id = spirit_no_to_id.get(no)
    if spirit_id is None:
        # 可能是 rocom-data 有但我们没有的精灵
        continue
    skill_details = []
    for sn in skill_names:
        if sn in SKILLS_DICT:
            skill_details.append(SKILLS_DICT[sn])
        else:
            # 技能不在 skills_all.csv 中，给个基础信息
            skill_details.append({
                "name": sn,
                "attribute": "未知",
                "type": "未知",
                "power": 0,
                "cost": 0,
                "effect": "",
                "source": "",
            })
    SPIRIT_SKILL_DETAILS[spirit_id] = skill_details

print(f"[✓] 构建精灵技能详情: {len(SPIRIT_SKILL_DETAILS)} 只精灵有技能数据")

# 统计
total_skills_mapped = sum(len(v) for v in SPIRIT_SKILL_DETAILS.values())
print(f"    共 {total_skills_mapped} 个技能条目")

# ==================== 5. 构建精灵克制映射 ====================
SPIRIT_MATCHUP_DETAILS: dict[int, dict] = {}  # spirit_id -> matchup

for no, matchup in SPRITE_MATCHUPS.items():
    spirit_id = spirit_no_to_id.get(no)
    if spirit_id is None:
        continue
    SPIRIT_MATCHUP_DETAILS[spirit_id] = matchup

print(f"[✓] 构建精灵克制映射: {len(SPIRIT_MATCHUP_DETAILS)} 只")

# ==================== 6. 导出 ====================
os.makedirs(TARGET_DIR, exist_ok=True)

# 6a. 技能字典
with open(TARGET_DIR / "skills_dict.json", "w", encoding="utf-8") as f:
    json.dump(SKILLS_DICT, f, ensure_ascii=False, indent=2)
print(f"[✓] 导出 skills_dict.json ({len(SKILLS_DICT)} 个技能)")

# 6b. 精灵技能映射（ID -> skill list）
output_skills = {}
for sid in sorted(SPIRIT_SKILL_DETAILS.keys()):
    output_skills[str(sid)] = SPIRIT_SKILL_DETAILS[sid]
with open(TARGET_DIR / "spirit_skills.json", "w", encoding="utf-8") as f:
    json.dump(output_skills, f, ensure_ascii=False, indent=2)
print(f"[✓] 导出 spirit_skills.json ({len(output_skills)} 只精灵)")

# 6c. 精灵克制映射（ID -> matchup）
output_matchups = {}
for sid in sorted(SPIRIT_MATCHUP_DETAILS.keys()):
    output_matchups[str(sid)] = SPIRIT_MATCHUP_DETAILS[sid]
with open(TARGET_DIR / "spirit_matchups.json", "w", encoding="utf-8") as f:
    json.dump(output_matchups, f, ensure_ascii=False, indent=2)
print(f"[✓] 导出 spirit_matchups.json ({len(output_matchups)} 只精灵)")

# ==================== 7. 统计匹配覆盖率 ====================
# 我们的精灵总数
our_total = len(spirits)
# rocom-data 精灵总数
their_total = len(SPRITE_SKILLS)

matched_skills = len(SPIRIT_SKILL_DETAILS)
matched_matchups = len(SPIRIT_MATCHUP_DETAILS)

# 找出没匹配到的
our_nos = set(spirit_no_to_id.keys())
their_nos = set(SPRITE_SKILLS.keys())

only_ours = sorted(our_nos - their_nos)
only_theirs = sorted(their_nos - our_nos)

print("\n=== 匹配统计 ===")
print(f"  我们的精灵: {our_total}")
print(f"  rocom-data 精灵: {their_total}")
print(f"  技能匹配: {matched_skills}/{our_total} ({100*matched_skills/our_total:.1f}%)")
print(f"  克制匹配: {matched_matchups}/{our_total} ({100*matched_matchups/our_total:.1f}%)")
print(f"  我们有但 rocom-data 没有的编号: {len(only_ours)} 个 {only_ours[:10]}{'...' if len(only_ours)>10 else ''}")
print(f"  rocom-data 有但我们没有的编号: {len(only_theirs)} 个 {only_theirs[:10]}{'...' if len(only_theirs)>10 else ''}")
