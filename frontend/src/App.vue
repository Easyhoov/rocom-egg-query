<script setup>
import ThemeToggle from './components/ThemeToggle.vue'
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
  <div class="app-shell">
    <header class="app-header">
      <div class="app-header__top">
        <h1 class="app-header__title">🥚 洛克王国孵蛋查询</h1>
        <div class="app-header__right">
          <ThemeToggle />
        </div>
      </div>
      <nav class="app-nav">
        <router-link
          to="/breed"
          class="app-nav__link"
          :class="{ active: route.path === '/' || route.path.startsWith('/breed') }"
        >🥚 孵蛋查询</router-link>
        <router-link
          to="/compendium"
          class="app-nav__link"
          :class="{ active: route.path.startsWith('/compendium') }"
        >📖 精灵图鉴</router-link>
      </nav>
    </header>
    <main class="app-main">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.app-shell {
  max-width: 1100px;
  margin: 0 auto;
  padding: 24px 16px;
  min-height: 100vh;
}
.app-header {
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border);
}
.app-header__top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.app-header__title {
  font-size: 22px;
  font-weight: 700;
  margin: 0;
}
.app-nav {
  display: flex;
  gap: 4px;
}
.app-nav__link {
  padding: 8px 16px;
  border-radius: 8px;
  text-decoration: none;
  color: var(--text-weak);
  font-size: 14px;
  font-weight: 500;
  transition: all 0.15s;
}
.app-nav__link:hover {
  background: var(--bg-hover);
  color: var(--text);
}
.app-nav__link.active {
  background: var(--accent);
  color: #fff;
}
.app-main {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
@media (max-width: 600px) {
  .app-shell { padding: 16px 12px; }
  .app-header__title { font-size: 18px; }
  .app-nav__link { font-size: 13px; padding: 6px 12px; }
}
</style>
