<script setup>
import { computed } from 'vue'

const props = defineProps({
  probability: {
    type: Number,
    required: true,
    default: 0
  }
})

const fillColor = computed(() => {
  if (props.probability > 80) return 'var(--success)'
  if (props.probability > 40) return 'var(--accent)'
  return 'var(--warning)'
})
</script>

<template>
  <div class="prob-bar">
    <div
      class="prob-bar__fill"
      :style="{ width: `${Math.min(100, Math.max(0, probability))}%`, backgroundColor: fillColor }"
    ></div>
  </div>
</template>

<style scoped>
.prob-bar {
  height: 6px;
  border-radius: var(--radius-pill);
  background-color: var(--bg-alt);
  overflow: hidden;
}
.prob-bar__fill {
  height: 100%;
  border-radius: var(--radius-pill);
  transition: width 0.6s ease;
}
</style>
