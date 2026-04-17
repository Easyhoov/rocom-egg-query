<script setup>
import { ref, onMounted } from 'vue'

const groups = ref([])
const selectedGroup = ref(null)
const spirits = ref([])
const loading = ref(false)
const loadingGroups = ref(true)

async function loadGroups() {
  loadingGroups.value = true
  try {
    const res = await fetch('/api/official-egg-groups')
    const data = await res.json()
    // 过滤掉"无法孵蛋"
    groups.value = (data.groups || []).filter(g => g.egg_group_name !== '无法孵蛋')
  } catch (e) {
    console.error('加载蛋组失败:', e)
  } finally {
    loadingGroups.value = false
  }
}

async function selectGroup(group) {
  selectedGroup.value = group
  loading.value = true
  spirits.value = []
  try {
    const params = new URLSearchParams({
      egg_group: group.egg_group_name,
      page_size: '100',
      page: '1',
    })
    const res = await fetch(`/api/spirits?${params}`)
    const data = await res.json()
    // 只保留可繁殖的
    spirits.value = (data.items || []).filter(s => s.can_breed)
  } catch (e) {
    console.error('加载精灵失败:', e)
  } finally {
    loading.value = false
  }
}

function goBack() {
  selectedGroup.value = null
  spirits.value = []
}

onMounted(loadGroups)
</script>

<template>
  <div class="egg">
    <div class="egg__box">
      <!-- 标题 -->
      <div class="egg__hd">
        <div class="egg__hd-row">
          <h1 v-if="!selectedGroup">🎯 蛋组配对</h1>
          <template v-else>
            <a href="javascript:void(0)" @click="goBack" class="egg__back">← 全部蛋组</a>
            <h1>{{ selectedGroup.egg_group_icon }} {{ selectedGroup.egg_group_name }}</h1>
          </template>
          <a href="/" class="egg__home">首页</a>
        </div>
        <p class="egg__sub" v-if="!selectedGroup">选择蛋组，查看可繁殖精灵</p>
        <p class="egg__sub" v-else>{{ spirits.length }} 只可繁殖精灵 · 同组可互相配对</p>
      </div>

      <!-- 蛋组列表 -->
      <div v-if="!selectedGroup && !loadingGroups" class="egg__groups">
        <div
          v-for="g in groups"
          :key="g.egg_group_name"
          class="egg__group-card"
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
        <div class="egg__spinner"></div>
        <p>加载中...</p>
      </div>

      <!-- 精灵列表 -->
      <div v-if="selectedGroup && !loading" class="egg__spirits">
        <div class="egg__spirit-grid">
          <router-link
            v-for="s in spirits"
            :key="s.spirit_id"
            :to="`/compendium/${s.spirit_id}`"
            class="egg__spirit"
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

      <div class="egg__ft">洛克王国：世界 · 蛋组配对</div>
    </div>
  </div>
</template>

<style scoped>
.egg {
  min-height: 100vh;
  background: linear-gradient(180deg, #e8f0fe 0%, #f5f0ff 50%, #fff 100%);
  padding: 16px;
  padding-bottom: env(safe-area-inset-bottom, 16px);
}
.egg__box { max-width: 420px; margin: 0 auto; }
.egg__hd { text-align: center; padding: 16px 0 12px; }
.egg__hd-row { display: flex; align-items: center; justify-content: center; gap: 12px; position: relative; }
.egg__hd h1 { font-size: 20px; color: #1a1a2e; font-weight: 700; }
.egg__back { font-size: 13px; color: #667eea; text-decoration: none; position: absolute; left: 0; }
.egg__home { font-size: 13px; color: #667eea; text-decoration: none; position: absolute; right: 0; }
.egg__sub { font-size: 12px; color: #aaa; margin-top: 4px; }

/* 蛋组卡片 */
.egg__groups { display: flex; flex-direction: column; gap: 8px; margin-top: 8px; }
.egg__group-card {
  background: #fff;
  border-radius: 14px;
  padding: 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,.06);
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
  background: #f0f2ff;
  border-radius: 14px;
  flex-shrink: 0;
}
.egg__group-info { flex: 1; }
.egg__group-name { font-size: 16px; font-weight: 700; color: #1a1a2e; }
.egg__group-count { font-size: 12px; color: #aaa; margin-top: 2px; }
.egg__group-arrow { font-size: 18px; color: #667eea; font-weight: 600; }

/* 精灵网格 */
.egg__spirits { margin-top: 8px; }
.egg__spirit-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}
.egg__spirit {
  background: #fff;
  border-radius: 14px;
  padding: 10px 6px 8px;
  text-align: center;
  text-decoration: none;
  color: inherit;
  box-shadow: 0 2px 8px rgba(0,0,0,.04);
  transition: .2s;
}
.egg__spirit:active { transform: scale(.96); }
.egg__spirit-img {
  width: 56px; height: 56px;
  margin: 0 auto 4px;
  display: flex; align-items: center; justify-content: center;
  background: #f8f9ff;
  border-radius: 50%;
}
.egg__spirit-img img { width: 48px; height: 48px; object-fit: contain; }
.egg__spirit-no { font-size: 10px; color: #bbb; }
.egg__spirit-name { font-size: 13px; font-weight: 600; color: #1a1a2e; margin: 2px 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.egg__spirit-attr { font-size: 9px; padding: 1px 5px; border-radius: 6px; background: #667eea15; color: #667eea; }

.egg__loading { text-align: center; padding: 60px 0; color: #ccc; }
.egg__spinner {
  width: 32px; height: 32px; border: 3px solid #e8e8e8; border-top-color: #667eea;
  border-radius: 50%; animation: spin .8s linear infinite; margin: 0 auto 12px;
}
@keyframes spin { to { transform: rotate(360deg); } }
.egg__empty { text-align: center; padding: 40px 0; color: #ccc; }
.egg__ft { text-align: center; padding: 20px 0 8px; font-size: 11px; color: #ccc; }
</style>
