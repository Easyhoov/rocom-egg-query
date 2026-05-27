<template>
  <div class="app-page" :class="{ 'app-page--has-nav': $route.name !== 'Home' }">
    <router-view />
  </div>
  <nav v-if="$route.name !== 'Home'" class="app-nav">
    <router-link to="/" class="app-nav__item" exact-active-class="app-nav__item--active">
      <img :src="'/img/roco-mascot.png'" class="app-nav__icon app-nav__icon--img" alt="" />
      <span class="app-nav__label">首页</span>
    </router-link>
    <router-link to="/egg-query" class="app-nav__item" active-class="app-nav__item--active">
      <img :src="'/img/favicon.png'" class="app-nav__icon app-nav__icon--img" alt="" />
      <span class="app-nav__label">孵蛋查询</span>
    </router-link>
    <router-link to="/compendium" class="app-nav__item" active-class="app-nav__item--active">
      <img :src="'/img/icon-decorative-book.6KbZJc7F.png'" class="app-nav__icon app-nav__icon--img" alt="" />
      <span class="app-nav__label">精灵图鉴</span>
    </router-link>
    <router-link to="/garden" class="app-nav__item" active-class="app-nav__item--active">
      <img :src="'/img/peach-icon.png'" class="app-nav__icon app-nav__icon--img" alt="" />
      <span class="app-nav__label">家园炼金</span>
    </router-link>
    <router-link to="/merchant" class="app-nav__item" active-class="app-nav__item--active">
      <img :src="'/img/yuanxingshangren.png'" class="app-nav__icon app-nav__icon--img" alt="" />
      <span class="app-nav__label">远行商人</span>
    </router-link>
  </nav>
</template>

<style>
/* 引入深色主题变量 */
@import './styles/dark-theme.css';

/* Global reset */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { font-size: 16px; -webkit-font-smoothing: antialiased; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
               'Helvetica Neue', Arial, 'Noto Sans SC', sans-serif;
  color: #1a1a2e;
  line-height: 1.5;
}
a { color: #8b3dff; text-decoration: none; }
a:hover { text-decoration: none; }
img { max-width: 100%; display: block; }

/* ===== Page wrapper ===== */
.app-page {
  min-height: 100vh;
}

/* ===== Bottom Nav (Mobile) - 深色主题 ===== */
.app-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(20, 20, 40, 0.85);
  backdrop-filter: blur(12px);
  box-shadow: 0 -2px 12px rgba(0,0,0,.3);
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 6px 0 env(safe-area-inset-bottom, 8px);
  z-index: 100;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.app-nav__item {
  text-decoration: none;
  color: rgba(255, 255, 255, 0.5);
  font-size: 11px;
  font-weight: 500;
  padding: 4px 6px;
  border-radius: 14px;
  transition: color .2s, background .2s;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  min-width: 52px;
}

.app-nav__item--active,
.app-nav__item:hover {
  color: #8b3dff;
  background: rgba(139, 61, 255, 0.15);
}

/* Icon container — unified size */
.app-nav__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  flex-shrink: 0;
}

/* Emoji icons */
.app-nav__icon--emoji {
  font-size: 20px;
  line-height: 1;
}

/* Image icon (精灵图鉴) */
.app-nav__icon--img {
  width: 22px;
  height: 22px;
  object-fit: contain;
}

.app-nav__label {
  white-space: nowrap;
  line-height: 1.2;
}

/* ===== Desktop: top bar - 深色主题 ===== */
@media (min-width: 768px) {
  /* Push page content below fixed top nav */
  .app-page--has-nav {
    padding-top: 60px;
  }

  .app-nav {
    position: fixed;
    top: 0;
    bottom: auto;
    left: 0;
    right: 0;
    justify-content: center;
    gap: 8px;
    padding: 10px 24px;
    box-shadow: 0 2px 12px rgba(0,0,0,.3);
    border-bottom: 1px solid rgba(255,255,255,.06);
  }

  .app-nav__item {
    flex-direction: row;
    gap: 6px;
    padding: 8px 18px;
    font-size: 14px;
    font-weight: 600;
    border-radius: 10px;
    min-width: auto;
  }

  .app-nav__item--active,
  .app-nav__item:hover {
    background: rgba(139, 61, 255, 0.15);
  }

  .app-nav__icon {
    width: 20px;
    height: 20px;
  }

  .app-nav__icon--emoji {
    font-size: 18px;
  }

  .app-nav__icon--img {
    width: 20px;
    height: 20px;
  }
}
</style>
