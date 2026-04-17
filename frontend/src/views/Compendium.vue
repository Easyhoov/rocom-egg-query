<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import SpiritCard from '../components/SpiritCard.vue'
import { useCompendium } from '../composables/useCompendium.js'

const route = useRoute()
const router = useRouter()

const {
  spirits, loading, total, totalPages,
  query, attribute, eggGroup, page, pageSize,
  eggGroups, attributes,
  fetchSpirits, fetchFilters
} = useCompendium()

// 初始化：从 URL 恢复筛选状态
onMounted(() => {
  query.value = route.query.q || ''
  attribute.value = route.query.attribute || ''
  eggGroup.value = route.query.eggGroup || ''
  page.value = parseInt(route.query.page) || 1
  fetchFilters()
  fetchSpirits()
})

// 同步 URL
watch([query, attribute, eggGroup, page], () => {
  const q = {}
  if (query.value) q.q = query.value
  if (attribute.value) q.attribute = attribute.value
  if (eggGroup.value) q.eggGroup = eggGroup.value
  if (page.value > 1) q.page = page.value
  router.replace({ query: q })
}, { deep: true })

// 搜索/筛选变化时重置页码并刷新
let debounceTimer = null
function onSearchInput() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    page.value = 1
    fetchSpirits()
  }, 300)
}

function onFilterChange() {
  page.value = 1
  fetchSpirits()
}

function goToPage(p) {
  page.value = p
  fetchSpirits()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function openDetail(spiritId) {
  router.push(`/compendium/${spiritId}`)
}
</script>

<template>
  <div class="compendium">
    <!-- 搜索 + 筛选 -->
    <div class="comp-toolbar">
      <div class="comp-search">
        <input
          v-model="query"
          @input="onSearchInput"
          placeholder="搜索精灵名称或编号..."
          class="comp-search__input"
        />
      </div>
      <div class="comp-filters">
        <select v-model="attribute" @change="onFilterChange" class="comp-select">
          <option value="">全部属性</option>
          <option v-for="a in attributes" :key="a" :value="a">{{ a }}</option>
        </select>
        <select v-model="eggGroup" @change="onFilterChange" class="comp-select">
          <option value="">全部蛋组</option>
          <option v-for="g in eggGroups" :key="g" :value="g">{{ g }}</option>
        </select>
      </div>
    </div>

    <!-- 总数 -->
    <div class="comp-stats" v-if="!loading">
      共 <strong>{{ total }}</strong> 只精灵
    </div>

    <!-- 加载 -->
    <div v-if="loading" class="comp-loading">
      <div class="comp-grid">
        <div class="skeleton-card" v-for="i in 12" :key="i">
          <div class="skeleton-img"></div>
          <div class="skeleton-text"></div>
        </div>
      </div>
    </div>

    <!-- 网格 -->
    <div v-else-if="spirits.length" class="comp-grid">
      <SpiritCard
        v-for="s in spirits"
        :key="s.spirit_id"
        :spirit="s"
        @click="openDetail(s.spirit_id)"
      />
    </div>

    <!-- 空 -->
    <div v-else class="comp-empty">
      <p>😅 没有找到匹配的精灵</p>
    </div>

    <!-- 分页 -->
    <div v-if="totalPages > 1" class="comp-pagination">
      <button
        :disabled="page <= 1"
        @click="goToPage(page - 1)"
        class="page-btn"
      >上一页</button>
      <span class="page-info">{{ page }} / {{ totalPages }}</span>
      <button
        :disabled="page >= totalPages"
        @click="goToPage(page + 1)"
        class="page-btn"
      >下一页</button>
    </div>
  </div>
</template>

<style scoped>
.compendium { display: flex; flex-direction: column; gap: 16px; }

.comp-toolbar {
  display: flex; gap: 12px; flex-wrap: wrap;
  align-items: center;
}
.comp-search { flex: 1; min-width: 200px; }
.comp-search__input {
  width: 100%; padding: 10px 14px;
  border: 1px solid var(--border); border-radius: 8px;
  background: var(--bg); color: var(--text);
  font-size: 14px; outline: none;
  transition: border-color 0.15s;
}
.comp-search__input:focus { border-color: var(--accent); }

.comp-filters { display: flex; gap: 8px; }
.comp-select {
  padding: 8px 12px; border: 1px solid var(--border);
  border-radius: 8px; background: var(--bg);
  color: var(--text); font-size: 13px;
  cursor: pointer; outline: none;
}

.comp-stats { font-size: 13px; color: var(--text-weak); }

.comp-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 12px;
}

.skeleton-card {
  background: var(--bg); border: 1px solid var(--border);
  border-radius: 10px; padding: 12px; text-align: center;
}
.skeleton-img {
  width: 80px; height: 80px; margin: 0 auto 8px;
  border-radius: 8px;
  background: linear-gradient(90deg, var(--border) 25%, var(--bg-alt) 50%, var(--border) 75%);
  background-size: 200% 100%; animation: shimmer 1.5s infinite;
}
.skeleton-text {
  height: 14px; width: 60%; margin: 0 auto;
  border-radius: 4px;
  background: linear-gradient(90deg, var(--border) 25%, var(--bg-alt) 50%, var(--border) 75%);
  background-size: 200% 100%; animation: shimmer 1.5s infinite;
}
@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

.comp-empty { text-align: center; padding: 40px; color: var(--text-weak); }

.comp-pagination {
  display: flex; justify-content: center; align-items: center; gap: 16px;
  padding: 16px 0;
}
.page-btn {
  padding: 8px 16px; border: 1px solid var(--border);
  border-radius: 8px; background: var(--bg);
  color: var(--text); font-size: 13px; cursor: pointer;
  transition: all 0.15s;
}
.page-btn:hover:not(:disabled) { background: var(--bg-alt); }
.page-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.page-info { font-size: 13px; color: var(--text-weak); }

@media (max-width: 600px) {
  .comp-grid { grid-template-columns: repeat(auto-fill, minmax(110px, 1fr)); gap: 8px; }
  .comp-toolbar { flex-direction: column; }
  .comp-filters { width: 100%; }
  .comp-select { flex: 1; }
}
</style>
