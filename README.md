# 洛克王国：世界 - 游戏工具套件

洛克王国世界游戏工具套件，提供孵蛋查询、精灵图鉴、蛋组配对、家园炼金、远行商人等功能。

在线体验：[http://175.178.176.174:2026](http://175.178.176.174:2026)

## 功能一览

| 功能 | 路由 | 说明 |
|------|------|------|
| 🥚 孵蛋查询 | `/egg-query` | 输入身高体重，查询可能孵化的精灵（R值排序） |
| 📖 精灵图鉴 | `/compendium` | 468只精灵数据，属性/蛋组筛选，详情页含技能列表 |
| 🎯 蛋组配对 | `/egg-group` | 查看各蛋组可繁殖精灵，同组可互相配对 |
| 🏡 家园炼金 | `/garden` | 种花、做饭、炼球最优方案推荐 |
| 🛒 远行商人 | `/merchant` | 查看当期轮次商品，倒计时，图标本地匹配 |
| 🔮 属性克制 | `/compendium/:id` | 精灵详情页附带属性克制环 |

## 技术栈

- **后端**: Python FastAPI + uvicorn
- **前端**: Vue 3 + Vite (SCSSless SPA) + 旧版静态 HTML
- **数据源**: 
  - 社区开源数据 (github.com/jiluoQAQ/RocomUID)
  - WeGame API (远行商人)
  - BWiki 道具/技能图标
- **部署**: 175.178.176.174:2026

## 快速开始

```bash
pip install -r requirements.txt
cd frontend && npm install && npx vite build && cd ..
python3 main.py
```

默认监听 `0.0.0.0:2026`。

## 设计规范

详见 [DESIGN.md](./DESIGN.md) — 浅色渐变主题，紫蓝主色调 #667eea/#8b3dff，18px 圆角，统一卡片风格。

## 前端架构

详见 [FRONTEND.md](./FRONTEND.md) — Vue 3 SPA + 旧版静态 HTML 混合架构。

## 项目结构

```
├── main.py              # FastAPI 入口 + 路由注册
├── models.py            # Pydantic 模型
├── api/                 # REST API 路由
│   ├── query.py         #   孵蛋查询
│   ├── spirits.py       #   精灵图鉴/技能
│   ├── pets.py          #   宠物数据
│   ├── stats.py         #   统计数据
│   ├── garden.py        #   家园炼金
│   └── merchant.py      #   远行商人
├── services/            # 业务逻辑
│   ├── breeding.py      #   孵蛋计算
│   ├── data_source.py   #   数据加载
│   ├── image.py         #   图片匹配
│   └── merchant.py      #   远行商人(WeGame API)
├── data/                # JSON 数据文件（本地生成，不入库）
├── static/              # 前端构建产物 + 静态资源
│   ├── index.html       #   旧版孵蛋查询首页
│   ├── item-icons/      #   道具图标（本地托管）
│   ├── skill-icons/     #   技能图标（本地托管）
│   ├── creature-atlas/  #   精灵图片（本地托管）
│   ├── garden-icons/    #   家园图标
│   └── assets/          #   Vue 构建产物
├── frontend/            # Vue 3 源码
│   └── src/views/       #   页面组件
└── FRONTEND.md          # 前端架构文档
```

## 数据来源

- [jiluoQAQ/RocomUID](https://github.com/jiluoQAQ/RocomUID) — 基础孵蛋数据
- [AofeiLi-code/rocom-data](https://github.com/AofeiLi-code/rocom-data) — 技能/属性克制数据
- [BWiki 洛克王国世界](https://wiki.biligame.com/rocom/) — 道具/技能图标
- WeGame 开放平台 API — 远行商人实时数据

## 许可证

MIT
