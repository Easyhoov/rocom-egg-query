<script setup>
import TierBadge from './TierBadge.vue'
import ProbBar from './ProbBar.vue'

const props = defineProps({
  pet: {
    type: Object,
    required: true
  }
})
</script>

<template>
  <div class="result-card">
    <div class="result-card__header">
      <img v-if="pet.image" :src="pet.image" alt="" class="result-card__avatar" />
      <span class="result-card__name">{{ pet.name }}</span>
      <span class="result-card__type" v-if="pet.egg_type_name">
        {{ pet.egg_type_icon }} {{ pet.egg_type_name }}
      </span>
    </div>
    <div class="result-card__row">
      <TierBadge :tier="pet.match_tier" />
      <span class="result-card__prob">概率 {{ pet.probability }}%</span>
    </div>
    <div class="result-card__bar-row">
      <ProbBar :probability="pet.probability" />
      <span class="result-card__bar-label">{{ pet.probability }}%</span>
    </div>
    <div class="result-card__details">
      身高: {{ pet.height_min?.toFixed(2) }} ~ {{ pet.height_max?.toFixed(2) }}m &nbsp;&nbsp;
      体重: {{ pet.weight_min?.toFixed(2) }} ~ {{ pet.weight_max?.toFixed(2) }}kg
    </div>
    <div class="result-card__details">
      R值: {{ pet.r_value?.toFixed(2) }} &nbsp;&nbsp; 差距: {{ pet.r_diff?.toFixed(2) }}
    </div>
  </div>
</template>

<style scoped>
.result-card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-card);
  box-shadow: var(--shadow-card);
  padding: 16px;
  margin-bottom: 12px;
  transition: background-color var(--transition), box-shadow var(--transition);
}
.result-card:hover {
  box-shadow: var(--shadow-soft);
}
.result-card__header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 8px;
}
.result-card__avatar {
  width: 32px;
  height: 32px;
  vertical-align: middle;
  margin-right: 8px;
}
.result-card__name {
  font-size: 18px;
  font-weight: 700;
  vertical-align: middle;
}
.result-card__type {
  font-size: 12px;
  color: var(--text-weak);
  background: var(--bg-alt);
  padding: 2px 8px;
  border-radius: var(--radius-pill);
}
.result-card__row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}
.result-card__prob {
  font-size: 14px;
  font-weight: 600;
}
.result-card__bar-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}
.result-card__bar-row :deep(.prob-bar) {
  flex: 1;
}
.result-card__bar-label {
  font-size: 12px;
  color: var(--text-weak);
  min-width: 40px;
  text-align: right;
}
.result-card__details {
  font-size: 13px;
  color: var(--text-weak);
  line-height: 1.8;
}
@media (max-width: 600px) {
  .result-card { padding: 12px; }
  .result-card__name { font-size: 16px; }
  .result-card__details { font-size: 12px; }
}
</style>
