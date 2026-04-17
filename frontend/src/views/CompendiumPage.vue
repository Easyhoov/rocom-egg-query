<script setup>
import { ref, watch, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// ── 状态 ──
const search = ref(String(route.query.q || ''))
const selectedAttr = ref(String(route.query.attribute || ''))
const selectedEggGroup = ref(String(route.query.egg_group || ''))
const page = ref(Number(route.query.page) || 1)
const pageSize = 24

const spirits = ref([])
const total = ref(0)
const totalPages = ref(1)
const loading = ref(false)

const attributes = ['火', '水', '草', '电', '冰', '光', '地', '幻', '幽', '恶', '普通', '机械', '武', '毒', '翼', '萌', '虫', '龙']
const eggGroups = ref([])

// ── 数据加载 ──
async function loadSpirits() {
  loading.value = true
  try {
    const params = new URLSearchParams()
    if (search.value) params.set('q', search.value)
    if (selectedAttr.value) params.set('attribute', selectedAttr.value)
    if (selectedEggGroup.value) params.set('egg_group', selectedEggGroup.value)
    params.set('page', String(page.value))
    params.set('page_size', String(pageSize))

    const resp = await fetch(`/api/spirits?${params}`)
    const data = await resp.json()
    if (data.success) {
      spirits.value = data.items
      total.value = data.total
      totalPages.value = data.total_pages
    }
  } finally {
    loading.value = false
  }
}

async function loadEggGroups() {
  const resp = await fetch('/api/official-egg-groups')
  const data = await resp.json()
  if (data.success) {
    eggGroups.value = data.groups
  }
}

// ── 同步 URL ──
function syncUrl() {
  const q = {}
  if (search.value) q.q = search.value
  if (selectedAttr.value) q.attribute = selectedAttr.value
  if (selectedEggGroup.value) q.egg_group = selectedEggGroup.value
  if (page.value > 1) q.page = String(page.value)
  router.replace({ query: q })
}

// ── 防抖搜索 ──
  let debounceTimer
function onSearchInput() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    page.value = 1
    loadSpirits()
    syncUrl()
  }, 300)
}

function onFilterChange() {
  page.value = 1
  loadSpirits()
  syncUrl()
}

function goToPage(p) {
  page.value = p
  loadSpirits()
  syncUrl()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// ── 分页窗口 ──
const pageWindow = computed(() => {
    const pages = []
  const total = totalPages.value
  const current = page.value

  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i)
    return pages
  }

  pages.push(1)
  if (current > 3) pages.push('...')

  const start = Math.max(2, current - 1)
  const end = Math.min(total - 1, current + 1)
  for (let i = start; i <= end; i++) pages.push(i)

  if (current < total - 2) pages.push('...')
  pages.push(total)

  return pages
})

onMounted(() => {
  loadEggGroups()
  loadSpirits()
})
</script>

<template>
  <div class="min-h-screen bg-gray-950 text-gray-100">
    <!-- 顶部导航 -->
    <header class="sticky top-0 z-10 bg-gray-950/90 backdrop-blur border-b border-gray-800">
      <div class="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
        <h1 class="text-lg font-bold text-yellow-400">📖 精灵图鉴</h1>
        <router-link
          to="/"
          class="text-sm text-gray-400 hover:text-white transition"
        >
          ← 回到孵蛋查询
        </router-link>
      </div>
    </header>

    <div class="max-w-7xl mx-auto px-4 py-6">
      <!-- 筛选栏 -->
      <div class="flex flex-wrap gap-3 mb-6">
        <!-- 搜索 -->
        <input
          v-model="search"
          @input="onSearchInput"
          placeholder="搜索精灵名称或编号..."
          class="flex-1 min-w-[200px] px-4 py-2 rounded-lg bg-gray-900 border border-gray-700
                 text-white placeholder-gray-500 focus:outline-none focus:border-yellow-500 transition"
        />

        <!-- 属性筛选 -->
        <select
          v-model="selectedAttr"
          @change="onFilterChange"
          class="px-4 py-2 rounded-lg bg-gray-900 border border-gray-700 text-white
                 focus:outline-none focus:border-yellow-500 transition cursor-pointer"
        >
          <option value="">全部属性</option>
          <option v-for="attr in attributes" :key="attr" :value="attr">{{ attr }}</option>
        </select>

        <!-- 蛋组筛选 -->
        <select
          v-model="selectedEggGroup"
          @change="onFilterChange"
          class="px-4 py-2 rounded-lg bg-gray-900 border border-gray-700 text-white
                 focus:outline-none focus:border-yellow-500 transition cursor-pointer"
        >
          <option value="">全部蛋组</option>
          <option
            v-for="g in eggGroups"
            :key="g.egg_group_name"
            :value="g.egg_group_name"
          >
            {{ g.egg_group_name }} ({{ g.spirit_count }})
          </option>
        </select>
      </div>

      <!-- 统计 -->
      <p class="text-sm text-gray-500 mb-4">
        共 {{ total }} 只精灵{{ loading ? ' · 加载中...' : '' }}
      </p>

      <!-- 精灵卡片网格 -->
      <div
        class="grid gap-4"
        style="grid-template-columns: repeat(auto-fill, minmax(150px, 1fr))"
      >
        <router-link
          v-for="s in spirits"
          :key="s.spirit_id"
          :to="`/compendium/${s.spirit_id}`"
          class="group bg-gray-900 rounded-xl border border-gray-800 hover:border-yellow-500/50
                 hover:bg-gray-800/80 transition-all overflow-hidden"
        >
          <!-- 图片 -->
          <div class="aspect-square flex items-center justify-center bg-gray-800/40 p-3">
            <img
              v-if="s.image"
              :src="s.image"
              :alt="s.display_name"
              class="w-full h-full object-contain group-hover:scale-110 transition-transform duration-300"
              loading="lazy"
            />
            <span v-else class="text-4xl opacity-30">❓</span>
          </div>

          <!-- 信息 -->
          <div class="px-3 py-2">
            <p class="text-xs text-gray-500">{{ s.spirit_no }}</p>
            <p class="font-medium text-sm truncate">
              {{ s.display_name }}
            </p>
            <div class="flex items-center gap-1 mt-1 flex-wrap">
              <span
                v-if="s.primary_attribute"
                class="text-[10px] px-1.5 py-0.5 rounded bg-gray-700 text-gray-300"
              >
                {{ s.primary_attribute }}
              </span>
              <span
                v-for="g in (s.egg_groups || []).slice(0, 2)"
                :key="g"
                class="text-[10px] px-1.5 py-0.5 rounded bg-yellow-900/30 text-yellow-400/70"
              >
                {{ g }}
              </span>
            </div>
          </div>
        </router-link>
      </div>

      <!-- 空状态 -->
      <div
        v-if="!loading && spirits.length === 0"
        class="text-center py-20 text-gray-500"
      >
        <p class="text-4xl mb-3">🔍</p>
        <p>没有找到匹配的精灵</p>
      </div>

      <!-- 分页 -->
      <div
        v-if="totalPages > 1"
        class="flex items-center justify-center gap-2 mt-8 pb-8"
      >
        <button
          v-if="page > 1"
          @click="goToPage(page - 1)"
          class="px-3 py-1.5 rounded-lg bg-gray-800 text-gray-300 hover:bg-gray-700 transition text-sm"
        >
          ← 上一页
        </button>

        <template v-for="p in pageWindow" :key="p">
          <span v-if="p === '...'" class="px-2 text-gray-600">…</span>
          <button
            v-else
            @click="goToPage(p)"
            :class="[
              'w-9 h-9 rounded-lg text-sm transition font-medium',
              p === page
                ? 'bg-yellow-500 text-gray-900'
                : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
            ]"
          >
            {{ p }}
          </button>
        </template>

        <button
          v-if="page < totalPages"
          @click="goToPage(page + 1)"
          class="px-3 py-1.5 rounded-lg bg-gray-800 text-gray-300 hover:bg-gray-700 transition text-sm"
        >
          下一页 →
        </button>
      </div>
    </div>
  </div>
</template>
