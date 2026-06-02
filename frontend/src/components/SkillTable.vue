<script setup>
import { computed } from 'vue'
import { getAttrIcon } from '../utils/attrIcons'

const props = defineProps({
  skills: { type: Array, required: true },
  loading: { type: Boolean, default: false }
})

const SKILL_TYPE_STYLES = {
  '物理': { bg: '#fee8e8', color: '#e74c3c', label: '物' },
  '魔法': { bg: '#e8e8ff', color: '#667eea', label: '魔' },
  '防御': { bg: '#e8f5e9', color: '#4caf50', label: '防' },
  '状态': { bg: '#fff3e0', color: '#ff9800', label: '变' },
}

const ATTR_NAME_MAP = {
  '光系': '光', '火系': '火', '水系': '水', '草系': '草', '冰系': '冰',
  '地系': '地', '龙系': '龙', '电系': '电', '毒系': '毒', '虫系': '虫',
  '武系': '武', '翼系': '翼', '萌系': '萌', '幽系': '幽', '恶系': '恶',
  '机械系': '机械', '幻系': '幻', '普通系': '普通',
}

function formatAttr(attr) {
  return ATTR_NAME_MAP[attr] || attr?.replace('系', '') || attr || ''
}

const sortedSkills = computed(() => {
  const seen = new Set()
  return props.skills.filter(s => {
    if (seen.has(s.name)) return false
    seen.add(s.name)
    return true
  }).sort((a, b) => a.cost - b.cost || a.name.localeCompare(b.name))
})
</script>

<template>
  <div v-if="loading" class="sk-loading">加载中...</div>
  <div v-else class="sk-grid">
    <div v-for="s in sortedSkills" :key="s.name" class="sk-card">
      <div class="sk-icon-wrap">
        <img v-if="s.icon_url" :src="s.icon_url" class="sk-icon" :alt="s.name" />
        <span v-else class="sk-icon-fallback">⚔️</span>
      </div>
      <div class="sk-body">
        <div class="sk-name">{{ s.name }}</div>
        <div class="sk-meta">
          <span class="sk-cost" :class="'sk-cost--' + (formatAttr(s.attribute) || '')">
            {{ s.cost }}
          </span>
          <span class="sk-type-badge" :style="{ background: (SKILL_TYPE_STYLES[s.type] || {}).bg || '#f5f5f5', color: (SKILL_TYPE_STYLES[s.type] || {}).color || '#888' }">
            {{ (SKILL_TYPE_STYLES[s.type] || {}).label || '?' }}
          </span>
          <span v-if="s.power > 0" class="sk-power">{{ s.power }}</span>
        </div>
        <div v-if="s.effect" class="sk-effect">{{ s.effect }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.sk-loading { text-align: center; padding: 20px 0; color: rgba(255,255,255,0.5); font-size: 13px; }
.sk-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}
.sk-card {
  display: flex;
  gap: 8px;
  background: var(--dt-card-bg, rgba(20,20,40,0.6));
  border: 1px solid var(--dt-border, rgba(255,255,255,0.1));
  border-radius: 12px;
  padding: 10px;
  min-height: 76px;
  position: relative;
}
.sk-icon-wrap {
  width: 44px;
  height: 44px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}
.sk-icon {
  width: 40px;
  height: 40px;
  object-fit: contain;
  border-radius: 6px;
}
.sk-icon-fallback {
  font-size: 22px;
  opacity: .3;
}
.sk-body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 3px;
}
.sk-name {
  font-size: 12px;
  font-weight: 600;
  color: var(--dt-text, #fff);
  line-height: 1.3;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.sk-meta {
  display: flex;
  align-items: center;
  gap: 4px;
  flex-wrap: wrap;
}
.sk-cost {
  font-size: 10px;
  font-weight: 700;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: #e3f2fd;
  color: #42a5f5;
}
.sk-cost--光 { background: #e8f5e9; color: #4caf50; }
.sk-cost--火 { background: #fee8e8; color: #e74c3c; }
.sk-cost--水 { background: #e3f2fd; color: #42a5f5; }
.sk-cost--草 { background: #e8f5e9; color: #4caf50; }
.sk-cost--冰 { background: #e3f2fd; color: #42a5f5; }
.sk-cost--电 { background: #fff3e0; color: #ff9800; }
.sk-cost--地 { background: #efebe9; color: #795548; }
.sk-cost--龙 { background: #ede7f6; color: #673ab7; }
.sk-cost--毒 { background: #f3e5f5; color: #9c27b0; }
.sk-cost--虫 { background: #e8f5e9; color: #4caf50; }
.sk-cost--武 { background: #fce4ec; color: #e91e63; }
.sk-cost--翼 { background: #e3f2fd; color: #2196f3; }
.sk-cost--萌 { background: #fce4ec; color: #e91e63; }
.sk-cost--幽 { background: #ede7f6; color: #673ab7; }
.sk-cost--恶 { background: #efebe9; color: #424242; }
.sk-cost--机械 { background: #eceff1; color: #607d8b; }
.sk-cost--幻 { background: #f3e5f5; color: #9c27b0; }
.sk-cost--普通 { background: #eceff1; color: #9e9e9e; }
.sk-type-badge {
  font-size: 9px;
  font-weight: 700;
  padding: 1px 5px;
  border-radius: 4px;
  line-height: 1.4;
}
.sk-power {
  font-size: 10px;
  color: rgba(255,255,255,0.6);
  font-weight: 500;
  margin-left: auto;
}
.sk-effect {
  font-size: 10px;
  color: rgba(255,255,255,0.5);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
