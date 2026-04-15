# 孵蛋查询工具 — 实施方案 v2.1

> **目标用户**: 朋友/社区玩家  
> **核心痛点**: 孵蛋查询  
> **策略**: 融合我们 + rocomegg 的优势，做最好的孵蛋查询工具  
> **设计风格**: Airtable 风格 — 干净专业、数据密集、色彩丰富、移动端友好  
> **技术栈**: Vue 3 + Vite + Airtable 设计系统（纯 CSS 变量）  
> **执行流程**: mattpocock write-a-prd（规划）→ subagent-driven-development（执行）  
> **日期**: 2026-04-15

---

## 一、功能融合清单

### 我们的优势（保留）
| 功能 | 说明 |
|------|------|
| R 值排序 | R = 体重/身高，按 r_diff 升序，判断匹配概率更直观 |
| 分层命中 | 精准/容差1/容差2/近似 四档，含概率估算 |
| REST API 后端 | 可被飞书/微信机器人调用 |
| 数据量 1623 条 | 比 rocomegg 多 207 条 |
| 三态蛋类型筛选 | 神奇的蛋/炫彩蛋/不限 |

### rocomegg 的优势（融合过来）
| 功能 | 融合方式 |
|------|----------|
| 概率进度条 | 用我们的 probability 字段 + CSS progress bar |
| 分层命中标签 | 我们已有 match_tier，加彩色标签展示 |
| 深色/浅色主题 | CSS 变量 + localStorage 切换 |
| 响应式布局 | Airtable 23 断点适配移动端 |
| Enter 快捷查询 | 键盘事件监听 |
| 蛋类型彩色标签 | Airtable 语义色彩系统 |

### 蛋组/繁殖（二期搁置）
- 蛋组查询、繁殖匹配 API 已完成后端，前端暂不做
- Vue Router 已预留路由，二期直接加页面即可

---

## 二、技术架构

### 为什么选 Vue 3 + Vite（不是纯 HTML）
1. 后期要加蛋组/繁殖/图鉴页面 → 组件复用，不用复制粘贴
2. Vue Router 天然支持多页面切换
3. 状态管理（查询参数、主题）比全局变量清晰
4. 社区开发者熟悉 Vue，方便贡献
5. Vite 构建快，开发体验好

### 项目结构
```
rocom-egg-query/
├── main.py              # FastAPI 后端（不变）
├── data/                # 数据文件（不变）
├── index.html           # 入口 HTML（Vite 生成）
├── frontend/            # 前端项目
│   ├── index.html       # Vite 入口
│   ├── src/
│   │   ├── main.js      # Vue 初始化
│   │   ├── App.vue      # 根组件（导航 + 主题）
│   │   ├── router/
│   │   │   └── index.js # 路由配置（预留多页）
│   │   ├── styles/
│   │   │   └── theme.css # Airtable 设计 Token
│   │   ├── views/
│   │   │   ├── EggQuery.vue      # 蛋尺寸查询（本期）
│   │   │   ├── EggGroup.vue      # 蛋组查询（二期）
│   │   │   └── Breeding.vue      # 繁殖匹配（二期）
│   │   └── components/
│   │       ├── QueryForm.vue     # 查询表单
│   │       ├── ResultCard.vue    # 结果卡片
│   │       ├── TierBadge.vue     # 命中层级标签
│   │       ├── ProbBar.vue       # 概率进度条
│   │       ├── EggTypeFilter.vue # 蛋类型筛选
│   │       └── ThemeToggle.vue   # 主题切换
│   └── package.json
```

### 设计系统：Airtable 风格

**核心 Token：**
```css
:root {
  /* 颜色 */
  --bg: #ffffff;
  --bg-alt: #f8fafc;
  --text: #181d26;              /* 深蓝黑 */
  --text-weak: rgba(4,14,32,0.69);
  --accent: #1b61c9;            /* Airtable Blue */
  --accent-hover: #254fad;
  --border: #e0e2e6;
  --success: #006400;
  --warning: #dd5b00;

  /* 命中层级颜色 */
  --tier-exact: #1b61c9;       /* 蓝 - 精准 */
  --tier-tolerance1: #dd5b00;  /* 橙 - 容差1 */
  --tier-tolerance2: #615d59;  /* 灰 - 容差2 */
  --tier-nearest: #a39e98;     /* 淡灰 - 近似 */

  /* 蛋类型颜色 */
  --egg-normal: #1b61c9;       /* 普通蛋 蓝 */
  --egg-precious: #e74c3c;     /* 炫彩蛋 红 */

  /* 圆角 */
  --radius-sm: 4px;
  --radius-btn: 12px;
  --radius-card: 16px;
  --radius-lg: 24px;
  --radius-pill: 9999px;

  /* 阴影（蓝调微影） */
  --shadow-card:
    rgba(0,0,0,0.32) 0px 0px 1px,
    rgba(0,0,0,0.08) 0px 0px 2px,
    rgba(45,127,249,0.28) 0px 1px 3px,
    rgba(0,0,0,0.06) 0px 0px 0px 0.5px inset;
  --shadow-soft: rgba(15,48,106,0.05) 0px 0px 20px;

  /* 字体 */
  --font: 'Inter', system-ui, -apple-system, sans-serif;
}

/* 深色模式 */
[data-theme="dark"] {
  --bg: #1a1a2e;
  --bg-alt: #16213e;
  --text: #e8e8e8;
  --text-weak: rgba(232,232,232,0.69);
  --accent: #4a90d9;
  --border: rgba(255,255,255,0.1);
  --shadow-card:
    rgba(0,0,0,0.4) 0px 0px 1px,
    rgba(0,0,0,0.2) 0px 0px 2px,
    rgba(74,144,217,0.2) 0px 1px 3px;
}
```

---

## 三、页面设计

### 蛋尺寸查询页面（唯一本期页面）

```
┌─────────────────────────────────────────┐
│  🥚 洛克王国孵蛋查询        [🌙 切换]   │
│  1623 条数据 · 16 个蛋组                │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────┐  ┌──────────┐             │
│  │ 蛋尺寸(m) │  │ 蛋重量(kg)│  [全部]    │
│  │  0.24    │  │  1.60    │  [普通蛋]   │
│  └──────────┘  └──────────┘  [炫彩蛋]   │
│              [🔍 立即查询]               │
│                                         │
├─────────────────────────────────────────┤
│  精准命中 3  │ 容差1 5  │ 容差2 2  │ 近似 0 │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────────────────────┐    │
│  │ 圆眼蜘蛛           #0168       │    │
│  │ [精准命中]  概率 99.4%         │    │
│  │ ████████████████████░░  99.4%  │    │
│  │ 身高: 0.20-0.28m  体重: 1.2-2.0kg │ │
│  │ R值: 6.72  差距: 0.05          │    │
│  └─────────────────────────────────┘    │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │ 绿耳松鼠           #049        │    │
│  │ [精准命中]  概率 92.8%         │    │
│  │ ██████████████████░░░░  92.8%  │    │
│  │ ...                            │    │
│  └─────────────────────────────────┘    │
│                                         │
└─────────────────────────────────────────┘
```

### 交互细节
1. **输入**: number 类型, step=0.001, Enter 键提交
2. **蛋类型筛选**: 三个 pill 按钮（全部/普通蛋/炫彩蛋），选中高亮
3. **查询**: fetch → /api/query → 骨架屏 → 渲染结果
4. **加载**: 3 个灰色骨架卡片
5. **结果排序**: 概率降序（后端已支持）
6. **命中统计**: 顶部横排 badge（精确 N / 容差1 N / 容差2 N / 近似 N）
7. **概率条**: CSS linear-gradient + transition 动画
8. **主题切换**: 右上角日/月图标，localStorage 记忆
9. **URL 同步**: hash 存参数，分享可直达
10. **空状态**: 友好提示 + 示例参数

---

## 四、实施步骤（按 subagent-driven-development 流程）

### Task 1: Vue 3 项目初始化
**文件**: frontend/package.json, frontend/vite.config.js, frontend/index.html, frontend/src/main.js
- [ ] npm create vite → Vue 3 模板
- [ ] 配置 Vite proxy 指向 localhost:2026
- [ ] 安装 vue-router
- [ ] 基础路由配置（/ → EggQuery）
- [ ] 验证: `npm run dev` 能打开空白页

### Task 2: 设计系统 + 主题
**文件**: frontend/src/styles/theme.css, frontend/src/components/ThemeToggle.vue
- [ ] CSS 变量定义（Airtable token 完整版）
- [ ] 深色模式变量
- [ ] ThemeToggle 组件（日/月切换）
- [ ] localStorage 持久化
- [ ] 验证: 切换主题后全站颜色变化

### Task 3: 查询表单
**文件**: frontend/src/components/QueryForm.vue, frontend/src/components/EggTypeFilter.vue
- [ ] 身高/体重输入框（number, step=0.001）
- [ ] 蛋类型 pill 按钮组（全部/普通/炫彩）
- [ ] 查询按钮 + Enter 键支持
- [ ] 表单验证（>0）
- [ ] URL hash 读取初始值
- [ ] 验证: 输入后点查询能触发回调

### Task 4: 结果卡片
**文件**: frontend/src/components/ResultCard.vue, frontend/src/components/TierBadge.vue, frontend/src/components/ProbBar.vue
- [ ] TierBadge: 命中层级标签（颜色+文字）
- [ ] ProbBar: 概率进度条（CSS 渐变+动画）
- [ ] ResultCard: 组合展示（名称+编号+标签+概率条+尺寸+R值）
- [ ] 深色模式适配
- [ ] 验证: 传入 mock 数据能正确渲染

### Task 5: 主页面集成
**文件**: frontend/src/views/EggQuery.vue, frontend/src/App.vue
- [ ] QueryForm + 结果列表集成
- [ ] fetch 调用 /api/query
- [ ] 骨架屏加载状态
- [ ] 命中统计 badge 横排
- [ ] 空状态提示
- [ ] 错误处理
- [ ] 验证: 完整查询流程端到端通过

### Task 6: 响应式 + 部署
**文件**: 各组件样式, main.py
- [ ] 移动端适配（<768px 单列）
- [ ] Vite build → 输出到 static/
- [ ] main.py 更新静态文件路由
- [ ] 本地测试
- [ ] Git commit
- [ ] 验证: 手机浏览器访问正常

---

## 五、验证标准

| 检查项 | 方法 |
|--------|------|
| 查询准确性 | 0.24m/1.60kg → 返回圆眼蜘蛛等，含 exact 标签 |
| 分层命中 | 极端值 → nearest 候选，概率 < 10% |
| 概率条动画 | 查询后进度条从 0 渐变到目标值 |
| 深色模式 | 切换后所有文字可读，卡片可见 |
| 移动端 | 375px 宽度下布局正常，按钮可点击 |
| URL 分享 | 带参数的 URL 打开后自动填充并查询 |
| API 兼容 | 旧版调用方不受影响 |
| 加载速度 | 首屏 < 1s |

---

## 六、Out of Scope（本次不做）

- ❌ 蛋组查询页面（API 就绪，前端二期）
- ❌ 繁殖匹配页面（同上）
- ❌ 异色孵化路线
- ❌ 精灵图鉴
- ❌ 分享长图
- ❌ 用户投稿
- ❌ 精灵图片（暂用蛋类型图标 + 编号代替）

---

## 七、设计风格选择理由

**为什么选 Airtable 不选 Notion：**
- Airtable 专为数据设计，Notion 偏内容阅读
- Airtable 标签系统更丰富（语义色），适合蛋类型/命中层级
- 12px 圆角比 Notion 的 4px 更现代友好
- 23 个响应式断点，移动端更精细
- 蓝色调阴影比 Notion 的"纸感"更有活力，适合游戏社区
