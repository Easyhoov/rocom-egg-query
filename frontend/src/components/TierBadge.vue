<script setup>
const props = defineProps({
  tier: {
    type: String,
    required: true
  }
})

const tierMap = {
  exact: '精准命中',
  tolerance1: '容差1',
  tolerance2: '容差2',
  nearest: '近似'
}
</script>

<template>
  <span class="badge" :class="`badge--${tier}`">{{ tierMap[tier] || tier }}</span>
</template>

<style scoped>
.badge {
  display: inline-flex;
  align-items: center;
  padding: 2px 10px;
  font-size: 12px;
  font-weight: 600;
  border-radius: var(--radius-pill);
  line-height: 1.5;
  white-space: nowrap;
}
.badge--exact {
  background-color: color-mix(in srgb, var(--tier-exact) 15%, transparent);
  color: var(--tier-exact);
}
.badge--tolerance1 {
  background-color: color-mix(in srgb, var(--tier-tolerance1) 15%, transparent);
  color: var(--tier-tolerance1);
}
.badge--tolerance2 {
  background-color: color-mix(in srgb, var(--tier-tolerance2) 15%, transparent);
  color: var(--tier-tolerance2);
}
.badge--nearest {
  background-color: color-mix(in srgb, var(--tier-nearest) 15%, transparent);
  color: var(--tier-nearest);
}
</style>
