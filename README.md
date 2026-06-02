# 洛克王国：世界 - 游戏工具套件 🥚

基于社区开源数据 + WeGame API 的洛克王国世界游戏工具箱，提供孵蛋查询、精灵图鉴、家园炼金、远行商人等一站式查询服务。

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![Vue](https://img.shields.io/badge/Vue_3-4FC08D?style=flat&logo=vue.js&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ 功能

- **🥚 孵蛋查询** — 输入身高体重，按 R 值排序展示匹配精灵
- **📖 精灵图鉴** — 468 只精灵数据，属性/蛋组筛选，详情页含技能列表 + 属性克制环
- **🎯 蛋组配对** — 查看各蛋组可繁殖精灵，同组可互配
- **🏡 家园炼金** — 种花、做饭、炼球最优方案推荐
- **🛒 远行商人** — 实时查看当前轮次商品 + 倒计时（*暂时下线*）

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+

### 安装运行

```bash
# 克隆仓库
git clone https://github.com/Easyhoov/rocom-egg-query.git
cd rocom-egg-query

# 安装后端依赖
pip install -r requirements.txt

# 构建前端
cd frontend && npm install && npm run build && cd ..

# 启动服务
python3 main.py
```

访问 `http://localhost:2026`

## 🏗️ 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python FastAPI + uvicorn |
| 前端 | Vue 3 + Vite + Vue Router |
| 数据 | JSON 静态文件（无数据库） |
| 主题 | 深色毛玻璃风格（CSS 变量） |

## 📁 项目结构

```
rocom-egg-query/
├── main.py                  # FastAPI 入口 + 路由
├── models.py                # Pydantic 数据模型
├── api/                     # REST API 路由
│   ├── query.py             # 孵蛋查询
│   ├── spirits.py           # 精灵图鉴 + 技能
│   ├── pets.py              # 蛋组数据
│   ├── garden.py            # 家园炼金
│   └── merchant.py          # 远行商人
├── services/                # 业务逻辑
│   ├── breeding.py          # 孵蛋计算引擎
│   ├── spirits.py           # 精灵数据加载
│   ├── image.py             # 图片匹配
│   └── merchant.py          # 商人 API 客户端
├── data/                    # JSON 数据文件
├── frontend/                # Vue 3 前端
│   └── src/
│       ├── views/           # 页面组件
│       ├── components/      # 公共组件（RadarChart/SkillTable 等）
│       ├── composables/     # 组合式函数（useApi）
│       └── styles/          # 主题样式（CSS 变量）
└── static/                  # 静态资源 + 构建产物
```

## 🎨 页面

| 页面 | 路由 | 功能 |
|------|------|------|
| 首页 | `/` | 工具箱入口 |
| 孵蛋查询 | `/egg-query` | 身高体重 → 孵化结果 |
| 精灵图鉴 | `/compendium` | 精灵列表 + 详情 |
| 蛋组配对 | `/egg-group` | 蛋组兼容查询 |
| 家园炼金 | `/garden` | 等级 → 最优配方 |
| 远行商人 | `/merchant` | 商人刷新信息（*暂时下线*） |

## 🔌 API 端点

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/api/query` | 孵蛋查询 |
| GET | `/api/spirits` | 精灵列表 |
| GET | `/api/spirits/{id}` | 精灵详情 |
| GET | `/api/spirits/{id}/skills` | 精灵技能 |
| GET | `/api/type-matchups` | 属性克制表 |
| GET | `/api/pets/egg_groups` | 蛋组列表 |
| GET | `/api/garden/query` | 家园炼金 |
| GET | `/api/garden/balls` | 球列表 |
| GET | `/api/merchant/info` | 远行商人 |
| GET | `/api/health` | 健康检查 |

## 🎯 架构特点
- **组件化前端** — Vue 3 Composition API + 可复用组件 + composables
- **单端口部署** — 2026 端口同时提供 API 和前端页面
- **SPA 架构** — Vue Router 客户端渲染，页面切换无刷新
- **无数据库** — JSON 静态文件存储，启动时加载到内存
- **图标本地化** — CDN URL 自动替换为本地路径
- **深色主题** — 统一 CSS 变量，毛玻璃卡片风格

## 📊 数据来源

| 数据 | 来源 |
|------|------|
| 孵蛋数据 | 社区开源数据（jiluoQAQ/RocomUID） |
| 精灵图鉴 | 社区开源数据（AofeiLi-code/rocom-data） |
| 远行商人 | WeGame API（测试 key 来自 astrbot_plugin_rocom） |

## 📝 License

MIT

## 🤝 贡献

欢迎 PR！如有 bug 或建议请提 issue。

## 📋 相关项目

- [jiluoQAQ/RocomUID](https://github.com/jiluoQAQ/RocomUID) — 游戏数据 UI
- [AofeiLi-code/rocom-data](https://github.com/AofeiLi-code/rocom-data) — 技能 & 属性数据
- [Entropy-Increase-Team/astrbot_plugin_rocom](https://github.com/Entropy-Increase-Team/astrbot_plugin_rocom) — 洛克王国数据查询插件（本项目 WeGame API 测试 key 来源）
