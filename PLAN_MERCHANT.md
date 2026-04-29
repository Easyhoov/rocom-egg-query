# 远行商人功能 实施方案

> **用于 Hermes：** 确认方案后按任务逐条实施。

**目标：** 在 rocom-egg-query 项目中新增远行商人功能，实时展示 WeGame API 返回的当前轮次商品。

**架构：** 后端新增 merchant API 路由 + 定时缓存服务 → Vue 前端新增 merchant 页面。

**前置条件：** WeGame API Key（测试 Key `sk-ff14f964051a5c966564e29b5bd3a768` 当前可用）

**Tech Stack：** httpx（API 请求）、FastAPI lifespan（定时刷新）、Vue 3 页面

---

## 整体设计

```
用户访问 /merchant
    ↓
Vue 页面请求 /api/merchant/info
    ↓
FastAPI 返回缓存数据（每 4 小时轮询 WeGame API）
    ↓
Vue 渲染商品卡片 + 轮次信息 + 倒计时
```

### 后端（FastAPI）

| 文件 | 用途 |
|------|------|
| `services/merchant.py` | WeGame API 调用 + 缓存 + 轮次计算 |
| `api/merchant.py` | REST API 路由 `/api/merchant/info` |
| `main.py` | 注册路由 + lifespan 启动定时刷新 |

### 前端（Vue）

| 文件 | 用途 |
|------|------|
| `frontend/src/views/Merchant.vue` | 远行商人页面 |
| `frontend/src/router/index.js` | 添加 `/merchant` 路由 |

### API 响应格式

```json
{
  "success": true,
  "merchant": {
    "round": { "current": 2, "total": 4, "id": "2026-04-29-2", "is_open": true },
    "countdown": "3小时45分钟",
    "goods": [
      { "name": "恶系血脉秘药", "icon": "https://...", "start_time": "...", "end_time": "..." },
      ...
    ]
  }
}
```

---

## 任务清单

### 任务 1：创建 merchant 后端服务

**文件：** 新建 `services/merchant.py`

核心逻辑：
- `fetch_merchant_goods()` — 调用 WeGame API（携带 API Key），解析 merchantActivities.get_props 为商品列表
- `compute_round()` — 根据当前时间计算轮次（08:00-24:00 营业，每 4 小时一轮）
- `format_countdown()` — 倒计时文本

API Key 从环境变量 `WEGAME_API_KEY` 读取，若无则使用测试 Key。

```python
WEGAME_API_KEY = os.getenv("WEGAME_API_KEY") or "sk-ff14f964051a5c966564e29b5bd3a768"
WEGAME_BASE_URL = "https://wegame.shallow.ink"
```

### 任务 2：创建 merchant API 路由

**文件：** 新建 `api/merchant.py`

- `GET /api/merchant/info` — 返回缓存的商品数据 + 轮次信息
- 首次请求或缓存过期时调用 WeGame API 刷新

### 任务 3：注册路由 + lifespan 启动定时刷新

**文件：** 修改 `main.py`

- 注册 `api.merchant.router`
- 添加 lifespan 事件：应用启动时预取一次，之后用 `asyncio.create_task` 每 4 小时后台刷新

### 任务 4：创建 Vue 页面 Merchant.vue

**文件：** 新建 `frontend/src/views/Merchant.vue`

页面布局：
- 标题 + 轮次信息（当前第 X/4 轮 + 倒计时）
- 商品列表（flex-wrap 网格，每张白色圆角卡片展示商品图标 + 名称 + 未售罄标识）
- 营业状态（营业中 / 已打烊）

样式沿用现有项目主题：浅色渐变背景、白卡片、紫蓝色调。

### 任务 5：注册前端路由 + 首页入口

**文件：** 修改 `frontend/src/router/index.js` 添加 `/merchant` → Merchant 组件
**文件：** 修改 `frontend/src/views/Home.vue` 添加远行商人入口卡片
**文件：** 修改 `frontend/src/App.vue` 底部导航栏添加远行商人图标

### 任务 6：构建前端 + 部署验证

```bash
cd frontend && npx vite build
# 重启服务
```

---

## 技术细节

### 轮次计算

```python
def compute_round():
    now = datetime.now()
    if now.hour < 8 or now.hour >= 24:
        return {"current": 0, "total": 4, "is_open": False}
    slot = (now.hour - 8) // 4  # 0-3
    return {"current": slot + 1, "total": 4, "is_open": True}
```

### 缓存策略

- 首次请求：调用 WeGame API，缓存结果
- 后续请求：直接用缓存（TTL = 30 分钟）
- 切轮次时自动刷新
- 后台每 4 小时定时预热

### WeGame API 调用

用 `httpx.AsyncClient` 异步调用，超时 15 秒。

```
GET https://wegame.shallow.ink/api/v1/games/rocom/merchant/info?refresh=true
Headers: X-API-Key: <key>
```

响应中的 `merchantActivities` 数组第一个元素为当前远行商人活动。其中的 `get_props` 数组即为本轮商品。

---

## 验证方式

1. 访问 `/api/merchant/info` 返回正确的 JSON
2. 访问 `/merchant` 页面渲染正常
3. 轮次信息显示正确
4. 倒计时更新正常
5. 营业状态切换正确
