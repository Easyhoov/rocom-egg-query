<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const features = [
  {
    icon: '🔍',
    title: '孵蛋查询',
    desc: '输入身高体重，查询可能孵化的精灵',
    route: '/egg-query',
    done: true,
  },
  {
    icon: '📖',
    title: '精灵图鉴',
    desc: '468只精灵数据，属性/蛋组筛选，详情查看',
    route: '/compendium',
    done: true,
  },
]

const upcoming = [
  { icon: '🎯', title: '蛋组配对查询', desc: '查看哪些精灵可以互相繁殖' },
  { icon: '🌈', title: '异色孵化路径', desc: '异色精灵的孵化概率与流程' },
  { icon: '📊', title: '六维雷达图', desc: '精灵属性六维可视化对比' },
  { icon: '🔗', title: '孵蛋↔图鉴联动', desc: '从图鉴详情直接跳转孵蛋查询' },
]
</script>

<template>
  <div class="min-h-screen bg-gray-950 text-gray-100 flex flex-col">
    <!-- Header -->
    <header class="border-b border-gray-800">
      <div class="max-w-2xl mx-auto px-4 py-6 text-center">
        <h1 class="text-3xl font-bold mb-1">🥚 洛克王国孵蛋查询</h1>
        <p class="text-sm text-gray-500">世界 · 1623条数据 · R值排序</p>
      </div>
    </header>

    <main class="max-w-2xl mx-auto px-4 py-8 flex-1 w-full">
      <!-- 功能入口 -->
      <section class="mb-10">
        <h2 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-4">功能</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <router-link
            v-for="f in features"
            :key="f.route"
            :to="f.route"
            class="group bg-gray-900 rounded-xl border border-gray-800 hover:border-yellow-500/50 hover:bg-gray-800/80 transition-all p-5"
          >
            <div class="text-3xl mb-3">{{ f.icon }}</div>
            <h3 class="text-lg font-bold mb-1 group-hover:text-yellow-400 transition">{{ f.title }}</h3>
            <p class="text-sm text-gray-500">{{ f.desc }}</p>
            <div class="mt-3 text-xs text-yellow-500/70 group-hover:text-yellow-400 transition">
              进入 →
            </div>
          </router-link>
        </div>
      </section>

      <!-- 即将上线 -->
      <section>
        <h2 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-4">即将上线</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div
            v-for="f in upcoming"
            :key="f.title"
            class="bg-gray-900/50 rounded-xl border border-gray-800/50 p-5 opacity-50 cursor-not-allowed"
          >
            <div class="text-3xl mb-3 grayscale">{{ f.icon }}</div>
            <h3 class="text-lg font-bold mb-1 text-gray-400">{{ f.title }}</h3>
            <p class="text-sm text-gray-600">{{ f.desc }}</p>
            <div class="mt-3 text-xs text-gray-700">
              🚧 开发中
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- Footer -->
    <footer class="border-t border-gray-800 py-4">
      <p class="text-center text-xs text-gray-700">
        数据来源：github.com/jiluoQAQ/RocomUID · 腾讯官方图鉴
      </p>
    </footer>
  </div>
</template>
