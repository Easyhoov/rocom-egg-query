<script setup>
import { ref, watch, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

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
let searchTimer = null

async function loadSpirits() {
  loading.value = true
  try {
    const params = new URLSearchParams()
    if (search.value) params.set('q', search.value)
    if (selectedAttr.value) params.set('attribute', selectedAttr.value)
    if (selectedEggGroup.value) params.set('egg_group', selectedEggGroup.value)
    params.set('page', String(page.value))
    params.set('page_size', String(pageSize))

    const res = await fetch(`/api/spirits?${params}`)
    const data = await res.json()
    spirits.value = data.items || []
    total.value = data.total || 0
    totalPages.value = data.total_pages || 1
  } catch (e) {
    console.error('加载失败:', e)
  } finally {
    loading.value = false
  }
}

async function loadEggGroups() {
  try {
    const res = await fetch('/api/official-egg-groups')
    const data = await res.json()
    eggGroups.value = data.groups || []
  } catch (e) { /* ignore */ }
}

function syncUrl() {
  const q = {}
  if (search.value) q.q = search.value
  if (selectedAttr.value) q.attribute = selectedAttr.value
  if (selectedEggGroup.value) q.egg_group = selectedEggGroup.value
  if (page.value > 1) q.page = String(page.value)
  router.replace({ query: q })
}

function onSearchInput() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
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

function clearAttr() {
  selectedAttr.value = ''
  onFilterChange()
}

function clearEggGroup() {
  selectedEggGroup.value = ''
  onFilterChange()
}

function goToPage(p) {
  page.value = p
  loadSpirits()
  syncUrl()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const pageWindow = computed(() => {
  const pages = []
  const t = totalPages.value
  const c = page.value
  if (t <= 7) { for (let i = 1; i <= t; i++) pages.push(i); return pages }
  pages.push(1)
  if (c > 3) pages.push('...')
  for (let i = Math.max(2, c - 1); i <= Math.min(t - 1, c + 1); i++) pages.push(i)
  if (c < t - 2) pages.push('...')
  pages.push(t)
  return pages
})

onMounted(() => { loadEggGroups(); loadSpirits() })
</script>

<template>
  <div class="comp">
    <div class="comp__box">
      <!-- 标题 -->
      <div class="comp__hd">
        <div class="comp__hd-row">
          <h1>📖 精灵图鉴</h1>
          <a href="/" class="comp__back">← 首页</a>
        </div>
        <p class="comp__sub">共 {{ total }} 只精灵{{ loading ? ' · 加载中...' : '' }}</p>
      </div>

      <!-- 搜索 -->
      <div class="comp__card">
        <input
          v-model="search"
          @input="onSearchInput"
          placeholder="搜索精灵名称或编号..."
          class="comp__input"
        />
      </div>

      <!-- 属性筛选 -->
      <div class="comp__card">
        <div class="comp__label">属性</div>
        <div class="comp__tags">
          <span
            class="comp__tag"
            :class="{ 'comp__tag--on': !selectedAttr }"
            @click="clearAttr"
          >全部</span>
          <span
            v-for="attr in attributes"
            :key="attr"
            class="comp__tag"
            :class="{ 'comp__tag--on': selectedAttr === attr }"
            @click="selectedAttr = attr; onFilterChange()"
          >{{ attr }}</span>
        </div>
      </div>

      <!-- 蛋组筛选 -->
      <div class="comp__card" v-if="eggGroups.length">
        <div class="comp__label">蛋组</div>
        <div class="comp__tags">
          <span
            class="comp__tag"
            :class="{ 'comp__tag--on': !selectedEggGroup }"
            @click="clearEggGroup"
          >全部</span>
          <span
            v-for="g in eggGroups"
            :key="g.egg_group_name"
            class="comp__tag"
            :class="{ 'comp__tag--on': selectedEggGroup === g.egg_group_name }"
            @click="selectedEggGroup = g.egg_group_name; onFilterChange()"
          >{{ g.egg_group_icon }} {{ g.egg_group_name }}</span>
        </div>
      </div>

      <!-- 精灵卡片网格 -->
      <div class="comp__grid">
        <router-link
          v-for="s in spirits"
          :key="s.spirit_id"
          :to="`/compendium/${s.spirit_id}`"
          class="comp__pet"
        >
          <div class="comp__pet-badge" v-if="!s.can_breed" style="background:#e74c3c">不可孵蛋</div>
          <div class="comp__pet-img">
            <img v-if="s.image" :src="s.image" :alt="s.display_name" loading="lazy" />
            <span v-else class="comp__pet-noimg">❓</span>
          </div>
          <div class="comp__pet-no">{{ s.spirit_no }}</div>
          <div class="comp__pet-name">{{ s.display_name }}</div>
          <div class="comp__pet-tags">
            <span v-if="s.primary_attribute" class="comp__pet-tag" style="background:#667eea15;color:#667eea">{{ s.primary_attribute }}</span>
            <span v-for="g in (s.egg_groups || []).slice(0,2)" :key="g" class="comp__pet-tag" style="background:#f5f0ff;color:#764ba2">{{ g }}</span>
          </div>
        </router-link>
      </div>

      <!-- 空状态 -->
      <div v-if="!loading && spirits.length === 0" class="comp__empty">
        <div class="comp__empty-icon">🔍</div>
        <p>没有找到匹配的精灵</p>
      </div>

      <!-- 分页 -->
      <div v-if="totalPages > 1" class="comp__pager">
        <button v-if="page > 1" @click="goToPage(page - 1)" class="comp__page-btn">← 上一页</button>
        <template v-for="p in pageWindow" :key="p">
          <span v-if="p === '...'" class="comp__page-dots">…</span>
          <button v-else @click="goToPage(p)" class="comp__page-btn" :class="{ 'comp__page-btn--on': p === page }">{{ p }}</button>
        </template>
        <button v-if="page < totalPages" @click="goToPage(page + 1)" class="comp__page-btn">下一页 →</button>
      </div>

      <div class="comp__ft">洛克王国：世界 · 精灵图鉴</div>
    </div>
  </div>
</template>

<style scoped>
.comp {
  min-height: 100vh;
  background: linear-gradient(180deg, #e8f0fe 0%, #f5f0ff 50%, #fff 100%);
  padding: 16px;
  padding-bottom: env(safe-area-inset-bottom, 16px);
}
.comp__box { max-width: 420px; margin: 0 auto; }
.comp__hd { text-align: center; padding: 16px 0 12px; }
.comp__hd-row { display: flex; align-items: center; justify-content: center; gap: 12px; position: relative; }
.comp__hd h1 { font-size: 20px; color: #1a1a2e; font-weight: 700; }
.comp__back { font-size: 13px; color: #667eea; text-decoration: none; position: absolute; right: 0; }
.comp__sub { font-size: 12px; color: #aaa; margin-top: 4px; }

.comp__card {
  background: #fff;
  border-radius: 14px;
  padding: 14px;
  box-shadow: 0 2px 12px rgba(0,0,0,.05);
  margin-bottom: 10px;
}
.comp__input {
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
.comp__input:focus { border-color: #667eea; background: #fff; }
.comp__label { font-size: 12px; color: #aaa; font-weight: 600; margin-bottom: 8px; }
.comp__tags { display: flex; flex-wrap: wrap; gap: 6px; }
.comp__tag {
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
.comp__tag--on { border-color: #667eea; background: #667eea; color: #fff; }

.comp__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  margin-top: 12px;
}
.comp__pet {
  background: #fff;
  border-radius: 14px;
  padding: 10px 6px 8px;
  text-align: center;
  text-decoration: none;
  color: inherit;
  box-shadow: 0 2px 8px rgba(0,0,0,.04);
  transition: .2s;
  position: relative;
  overflow: hidden;
}
.comp__pet:active { transform: scale(.96); }
.comp__pet-badge {
  position: absolute;
  top: 4px;
  right: 4px;
  font-size: 9px;
  padding: 1px 5px;
  border-radius: 6px;
  color: #fff;
  font-weight: 600;
}
.comp__pet-img {
  width: 56px;
  height: 56px;
  margin: 0 auto 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9ff;
  border-radius: 50%;
}
.comp__pet-img img { width: 48px; height: 48px; object-fit: contain; }
.comp__pet-noimg { font-size: 24px; opacity: .3; }
.comp__pet-no { font-size: 10px; color: #bbb; }
.comp__pet-name { font-size: 13px; font-weight: 600; color: #1a1a2e; margin: 2px 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.comp__pet-tags { display: flex; gap: 3px; justify-content: center; flex-wrap: wrap; }
.comp__pet-tag { font-size: 9px; padding: 1px 5px; border-radius: 6px; }

.comp__empty { text-align: center; padding: 40px 0; color: #ccc; }
.comp__empty-icon { font-size: 48px; margin-bottom: 8px; }

.comp__pager { display: flex; align-items: center; justify-content: center; gap: 6px; margin: 20px 0; flex-wrap: wrap; }
.comp__page-btn {
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 13px;
  border: 1.5px solid #e8e8e8;
  background: #fff;
  color: #666;
  cursor: pointer;
  transition: .2s;
}
.comp__page-btn--on { border-color: #667eea; background: #667eea; color: #fff; font-weight: 600; }
.comp__page-dots { color: #ccc; padding: 0 4px; }

.comp__ft { text-align: center; padding: 20px 0 8px; font-size: 11px; color: #ccc; }
</style>
