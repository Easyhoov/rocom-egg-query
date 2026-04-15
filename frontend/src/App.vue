<script setup>
import ThemeToggle from './components/ThemeToggle.vue'
</script>

<template>
  <div class="app-shell">
    <header class="app-header">
      <div class="app-header__left">
        <h1 class="app-header__title">🥚 洛克王国孵蛋查询</h1>
        <span class="app-header__subtitle">1623 条数据 · 16 个蛋组</span>
      </div>
      <div class="app-header__right">
        <ThemeToggle />
      </div>
    </header>
    <main class="app-main">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.app-shell {
  max-width: 720px;
  margin: 0 auto;
  padding: 24px 16px;
  min-height: 100vh;
}
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border);
}
.app-header__title {
  font-size: 22px;
  font-weight: 700;
  margin: 0;
}
.app-header__subtitle {
  font-size: 13px;
  color: var(--text-weak);
  display: block;
  margin-top: 4px;
}
.app-main {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
@media (max-width: 600px) {
  .app-shell { padding: 16px 12px; }
  .app-header__title { font-size: 18px; }
  .app-header__subtitle { font-size: 12px; }
}

@media (max-width: 380px) {
  .app-header { flex-direction: column; gap: 8px; align-items: flex-start; }
  .app-header__right { align-self: flex-end; }
}
</style>
