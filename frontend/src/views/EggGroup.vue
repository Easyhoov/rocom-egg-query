<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '../composables/useApi'
import '../styles/dark-theme.css'
const { loading, fetchJson } = useApi()

const groups = ref([])
const selectedGroup = ref(null)
const spirits = ref([])
const loadingGroups = ref(true)

async function loadGroups() {
  loadingGroups.value = true
  const data = await fetchJson('/api/official-egg-groups')
  if (data) {
    groups.value = (data.groups || []).filter(g => g.egg_group_name !== '无法孵蛋')
  }
  loadingGroups.value = false
}

async function selectGroup(group) {
  selectedGroup.value = group
  spirits.value = []
  const params = new URLSearchParams({
    egg_group: group.egg_group_name,
    page_size: '100',
    page: '1',
  })
  const data = await fetchJson(`/api/spirits?${params}`)
  if (data) {
    spirits.value = (data.items || []).filter(s => s.can_breed)
  }
}

function goBack() {
  selectedGroup.value = null
  spirits.value = []
}

onMounted(loadGroups)
</script>

<template>
  <div class="egg dark-page">
    <div class="egg__box">
      <!-- 标题 -->
      <div class="egg__hd">
        <h1 v-if="!selectedGroup">🎯 蛋组配对</h1>
        <template v-else>
          <div class="egg__back" @click="goBack">← 全部蛋组</div>
          <h1>{{ selectedGroup.egg_group_icon }} {{ selectedGroup.egg_group_name }}</h1>
        </template>
        <p class="egg__sub" v-if="!selectedGroup">选择蛋组，查看可繁殖精灵</p>
        <p class="egg__sub" v-else>{{ spirits.length }} 只可繁殖精灵 · 同组可互相配对</p>
      </div>

      <!-- 蛋组列表 -->
      <div v-if="!selectedGroup && !loadingGroups" class="egg__groups">
        <div
          v-for="g in groups"
          :key="g.egg_group_name"
          class="egg__group-card dark-card"
          @click="selectGroup(g)"
        >
          <div class="egg__group-icon">{{ g.egg_group_icon }}</div>
          <div class="egg__group-info">
            <div class="egg__group-name">{{ g.egg_group_name }}</div>
            <div class="egg__group-count">{{ g.spirit_count }} 只精灵</div>
          </div>
          <div class="egg__group-arrow">→</div>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading || loadingGroups" class="egg__loading">
        <div class="dt-spinner"></div>
        <p>加载中...</p>
      </div>

      <!-- 精灵列表 -->
      <div v-if="selectedGroup && !loading" class="egg__spirits">
        <div class="egg__spirit-grid">
          <router-link
            v-for="s in spirits"
            :key="s.spirit_id"
            :to="`/compendium/${s.spirit_id}`"
            class="egg__spirit dark-card"
          >
            <div class="egg__spirit-img">
              <img v-if="s.image" :src="s.image" :alt="s.base_name" loading="lazy" />
              <span v-else>❓</span>
            </div>
            <div class="egg__spirit-no">{{ s.spirit_no }}</div>
            <div class="egg__spirit-name">{{ s.display_name }}</div>
            <span v-if="s.primary_attribute" class="egg__spirit-attr">{{ s.primary_attribute }}</span>
          </router-link>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-if="selectedGroup && !loading && spirits.length === 0" class="egg__empty">
        <p>该蛋组暂无繁殖数据</p>
      </div>

      <div class="dt-footer">洛克王国：世界 · 蛋组配对</div>
    </div>
  </div>
</template>

<style scoped>
.egg {
  padding: 16px 16px 80px;
}

.egg__box { max-width: 420px; width: 100%; margin: 0 auto; }
.egg__box { position: relative; z-index: 1; }
.egg__hd { text-align: center; padding: 24px 0 20px; position: relative; }
.egg__hd h1 { font-size: 22px; color: var(--dt-text, #fff); font-weight: 700; margin: 0; }
.egg__back { font-size: 13px; color: #8b3dff; cursor: pointer; margin-bottom: 10px; }
.egg__sub { font-size: 13px; color: var(--dt-text-secondary, rgba(255,255,255,0.75)); margin-top: 6px; }

/* 蛋组卡片 */
.egg__groups { display: flex; flex-direction: column; gap: 8px; margin-top: 8px; }
.egg__group-card {
  background: var(--dt-card-bg, rgba(20,20,40,0.6));
  border-radius: 18px;
  padding: 16px;
  border: 1px solid var(--dt-border, rgba(255,255,255,0.1));
  backdrop-filter: blur(8px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.3);
  display: flex;
  align-items: center;
  gap: 14px;
  cursor: pointer;
  transition: .2s;
}
.egg__group-card:active { transform: scale(.97); }
.egg__group-icon {
  width: 48px; height: 48px;
  display: flex; align-items: center; justify-content: center;
  font-size: 28px;
  background: rgba(139,61,255,0.15);
  border-radius: 14px;
  flex-shrink: 0;
}
.egg__group-info { flex: 1; }
.egg__group-name { font-size: 16px; font-weight: 700; color: var(--dt-text, #fff); }
.egg__group-count { font-size: 12px; color: var(--dt-text-secondary, rgba(255,255,255,0.5)); margin-top: 2px; }
.egg__group-arrow { font-size: 18px; color: #8b3dff; font-weight: 600; }

/* 精灵网格 */
.egg__spirits { margin-top: 8px; }
.egg__spirit-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}
.egg__spirit {
  background: var(--dt-card-bg, rgba(20,20,40,0.6));
  border-radius: 14px;
  padding: 10px 6px 8px;
  text-align: center;
  text-decoration: none;
  color: inherit;
  border: 1px solid var(--dt-border, rgba(255,255,255,0.1));
  backdrop-filter: blur(8px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.3);
  transition: .2s;
}
.egg__spirit:hover { box-shadow: 0 8px 24px rgba(139,61,255,0.12); }
.egg__spirit:active { transform: scale(.96); }
.egg__spirit-img {
  width: 56px; height: 56px;
  margin: 0 auto 4px;
  display: flex; align-items: center; justify-content: center;
  background: rgba(139,61,255,0.15);
  border-radius: 50%;
}
.egg__spirit-img img { width: 48px; height: 48px; object-fit: contain; }
.egg__spirit-no { font-size: 10px; color: var(--dt-text-secondary, rgba(255,255,255,0.5)); }
.egg__spirit-name { font-size: 13px; font-weight: 600; color: var(--dt-text, #fff); margin: 2px 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.egg__spirit-attr { font-size: 9px; padding: 1px 5px; border-radius: 6px; background: rgba(139,61,255,0.2); color: #8b3dff; }

.egg__loading { text-align: center; padding: 60px 0; color: var(--dt-text-secondary, rgba(255,255,255,0.5)); }

.egg__empty { text-align: center; padding: 40px 0; color: var(--dt-text-secondary, rgba(255,255,255,0.5)); }

</style>
