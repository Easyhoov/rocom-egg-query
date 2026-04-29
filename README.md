# 洛克王国：世界 - 游戏工具套件

> 基于社区开源数据 + WeGame API 的洛克王国世界游戏工具箱，提供孵蛋查询、精灵图鉴、家园炼金、远行商人等一站式查询服务。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 为什么需要这个

洛克王国世界游戏内有大量隐藏数据和实时变化的活动信息——孵蛋需要查身高体重表、炼金需要翻配方、远行商人每 4 小时换一轮商品还要记住哪个道具长什么样。这个项目把这些分散的数据汇集到一个界面，不用切后台翻文档。

## 快速开始

```bash
pip install -r requirements.txt
cd frontend && npm install && npx vite build && cd ..
python3 main.py
```

服务默认启动在 `http://0.0.0.0:2026`。

## 功能

### 🥚 孵蛋查询

输入身高体重，查询可能孵化的精灵。数据基于社区整理的 1623 条孵蛋记录，按 R 值排序展示。

- 路由：`/egg-query`（Vue SPA）/ `/`（旧版静态 HTML）
- API：`POST /api/query` → 接收 `{height, weight}`，返回匹配精灵列表
- 来源：开源数据（jiluoQAQ/RocomUID）

### 📖 精灵图鉴

468 只精灵的完整数据，支持属性筛选、蛋组筛选、名称搜索。详情页包含技能列表（按类型分组，带威力/耗能/效果说明）和属性克制环。

- 路由：`/compendium` / `/compendium/:id`
- API：`GET /api/spirits/{id}` → 精灵详情 + 技能列表
- API：`GET /api/type-matchups` → 属性克制关系
- 来源：AofeiLi-code/rocom-data（488 技能导入）

### 🎯 蛋组配对

查看各蛋组包含的可繁殖精灵列表，同组精灵可以互相配对孵化。

- 路由：`/egg-group`
- API：`GET /api/pets/egg_groups` → 蛋组列表
- 来源：基于孵蛋数据自动聚合

### 🏡 家园炼金

种花、做饭、炼球的最优方案推荐。包含 24 种子、24 配方、9 精灵球、10 材料、10 食物的完整配方数据。

- 路由：`/garden`
- API：`GET /api/garden/recipes` → 配方列表
- API：`GET /api/garden/seeds` → 种子列表
- 来源：游戏内数据整理

### 🛒 远行商人

实时查看远行商人当前轮次的商品，自动展示倒计时和营业状态。道具图标优先使用本地托管图片，本地缺失时通过模糊匹配（最长公共子串）自动关联图片。

- 路由：`/merchant`
- API：`GET /api/merchant/info` → 当前商品 + 轮次信息
- 来源：WeGame API（每 4 小时轮询 + 30 分钟缓存）
- 营业时间：每天 08:00–24:00，每 4 小时一轮

## 安装

### 前置条件

- Python 3.10+
- Node.js 18+
- （可选）WeGame API Key——不设置时使用内置测试 Key，商品数据有限

### 步骤

```bash
# 克隆
git clone https://github.com/Easyhoov/rocom-egg-query.git
cd rocom-egg-query

# 后端依赖
pip install -r requirements.txt

# 前端构建
cd frontend
npm install
npx vite build
cd ..

# 启动
python3 main.py
```

> **提示**：如需远行商人功能，设置环境变量 `WEGAME_API_KEY=你的Key`。首次启动会自动预取数据。

## 项目结构

```
├── main.py                  # FastAPI 入口 + 路由注册 + 生命周期
├── models.py                # Pydantic 模型（请求/响应 schema）
│
├── api/                     # REST API 路由
│   ├── query.py             #   孵蛋查询 POST /api/query
│   ├── spirits.py           #   精灵图鉴 + 技能 GET /api/spirits/{id}
│   ├── pets.py              #   宠物/蛋组数据 GET /api/pets/egg_groups
│   ├── stats.py             #   统计数据
│   ├── garden.py            #   家园炼金 GET /api/garden/recipes
│   └── merchant.py          #   远行商人 GET /api/merchant/info
│
├── services/                # 业务逻辑层
│   ├── breeding.py          #   孵蛋计算引擎
│   ├── data_source.py       #   社区数据加载
│   ├── image.py             #   图片匹配器（Spirit 图片缓存）
│   └── merchant.py          #   WeGame API 调用 + 缓存 + 图标匹配
│
├── frontend/src/            # Vue 3 源码
│   └── views/
│       ├── Home.vue         #   首页（功能入口卡片）
│       ├── EggQuery.vue     #   孵蛋查询
│       ├── CompendiumPage.vue # 精灵图鉴列表
│       ├── SpiritDetail.vue #   精灵详情（技能 + 克制环）
│       ├── EggGroup.vue     #   蛋组配对
│       ├── Garden.vue       #   家园炼金
│       └── Merchant.vue     #   远行商人
│
├── static/                  # 前端构建产物 + 静态资源
│   ├── index.html           #   旧版孵蛋查询首页（纯 HTML）
│   └── assets/              #   Vue 构建产物
│
├── data/                    # JSON 数据（本地生成，不入版本库）
├── FRONTEND.md              # 前端架构说明
└── DESIGN.md                # 设计规范文档
```

## API 参考

### 公共端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/health` | GET | 健康检查 |
| `/api/test` | GET | 路由连通性测试 |
| `/api/refresh-image-cache` | GET | 刷新图片匹配缓存 |

### 孵蛋查询

```
POST /api/query
Content-Type: application/json

{
  "height": 1.0,      # 身高（米）
  "weight": 24.0      # 体重（千克）
}
```

**响应**：按 R 值排序的匹配精灵列表，包含名称、蛋组、最小/最大身高体重、精灵图标 URL。

### 精灵图鉴

```
GET /api/spirits
GET /api/spirits/{id}
GET /api/spirits/{id}/skills    # 技能列表（带图标 URL）
GET /api/type-matchups          # 属性克制关系
```

**查询参数**（`/api/spirits`）：`type`（属性过滤）、`egg_group`（蛋组过滤）、`search`（名称搜索）

**响应示例**（`/api/spirits/{id}/skills`）：
```json
{
  "success": true,
  "spirit_id": "1",
  "skills": [
    { "name": "抓", "type": "普通", "power": 40, "pp": 35, "effect": "",
      "icon_url": "/skill-icons/1.png" }
  ]
}
```

### 家园炼金

```
GET /api/garden/recipes     # 全部配方
GET /api/garden/seeds       # 全部种子
GET /api/garden/materials   # 全部材料
GET /api/garden/foods       # 全部食物
GET /api/garden/balls       # 全部精灵球
```

### 远行商人

```
GET /api/merchant/info
GET /api/merchant/info?refresh=true    # 强制刷新缓存
```

**响应示例**：
```json
{
  "success": true,
  "merchant": {
    "round": {
      "current": 2,
      "total": 4,
      "is_open": true,
      "countdown": "3小时45分钟",
      "round_id": "2026-04-29-2"
    },
    "goods": [
      { "name": "恶系血脉秘药", "icon": "/item-icons/恶系血脉秘药.png",
        "time_label": "08:00 ~ 12:00" }
    ],
    "goods_count": 7
  }
}
```

## 设计规范

项目采用浅色渐变主题，详见 [DESIGN.md](./DESIGN.md)。

- **主色调**：`#667eea` / `#8b3dff`（紫蓝）
- **卡片**：白色圆角 18px，阴影 `0 4px 16px rgba(15,16,21,0.08)`
- **背景**：`linear-gradient(180deg, #f0ecff, #ffffff)`
- **远行商人**：暖色调（杏色/金色），独立视觉风格
- **全部静态资源**（图标、精灵图片）本地托管，不依赖外部 CDN

## 数据来源

| 数据 | 来源 | 更新方式 |
|------|------|---------|
| 孵蛋数据 | [jiluoQAQ/RocomUID](https://github.com/jiluoQAQ/RocomUID) | 手动导入 |
| 技能/属性 | [AofeiLi-code/rocom-data](https://github.com/AofeiLi-code/rocom-data) | 手动导入 |
| 道具图标 | [BWiki 洛克王国世界](https://wiki.biligame.com/rocom/) | 批量下载到本地 |
| 技能图标 | BWiki 技能图鉴页 | 批量下载到本地 |
| 远行商人 | WeGame 开放平台 API | 实时轮询（每 4 小时） |
| 天气（早报） | open-meteo.com | 每日定时抓取 |
| 新闻（早报） | [60s.viki.moe](https://60s.viki.moe) | 每日定时抓取 |

## 参与贡献

欢迎提交 Issue 或 Pull Request。代码风格无强制要求，但新功能建议先开 Issue 讨论。

### 本地开发

```bash
# 前端热更新
cd frontend && npm run dev

# 后端服务
python3 main.py

# 前端构建部署
cd frontend && npx vite build && sudo systemctl restart rocom-egg-query
```

## 许可证

MIT © Easyhoov

## 相关项目

- [jiluoQAQ/RocomUID](https://github.com/jiluoQAQ/RocomUID) — 洛克王国世界解包数据 UI
- [AofeiLi-code/rocom-data](https://github.com/AofeiLi-code/rocom-data) — 技能/属性数据
- [Easyhoov/rocom-miniapp](https://github.com/Easyhoov/rocom-miniapp) — 微信小程序版
- [mfskys/rocomegg](https://github.com/mfskys/rocomegg) — 蛋组繁殖匹配工具
- [aoe-top/rocom.aoe.top](https://github.com/aoe-top/rocom.aoe.top) — 游戏数据解包工具箱
