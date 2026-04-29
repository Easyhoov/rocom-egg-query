# 洛克王国：世界 - 游戏工具套件 🥚

基于社区开源数据 + WeGame API 的洛克王国世界游戏工具箱，提供孵蛋查询、精灵图鉴、家园炼金、远行商人等一站式查询服务。

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![Vue](https://img.shields.io/badge/Vue_3-4FC08D?style=flat&logo=vue.js&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- **🥚 孵蛋查询** — 输入身高体重，按 R 值排序展示匹配精灵
- **📖 精灵图鉴** — 468 只精灵数据，属性/蛋组筛选，详情页含技能列表 + 属性克制环
- **🎯 蛋组配对** — 查看各蛋组可繁殖精灵，同组可互配
- **🏡 家园炼金** — 种花、做饭、炼球最优方案推荐
- **🛒 远行商人** — 实时查看当前轮次商品 + 倒计时，图标自动匹配

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+

### Install & Run

```bash
git clone https://github.com/Easyhoov/rocom-egg-query.git
cd rocom-egg-query
pip install -r requirements.txt
cd frontend && npm install && npx vite build && cd ..
python3 main.py
```

Open `http://localhost:2026` in your browser.

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python FastAPI + uvicorn |
| Frontend | Vue 3 + Vite |
| Legacy UI | Static HTML |
| Data | Community-sourced JSON |

## 📁 Project Structure

```
├── main.py                  # FastAPI entry + routing
├── models.py                # Pydantic models
├── api/                     # REST API routes
│   ├── query.py             # Egg query
│   ├── spirits.py           # Spirit compendium + skills
│   ├── pets.py              # Egg group data
│   ├── stats.py             # Statistics
│   ├── garden.py            # Garden alchemy
│   └── merchant.py          # In-game merchant
├── services/                # Business logic
│   ├── breeding.py          # Egg calculation
│   ├── data_source.py       # Data loading
│   ├── image.py             # Image matching
│   └── merchant.py          # Merchant API + cache
├── frontend/src/views/      # Vue 3 pages
└── static/                  # Built frontend
```

## 🎮 Features

### Egg Query

Input height & weight to find matching spirits. Powered by 1623 community-curated records, sorted by R-value.

### Spirit Compendium

Browse 468 spirits with type/egg group filters. Detail page includes skill list (grouped by type, with power/cost/effect) and type matchup chart.

### Egg Group Matching

View breedable spirits per egg group — same-group spirits can pair for breeding.

### Garden Alchemy

Optimal recipes for planting, cooking, and ball crafting. Covers 24 seeds, 24 recipes, 9 balls, 10 materials, 10 foods.

### In-Game Merchant

Real-time merchant round info with countdown and item icons. Icons are auto-matched from local assets (fuzzy matching via longest common substring).

## 🔌 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /api/query` | Egg query by height/weight |
| `GET /api/spirits` | Spirit list (with type/egg group filters) |
| `GET /api/spirits/{id}` | Spirit detail |
| `GET /api/spirits/{id}/skills` | Spirit skills with icons |
| `GET /api/type-matchups` | Type matchup chart |
| `GET /api/pets/egg_groups` | Egg group list |
| `GET /api/garden/recipes` | Garden recipes |
| `GET /api/merchant/info` | Current merchant info |

## 📝 License

MIT

## 🤝 Contributing

PRs welcome! Feel free to open issues for bugs or feature requests.

## 📋 Related Projects

- [jiluoQAQ/RocomUID](https://github.com/jiluoQAQ/RocomUID) — Game data UI
- [AofeiLi-code/rocom-data](https://github.com/AofeiLi-code/rocom-data) — Skills & type data
- [Easyhoov/rocom-miniapp](https://github.com/Easyhoov/rocom-miniapp) — WeChat Mini Program version
