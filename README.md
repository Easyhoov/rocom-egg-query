# 洛克王国：世界 - 孵蛋查询工具

基于 FastAPI + 开源数据的精灵孵蛋查询 API。

## 数据源

- [jiluoQAQ/RocomUID](https://github.com/jiluoQAQ/RocomUID) — breeding.json (1623条记录)

## 功能

- 按身高/体重查询可能孵出的精灵
- 蛋类型筛选（神奇的蛋/炫彩蛋/不限）
- R 值计算（体重/身高）并按差距排序
- 精灵列表分页查询
- 数据统计

## 本地运行

```bash
pip install -r requirements.txt
python download_data.py   # 下载数据
uvicorn main:app --host 0.0.0.0 --port 2026
```

## API 端点

| 端点 | 说明 |
|------|------|
| GET / | 健康检查 |
| GET /api/query?height=0.24&weight=1.60 | 按身高体重查孵蛋结果 |
| POST /api/query | 同上（POST） |
| GET /api/pets?page=1&size=20 | 精灵列表 |
| GET /api/stats | 数据统计 |

## 部署

- 服务器: 175.178.176.174:2026
- 进程管理: 见 deploy 脚本
