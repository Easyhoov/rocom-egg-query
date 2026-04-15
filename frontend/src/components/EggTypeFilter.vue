<script setup>
const props = defineProps({
  modelValue: {
    type: String,
    default: 'all'
  }
})

const emit = defineEmits(['update:modelValue'])

const options = [
  { value: 'all', label: '全部', color: null },
  { value: 'normal', label: '普通蛋', color: 'var(--egg-normal)' },
  { value: 'precious', label: '炫彩蛋', color: 'var(--egg-precious)' }
]

function select(value) {
  emit('update:modelValue', value)
}
</script>

<template>
  <div class="egg-type-filter">
    <button
      v-for="opt in options"
      :key="opt.value"
      type="button"
      class="pill"
      :class="{ active: modelValue === opt.value }"
      :style="modelValue === opt.value && opt.color ? { backgroundColor: opt.color, borderColor: opt.color, color: '#fff' } : {}"
      @click="select(opt.value)"
    >
      {{ opt.label }}
    </button>
  </div>
</template>

<style scoped>
.egg-type-filter {
  display: flex;
  gap: 8px;
}

.pill {
  padding: 6px 16px;
  border-radius: var(--radius-pill);
  border: 1px solid var(--border);
  background-color: var(--bg);
  color: var(--text);
  font-family: var(--font);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color var(--transition), border-color var(--transition), color var(--transition);
}

.pill:hover {
  border-color: var(--accent);
}

.pill.active {
  background-color: var(--accent);
  color: #fff;
  border-color: var(--accent);
}
</style>
