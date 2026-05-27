# 洛克王国孵蛋查询 — 前端设计模板

> 基于现有 7 个页面 + 6 个组件提取的统一设计规范，用于后续新增页面或重构时参考。

---

## 一、设计语言总览

| 维度 | 规范 |
|------|------|
| **布局** | 移动端优先，`max-width: 420px` 居中（商人页 860px） |
| **背景** | 浅紫渐变 `linear-gradient(180deg, #f0ecff 0%, #ffffff 100%)` |
| **主色调** | `#8b3dff`（紫色） |
| **正文色** | `#1a1a2e`（深蓝黑） |
| **卡片** | 白底圆角 16~18px，阴影 `0 4px 16px rgba(15,16,21,0.08)` |
| **字体** | `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans SC', sans-serif` |
| **底部导航** | 固定底部，5 个入口，图标用本地图片 |

---

## 二、页面结构模板

### 2.1 标准内页（图鉴/孵蛋查询/蛋组配对/家园炼金）

```vue
<template>
  <div class="page">
    <div class="page__box">
      <!-- 标题区 -->
      <div class="page__hd">
        <h1><img :src="'/img/xxx.png'" class="page__title-icon" /> 页面标题</h1>
        <p class="page__sub">副标题或统计信息</p>
      </div>

      <!-- 筛选卡片 -->
      <div class="page__card">
        <div class="page__label">筛选条件</div>
        <div class="page__tags">
          <span class="page__tag page__tag--on">全部</span>
          <span class="page__tag">标签1</span>
        </div>
      </div>

      <!-- 内容区 -->
      <div class="page__card">
        <!-- 列表/网格等 -->
      </div>

      <!-- 底部 -->
      <div class="page__ft">洛克王国：世界 · XXX</div>
    </div>
  </div>
</template>

<style scoped>
.page {
  min-height: 100vh;
  background: linear-gradient(180deg, #f0ecff 0%, #ffffff 100%);
  padding: 16px 16px 80px; /* 底部留 80px 给导航栏 */
}
.page__box { max-width: 420px; margin: 0 auto; }

/* 标题区 */
.page__hd { text-align: center; padding: 24px 0 20px; }
.page__hd h1 {
  font-size: 22px;
  color: #1a1a2e;
  font-weight: 700;
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
.page__title-icon { width: 28px; height: 28px; object-fit: contain; }
.page__sub { font-size: 13px; color: #888; margin-top: 6px; }

/* 卡片 */
.page__card {
  background: #fff;
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 4px 16px rgba(15,16,21,0.08);
  margin-bottom: 12px;
}

/* 标签区 */
.page__label { font-size: 12px; color: #aaa; font-weight: 600; margin-bottom: 8px; }
.page__tags { display: flex; flex-wrap: wrap; gap: 6px; }
.page__tag {
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 12px;
  border: 1.5px solid #e8e8e8;
  background: #fff;
  color: #666;
  cursor: pointer;
  transition: .2s;
  user-select: none;
}
.page__tag--on { border-color: #8b3dff; background: #8b3dff; color: #fff; }

/* 底部 */
.page__ft {
  text-align: center;
  padding: 20px 0 0;
  margin-top: 20px;
  border-top: 1px solid rgba(140, 115, 80, 0.12);
  font-size: 12px;
  color: #ccc;
}
</style>
```

### 2.2 首页（功能入口卡片式）

```vue
<template>
  <div class="home">
    <div class="home__bg"></div>
    <div class="home__content">
      <!-- 顶部横幅 -->
      <div class="home__header">
        <div class="home__header-bg"
             :style="{ backgroundImage: 'url(/img/卡片整体bg.png)' }">
        </div>
        <div class="home__header-inner">
          <img class="home__logo" src="/img/洛克王国大标题-白.png" alt="洛克王国" />
          <div class="home__subtitle">孵蛋查询工具</div>
        </div>
      </div>

      <!-- 功能入口列表 -->
      <div class="home__section">
        <div class="home__section-label">
          <span class="home__label-bar"></span>
          功能
        </div>
        <div class="home__card-list">
          <a v-for="f in features" :key="f.title" :href="f.href" class="home__card">
            <img v-if="f.icon.startsWith('/')" class="home__card-icon-img"
                 :src="f.icon" :alt="f.title" />
            <div v-else class="home__card-icon">{{ f.icon }}</div>
            <div class="home__card-body">
              <div class="home__card-title">{{ f.title }}</div>
              <div class="home__card-desc">{{ f.desc }}</div>
            </div>
            <div class="home__card-arrow">›</div>
          </a>
        </div>
      </div>

      <!-- 装饰图 -->
      <div class="home__decor">
        <img src="/img/小洛克.png" alt="" />
      </div>

      <!-- 底部 -->
      <div class="home__footer">
        <a href="https://github.com/Easyhoov/rocom-egg-query" target="_blank">GitHub</a>
        <span class="dot">·</span>
        <span>数据 RocomUID</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home {
  min-height: 100vh;
  background: #f5efe6;
  position: relative;
  overflow: hidden;
}
.home__bg {
  position: absolute; inset: 0;
  background:
    radial-gradient(ellipse 600px 400px at 20% 10%, rgba(218,180,120,0.08), transparent),
    radial-gradient(ellipse 500px 300px at 80% 30%, rgba(210,170,100,0.06), transparent),
    radial-gradient(ellipse 400px 500px at 50% 80%, rgba(200,160,90,0.05), transparent);
  pointer-events: none;
}
.home__content {
  position: relative; z-index: 1;
  max-width: 420px; margin: 0 auto;
  padding: 24px 16px 60px;
}

/* 横幅 */
.home__header {
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  margin-bottom: 24px;
}
.home__header-bg {
  position: absolute; inset: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.78), rgba(245,236,221,0.65));
  background-size: cover;
  border: 1px solid rgba(140,115,80,0.15);
  border-radius: 20px;
}
.home__header-inner {
  position: relative;
  display: flex; flex-direction: column; align-items: center;
  padding: 28px 20px 24px;
}
.home__logo { height: 48px; width: auto; object-fit: contain; }
.home__subtitle {
  font-size: 15px; color: #8c7a61;
  margin-top: 8px; letter-spacing: 2px;
}

/* 区块标题 */
.home__section { margin-bottom: 20px; }
.home__section-label {
  display: flex; align-items: center; gap: 10px;
  font-size: 14px; font-weight: 700; color: #7a6548;
  margin-bottom: 14px; padding-left: 4px;
  text-transform: uppercase; letter-spacing: 1px;
}
.home__label-bar {
  display: block; width: 4px; height: 18px;
  background: #c97926; border-radius: 2px;
}

/* 功能卡片 */
.home__card-list { display: flex; flex-direction: column; gap: 10px; }
.home__card {
  display: flex; align-items: center; gap: 14px;
  padding: 16px;
  background: rgba(255,255,255,0.68);
  border: 1px solid rgba(140,115,80,0.1);
  border-radius: 18px;
  text-decoration: none; color: inherit;
  transition: all 0.15s;
  cursor: pointer;
  backdrop-filter: blur(8px);
}
.home__card:active {
  transform: scale(0.97);
  background: rgba(255,255,255,0.85);
}
.home__card-icon {
  width: 48px; height: 48px;
  display: flex; align-items: center; justify-content: center;
  font-size: 28px;
  background: linear-gradient(135deg, rgba(255,240,210,0.6), rgba(245,225,185,0.4));
  border-radius: 14px; flex-shrink: 0;
}
.home__card-icon-img {
  width: 48px; height: 48px;
  object-fit: contain; border-radius: 14px; flex-shrink: 0;
  background: linear-gradient(135deg, rgba(255,240,210,0.6), rgba(245,225,185,0.4));
  padding: 4px;
}
.home__card-body { flex: 1; min-width: 0; }
.home__card-title { font-size: 17px; font-weight: 800; color: #3d2b16; margin-bottom: 3px; }
.home__card-desc { font-size: 13px; color: #8c7a61; line-height: 1.4; }
.home__card-arrow { font-size: 24px; color: #c97926; font-weight: 300; flex-shrink: 0; opacity: 0.6; }

/* 装饰 */
.home__decor {
  text-align: right; margin-top: -10px; margin-bottom: 10px;
  opacity: 0.08; pointer-events: none;
}
.home__decor img { width: 200px; height: auto; }

/* 底部 */
.home__footer {
  text-align: center; margin-top: 20px; padding-top: 20px;
  border-top: 1px solid rgba(140,115,80,0.12);
  font-size: 12px; color: #bfae95;
}
.home__footer a { color: #9a8a70; text-decoration: none; }
.dot { margin: 0 6px; color: #d4c8b5; }
</style>
```

---

## 三、卡片组件模板

### 3.1 标准白卡

```css
.card {
  background: #fff;
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 4px 16px rgba(15,16,21,0.08);
  margin-bottom: 12px;
}
```

### 3.2 精灵网格卡（3列）

```css
.pet-card {
  background: #fff;
  border-radius: 14px;
  padding: 10px 6px 8px;
  text-align: center;
  text-decoration: none;
  color: inherit;
  box-shadow: 0 8px 24px rgba(15,16,21,0.08);
  transition: .2s;
  position: relative;
  overflow: hidden;
}
.pet-card:hover { box-shadow: 0 8px 24px rgba(139,61,255,0.12); }
.pet-card:active { transform: scale(.96); }
```

### 3.3 毛玻璃功能卡（首页用）

```css
.feature-card {
  background: rgba(255,255,255,0.68);
  border: 1px solid rgba(140,115,80,0.1);
  border-radius: 18px;
  padding: 16px;
  backdrop-filter: blur(8px);
  transition: all 0.15s;
}
.feature-card:active {
  transform: scale(0.97);
  background: rgba(255,255,255,0.85);
}
```

### 3.4 商人暖色卡

```css
.merchant-card {
  background: linear-gradient(135deg, rgba(255,255,255,0.72), rgba(244,236,224,0.88));
  border: 1px solid rgba(118,97,74,0.14);
  border-radius: 22px;
  box-shadow: 0 10px 26px rgba(58,39,21,0.06);
}
```

### 3.5 珍贵/异色变体

```css
.card--precious {
  background: linear-gradient(135deg, #fffdf0, #fff8dc);
  border-color: rgba(102,126,234,0.25);
}
```

---

## 四、色彩系统

### 4.1 主色板

```
主色     #8b3dff   按钮/链接/激活态/聚焦边框
正文     #1a1a2e   标题/正文
副文     #888      副标题/描述
弱文     #aaa      标签/占位符
禁用     #ccc      禁用态/空状态
边框     #e8e8e8   输入框/标签边框
背景     #f0ecff   页面渐变起始
卡片     #fff      卡片背景
```

### 4.2 语义色

```
成功/草   #4caf50   防御技能/草属性/HP
错误/物攻 #e74c3c   物理攻击/错误提示
信息/水冰 #42a5f5   水/冰/电属性
魔法     #667eea   魔法攻击
紫色     #9b59b6   异色精灵/魔法属性
金色     #f39c12   种族值总和/魔法防御
青色     #1abc9c   速度
橙色     #ff9800   状态技能
```

### 4.3 属性标签配色

```css
/* 属性标签 — 紫色系 */
.attr-tag {
  background: #8b3dff15;
  color: #8b3dff;
}

/* 蛋组标签 — 浅紫底 */
.egg-tag {
  background: #f5f0ff;
  color: #8b3dff;
}

/* 异色标签 — 金色边 */
.shiny-tag {
  background: #fff8e1;
  border-color: #ffd700;
  color: #9b59b6;
}

/* 不可繁殖 — 红色 */
.no-breed-tag {
  background: #fee;
  color: #e74c3c;
}
```

### 4.4 技能类型色

| 类型 | 背景 | 文字 |
|------|------|------|
| 物理 | `#fee8e8` | `#e74c3c` |
| 魔法 | `#e8e8ff` | `#667eea` |
| 防御 | `#e8f5e9` | `#4caf50` |
| 状态 | `#fff3e0` | `#ff9800` |

---

## 五、间距与圆角

### 5.1 圆角阶梯

```
 4px   小徽章/技能类型标签
 6px   精灵标签/小tag
 8px   按钮/表单标签
10px   输入框/蛋组卡片
12px   摘要卡片/技能卡/操作按钮
14px   精灵网格卡/图标容器
16px   标准白卡
18px   功能入口卡/导航项
20px   筛选标签(pill)/头像容器
22px   商人卡片
50%    圆形头像/精灵图片
999px  胶囊标签(pill)
```

### 5.2 间距阶梯

```
 2px   图标与文字最小间距
 4px   紧凑元素间距
 6px   标签间距/紧凑卡片间距
 8px   网格间距/标签与内容
10px   卡片列表间距
12px   标准卡片间距
14px   区块内间距
16px   卡片内边距/页面左右边距
20px   标题区上下间距
24px   页面顶部内边距
```

---

## 六、导航栏

```vue
<template>
  <nav v-if="$route.name !== 'Home'" class="app-nav">
    <router-link to="/" class="app-nav__item">🏠 首页</router-link>
    <a href="/egg-query" class="app-nav__item">🥚 孵蛋查询</a>
    <router-link to="/compendium" class="app-nav__item">
      <img :src="'/img/icon-decorative-book.6KbZJc7F.png'" class="app-nav__icon" />
      精灵图鉴
    </router-link>
    <router-link to="/garden" class="app-nav__item">🌿 家园炼金</router-link>
    <router-link to="/merchant" class="app-nav__item">🛒 远行商人</router-link>
  </nav>
</template>

<style>
.app-nav {
  position: fixed;
  bottom: 0; left: 0; right: 0;
  background: #fff;
  box-shadow: 0 -2px 12px rgba(0,0,0,.06);
  display: flex;
  justify-content: space-around;
  padding: 10px 0 env(safe-area-inset-bottom, 10px);
  z-index: 100;
}
.app-nav__item {
  text-decoration: none; color: #999;
  font-size: 12px; font-weight: 500;
  padding: 4px 8px; border-radius: 18px;
  transition: .2s;
  display: flex; flex-direction: column;
  align-items: center; gap: 2px;
}
.app-nav__item--active,
.app-nav__item:hover { color: #8b3dff; background: #f0ecff; }
.app-nav__icon { width: 18px; height: 18px; object-fit: contain; margin-bottom: 2px; }
</style>
```

---

## 七、输入框与按钮

```css
/* 搜索输入框 */
.input {
  width: 100%;
  padding: 10px 14px;
  border: 1.5px solid #e8e8e8;
  border-radius: 10px;
  font-size: 15px;
  background: #fafafa;
  outline: none;
  transition: .2s;
  box-sizing: border-box;
}
.input:focus { border-color: #8b3dff; background: #fff; }

/* 主按钮 */
.btn-primary {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #8b3dff, #667eea);
  color: #fff;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: .2s;
}
.btn-primary:hover { box-shadow: 0 4px 12px rgba(102,126,234,.4); }

/* 重置按钮 */
.btn-reset {
  padding: 8px 16px;
  background: #f5f5f5;
  color: #666;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  cursor: pointer;
  transition: .2s;
}
```

---

## 八、可用素材清单

### 8.1 `/img/` — 通用 UI 图片

| 文件 | 用途 |
|------|------|
| `洛克王国大标题-白.png` | 首页横幅标题 |
| `卡片整体bg.png` | 首页横幅背景 |
| `小洛克.png` | 角色装饰图 |
| `favicon.png`（神奇的蛋） | 网站图标/孵蛋查询入口图标 |
| `icon-decorative-book.6KbZJc7F.png` | 精灵图鉴入口图标 |
| `icon-chapter.DoUojjEg.png` | 章节图标 |
| `icon-stay-tuned.DHbzz5us.png` | "敬请期待"占位图标 |
| `yuanxingshangren.png` | 远行商人 NPC 图标 |
| `宝箱标.png` | 宝箱徽章 |
| `coin.png` | 货币图标 |
| `ai卡片.png` | AI 卡片背景 |
| `ai评分*.png` | AI 评分相关 UI 元素 |
| `精灵pg.png` | 精灵预览图 |

### 8.2 `/attr-icons/` — 18 个属性图标（30×30）

火/水/草/电/冰/光/地/幻/幽/恶/普通/机械/武/毒/翼/萌/虫/龙

### 8.3 `/creature-atlas/` — 465 张精灵图鉴 WebP

命名格式: `{id}-{variant}.webp`（如 `001-base.webp`）

### 8.4 `/item-icons/` — 274 张道具图标 PNG

中文命名（如 `神奇的蛋.png`、`万能血脉秘药.png`）

### 8.5 `/skill-icons/` — 433 张技能图标 PNG

中文命名（如 `一拳.png`、`乘胜追击.png`）

### 8.6 `/garden-icons/` — 家园素材

| 子目录 | 数量 | 内容 |
|--------|------|------|
| `seeds/` | 24 | 种子 |
| `materials/` | 10 | 炼金材料 |
| `foods/` | 10 | 食物 |
| `balls/` | 9 | 精灵球 |

---

## 九、新增页面 Checklist

1. **路由** — 在 `frontend/src/router/index.js` 添加路由
2. **导航** — 在 `App.vue` 的 `<nav>` 添加入口（如有需要）
3. **首页入口** — 在 `Home.vue` 的 `features` 数组添加条目
4. **页面文件** — 在 `frontend/src/views/` 创建 `XxxPage.vue`
5. **API 路由** — 在 `main.py` 添加页面路由（返回 `INDEX_HTML`）
6. **静态资源** — 新增的 mount 目录必须在 `main.py` 显式注册
7. **构建** — `cd frontend && npx vite build`
8. **重启** — `kill` 旧进程后重启 `uvicorn`

---

## 十、设计原则

1. **移动端优先** — 所有页面 420px 宽度居中，底部留 80px 给导航栏
2. **浅色渐变背景** — `#f0ecff → #ffffff`，绝不用深色主题
3. **白色圆角卡片** — 内容用白色卡片承载，圆角 16~18px
4. **紫色主色调** — `#8b3dff` 用于所有交互态（按钮/链接/激活/聚焦）
5. **本地素材优先** — 图标/图片全部放 `static/` 本地托管，不依赖外部 CDN
6. **图片用动态绑定** — Vue 模板中 `:src="'/img/xxx.png'"` 避免 Vite 构建报错
7. **平滑过渡** — 所有交互元素加 `transition: .2s`
8. **按压缩放反馈** — 可点击元素加 `:active { transform: scale(0.97) }`
