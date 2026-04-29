# 洛克王国：世界 - 孵蛋查询

洛克王国世界游戏工具套件，提供孵蛋查询、精灵图鉴、蛋组配对、家园炼金等功能。

## 技术栈

- **后端**: Python FastAPI
- **前端**: Vue 3 + Vite (SCSSless SPA)
- **数据**: 社区开源数据 (github.com/jiluoQAQ/RocomUID)
- **部署**: 175.178.176.174:2026

## 快速开始

```bash
pip install -r requirements.txt
cd frontend && npm install && npx vite build && cd ..
python3 main.py --port 2026
```

## 设计规范

详见 [DESIGN.md](./DESIGN.md) — 浅色渐变主题，紫蓝主色调 #667eea/#8b3dff，18px 圆角，统一卡片风格。

## 前端架构

详见 [FRONTEND.md](./FRONTEND.md) — Vue 3 SPA 架构，路由表，构建说明，维护注意事项。

## 项目结构

```
├── main.py              # FastAPI 入口 + 路由
├── api/                 # REST API 路由
├── services/            # 业务逻辑
├── models.py            # Pydantic 模型
├── data/                # JSON 数据文件
├── static/              # 前端构建产物 + 静态资源
├── frontend/            # Vue 3 源码
└── FRONTEND.md          # 前端架构文档
```
