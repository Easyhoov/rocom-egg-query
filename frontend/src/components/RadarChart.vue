<script setup>
import { computed } from 'vue'

const props = defineProps({
  stats: { type: Object, required: true }
  // stats: { hp, attack, defense, magic_defense, magic_attack, speed }
})

const statOrder = ['hp', 'attack', 'defense', 'magic_defense', 'magic_attack', 'speed']
const statLabels = {
  hp: { label: '生命', color: '#4caf50' },
  attack: { label: '物攻', color: '#e74c3c' },
  defense: { label: '物防', color: '#3498db' },
  magic_defense: { label: '魔防', color: '#f39c12' },
  magic_attack: { label: '魔攻', color: '#9b59b6' },
  speed: { label: '速度', color: '#1abc9c' },
}

const CX = 150, CY = 150, R = 110
const MAX_STAT = 150
const GRID_LEVELS = 5

function axisAngle(i) {
  return (-90 + i * 60) * Math.PI / 180
}
function polarToXY(i, r) {
  const a = axisAngle(i)
  return { x: CX + r * Math.cos(a), y: CY + r * Math.sin(a) }
}
function gridPoints(level) {
  const r = R * level / GRID_LEVELS
  return Array.from({ length: 6 }, (_, i) => {
    const p = polarToXY(i, r)
    return `${p.x},${p.y}`
  }).join(' ')
}
function axisEnd(i) {
  return polarToXY(i, R)
}
const radarPoints = computed(() => {
  if (!props.stats) return ''
  return statOrder.map((key, i) => {
    const val = props.stats[key] || 0
    const r = R * Math.min(val / MAX_STAT, 1)
    const p = polarToXY(i, r)
    return `${p.x},${p.y}`
  }).join(' ')
})
function labelPos(i) {
  return polarToXY(i, R + 24)
}
function labelAnchor(i) {
  const a = axisAngle(i)
  const cos = Math.cos(a)
  if (Math.abs(cos) < 0.1) return 'middle'
  return cos > 0 ? 'start' : 'end'
}
const statItems = computed(() => {
  if (!props.stats) return []
  return statOrder.map(key => ({
    key, ...statLabels[key], value: props.stats[key] || 0
  }))
})
</script>

<template>
  <div class="radar-chart">
    <svg viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg">
      <!-- 网格线 -->
      <polygon v-for="lv in GRID_LEVELS" :key="'g' + lv" :points="gridPoints(lv)" fill="none" stroke="#e8e8f0" stroke-width="1" />
      <!-- 轴线 -->
      <line v-for="i in 6" :key="'a' + i" :x1="CX" :y1="CY" :x2="axisEnd(i - 1).x" :y2="axisEnd(i - 1).y" stroke="#e0e0e8" stroke-width="1" />
      <!-- 数据区域 -->
      <polygon v-if="radarPoints" :points="radarPoints" fill="rgba(102, 126, 234, 0.2)" stroke="#8b3dff" stroke-width="2" />
      <!-- 数据点 -->
      <circle v-for="(s, i) in statItems" :key="'d' + s.key" :cx="polarToXY(i, R * Math.min(s.value / MAX_STAT, 1)).x" :cy="polarToXY(i, R * Math.min(s.value / MAX_STAT, 1)).y" r="4" :fill="s.color" stroke="#fff" stroke-width="1.5" />
      <!-- 标签 -->
      <text v-for="(s, i) in statItems" :key="'l' + s.key" :x="labelPos(i).x" :y="labelPos(i).y" :text-anchor="labelAnchor(i)" dominant-baseline="middle" font-size="12" font-weight="600" :fill="s.color">{{ s.label }} {{ s.value }}</text>
    </svg>
  </div>
</template>

<style scoped>
.radar-chart { display: flex; justify-content: center; }
.radar-chart svg { width: 100%; max-width: 300px; }
</style>
