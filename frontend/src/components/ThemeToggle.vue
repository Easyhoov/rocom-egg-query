<template>
  <button
    class="theme-toggle"
    :aria-label="isDark ? '切换到亮色模式' : '切换到暗色模式'"
    @click="toggle"
  >
    {{ isDark ? '☀️' : '🌙' }}
  </button>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const isDark = ref(false)

function applyTheme(dark) {
  isDark.value = dark
  document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light')
  localStorage.setItem('theme', dark ? 'dark' : 'light')
}

function toggle() {
  applyTheme(!isDark.value)
}

onMounted(() => {
  const saved = localStorage.getItem('theme')
  if (saved) {
    applyTheme(saved === 'dark')
  } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    applyTheme(true)
  }
})
</script>

<style scoped>
.theme-toggle {
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  background: transparent;
  font-size: 20px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: background-color var(--transition, 0.25s ease), transform 0.15s ease;
  line-height: 1;
}

.theme-toggle:hover {
  background-color: var(--bg-alt, #f8fafc);
}

.theme-toggle:active {
  transform: scale(0.92);
}
</style>
