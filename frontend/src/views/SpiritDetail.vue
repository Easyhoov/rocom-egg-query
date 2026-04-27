<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getAttrIcon } from '../utils/attrIcons'

const route = useRoute()
const router = useRouter()
const spirit = ref(null)
const loading = ref(true)
const showShiny = ref(false)
const spiritId = computed(() => route.params.id)

// 六维雷达图配置
const statOrder = ['hp', 'attack', 'defense', 'magic_defense', 'magic_attack', 'speed']
const statLabels = {
  hp: { label: '生命', color: '#4caf50' },
  attack: { label: '物攻', color: '#e74c3c' },
  defense: { label: '物防', color: '#3498db' },
  magic_defense: { label: '魔防', color: '#f39c12' },
  magic_attack: { label: '魔攻', color: '#9b59b6' },
  speed: { label: '速度', color: '#1abc9c' },
}

const RADAR_CX = 150, RADAR_CY = 150, RADAR_R = 110
const MAX_STAT = 150
const GRID_LEVELS = 5

// 每个轴的角度（从顶部顺时针，6轴60°间隔）
function axisAngle(i) {
  return (-90 + i * 60) * Math.PI / 180
}

function polarToXY(i, r) {
  const a = axisAngle(i)
  return { x: RADAR_CX + r * Math.cos(a), y: RADAR_CY + r * Math.sin(a) }
}

// 网格多边形点
function gridPoints(level) {
  const r = RADAR_R * level / GRID_LEVELS
  return Array.from({ length: 6 }, (_, i) => {
    const p = polarToXY(i, r)
    return `${p.x},${p.y}`
  }).join(' ')
}

// 轴线端点
function axisEnd(i) {
  return polarToXY(i, RADAR_R)
}

// 数据多边形点
const radarPoints = computed(() => {
  if (!spirit.value) return ''
  return statOrder.map((key, i) => {
    const val = spirit.value[key] || 0
    const r = RADAR_R * Math.min(val / MAX_STAT, 1)
    const p = polarToXY(i, r)
    return `${p.x},${p.y}`
  }).join(' ')
})

// 标签位置（稍微超出雷达半径）
function labelPos(i) {
  const p = polarToXY(i, RADAR_R + 24)
  return p
}

function labelAnchor(i) {
  const a = axisAngle(i)
  const cos = Math.cos(a)
  if (Math.abs(cos) < 0.1) return 'middle'
  return cos > 0 ? 'start' : 'end'
}

const stats = computed(() => {
  if (!spirit.value) return []
  return statOrder.map(key => ({
    key,
    ...statLabels[key],
    value: spirit.value[key] || 0
  }))
})

async function fetchDetail() {
  loading.value = true
  try {
    const res = await fetch(`/api/spirits/${spiritId.value}`)
    const data = await res.json()
    if (data.success) spirit.value = data.spirit
  } catch (e) {
    console.error('获取精灵详情失败:', e)
  } finally {
    loading.value = false
  }
}

function goBack() {
  if (window.history.length > 1) router.back()
  else router.push('/compendium')
}

onMounted(fetchDetail)
watch(spiritId, fetchDetail)
</script>

<template>
  <div class="detail">
    <div class="detail__box">
      <!-- 返回 -->
      <div class="detail__nav">
        <a href="javascript:void(0)" @click="goBack" class="detail__back">← 返回图鉴</a>
        <span v-if="spirit" class="detail__nav-no">{{ spirit.spirit_no }}</span>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="detail__loading">
        <div class="detail__spinner"></div>
        <p>加载中...</p>
      </div>

      <!-- Not Found -->
      <div v-else-if="!spirit" class="detail__empty">
        <p class="detail__empty-icon">❌</p>
        <p>精灵不存在</p>
        <a href="/compendium" class="detail__btn">返回图鉴</a>
      </div>

      <template v-else>
        <!-- 基础信息卡片 -->
        <div class="detail__card">
          <div class="detail__hero">
            <div class="detail__img">
              <img v-if="spirit.has_shiny_variant && showShiny && spirit.shiny_image" :src="spirit.shiny_image" :alt="spirit.base_name + ' 异色'" />
              <img v-else-if="spirit.image" :src="spirit.image" :alt="spirit.base_name" />
              <span v-else class="detail__noimg">❓</span>
              <button v-if="spirit.has_shiny_variant && spirit.shiny_image" class="detail__shiny-toggle" @click="showShiny = !showShiny">
                {{ showShiny ? '✨ 异色' : '🥚 普通' }}
              </button>
            </div>
            <div class="detail__info">
              <h1>{{ spirit.display_name || spirit.base_name }}</h1>
              <div class="detail__tags">
                <span v-if="spirit.primary_attribute" class="detail__tag" style="background:#667eea;color:#fff">
                  <img v-if="getAttrIcon(spirit.primary_attribute)" :src="getAttrIcon(spirit.primary_attribute)" class="detail__tag-icon" />
                  {{ spirit.primary_attribute }}
                </span>
                <span v-if="spirit.secondary_attribute" class="detail__tag" style="background:#4caf50;color:#fff">
                  <img v-if="getAttrIcon(spirit.secondary_attribute)" :src="getAttrIcon(spirit.secondary_attribute)" class="detail__tag-icon" />
                  {{ spirit.secondary_attribute }}
                </span>
                <span v-if="spirit.form_name" class="detail__tag" style="background:#f5f0ff;color:#764ba2">{{ spirit.form_name }}</span>
                <span v-if="!spirit.can_breed" class="detail__tag" style="background:#fee;color:#e74c3c">不可孵蛋</span>
                <span v-if="spirit.has_shiny_variant" class="detail__tag" style="background:#f5f0ff;color:#9b59b6">✨ 异色</span>
              </div>
              <div class="detail__meta">
                <span v-if="spirit.height_text">📏 {{ spirit.height_text }}</span>
                <span v-if="spirit.weight_text">⚖️ {{ spirit.weight_text }}</span>
                <span v-if="spirit.race_total" class="detail__race">⭐ {{ spirit.race_total }}</span>
              </div>
              <div v-if="spirit.egg_groups?.length" class="detail__egg-groups">
                <span class="detail__egg-label">蛋组：</span>
                <span v-for="g in spirit.egg_groups" :key="g" class="detail__egg-tag">{{ g }}</span>
              </div>
            </div>
          </div>
          <p v-if="spirit.description" class="detail__desc">{{ spirit.description }}</p>
        </div>

        <!-- 特性 -->
        <div v-if="spirit.trait_name" class="detail__card">
          <h2 class="detail__card-title">💡 特性</h2>
          <div class="detail__trait">
            <span class="detail__trait-name">{{ spirit.trait_name }}</span>
            <span v-if="spirit.trait_effect" class="detail__trait-desc">{{ spirit.trait_effect }}</span>
          </div>
        </div>

        <!-- 种族值 -->
        <div v-if="spirit.race_total" class="detail__card">
          <h2 class="detail__card-title">📊 种族值 <span class="detail__card-sub">总和 {{ spirit.race_total }}</span></h2>
          <div class="detail__radar">
            <svg viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg">
              <!-- 网格线 -->
              <polygon
                v-for="lv in GRID_LEVELS"
                :key="'g' + lv"
                :points="gridPoints(lv)"
                fill="none"
                stroke="#e8e8f0"
                stroke-width="1"
              />
              <!-- 轴线 -->
              <line
                v-for="i in 6"
                :key="'a' + i"
                :x1="RADAR_CX" :y1="RADAR_CY"
                :x2="axisEnd(i - 1).x" :y2="axisEnd(i - 1).y"
                stroke="#e0e0e8"
                stroke-width="1"
              />
              <!-- 数据区域 -->
              <polygon
                v-if="radarPoints"
                :points="radarPoints"
                fill="rgba(102, 126, 234, 0.2)"
                stroke="#667eea"
                stroke-width="2"
              />
              <!-- 数据点 -->
              <circle
                v-for="(s, i) in stats"
                :key="'d' + s.key"
                :cx="polarToXY(i, RADAR_R * Math.min(s.value / MAX_STAT, 1)).x"
                :cy="polarToXY(i, RADAR_R * Math.min(s.value / MAX_STAT, 1)).y"
                r="4"
                :fill="s.color"
                stroke="#fff"
                stroke-width="1.5"
              />
              <!-- 标签 -->
              <text
                v-for="(s, i) in stats"
                :key="'l' + s.key"
                :x="labelPos(i).x"
                :y="labelPos(i).y"
                :text-anchor="labelAnchor(i)"
                dominant-baseline="middle"
                font-size="12"
                font-weight="600"
                :fill="s.color"
              >{{ s.label }} {{ s.value }}</text>
            </svg>
          </div>
        </div>

        <!-- 进化链 -->
        <div v-if="spirit.evolution_chain?.length > 1" class="detail__card">
          <h2 class="detail__card-title">🔄 进化链</h2>
          <div class="detail__evo">
            <template v-for="(evo, idx) in spirit.evolution_chain" :key="evo.spirit_id">
              <div v-if="idx > 0" class="detail__evo-arrow">
                <span>→</span>
                <span v-if="evo.evolution_level_text" class="detail__evo-lv">Lv.{{ evo.evolution_level_text }}</span>
              </div>
              <router-link
                :to="`/compendium/${evo.spirit_id}`"
                class="detail__evo-node"
                :class="{ 'detail__evo-node--current': evo.spirit_id === spirit.spirit_id }"
              >
                <div class="detail__evo-img">
                  <img v-if="evo.image" :src="evo.image" :alt="evo.base_name" loading="lazy" />
                  <span v-else>❓</span>
                </div>
                <span class="detail__evo-name">{{ evo.base_name }}</span>
                <span class="detail__evo-no">{{ evo.spirit_no }}</span>
              </router-link>
            </template>
          </div>
        </div>

        <!-- 其他形态 -->
        <div v-if="spirit.forms?.length > 1" class="detail__card">
          <h2 class="detail__card-title">🎭 其他形态</h2>
          <div class="detail__forms">
            <router-link
              v-for="form in spirit.forms"
              :key="form.spirit_id"
              :to="`/compendium/${form.spirit_id}`"
              class="detail__form-tag"
              :class="{ 'detail__form-tag--current': form.spirit_id === spirit.spirit_id }"
            >
              {{ form.display_name || form.base_name }}
              <span v-if="form.form_name" class="detail__form-sub">({{ form.form_name }})</span>
            </router-link>
          </div>
        </div>

        <!-- 出没地点 -->
        <div v-if="spirit.locations?.length" class="detail__card">
          <h2 class="detail__card-title">📍 出没地点</h2>
          <div class="detail__locations">
            <span v-for="loc in spirit.locations" :key="loc" class="detail__loc">{{ loc }}</span>
          </div>
        </div>
      </template>

      <div class="detail__ft">洛克王国：世界 · 精灵详情</div>
    </div>
  </div>
</template>

<style scoped>
.detail {
  min-height: 100vh;
  background: linear-gradient(180deg, #e8f0fe 0%, #f5f0ff 50%, #fff 100%);
  padding: 16px 16px 80px;
}
.detail__box { max-width: 420px; margin: 0 auto; }
.detail__nav { display: flex; align-items: center; justify-content: space-between; padding: 8px 0 12px; }
.detail__back { font-size: 13px; color: #667eea; text-decoration: none; }
.detail__nav-no { font-size: 12px; color: #bbb; }

.detail__card {
  background: #fff;
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,.06);
  margin-bottom: 12px;
}
.detail__card-title {
  font-size: 15px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 12px;
}
.detail__card-sub { font-size: 12px; color: #667eea; font-weight: 400; margin-left: 6px; }

.detail__hero { display: flex; gap: 14px; align-items: flex-start; }
.detail__img {
  width: 100px; height: 100px; flex-shrink: 0; position: relative;
  display: flex; align-items: center; justify-content: center;
  background: #f8f9ff; border-radius: 14px; overflow: visible;
}
.detail__img img { width: 88px; height: 88px; object-fit: contain; }
.detail__noimg { font-size: 40px; opacity: .3; }
.detail__shiny-toggle {
  position: absolute; bottom: -8px; left: 50%; transform: translateX(-50%);
  font-size: 10px; padding: 2px 8px; border-radius: 8px;
  background: #fff8e1; color: #f57f17; border: 1px solid #ffe082;
  cursor: pointer; white-space: nowrap; font-weight: 600;
}
.detail__shiny-toggle:active { transform: translateX(-50%) scale(.95); }
.detail__info { flex: 1; min-width: 0; }
.detail__info h1 { font-size: 20px; font-weight: 700; color: #1a1a2e; margin-bottom: 6px; }
.detail__tags { display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 8px; }
.detail__tag { font-size: 11px; padding: 2px 8px; border-radius: 10px; font-weight: 600; display: inline-flex; align-items: center; gap: 3px; }
.detail__tag-icon { width: 14px; height: 14px; }
.detail__meta { font-size: 12px; color: #888; display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 6px; }
.detail__race { color: #f39c12; font-weight: 600; }
.detail__egg-groups { font-size: 12px; }
.detail__egg-label { color: #aaa; }
.detail__egg-tag { display: inline-block; font-size: 11px; padding: 1px 6px; border-radius: 6px; background: #f5f0ff; color: #764ba2; margin-left: 4px; }
.detail__desc { font-size: 13px; color: #999; line-height: 1.6; margin-top: 10px; padding-top: 10px; border-top: 1px solid #f0f0f0; }

.detail__trait { display: flex; align-items: flex-start; gap: 10px; flex-wrap: wrap; }
.detail__trait-name { font-size: 13px; font-weight: 600; background: #fff8e1; color: #f57f17; padding: 4px 10px; border-radius: 8px; }
.detail__trait-desc { font-size: 13px; color: #888; line-height: 1.6; flex: 1; min-width: 200px; }

.detail__radar { display: flex; justify-content: center; }
.detail__radar svg { width: 100%; max-width: 300px; }

.detail__evo { display: flex; align-items: center; flex-wrap: wrap; gap: 4px; }
.detail__evo-arrow { display: flex; flex-direction: column; align-items: center; padding: 0 2px; }
.detail__evo-arrow span:first-child { color: #ccc; font-size: 16px; }
.detail__evo-lv { font-size: 10px; color: #bbb; }
.detail__evo-node {
  display: flex; flex-direction: column; align-items: center;
  padding: 8px; border-radius: 10px; text-decoration: none; color: inherit;
  transition: .2s; min-width: 72px;
}
.detail__evo-node:active { transform: scale(.95); }
.detail__evo-node--current { background: #f5f0ff; box-shadow: 0 0 0 2px #667eea40; }
.detail__evo-img {
  width: 48px; height: 48px; display: flex; align-items: center; justify-content: center;
  background: #f8f9ff; border-radius: 50%; margin-bottom: 4px; overflow: hidden;
}
.detail__evo-img img { width: 40px; height: 40px; object-fit: contain; }
.detail__evo-name { font-size: 12px; font-weight: 600; color: #1a1a2e; }
.detail__evo-no { font-size: 10px; color: #ccc; }

.detail__forms { display: flex; flex-wrap: wrap; gap: 6px; }
.detail__form-tag {
  padding: 6px 12px; border-radius: 10px; font-size: 13px; font-weight: 500;
  background: #f8f9ff; color: #666; text-decoration: none; border: 1.5px solid #e8e8e8; transition: .2s;
}
.detail__form-tag--current { background: #667eea; color: #fff; border-color: #667eea; }
.detail__form-sub { font-size: 11px; color: inherit; opacity: .6; }

.detail__locations { display: flex; flex-wrap: wrap; gap: 6px; }
.detail__loc { font-size: 12px; padding: 4px 10px; border-radius: 8px; background: #f0f2ff; color: #667eea; }

.detail__loading { text-align: center; padding: 60px 0; color: #ccc; }
.detail__spinner {
  width: 32px; height: 32px; border: 3px solid #e8e8e8; border-top-color: #667eea;
  border-radius: 50%; animation: spin .8s linear infinite; margin: 0 auto 12px;
}
@keyframes spin { to { transform: rotate(360deg); } }
.detail__empty { text-align: center; padding: 60px 0; color: #ccc; }
.detail__empty-icon { font-size: 48px; margin-bottom: 8px; }
.detail__btn { display: inline-block; margin-top: 12px; padding: 8px 20px; background: #667eea; color: #fff; border-radius: 10px; text-decoration: none; font-size: 14px; }

.detail__ft { text-align: center; padding: 20px 0 8px; font-size: 11px; color: #ccc; }
</style>
