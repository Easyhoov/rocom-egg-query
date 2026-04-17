# rocom-egg-query 重构方案

## 目标

整理 Phase 1 + Phase 2 混合后的代码混乱，让项目结构清晰、前后端数据一致、可维护。

## 当前问题

### 1. 后端 `main.py` 膨胀到 618 行
- 孵蛋查询、图鉴 API、数据加载、静态文件配置全塞一个文件
- Phase 1 和 Phase 2 代码风格不一致

### 2. 前后端数据不一致
- `ResultCard.vue` 引用 `match_tier`、`probability` — 后端从未返回
- `EggQuery.vue` 引用 `data.tier_counts` — 后端从未返回
- `PetResult` Pydantic model 定义了但没用到（后端直接返回 dict）

### 3. Vue 前端冗余文件
- `Compendium.vue` (207行) — 引用 `useCompendium` composable + `SpiritCard` 组件，但没被使用
- `CompendiumPage.vue` (276行) — 路由实际指向这个，逻辑内联
- `Home.vue` (20行) — 占位符，没内容
- 两个 Compendium 实现方式不同，不知道该保留哪个

### 4. 路由混乱
- 首页 `/` 用旧 `index.html`（手动绕过 Vue）
- `/compendium` 用 Vue SPA
- 旧 `index.html` 和 Vue 前端共存在项目根目录

### 5. 缺少 composables/components
- `Compendium.vue` 引用 `useCompendium.js` 和 `SpiritCard.vue` — 文件可能不存在（编译过了说明有，但功能分散）

---

## 重构方案

### 阶段一：后端拆分（不动前端）

把 `main.py` 拆成模块：

```
main.py                    # ~80行：FastAPI app、路由挂载、启动
├── api/
│   ├── __init__.py
│   ├── query.py           # /api/query GET/POST（孵蛋查询核心）
│   ├── spirits.py         # /api/spirits, /api/spirits/{id}, /api/official-egg-groups
│   ├── pets.py            # /api/pets（列表）
│   └── stats.py           # /api/stats
├── services/
│   ├── __init__.py
│   ├── breeding.py        # load_breeding_data, query_egg 逻辑
│   ├── spirits.py         # load_spirits_data, load_official_egg_groups
│   └── image.py           # _build_image_index, get_spirit_image, image_matcher
└── models.py              # 所有 Pydantic model
```

**改动点：**
- `main.py` 只剩 app 创建、CORS、静态文件、路由注册、启动
- 孵蛋逻辑 (`query_egg` 函数) 移到 `services/breeding.py`
- 图鉴数据加载移到 `services/spirits.py`
- 图片匹配移到 `services/image.py`
- API 端点按资源拆到 `api/` 目录
- Pydantic model 统一放 `models.py`

### 阶段二：修复前后端数据契约

**后端补充缺失字段（在 `query_egg` 返回结果中）：**
- `match_tier`: 根据 `r_diff` 计算 (`exact`/`tolerance1`/`tolerance2`/`nearest`)
- `probability`: 根据匹配精度估算百分比

**规则：**
```
r_diff == 0      → tier="exact",     prob=100
r_diff <= 0.1    → tier="tolerance1", prob=80-99
r_diff <= 0.3    → tier="tolerance2", prob=50-79
r_diff <= 1.0    → tier="nearest",   prob=10-49
r_diff > 1.0     → tier="nearest",   prob=1-9
```

### 阶段三：Vue 前端整理

**删除冗余：**
- 删除 `Compendium.vue`（未被路由引用）
- 删除 `Home.vue`（占位符）

**保留：**
- `CompendiumPage.vue` → 改名 `Compendium.vue`（统一命名）
- `EggQuery.vue` — 修复引用的不存在字段
- `SpiritDetail.vue` — 保持

**修复路由：**
```js
// router/index.js
routes: [
  { path: '/', redirect: '/egg-query' },
  { path: '/egg-query', name: 'EggQuery', component: EggQuery },
  { path: '/compendium', name: 'Compendium', component: Compendium },
  { path: '/compendium/:id', name: 'SpiritDetail', component: SpiritDetail },
]
```

**修复 ResultCard.vue：**
- 删除对 `match_tier` 和 `probability` 的引用（后端补充后改为使用）
- 或改为条件渲染：有数据显示，没数据隐藏

**统一首页：**
- 方案 A：Vue 做统一入口，首页双卡片（孵蛋查询 + 图鉴），删掉旧 `index.html`
- 方案 B：保留旧 `index.html` 做孵蛋查询入口，Vue 只管图鉴

→ **推荐方案 B**，因为用户明确喜欢旧 UI 风格

### 阶段四：静态文件整理

```
static/
├── index.html              # 旧版孵蛋查询 UI（从根目录移入）
├── compendium.html          # Vue 构建产物
├── assets/                  # Vue 构建的 JS/CSS
└── creature-atlas/          # 精灵图片
```

**main.py 路由更新：**
- `/` → `static/index.html`（旧 UI）
- `/compendium` → `static/compendium.html`（Vue SPA）
- 删掉根目录的旧 `index.html`

---

## 改动文件清单

| 文件 | 操作 |
|---|---|
| `main.py` | 拆分，只保留 app 初始化和路由 |
| `api/query.py` | 新建 |
| `api/spirits.py` | 新建 |
| `api/pets.py` | 新建 |
| `api/stats.py` | 新建 |
| `services/breeding.py` | 新建 |
| `services/spirits.py` | 新建 |
| `services/image.py` | 新建 |
| `models.py` | 新建 |
| `frontend/src/views/Compendium.vue` | 删除 |
| `frontend/src/views/CompendiumPage.vue` | 改名 Compendium.vue |
| `frontend/src/views/Home.vue` | 删除 |
| `frontend/src/router/index.js` | 更新路由 |
| `frontend/src/components/ResultCard.vue` | 修复字段引用 |
| `frontend/src/views/EggQuery.vue` | 修复 tier_counts 引用 |
| `index.html` | 移到 static/ |
| `vite.config.js` | 更新构建输出路径 |

## 验证步骤

1. 后端启动无报错
2. `GET /api/query?height=0.24&weight=1.6` 返回 `match_tier` 和 `probability` 字段
3. `GET /` 显示旧 UI，图片正常
4. `GET /compendium` 显示图鉴页，筛选、分页正常
5. `GET /compendium/1` 显示精灵详情
6. Vue 构建无警告

## 风险

- 拆分后 import 路径可能出错 → 重构后立即启动测试
- 旧 `index.html` 移到 `static/` 后相对路径要确认 → 测试图片加载
- CompendiumPage 改名后需要更新所有引用
