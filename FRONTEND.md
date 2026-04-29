# 前端架构说明

## 技术栈

- **框架**: Vue 3 (Composition API + `<script setup>`)
- **路由**: vue-router (hash mode)
- **构建**: Vite 5
- **样式**: 原生 CSS (scoped)，无 UI 框架

## 目录结构

```
frontend/
├── src/
│   ├── main.js              # Vue 入口
│   ├── App.vue              # 根组件（底栏导航）
│   ├── router/index.js      # 路由表
│   ├── utils/attrIcons.js   # 属性图标映射工具
│   ├── components/          # 共享组件
│   │   ├── EggTypeFilter.vue
│   │   ├── ProbBar.vue
│   │   ├── QueryForm.vue
│   │   ├── ResultCard.vue
│   │   ├── ThemeToggle.vue      # 已废弃（保留未删）
│   │   └── TierBadge.vue
│   └── views/               # 页面组件
│       ├── Home.vue             # /
│       ├── EggQuery.vue         # /egg-query
│       ├── CompendiumPage.vue   # /compendium
│       ├── SpiritDetail.vue     # /compendium/:id
│       ├── EggGroup.vue         # /egg-group
│       └── Garden.vue           # /garden
├── index.html               # 开发入口
├── vite.config.js           # Vite 配置
├── package.json
└── node_modules/            # gitignored
```

## 路由表

| 路径 | 组件 | 说明 |
|------|------|------|
| `/` | `Home.vue` | 首页，入口卡片（孵蛋查询 / 图鉴 / 蛋组 / 家园炼金） |
| `/egg-query` | `EggQuery.vue` | 孵蛋查询（3列卡片网格，浅色渐变主题） |
| `/compendium` | `CompendiumPage.vue` | 精灵图鉴列表（搜索 + 筛选 + 分页） |
| `/compendium/:id` | `SpiritDetail.vue` | 精灵详情（属性/特性/种族值/技能/进化/属性克制） |
| `/egg-group` | `EggGroup.vue` | 蛋组配对查询 |
| `/garden` | `Garden.vue` | 家园炼金 |
| `/*` | SPA fallback | 未匹配路由 → `index.html` |

所有页面共享底部导航栏（`App.vue` 中的 `BottomNav` 组件）。

## 构建与部署

```bash
# 构建
cd frontend && npx vite build

# 产物输出到 ../static/ （Vite 配置见 vite.config.js）
# 最终结构：
static/
├── index.html                # 唯一入口，引用 hash 化 JS/CSS
├── assets/                   # 构建产物（hash 化文件名）
│   ├── index-*.js            # 主 entry（含 vue-router + 公共代码）
│   ├── index-*.css           # 全局样式
│   ├── attrIcons-*.js        # 属性图标映射（按需加载）
│   ├── Home-*.js / *.css
│   ├── EggQuery-*.js / *.css
│   ├── CompendiumPage-*.js / *.css
│   ├── SpiritDetail-*.js / *.css
│   ├── EggGroup-*.js / *.css
│   └── Garden-*.js / *.css
├── .vite/manifest.json       # Vite 构建清单（用于找孤本）
├── creature-atlas/           # 精灵图片（本地托管）
├── attr-icons/               # 属性图标
├── skill-icons/              # 技能图标
└── garden-icons/             # 家园炼金图标
```

## API 端总路由

FastAPI (`main.py`):

- **Vue SPA** — `/`, `/egg-query`, `/compendium`, `/compendium/:id`, `/egg-group`, `/garden` 全部返回 `static/index.html`
- **静态资源** — `/creature-atlas/*`, `/assets/*`, `/attr-icons/*`, `/skill-icons/*`, `/garden-icons/*` 挂载静态目录
- **REST API** — `/api/*`（图鉴、查询、花园、统计等）
- **SPA fallback** — `/{full_path}` 兜底返回 `index.html`

## 维护注意事项

1. **构建产物清理** — 每次 `vite build` 会生成新 hash 文件，旧文件不会自动删除。按 `.vite/manifest.json` 对比清理孤本：
   ```bash
   python3 -c "
   import json, os
   m = json.load(open('static/.vite/manifest.json'))
   cur = set()
   for e in m.values():
       cur.add(e['file'].replace('assets/',''))
       for i in e.get('imports',[]):
           if i in m: cur.add(m[i]['file'].replace('assets/',''))
       for c in e.get('css',[]): cur.add(c.replace('assets/',''))
   for f in os.listdir('static/assets/'):
       if os.path.isfile(f'static/assets/{f}') and f not in cur:
           print(f'orphan: {f}')
   "
   ```

2. **样式风格** — 浅色渐变背景 + 白色圆角卡片 + #667eea/#8b3dff 紫蓝主色调。不要深色主题。

3. **图片资源** — 所有精灵图片、属性图标、技能图标、花园图标均本地托管，不依赖外部 CDN。

4. **新增 Vue 页面** — 在 `frontend/src/views/` 创建组件 → `router/index.js` 添加路由 → 构建部署。`main.py` 不需要改（SPA fallback 自动处理）。
