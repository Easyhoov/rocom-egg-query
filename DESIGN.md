# Rocom Egg Query — 洛克王国孵蛋查询 Design System

> DESIGN.md — 统一设计规范文档
> 参考 Claude Design 规范格式，适用于所有 Vue 页面

---

## 1. 视觉主题与氛围

**游戏工具 · 童趣亲和 · 紫蓝品质感**

页面读起来像一个温暖的数字工具箱——浅色渐变背景、白色圆角卡片、统一的紫色主色 `#8b3dff`。不追求科技感的冷峻，也不过度卡通化；在干净与趣味之间取平衡。

情绪词：**亲和、轻快、有条理、有品质感**

---

## 2. 色板与角色

### 主色板

```css
--bg-gradient: linear-gradient(180deg, #f0ecff 0%, #ffffff 100%)
   /* 页面背景渐变 — 浅紫到白，Canva风格 */

--surface-card: #ffffff
   /* 白色卡片底色 — 所有内容卡片、表单区 */

--surface-card-hover: #f0ecff
   /* 卡片/导航悬停背景 — 配合主色使用 */

--surface-icon: #f0ecff
   /* 图标/头像圆形底色 — 首页功能卡图标区 */

--surface-tag-bg: #f5f2ff
   /* 精灵头像圆形底色 — 图鉴/蛋组网格中 */

--surface-filter: #f5f5f5
   /* 标签栏底色 — 孵蛋查询 tab 切换 */

--text-primary: #1a1a2e
   /* 主文字 — 标题、卡片名称、关键信息 */

--text-body: #333333
   /* 正文 — 次要文字内容 */

--text-secondary: #666666 / #888888
   /* 辅助文字 — 说明、副标题 */

--text-muted: #999999 / #aaaaaa
   /* 弱化文字 — 数据来源、标签分类 */

--text-dim: #bbbbbb / #cccccc / #dddddd
   /* 极弱文字 — 编号、占位、底部版权 */

--accent: #8b3dff
   /* 主色调紫色（Canva Purple） — 按钮、链接、选中态、高亮 */

--accent-hover: #7929e6
   /* 主色悬停加深 */

--accent-soft: #f0ecff
   /* 主色透明浅底 — 属性标签底色 */

--accent-deep: #8b3dff
   /* 深紫 — R值高亮、特殊数据（复用主色） */

--border: #e8e8e8
   /* 边框 — 输入框、标签边框、分隔线 */

--border-strong: #d1d1d6
   /* 强调边框 — 选中标签边框 */

--status-shiny: #ffd700
   /* 金色 — 异色/稀有标注 */

--status-danger: #e74c3c
   /* 红色 — 不可孵蛋标识、错误提示 */

--status-info: #f57f17
   /* 琥珀色 — 特性标签 */

--status-success: #4caf50
   /* 绿色 — 副属性标签、成功状态 */
```

### 使用规则

- **`--accent` (#8b3dff) 是唯一的品牌色。** 用于按钮填充、链接、选中态、活动标签。禁止在其他装饰性元素上使用。
- **紫蓝渐变色 `linear-gradient(135deg, #8b3dff, #8b3dff)` 不再使用。** 按钮统一纯色。
- **状态色保留各自语义位置**，不挪用做装饰。
- 按钮悬停/点击使用 scale 缩放反馈（0.97），不用颜色变化。
- 背景渐变固定为 `#f0ecff → #f0ecff → #fff`，所有页面统一。

---

## 3. 排版规则

### 字体

```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
             'Helvetica Neue', Arial, 'Noto Sans SC', sans-serif
```

系统字体栈，无自定义字体引入（保持加载速度）。

### 字号 Scale

| 用途 | 大小 | 字重 | 颜色 | 场景 |
|------|------|------|------|------|
| Display/Logo | 48px | — | — | 首页大图标 emoji |
| H1 标题 | 22px | 700 | `#1a1a2e` | 页面主标题 |
| H2 小标题 | 16px | 700 | `#1a1a2e` / `#333` | 卡片内标题、弹窗标题 |
| 卡片标题 | 16px | 700 | `#1a1a2e` | 功能名称、精灵名称 |
| 正文 | 15px / 14px | 400/500 | `#333` | 输入框文字、表单 |
| 说明文字 | 13px | 400 | `#888` / `#666` | 副标题、描述、按钮文字 |
| 标签文字 | 12px | — | `#aaa` / `#666` | 分类标签、元信息 |
| 小号标签 | 11px | — | `#bbb` / `#999` | 精灵编号、footer |
| 极小号 | 9-10px | — | `#bbb` | R值、差值、极小标注 |

### 文本规则

- 标题使用 `text-wrap: balance` 保持视觉平衡
- 禁止文字斜体——强调使用字重 600/700
- 数字使用常规数字，特殊数据（R值）使用主色高亮
- 链接统一 `color: #8b3dff` + `text-decoration: none`

---

## 4. 组件样式

### 4.1 页面容器

```css
.page-root {
  min-height: 100vh;
  background: linear-gradient(180deg, #f0ecff 0%, #ffffff 100%);
  padding: 16px 16px 80px;  /* 底部留导航栏空间 */
}
.page-box {
  max-width: 420px;   /* 移动端适配，居中 */
  margin: 0 auto;
}
```

### 4.2 页面头部

```css
.page-header {
  text-align: center;
  padding: 24px 0 20px;
}
.page-header h1 {
  font-size: 22px;
  color: #1a1a2e;
  font-weight: 700;
  margin: 0;
}
.page-subtitle {
  font-size: 13px;
  color: #888;
  margin-top: 6px;
}
```

### 4.3 卡片（最核心组件）

```css
.card {
  background: #fff;
  border-radius: 18px;
  padding: 16px;
  box-shadow: 0 4px 16px rgba(15,16,21,0.08);
  margin-bottom: 12px;
}
.card:hover {
  box-shadow: 0 8px 24px rgba(139,61,255,0.12);
}
```

### 4.4 按钮

```css
.btn-primary {
  background: #8b3dff;
  color: #fff;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: .15s;
}
.btn-primary:active { transform: scale(.97); }
.btn-primary:disabled { opacity: .5; cursor: not-allowed; }

.btn-ghost {
  background: #f5f5f5;
  color: #888;
  border: 1.5px solid #e8e8e8;
  border-radius: 12px;
  cursor: pointer;
}
```

- 按钮统一纯色 `#8b3dff`，**禁止渐变背景**
- 全宽按钮 `padding: 12px` + `font-size: 16px`
- 内联按钮 `padding: 10px 24px` + `font-size: 15px`

### 4.5 输入框

```css
.input {
  width: 100%;
  padding: 12px;
  border: 1.5px solid #e8e8e8;
  border-radius: 10px;
  font-size: 17px;
  font-weight: 500;
  background: #fafafa;
  transition: .2s;
  box-sizing: border-box;
  outline: none;
}
.input:focus {
  border-color: #8b3dff;
  background: #fff;
}
```

- 标签：`font-size: 12px; color: #888; margin-bottom: 6px;`

### 4.6 标签（Tag / 筛选）

```css
.tag {
  padding: 5px 12px;          /* 图鉴筛选栏 */
  /* 或 */
  padding: 7px 14px;          /* 孵蛋查询标签 */
  border-radius: 20px;        /* 椭圆形 */
  font-size: 12px / 13px;
  border: 1.5px solid #e8e8e8;
  background: #fff;
  color: #666;
  cursor: pointer;
  transition: .2s;
  user-select: none;
}
.tag--active {
  border-color: #8b3dff;
  background: #8b3dff;
  color: #fff;
}
```

### 4.7 Tab 切换

```css
.tabs {
  display: flex;
  background: #f5f5f5;
  border-radius: 10px;
  padding: 3px;
  margin-bottom: 8px;
}
.tab {
  flex: 1;
  padding: 8px 0;
  text-align: center;
  border-radius: 8px;
  font-size: 13px;
  color: #888;
  cursor: pointer;
  border: none;
  background: none;
  transition: .2s;
}
.tab--active {
  background: #fff;
  color: #333;
  font-weight: 600;
  box-shadow: 0 1px 4px rgba(0,0,0,.08);
}
```

### 4.8 精灵网格卡片

```css
.pet-card {
  background: #fff;
  border-radius: 14px;
  padding: 10px 6px 8px;
  text-align: center;
  text-decoration: none;
  color: inherit;
  box-shadow: 0 2px 8px rgba(0,0,0,.04);
  transition: .2s;
}
.pet-card:active { transform: scale(.96); }

.pet-card-img {
  width: 56px; height: 56px;
  margin: 0 auto 4px;
  display: flex; align-items: center; justify-content: center;
  background: #f8f9ff;
  border-radius: 50%;
}
.pet-card-img img { width: 48px; height: 48px; object-fit: contain; }
.pet-card-name { font-size: 13px; font-weight: 600; color: #1a1a2e; }
.pet-card-no { font-size: 10px; color: #bbb; }
```

### 4.9 底部导航栏

```css
.app-nav {
  position: fixed; bottom: 0; left: 0; right: 0;
  background: #fff;
  box-shadow: 0 -2px 12px rgba(0,0,0,.06);
  display: flex; justify-content: space-around;
  padding: 10px 0 env(safe-area-inset-bottom, 10px);
  z-index: 100;
}
.app-nav__item {
  text-decoration: none; color: #999;
  font-size: 12px; font-weight: 500;
  padding: 4px 8px; border-radius: 18px;
  transition: .2s;
  display: flex; flex-direction: column; align-items: center;
  gap: 2px;
}
.app-nav__item--active, .app-nav__item:hover {
  color: #8b3dff; background: #f0ecff;
}
```

- 首页（路由 `/`）不显示底部导航栏
- 其他页面保持显示

### 4.10 加载状态

```css
/* 加载旋转器 */
.loading-spinner {
  width: 32px; height: 32px;
  border: 3px solid #e8e8e8;
  border-top-color: #8b3dff;
  border-radius: 50%;
  animation: spin .8s linear infinite;
  margin: 0 auto 12px;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* 空状态 */
.empty-state { text-align: center; padding: 60px 0; color: #ccc; }
.empty-state-icon { font-size: 48px; margin-bottom: 8px; }

/* 错误提示 */
.error-msg {
  background: #fff0f0;
  color: #e74c3c;
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
  text-align: center;
  margin-bottom: 12px;
}
```

### 4.11 弹窗（Modal）

```css
.modal-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,.4);
  z-index: 100;
  display: flex; justify-content: center; align-items: center;
}
.modal-box {
  background: #fff;
  border-radius: 18px;
  padding: 24px;
  width: 85%;
  max-width: 320px;
}
.modal-box h3 { font-size: 16px; margin-bottom: 12px; }
.modal-box p { font-size: 13px; color: #666; line-height: 1.8; }
.modal-box button {
  margin-top: 16px; width: 100%; padding: 10px;
  border: none; background: #8b3dff; color: #fff;
  border-radius: 8px; font-size: 14px; cursor: pointer;
}
```

### 4.12 底部版权信息

```css
.page-footer {
  text-align: center;
  padding: 24px 0 16px;
  font-size: 11px;
  color: #ccc;
}
.page-footer a { color: #999; }
```

---

## 5. 布局原则

- **移动优先。** 所有页面 max-width: 420px，居中。
- **垂直堆叠。** 从上到下：Header → 表单/筛选 → 内容网格 → Footer。
- **3列网格。** 精灵卡片 `repeat(3, 1fr)`，间距 8px。
- **功能卡片入口** 使用纵向列表，图标+文字+箭头，间距 10px。
- **间距体系：** 4 / 6 / 8 / 10 / 12 / 14 / 16 / 20 / 24 / 60(px)。
- 卡片间间距统一 12px，与导航栏上方保留 80px。

---

## 6. 深度与层级

- **扁平为主。** 层次通过背景渐变（浅→白）和白色卡片区分。
- **阴影策略：** `box-shadow: 0 4px 16px rgba(15,16,21,0.08)` 用于标准卡片；`0 2px 8px rgba(0,0,0,.04)` 用于网格小卡片。
- **模态弹窗：** 使用半透明黑色遮罩 `rgba(0,0,0,.4)`，弹窗用白色圆角卡片。
- **点击反馈：** 统一 `scale(0.97)` 或 `scale(0.96)`，96ms ease-out。
- 禁止 neumorphism、禁止多层阴影堆叠、禁止异形形状。

---

## 7. Do's and Don'ts

### ✅ Do

- 白色圆角卡片作为内容容器（`border-radius: 18px`）
- 紫蓝 #8b3dff 作为唯一的主动作色（按钮、链接、选中态）
- 浅色渐变背景（`#f0ecff → #f0ecff → #fff`）
- 系统字体栈，不引入外部字体
- 底部导航栏仅显示在非首页页面
- 所有精灵图片显示在圆形 `#f8f9ff` 背景中
- 使用 emoji 作为图标（功能图标、标签图标），不引入图标库
- 点击反馈：缩放 0.97

### ❌ Don't

- **不用渐变按钮**（`linear-gradient(135deg, #8b3dff, #8b3dff)` 已废弃）
- 不用深色/暗色主题
- 不用外部 CDN 图标库（emoji 和本地图片够用）
- 不用异形卡片（菱形、圆角不统一的形状）
- 不用玻璃态（glassmorphism）、毛玻璃等效果
- 不用多主色调调色板
- 不用动画过度（除点击反馈外）
- 首页不显示底部导航栏

---

## 8. 响应式行为

| 条件 | 行为 |
|------|------|
| >420px | 内容居中，max-width 420px，两侧留白 |
| <420px | 自适应缩窄，padding: 16px 保持 |
| Grid | 3列网格始终不变（移动端也能显示3列） |
| 表单 | 双列输入框在移动端依然并排（flex: 1） |
| 底部导航 | 固定底栏，使用 `env(safe-area-inset-bottom)` 适配刘海屏 |
| Tab/标签 | 过多标签自动换行（flex-wrap: wrap） |

---

## 9. Agent Prompt Guide

**Bias:** 浅色渐变背景（#f0ecff → #f0ecff → #fff），纯色紫蓝 #8b3dff 按钮，白色圆角卡片（border-radius: 18px），系统字体栈，emoji 图标，3列精灵网格，扁平设计无投影堆叠，移动端优先 max-width: 420px，底部固定导航栏，`scale(0.97)` 点击反馈。

**Reject:** 深色主题，渐变按钮（#8b3dff 纯色），圆形以外的精灵头像形状，外部字体/CDN 图标，玻璃态效果，多色主色调，翻页/滚动动画，桌面端优先布局。
