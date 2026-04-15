<script setup>
import { ref, watch } from 'vue'
import EggTypeFilter from './EggTypeFilter.vue'

const props = defineProps({
  modelHeight: {
    type: String,
    default: ''
  },
  modelWeight: {
    type: String,
    default: ''
  },
  eggType: {
    type: String,
    default: 'all'
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelHeight', 'update:modelWeight', 'update:eggType', 'search'])

const localEggType = ref(props.eggType)

watch(localEggType, (val) => {
  emit('update:eggType', val)
})

function onSubmit() {
  if (props.loading) return
  emit('search')
}
</script>

<template>
  <form @submit.prevent="onSubmit" class="query-form">
    <div class="input-group">
      <label>蛋尺寸 (m)</label>
      <input
        type="number"
        step="0.001"
        min="0"
        placeholder="0.24"
        :value="modelHeight"
        @input="$emit('update:modelHeight', $event.target.value)"
      />
    </div>
    <div class="input-group">
      <label>蛋重量 (kg)</label>
      <input
        type="number"
        step="0.001"
        min="0"
        placeholder="1.60"
        :value="modelWeight"
        @input="$emit('update:modelWeight', $event.target.value)"
      />
    </div>
    <EggTypeFilter v-model="localEggType" />
    <button type="submit" class="submit-btn" :disabled="loading">
      {{ loading ? '查询中...' : '🔍 立即查询' }}
    </button>
  </form>
</template>

<style scoped>
.query-form {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  background-color: var(--bg-alt);
  padding: 20px;
  border-radius: var(--radius-card);
  box-shadow: var(--shadow-card);
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.input-group label {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-weak);
}

.input-group input {
  padding: 10px 12px;
  font-family: var(--font);
  font-size: 14px;
  color: var(--text);
  background-color: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  transition: border-color var(--transition), box-shadow var(--transition);
  outline: none;
}

.input-group input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 2px color-mix(in srgb, var(--accent) 20%, transparent);
}

.input-group input::placeholder {
  color: var(--text-weak);
}

.submit-btn {
  grid-column: 1 / -1;
  padding: 12px 24px;
  font-family: var(--font);
  font-size: 15px;
  font-weight: 600;
  color: #fff;
  background-color: var(--accent);
  border: none;
  border-radius: var(--radius-btn);
  cursor: pointer;
  transition: background-color var(--transition), transform 0.1s ease;
}

.submit-btn:hover:not(:disabled) {
  background-color: var(--accent-hover);
}

.submit-btn:active:not(:disabled) {
  transform: scale(0.97);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 480px) {
  .query-form {
    grid-template-columns: 1fr;
  }
}
</style>
