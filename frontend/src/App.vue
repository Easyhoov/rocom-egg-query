<template>
  <router-view />
  <nav v-if="$route.name !== 'Home'" class="app-nav">
    <router-link to="/" class="app-nav__item" exact-active-class="app-nav__item--active">🏠 首页</router-link>
    <a href="/egg-query" class="app-nav__item">🥚 孵蛋查询</a>
    <router-link to="/compendium" class="app-nav__item" active-class="app-nav__item--active">📖 精灵图鉴</router-link>
    <router-link to="/garden" class="app-nav__item" active-class="app-nav__item--active">🌿 家园炼金</router-link>
  </nav>
</template>

<style>
.app-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #fff;
  box-shadow: 0 -2px 12px rgba(0,0,0,.06);
  display: flex;
  justify-content: space-around;
  padding: 10px 0 env(safe-area-inset-bottom, 10px);
  z-index: 100;
}
.app-nav__item {
  text-decoration: none;
  color: #999;
  font-size: 12px;
  font-weight: 500;
  padding: 4px 8px;
  border-radius: 16px;
  transition: .2s;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}
.app-nav__item--active,
.app-nav__item:hover {
  color: #667eea;
  background: #f0f4ff;
}
</style>
