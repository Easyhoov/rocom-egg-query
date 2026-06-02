<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getAttrIcon } from '../utils/attrIcons'
import { useApi } from '../composables/useApi'
import RadarChart from '../components/RadarChart.vue'
import SkillTable from '../components/SkillTable.vue'
import '../styles/dark-theme.css'

const route = useRoute()
const router = useRouter()
const spirit = ref(null)
const skills = ref([])
const matchups = ref(null)
const loading = ref(true)
const skillsLoading = ref(true)
const showShiny = ref(false)
const spiritId = computed(() => route.params.id)

const { fetchJson: fetchDetailJson } = useApi()
const { fetchJson: fetchSkillsJson } = useApi()
const { fetchJson: fetchMatchupsJson } = useApi()

async function fetchDetail() {
  loading.value = true
  const data = await fetchDetailJson(`/api/spirits/${spiritId.value}`)
  if (data?.success) spirit.value = data.spirit
  loading.value = false
}

async function fetchSkills() {
  skillsLoading.value = true
  const data = await fetchSkillsJson(`/api/spirits/${spiritId.value}/skills`)
  if (data?.success) skills.value = data.skills || []
  else skills.value = []
  skillsLoading.value = false
}

async function fetchMatchups() {
  const data = await fetchMatchupsJson(`/api/spirits/${spiritId.value}/type-matchups`)
  if (data?.success) matchups.value = data
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
  <div class="detail dark-page">
    <div class="detail__box">
      <!-- 返回 -->
      <div class="detail__nav">
        <a href="javascript:void(0)" @click="goBack" class="detail__back">← 返回图鉴</a>
        <span v-if="spirit" class="detail__nav-no">{{ spirit.spirit_no }}</span>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="detail__loading">
        <div class="dt-spinner"></div>
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
        <div class="detail__card dark-card">
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
        <div v-if="spirit.trait_name" class="detail__card dark-card">
          <h2 class="detail__card-title">💡 特性</h2>
          <div class="detail__trait">
            <span class="detail__trait-name">{{ spirit.trait_name }}</span>
            <span v-if="spirit.trait_effect" class="detail__trait-desc">{{ spirit.trait_effect }}</span>
          </div>
        </div>

        <!-- 种族值 -->
        <div v-if="spirit.race_total" class="detail__card dark-card">
          <h2 class="detail__card-title">📊 种族值 <span class="detail__card-sub">总和 {{ spirit.race_total }}</span></h2>
          <RadarChart :stats="spirit" />
        </div>

        <!-- 属性克制 -->
        <div v-if="matchups" class="detail__card detail__matchups dark-card">
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

        <!-- 技能列表 -->
        <div v-if="skills.length > 0 || skillsLoading" class="detail__card dark-card">
          <h2 class="detail__card-title">⚡ 技能 <span v-if="skills.length" class="detail__card-sub">共 {{ skills.length }} 个</span></h2>
          <SkillTable :skills="skills" :loading="skillsLoading" />
        </div>

        <!-- 进化链 -->
        <div v-if="spirit.evolution_chain?.length > 1" class="detail__card dark-card">
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
        <div v-if="spirit.forms?.length > 1" class="detail__card dark-card">
          <h2 class="detail__card-title">🎭 其他形态</h2>
          <div class="detail__forms">
            <router-link v-for="form in spirit.forms" :key="form.spirit_id" :to="`/compendium/${form.spirit_id}`" class="detail__form-tag" :class="{ 'detail__form-tag--current': form.spirit_id === spirit.spirit_id }">
              {{ form.display_name || form.base_name }}
              <span v-if="form.form_name" class="detail__form-sub">({{ form.form_name }})</span>
            </router-link>
          </div>
        </div>

        <!-- 出没地点 -->
        <div v-if="spirit.locations?.length" class="detail__card dark-card">
          <h2 class="detail__card-title">📍 出没地点</h2>
          <div class="detail__locations">
            <span v-for="loc in spirit.locations" :key="loc" class="detail__loc">{{ loc }}</span>
          </div>
        </div>
      </template>

      <div class="dt-footer">洛克王国：世界 · 精灵详情</div>
    </div>
  </div>
</template>

<style scoped>
.detail {
  padding: 16px 16px 80px;
}
.detail__box { position: relative; z-index: 1; max-width: 420px; margin: 0 auto; }
.detail__nav { display: flex; align-items: center; justify-content: space-between; padding: 8px 0 12px; }
.detail__back { font-size: 13px; color: #8b3dff; text-decoration: none; }
.detail__nav-no { font-size: 12px; color: var(--dt-text-secondary, rgba(255,255,255,0.5)); }

.detail__card {
  padding: 16px;
  margin-bottom: 12px;
}
.detail__card-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--dt-text, #fff);
  margin-bottom: 12px;
}
.detail__card-sub { font-size: 12px; color: #8b3dff; font-weight: 400; margin-left: 6px; }

.detail__hero { display: flex; gap: 14px; align-items: flex-start; }
.detail__img {
  width: 100px; height: 100px; flex-shrink: 0; position: relative;
  display: flex; align-items: center; justify-content: center;
  background: rgba(139,61,255,0.15); border-radius: 14px; overflow: visible;
}
.detail__img img { width: 88px; height: 88px; object-fit: contain; }
.detail__noimg { font-size: 40px; opacity: .3; }
.detail__shiny-toggle {
  position: absolute; bottom: -8px; left: 50%; transform: translateX(-50%);
  font-size: 10px; padding: 2px 8px; border-radius: 8px;
  background: rgba(255,248,225,0.15); color: #f57f17; border: 1px solid rgba(255,224,130,0.3);
  cursor: pointer; white-space: nowrap; font-weight: 600;
}
.detail__shiny-toggle:active { transform: translateX(-50%) scale(.95); }
.detail__info { flex: 1; min-width: 0; }
.detail__info h1 { font-size: 20px; font-weight: 700; color: var(--dt-text, #fff); margin-bottom: 6px; }
.detail__tags { display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 8px; }
.detail__tag { font-size: 11px; padding: 2px 8px; border-radius: 10px; font-weight: 600; display: inline-flex; align-items: center; gap: 3px; }
.detail__tag-icon { width: 14px; height: 14px; }
.detail__meta { font-size: 12px; color: var(--dt-text-secondary, rgba(255,255,255,0.75)); display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 6px; }
.detail__race { color: #f39c12; font-weight: 600; }
.detail__egg-groups { font-size: 12px; }
.detail__egg-label { color: var(--dt-text-secondary, rgba(255,255,255,0.5)); }
.detail__egg-tag { display: inline-block; font-size: 11px; padding: 1px 6px; border-radius: 6px; background: rgba(139,61,255,0.2); color: #8b3dff; margin-left: 4px; }
.detail__desc { font-size: 13px; color: var(--dt-text-secondary, rgba(255,255,255,0.75)); line-height: 1.6; margin-top: 10px; padding-top: 10px; border-top: 1px solid var(--dt-border, rgba(255,255,255,0.1)); }

.detail__trait { display: flex; align-items: flex-start; gap: 10px; flex-wrap: wrap; }
.detail__trait-name { font-size: 13px; font-weight: 600; background: rgba(255,248,225,0.15); color: #f57f17; padding: 4px 10px; border-radius: 8px; }
.detail__trait-desc { font-size: 13px; color: var(--dt-text-secondary, rgba(255,255,255,0.75)); line-height: 1.6; flex: 1; min-width: 200px; }

/* 属性克制 */
.detail__mu-row { display: flex; flex-direction: column; gap: 8px; }
.detail__mu-group { display: flex; align-items: flex-start; gap: 8px; }
.detail__mu-label {
  font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 6px;
  flex-shrink: 0; min-width: 42px; text-align: center;
}
.detail__mu-label--advantage { background: rgba(46,125,50,0.15); color: #4caf50; }
.detail__mu-label--disadvantage { background: rgba(198,40,40,0.15); color: #ef5350; }
.detail__mu-label--resist { background: rgba(21,101,192,0.15); color: #42a5f5; }
.detail__mu-label--weak { background: rgba(255,255,255,0.06); color: var(--dt-text-secondary, rgba(255,255,255,0.5)); }
.detail__mu-tags { display: flex; flex-wrap: wrap; gap: 4px; }
.detail__mu-tag {
  font-size: 11px; padding: 2px 8px; border-radius: 8px;
  display: inline-flex; align-items: center; gap: 3px; font-weight: 500;
}
.detail__mu-tag--advantage { background: rgba(46,125,50,0.15); color: #4caf50; }
.detail__mu-tag--disadvantage { background: rgba(198,40,40,0.15); color: #ef5350; }
.detail__mu-tag--resist { background: rgba(21,101,192,0.15); color: #42a5f5; }
.detail__mu-tag--weak { background: rgba(255,255,255,0.06); color: var(--dt-text-secondary, rgba(255,255,255,0.5)); }
.detail__mu-icon { width: 14px; height: 14px; }
.detail__mu-note { font-size: 10px; color: var(--dt-text-secondary, rgba(255,255,255,0.4)); text-align: right; margin-top: 6px; }

.detail__evo { display: flex; align-items: center; flex-wrap: wrap; gap: 4px; }
.detail__evo-arrow { display: flex; flex-direction: column; align-items: center; padding: 0 2px; }
.detail__evo-arrow span:first-child { color: var(--dt-text-secondary, rgba(255,255,255,0.5)); font-size: 16px; }
.detail__evo-lv { font-size: 10px; color: var(--dt-text-secondary, rgba(255,255,255,0.5)); }
.detail__evo-node {
  display: flex; flex-direction: column; align-items: center;
  padding: 8px; border-radius: 10px; text-decoration: none; color: inherit;
  transition: .2s; min-width: 72px;
}
.detail__evo-node:active { transform: scale(.95); }
.detail__evo-node--current { background: rgba(139,61,255,0.15); box-shadow: 0 0 0 2px #8b3dff40; }
.detail__evo-img {
  width: 48px; height: 48px; display: flex; align-items: center; justify-content: center;
  background: rgba(139,61,255,0.15); border-radius: 50%; margin-bottom: 4px; overflow: hidden;
}
.detail__evo-img img { width: 40px; height: 40px; object-fit: contain; }
.detail__evo-name { font-size: 12px; font-weight: 600; color: var(--dt-text, #fff); }
.detail__evo-no { font-size: 10px; color: var(--dt-text-secondary, rgba(255,255,255,0.5)); }

.detail__forms { display: flex; flex-wrap: wrap; gap: 6px; }
.detail__form-tag {
  padding: 6px 12px; border-radius: 10px; font-size: 13px; font-weight: 500;
  background: rgba(139,61,255,0.1); color: var(--dt-text, #fff); text-decoration: none; border: 1.5px solid var(--dt-border, rgba(255,255,255,0.2)); transition: .2s;
}
.detail__form-tag--current { background: #8b3dff; color: #fff; border-color: #8b3dff; }
.detail__form-sub { font-size: 11px; color: inherit; opacity: .6; }

.detail__locations { display: flex; flex-wrap: wrap; gap: 6px; }
.detail__loc { font-size: 12px; padding: 4px 10px; border-radius: 8px; background: rgba(139,61,255,0.15); color: #8b3dff; }

.detail__loading { text-align: center; padding: 60px 0; color: var(--dt-text-secondary, rgba(255,255,255,0.5)); }
.detail__empty { text-align: center; padding: 60px 0; color: var(--dt-text-secondary, rgba(255,255,255,0.5)); }
.detail__empty-icon { font-size: 48px; margin-bottom: 8px; }
.detail__btn { display: inline-block; margin-top: 12px; padding: 8px 20px; background: #8b3dff; color: #fff; border-radius: 10px; text-decoration: none; font-size: 14px; }
</style>
