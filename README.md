# 洛克王国：世界 - 孵蛋查询工具

基于 FastAPI + 开源数据的精灵孵蛋查询 API，支持精灵图片显示。

## 访问地址

**http://your-server-ip:2026/**

## 功能

- ✅ 按身高/体重查询可能孵出的精灵
- ✅ 蛋类型筛选（神奇的蛋/炫彩蛋/不限）
- ✅ R 值计算（体重/身高）并按差距排序
- ✅ **精灵图片显示**（集成 rocomegg 资源）
- ✅ 精灵列表分页查询
- ✅ 数据统计
- ✅ 移动端适配

## 数据源

- [jiluoQAQ/RocomUID](https://github.com/jiluoQAQ/RocomUID) — breeding.json (1623条记录)
- [mfskys/rocomegg](https://github.com/mfskys/rocomegg) — 精灵图片 (465张webp)

## 本地运行

```bash
pip install -r requirements.txt
python download_data.py   # 下载数据
python main.py            # 启动服务
```

## API 端点

| 端点 | 说明 |
|------|------|
| `GET /` | 前端页面 |
| `GET /api/query?height=0.24&weight=1.60` | 按身高体重查孵蛋结果 |
| `POST /api/query` | 同上（POST） |
| `GET /api/pets?page=1&size=20` | 精灵列表 |
| `GET /api/stats` | 数据统计 |
| `GET /creature-atlas/{id}-base.webp` | 精灵图片 |

## 项目结构

```
rocom-egg-query/
├── main.py                    # FastAPI 后端
├── image_matcher_fastapi.py   # 图片匹配模块
├── index.html                 # 前端页面
├── data/
│   └── breeding.json          # 孵蛋数据（1623条）
├── static/
│   └── creature-atlas/        # 精灵图片（465张webp）
└── docs/
    ├── PLAN.md                # 实施方案
    └── PRD.md                 # 产品需求文档
```

## 部署

- 服务器: your-server-ip:2026
- 进程管理: `nohup python3 main.py > server.log 2>&1 &`

## 详细文档

- [实施方案](docs/PLAN.md)
- [产品需求](docs/PRD.md)
