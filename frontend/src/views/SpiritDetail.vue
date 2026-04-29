<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getAttrIcon } from '../utils/attrIcons'

const route = useRoute()
const router = useRouter()
const spirit = ref(null)
const skills = ref([])
const matchups = ref(null)
const loading = ref(true)
const skillsLoading = ref(true)
const showShiny = ref(false)
const spiritId = computed(() => route.params.id)

// 属性名称映射： skills_all.csv 中的"光系" → "光"
const ATTR_NAME_MAP = {
  '光系': '光', '火系': '火', '水系': '水', '草系': '草', '冰系': '冰',
  '地系': '地', '龙系': '龙', '电系': '电', '毒系': '毒', '虫系': '虫',
  '武系': '武', '翼系': '翼', '萌系': '萌', '幽系': '幽', '恶系': '恶',
  '机械系': '机械', '幻系': '幻', '普通系': '普通',
}

// 技能类型颜色
const SKILL_TYPE_STYLES = {
  '物理': { bg: '#fee8e8', color: '#e74c3c', label: '物' },
  '魔法': { bg: '#e8e8ff', color: '#667eea', label: '魔' },
  '防御': { bg: '#e8f5e9', color: '#4caf50', label: '防' },
  '状态': { bg: '#fff3e0', color: '#ff9800', label: '变' },
}

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

function axisAngle(i) {
  return (-90 + i * 60) * Math.PI / 180
}
function polarToXY(i, r) {
  const a = axisAngle(i)
  return { x: RADAR_CX + r * Math.cos(a), y: RADAR_CY + r * Math.sin(a) }
}
function gridPoints(level) {
  const r = RADAR_R * level / GRID_LEVELS
  return Array.from({ length: 6 }, (_, i) => {
    const p = polarToXY(i, r)
    return `${p.x},${p.y}`
  }).join(' ')
}
function axisEnd(i) {
  return polarToXY(i, RADAR_R)
}
const radarPoints = computed(() => {
  if (!spirit.value) return ''
  return statOrder.map((key, i) => {
    const val = spirit.value[key] || 0
    const r = RADAR_R * Math.min(val / MAX_STAT, 1)
    const p = polarToXY(i, r)
    return `${p.x},${p.y}`
  }).join(' ')
})
function labelPos(i) {
  return polarToXY(i, RADAR_R + 24)
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
    key, ...statLabels[key], value: spirit.value[key] || 0
  }))
})

// 技能去重 + 排序：按耗能升序
const sortedSkills = computed(() => {
  const seen = new Set()
  return skills.value.filter(s => {
    const key = s.name
    if (seen.has(key)) return false
    seen.add(key)
    return true
  }).sort((a, b) => a.cost - b.cost || a.name.localeCompare(b.name))
})

// 技能按类型分组
const groupedSkills = computed(() => {
  const groups = { '物理': [], '魔法': [], '防御': [], '状态': [] }
  for (const s of sortedSkills.value) {
    const t = SKILL_TYPE_STYLES[s.type] ? s.type : '状态'
    groups[t].push(s)
  }
  return Object.entries(groups).filter(([_, list]) => list.length > 0)
})

// 属性名映射（去掉"系"后缀）
function formatAttr(attr) {
  return ATTR_NAME_MAP[attr] || attr?.replace('系', '') || attr || ''
}

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

async function fetchSkills() {
  skillsLoading.value = true
  try {
    const res = await fetch(`/api/spirits/${spiritId.value}/skills`)
    const data = await res.json()
    if (data.success) skills.value = data.skills || []
  } catch (e) {
    console.error('获取技能列表失败:', e)
    skills.value = []
  } finally {
    skillsLoading.value = false
  }
}

async function fetchMatchups() {
  try {
    const res = await fetch(`/api/spirits/${spiritId.value}/type-matchups`)
    const data = await res.json()
    if (data.success) matchups.value = data
  } catch (e) {
    console.error('获取属性克制失败:', e)
  }
}

function goBack() {
  if (window.history.length > 1) router.back()
  else router.push('/compendium')
}

onMounted(() => {
  fetchDetail()
  fetchSkills()
  fetchMatchups()
})
watch(spiritId, () => {
  fetchDetail()
  fetchSkills()
  fetchMatchups()
})
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
                <span v-if="spirit.primary_attribute" class="detail__tag" style="background:#8b3dff;color:#fff">
                  <img v-if="getAttrIcon(spirit.primary_attribute)" :src="getAttrIcon(spirit.primary_attribute)" class="detail__tag-icon" />
                  {{ spirit.primary_attribute }}
                </span>
                <span v-if="spirit.secondary_attribute" class="detail__tag" style="background:#4caf50;color:#fff">
                  <img v-if="getAttrIcon(spirit.secondary_attribute)" :src="getAttrIcon(spirit.secondary_attribute)" class="detail__tag-icon" />
                  {{ spirit.secondary_attribute }}
                </span>
                <span v-if="spirit.form_name" class="detail__tag" style="background:#f5f0ff;color:#8b3dff">{{ spirit.form_name }}</span>
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
              <polygon v-for="lv in GRID_LEVELS" :key="'g' + lv" :points="gridPoints(lv)" fill="none" stroke="#e8e8f0" stroke-width="1" />
              <!-- 轴线 -->
              <line v-for="i in 6" :key="'a' + i" :x1="RADAR_CX" :y1="RADAR_CY" :x2="axisEnd(i - 1).x" :y2="axisEnd(i - 1).y" stroke="#e0e0e8" stroke-width="1" />
              <!-- 数据区域 -->
              <polygon v-if="radarPoints" :points="radarPoints" fill="rgba(102, 126, 234, 0.2)" stroke="#8b3dff" stroke-width="2" />
              <!-- 数据点 -->
              <circle v-for="(s, i) in stats" :key="'d' + s.key" :cx="polarToXY(i, RADAR_R * Math.min(s.value / MAX_STAT, 1)).x" :cy="polarToXY(i, RADAR_R * Math.min(s.value / MAX_STAT, 1)).y" r="4" :fill="s.color" stroke="#fff" stroke-width="1.5" />
              <!-- 标签 -->
              <text v-for="(s, i) in stats" :key="'l' + s.key" :x="labelPos(i).x" :y="labelPos(i).y" :text-anchor="labelAnchor(i)" dominant-baseline="middle" font-size="12" font-weight="600" :fill="s.color">{{ s.label }} {{ s.value }}</text>
            </svg>
          </div>
        </div>

        <!-- 属性克制 -->
        <div v-if="matchups" class="detail__card detail__matchups">
          <h2 class="detail__card-title">⚔️ 属性克制</h2>
          <div class="detail__mu-row">
            <div v-if="matchups.strong_against?.length" class="detail__mu-group">
              <span class="detail__mu-label detail__mu-label--advantage">克制</span>
              <div class="detail__mu-tags">
                <span v-for="attr in matchups.strong_against" :key="'s-' + attr" class="detail__mu-tag detail__mu-tag--advantage">
                  <img v-if="getAttrIcon(attr)" :src="getAttrIcon(attr)" class="detail__mu-icon" />
                  {{ attr }}
                </span>
              </div>
            </div>
            <div v-if="matchups.weak_to?.length" class="detail__mu-group">
              <span class="detail__mu-label detail__mu-label--disadvantage">被克</span>
              <div class="detail__mu-tags">
                <span v-for="attr in matchups.weak_to" :key="'w-' + attr" class="detail__mu-tag detail__mu-tag--disadvantage">
                  <img v-if="getAttrIcon(attr)" :src="getAttrIcon(attr)" class="detail__mu-icon" />
                  {{ attr }}
                </span>
              </div>
            </div>
            <div v-if="matchups.resists?.length" class="detail__mu-group">
              <span class="detail__mu-label detail__mu-label--resist">抵抗</span>
              <div class="detail__mu-tags">
                <span v-for="attr in matchups.resists" :key="'r-' + attr" class="detail__mu-tag detail__mu-tag--resist">
                  <img v-if="getAttrIcon(attr)" :src="getAttrIcon(attr)" class="detail__mu-icon" />
                  {{ attr }}
                </span>
              </div>
            </div>
            <div v-if="matchups.resisted_by?.length" class="detail__mu-group">
              <span class="detail__mu-label detail__mu-label--weak">被抵抗</span>
              <div class="detail__mu-tags">
                <span v-for="attr in matchups.resisted_by" :key="'rb-' + attr" class="detail__mu-tag detail__mu-tag--weak">
                  <img v-if="getAttrIcon(attr)" :src="getAttrIcon(attr)" class="detail__mu-icon" />
                  {{ attr }}
                </span>
              </div>
            </div>
          </div>
          <div class="detail__mu-note">数据来源：BWiki</div>
        </div>

        <!-- 技能列表（两列卡片网格） -->
        <div v-if="skills.length > 0" class="detail__card">
          <h2 class="detail__card-title">⚡ 技能 <span class="detail__card-sub">共 {{ skills.length }} 个</span></h2>
          <div class="detail__skills-loading" v-if="skillsLoading">加载中...</div>
          <div v-else class="sk-grid">
            <div v-for="s in sortedSkills" :key="s.name" class="sk-card">
              <div class="sk-card__icon-wrap">
                <img v-if="s.icon_url" :src="s.icon_url" class="sk-card__icon" :alt="s.name" />
                <span v-else class="sk-card__icon-fallback">⚔️</span>
              </div>
              <div class="sk-card__body">
                <div class="sk-card__name">{{ s.name }}</div>
                <div class="sk-card__meta">
                  <span class="sk-card__cost" :class="'sk-card__cost--' + (formatAttr(s.attribute) || '')">
                    {{ s.cost }}
                  </span>
                  <span class="sk-card__type-badge" :style="{ background: (SKILL_TYPE_STYLES[s.type] || {}).bg || '#f5f5f5', color: (SKILL_TYPE_STYLES[s.type] || {}).color || '#888' }">
                    {{ (SKILL_TYPE_STYLES[s.type] || {}).label || '?' }}
                  </span>
                  <span v-if="s.power > 0" class="sk-card__power">{{ s.power }}</span>
                </div>
                <div v-if="s.effect" class="sk-card__effect">{{ s.effect }}</div>
              </div>
            </div>
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
              <router-link :to="`/compendium/${evo.spirit_id}`" class="detail__evo-node" :class="{ 'detail__evo-node--current': evo.spirit_id === spirit.spirit_id }">
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
            <router-link v-for="form in spirit.forms" :key="form.spirit_id" :to="`/compendium/${form.spirit_id}`" class="detail__form-tag" :class="{ 'detail__form-tag--current': form.spirit_id === spirit.spirit_id }">
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
  background: linear-gradient(180deg, #f0ecff 0%, #ffffff 100%);
  padding: 16px 16px 80px;
}
.detail__box { max-width: 420px; margin: 0 auto; }
.detail__nav { display: flex; align-items: center; justify-content: space-between; padding: 8px 0 12px; }
.detail__back { font-size: 13px; color: #8b3dff; text-decoration: none; }
.detail__nav-no { font-size: 12px; color: #bbb; }

.detail__card {
  background: #fff;
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 4px 16px rgba(15,16,21,0.08);
  margin-bottom: 12px;
}
.detail__card-title {
  font-size: 15px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 12px;
}
.detail__card-sub { font-size: 12px; color: #8b3dff; font-weight: 400; margin-left: 6px; }

.detail__hero { display: flex; gap: 14px; align-items: flex-start; }
.detail__img {
  width: 100px; height: 100px; flex-shrink: 0; position: relative;
  display: flex; align-items: center; justify-content: center;
  background: #f5f2ff; border-radius: 14px; overflow: visible;
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
.detail__egg-tag { display: inline-block; font-size: 11px; padding: 1px 6px; border-radius: 6px; background: #f5f0ff; color: #8b3dff; margin-left: 4px; }
.detail__desc { font-size: 13px; color: #999; line-height: 1.6; margin-top: 10px; padding-top: 10px; border-top: 1px solid #f0f0f0; }

.detail__trait { display: flex; align-items: flex-start; gap: 10px; flex-wrap: wrap; }
.detail__trait-name { font-size: 13px; font-weight: 600; background: #fff8e1; color: #f57f17; padding: 4px 10px; border-radius: 8px; }
.detail__trait-desc { font-size: 13px; color: #888; line-height: 1.6; flex: 1; min-width: 200px; }

.detail__radar { display: flex; justify-content: center; }
.detail__radar svg { width: 100%; max-width: 300px; }

/* 属性克制 */
.detail__mu-row { display: flex; flex-direction: column; gap: 8px; }
.detail__mu-group { display: flex; align-items: flex-start; gap: 8px; }
.detail__mu-label {
  font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 6px;
  flex-shrink: 0; min-width: 42px; text-align: center;
}
.detail__mu-label--advantage { background: #e8f5e9; color: #2e7d32; }
.detail__mu-label--disadvantage { background: #ffebee; color: #c62828; }
.detail__mu-label--resist { background: #e3f2fd; color: #1565c0; }
.detail__mu-label--weak { background: #f5f5f5; color: #888; }
.detail__mu-tags { display: flex; flex-wrap: wrap; gap: 4px; }
.detail__mu-tag {
  font-size: 11px; padding: 2px 8px; border-radius: 8px;
  display: inline-flex; align-items: center; gap: 3px; font-weight: 500;
}
.detail__mu-tag--advantage { background: #e8f5e9; color: #2e7d32; }
.detail__mu-tag--disadvantage { background: #ffebee; color: #c62828; }
.detail__mu-tag--resist { background: #e3f2fd; color: #1565c0; }
.detail__mu-tag--weak { background: #f5f5f5; color: #888; }
.detail__mu-icon { width: 14px; height: 14px; }
.detail__mu-note { font-size: 10px; color: #ccc; text-align: right; margin-top: 6px; }

/* 技能列表-两列卡片网格 */
.detail__skills-loading { text-align: center; padding: 20px 0; color: #ccc; font-size: 13px; }
.sk-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}
.sk-card {
  display: flex;
  gap: 8px;
  background: #fff;
  border: 1px solid #f0f0f0;
  border-radius: 12px;
  padding: 10px;
  min-height: 76px;
  position: relative;
}
.sk-card__icon-wrap {
  width: 44px;
  height: 44px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}
.sk-card__icon {
  width: 40px;
  height: 40px;
  object-fit: contain;
  border-radius: 6px;
}
.sk-card__icon-fallback {
  font-size: 22px;
  opacity: .3;
}
.sk-card__body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 3px;
}
.sk-card__name {
  font-size: 12px;
  font-weight: 600;
  color: #222;
  line-height: 1.3;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.sk-card__meta {
  display: flex;
  align-items: center;
  gap: 4px;
  flex-wrap: wrap;
}
.sk-card__cost {
  font-size: 10px;
  font-weight: 700;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.sk-card__cost--光 { background: #e8f5e9; color: #4caf50; }
.sk-card__cost--火 { background: #e8f5e9; color: #4caf50; }
.sk-card__cost--水 { background: #e3f2fd; color: #42a5f5; }
.sk-card__cost--草 { background: #e8f5e9; color: #4caf50; }
.sk-card__cost--冰 { background: #e3f2fd; color: #42a5f5; }
.sk-card__cost--电 { background: #e3f2fd; color: #42a5f5; }
.sk-card__cost--地 { background: #e8f5e9; color: #4caf50; }
.sk-card__cost--龙 { background: #e8f5e9; color: #4caf50; }
.sk-card__cost--毒 { background: #e3f2fd; color: #42a5f5; }
.sk-card__cost--虫 { background: #e8f5e9; color: #4caf50; }
.sk-card__cost--武 { background: #e3f2fd; color: #42a5f5; }
.sk-card__cost--翼 { background: #e3f2fd; color: #42a5f5; }
.sk-card__cost--萌 { background: #e3f2fd; color: #42a5f5; }
.sk-card__cost--幽 { background: #e3f2fd; color: #42a5f5; }
.sk-card__cost--恶 { background: #e3f2fd; color: #42a5f5; }
.sk-card__cost--机械 { background: #e3f2fd; color: #42a5f5; }
.sk-card__cost--幻 { background: #e3f2fd; color: #42a5f5; }
.sk-card__cost--普通 { background: #e3f2fd; color: #42a5f5; }
.sk-card__type-badge {
  font-size: 9px;
  font-weight: 700;
  padding: 1px 5px;
  border-radius: 4px;
  line-height: 1.4;
}
.sk-card__power {
  font-size: 10px;
  color: #999;
  font-weight: 500;
  margin-left: auto;
}
.sk-card__effect {
  font-size: 10px;
  color: #999;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

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
.detail__evo-node--current { background: #f5f0ff; box-shadow: 0 0 0 2px #8b3dff40; }
.detail__evo-img {
  width: 48px; height: 48px; display: flex; align-items: center; justify-content: center;
  background: #f5f2ff; border-radius: 50%; margin-bottom: 4px; overflow: hidden;
}
.detail__evo-img img { width: 40px; height: 40px; object-fit: contain; }
.detail__evo-name { font-size: 12px; font-weight: 600; color: #1a1a2e; }
.detail__evo-no { font-size: 10px; color: #ccc; }

.detail__forms { display: flex; flex-wrap: wrap; gap: 6px; }
.detail__form-tag {
  padding: 6px 12px; border-radius: 10px; font-size: 13px; font-weight: 500;
  background: #f5f2ff; color: #666; text-decoration: none; border: 1.5px solid #e8e8e8; transition: .2s;
}
.detail__form-tag--current { background: #8b3dff; color: #fff; border-color: #8b3dff; }
.detail__form-sub { font-size: 11px; color: inherit; opacity: .6; }

.detail__locations { display: flex; flex-wrap: wrap; gap: 6px; }
.detail__loc { font-size: 12px; padding: 4px 10px; border-radius: 8px; background: #f0ecff; color: #8b3dff; }

.detail__loading { text-align: center; padding: 60px 0; color: #ccc; }
.detail__spinner {
  width: 32px; height: 32px; border: 3px solid #e8e8e8; border-top-color: #8b3dff;
  border-radius: 50%; animation: spin .8s linear infinite; margin: 0 auto 12px;
}
@keyframes spin { to { transform: rotate(360deg); } }
.detail__empty { text-align: center; padding: 60px 0; color: #ccc; }
.detail__empty-icon { font-size: 48px; margin-bottom: 8px; }
.detail__btn { display: inline-block; margin-top: 12px; padding: 8px 20px; background: #8b3dff; color: #fff; border-radius: 10px; text-decoration: none; font-size: 14px; }

.detail__ft { text-align: center; padding: 20px 0 8px; font-size: 11px; color: #ccc; }
</style>
