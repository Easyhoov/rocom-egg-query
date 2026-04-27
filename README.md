<div align="center">
  <h1>🥚 洛克王国：世界 · 孵蛋查询</h1>
  <p><b>游戏工具</b> · 按身高体重查询精灵孵蛋 · Vue 3 + FastAPI</p>
  <p>
    <img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT">
    <img src="https://img.shields.io/badge/FastAPI-2.0+-green" alt="FastAPI">
    <img src="https://img.shields.io/badge/Vue-3.5-purple" alt="Vue 3">
    <img src="https://img.shields.io/badge/data-1623条记录-orange" alt="数据量">
  </p>
  <p>
    <a href="#-design-system">设计系统</a> ·
    <a href="#-功能">功能</a> ·
    <a href="#-快速开始">快速开始</a> ·
    <a href="#-api">API</a>
  </p>
  <br>
</div>

---

## 🎨 Design System

参考 **[awesome-claude-design](https://github.com/rohitg00/awesome-claude-design)** 中 **Canva（Playful）** 风格重建。

| 维度 | 规范 |
|------|------|
| **主色** | `#8b3dff`（Canva Purple）|
| **背景** | `linear-gradient(180deg, #f0ecff 0%, #ffffff 100%)` |
| **卡片** | 白色圆角 `18px` · 阴影 `0 4px 16px rgba(15,16,21,0.08)` |
| **hover** | `0 8px 24px rgba(139,61,255,0.12)` 紫色光晕 |
| **按钮** | 纯色 `#8b3dff` · 圆角 `14px` · 禁止渐变 |
| **字体** | 系统字体栈（-apple-system + Noto Sans SC）|
| **布局** | 移动优先 · `max-width: 420px` · 3列精灵网格 |

完整规范见 [`DESIGN.md`](./DESIGN.md) | 飞书云文档：[查看](https://bytedance.feishu.cn/docx/DDsEd1LXzowvKaxx6FWc8y9hngg)

---

## ✨ 功能

- **🥚 孵蛋查询** — 输入身高体重，智能匹配可能孵化的精灵，按 R 值排序
- **📖 精灵图鉴** — 468 只精灵数据，支持名称/属性/蛋组搜索筛选
- **👤 精灵详情** — 六维雷达图、进化链、形态、出没地点
- **🎯 蛋组配对** — 按蛋组查看可繁殖精灵，同组互相配对
- **🌿 家园炼金** — 种花、做饭、炼球最优方案推荐

## 📊 数据

- **1623 条** 孵蛋记录（来自 [jiluoQAQ/RocomUID](https://github.com/jiluoQAQ/RocomUID)）
- **465 张** 精灵图片（来自 [mfskys/rocomegg](https://github.com/mfskys/rocomegg)）
- 18 种属性图标（本地托管，来源 bilibili wiki）

---

## 🚀 快速开始

### 环境要求

- Python 3.9+
- Node.js 18+（前端构建）

### 本地运行

```bash
# 1. 安装后端依赖
pip install -r requirements.txt

# 2. 下载数据
python download_data.py

# 3. 构建前端
cd frontend && npm install && npm run build && cd ..

# 4. 启动服务
python main.py
```

访问 `http://localhost:2026`

---

## 📡 API

| 端点 | 说明 |
|------|------|
| `GET /` | Vue SPA 入口 |
| `GET /api/query?height=0.24&weight=1.60` | 孵蛋查询 |
| `GET /api/spirits?q=&attribute=&egg_group=&page=1&page_size=24` | 精灵列表/搜索 |
| `GET /api/spirits/{id}` | 精灵详情 |
| `GET /api/official-egg-groups` | 官方蛋组列表 |
| `GET /api/garden/query?level=16&target_ball=` | 家园炼金查询 |
| `GET /api/garden/balls` | 可炼制精灵球列表 |
| `GET /api/stats` | 统计数据 |
| `GET /docs` | API 文档（Swagger） |

---

## 🏗 项目结构

```
rocom-egg-query/
├── main.py                    # FastAPI 后端入口
├── DESIGN.md                  # 设计规范文档
├── api/                       # API 路由模块
│   ├── __init__.py
│   ├── query.py               # 孵蛋查询
│   ├── spirits.py             # 精灵列表/详情
│   └── garden.py              # 家园炼金
├── services/                  # 业务逻辑层
├── models/                    # 数据模型
├── data/                      # JSON 数据文件
├── frontend/                  # Vue 3 前端
│   └── src/
│       ├── App.vue            # 根组件（含全局 reset）
│       ├── views/             # 6 个页面组件
│       ├── router/            # 路由配置
│       └── utils/             # 工具函数
└── static/                    # 构建产物 + 静态资源
    ├── creature-atlas/        # 精灵图片（465张）
    ├── attr-icons/            # 属性图标（18个）
    └── garden-icons/          # 炼金图标
```

---

## 🧩 页面一览

| 路由 | 页面 | 组件 |
|------|------|------|
| `/` | 首页（功能入口） | `Home.vue` |
| `/egg-query` | 孵蛋查询 | `EggQuery.vue` |
| `/compendium` | 精灵图鉴 | `CompendiumPage.vue` |
| `/compendium/:id` | 精灵详情 | `SpiritDetail.vue` |
| `/egg-group` | 蛋组配对 | `EggGroup.vue` |
| `/garden` | 家园炼金 | `Garden.vue` |

---

## 📄 许可证

MIT License

---

<div align="center">
  <sub>数据来源 · <a href="https://github.com/jiluoQAQ/RocomUID">RocomUID</a> · 洛克王国：世界</sub>
  <br>
  <sub>Built with ❤️ for the Rocom community</sub>
</div>
