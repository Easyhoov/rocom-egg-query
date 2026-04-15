<script setup>
import { ref, onMounted, watch } from 'vue'
import QueryForm from '../components/QueryForm.vue'
import ResultCard from '../components/ResultCard.vue'

const height = ref('')
const weight = ref('')
const eggType = ref('all')
const loading = ref(false)
const results = ref([])
const summary = ref(null)
const error = ref('')
const hasSearched = ref(false)

function parseEggType(val) {
  if (val === 'normal') return 0
  if (val === 'precious') return 1
  return null
}

async function doSearch() {
  const h = parseFloat(height.value)
  const w = parseFloat(weight.value)
  if (!h || h <= 0 || !w || w <= 0) {
    error.value = '请输入有效的身高和重量（大于0）'
    return
  }

  loading.value = true
  error.value = ''
  hasSearched.value = true

  try {
    const params = new URLSearchParams({
      height: String(h),
      weight: String(w),
    })
    if (eggType.value === 'normal') params.set('precious', '0')
    else if (eggType.value === 'precious') params.set('precious', '1')
    const res = await fetch(`/api/query?${params}`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const data = await res.json()
    results.value = data.results || []
    summary.value = data.tier_counts || null

    // Update URL hash for sharing
    const hash = `#h=${h}&w=${w}`
    if (window.location.hash !== hash) {
      window.history.replaceState(null, '', hash)
    }
  } catch (e) {
    error.value = `查询失败: ${e.message}`
    results.value = []
    summary.value = null
  } finally {
    loading.value = false
  }
}

// Read initial values from URL hash
onMounted(() => {
  const hash = window.location.hash
  if (hash) {
    const params = new URLSearchParams(hash.slice(1))
    if (params.get('h')) height.value = params.get('h')
    if (params.get('w')) weight.value = params.get('w')
    if (height.value && weight.value) doSearch()
  }
})
</script>

<template>
  <div class="egg-query">
    <!-- Query Form -->
    <QueryForm
      :modelHeight="height"
      :modelWeight="weight"
      :eggType="eggType"
      :loading="loading"
      @update:modelHeight="height = $event"
      @update:modelWeight="weight = $event"
      @update:eggType="eggType = $event"
      @search="doSearch"
    />

    <!-- Error -->
    <div v-if="error" class="error-msg">
      {{ error }}
    </div>

    <!-- Summary badges -->
    <div v-if="summary" class="summary-bar">
      <span class="summary-badge summary-badge--exact">精准 {{ summary.exact }}</span>
      <span class="summary-badge summary-badge--tol1">容差1 {{ summary.tolerance1 }}</span>
      <span class="summary-badge summary-badge--tol2">容差2 {{ summary.tolerance2 }}</span>
      <span v-if="summary.nearest" class="summary-badge summary-badge--nearest">近似 {{ summary.nearest }}</span>
    </div>

    <!-- Loading skeletons -->
    <div v-if="loading" class="skeleton-list">
      <div class="skeleton-card" v-for="i in 3" :key="i">
        <div class="skeleton-line skeleton-line--title"></div>
        <div class="skeleton-line skeleton-line--short"></div>
        <div class="skeleton-line skeleton-line--bar"></div>
        <div class="skeleton-line skeleton-line--medium"></div>
      </div>
    </div>

    <!-- Results -->
    <div v-if="!loading && results.length" class="results-list">
      <ResultCard v-for="(pet, idx) in results" :key="pet.name + '-' + idx" :pet="pet" />
    </div>

    <!-- Empty state -->
    <div v-if="!loading && hasSearched && !results.length && !error" class="empty-state">
      <p>😅 没有找到匹配结果</p>
      <p class="empty-hint">试试 0.24m / 1.60kg 看看</p>
    </div>
  </div>
</template>

<style scoped>
.egg-query {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.error-msg {
  background: color-mix(in srgb, var(--warning) 10%, transparent);
  color: var(--warning);
  padding: 12px 16px;
  border-radius: var(--radius-sm);
  font-size: 14px;
}

.summary-bar {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.summary-badge {
  padding: 4px 12px;
  border-radius: var(--radius-pill);
  font-size: 13px;
  font-weight: 600;
  color: #fff;
}

.summary-badge--exact { background: var(--tier-exact); }
.summary-badge--tol1 { background: var(--tier-tolerance1); }
.summary-badge--tol2 { background: var(--tier-tolerance2); }
.summary-badge--nearest { background: var(--tier-nearest); }

/* Skeleton loading */
.skeleton-list { display: flex; flex-direction: column; gap: 12px; }
.skeleton-card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-card);
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.skeleton-line {
  height: 14px;
  border-radius: 4px;
  background: linear-gradient(90deg, var(--border) 25%, var(--bg-alt) 50%, var(--border) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}
.skeleton-line--title { width: 40%; height: 20px; }
.skeleton-line--short { width: 30%; }
.skeleton-line--bar { width: 100%; height: 6px; }
.skeleton-line--medium { width: 60%; }

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: var(--text-weak);
}
.empty-state p:first-child { font-size: 18px; margin-bottom: 8px; }
.empty-hint { font-size: 14px; }
@media (max-width: 600px) {
  .egg-query { gap: 12px; }
  .summary-badge { font-size: 12px; padding: 3px 10px; }
  .skeleton-card { padding: 12px; }
  .empty-state { padding: 30px 16px; }
}
</style>
