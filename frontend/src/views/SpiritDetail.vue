<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const spirit = ref(null)
const loading = ref(true)

const spiritId = computed(() => route.params.id)

const statLabels = {
  hp: '生命', attack: '物攻', magic_attack: '魔攻',
  defense: '物防', magic_defense: '魔防', speed: '速度'
}

function getImageUrl(s) {
  if (s?.image) return s.image
  return null
}

const stats = computed(() => {
  if (!spirit.value) return []
  const s = spirit.value
  return [
    { key: 'hp', label: '生命', value: s.hp, color: '#4caf50' },
    { key: 'attack', label: '物攻', value: s.attack, color: '#e74c3c' },
    { key: 'magic_attack', label: '魔攻', value: s.magic_attack, color: '#9b59b6' },
    { key: 'defense', label: '物防', value: s.defense, color: '#3498db' },
    { key: 'magic_defense', label: '魔防', value: s.magic_defense, color: '#f39c12' },
    { key: 'speed', label: '速度', value: s.speed, color: '#1abc9c' },
  ]
})

async function fetchDetail() {
  loading.value = true
  try {
    const res = await fetch(`/api/spirits/${spiritId.value}`)
    const data = await res.json()
    if (data.success) spirit.value = data.spirit
  } catch (e) {
    console.error('获取精灵详情失败:', e)
  } finally {
    loading.value = false
  }
}

function goBack() {
  if (window.history.length > 1) router.back()
  else router.push('/compendium')
}

onMounted(fetchDetail)
watch(spiritId, fetchDetail)
</script>

<template>
  <div class="min-h-screen bg-gray-950 text-gray-100">
    <!-- 顶部导航 -->
    <header class="sticky top-0 z-10 bg-gray-950/90 backdrop-blur border-b border-gray-800">
      <div class="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
        <button
          @click="goBack"
          class="text-sm text-gray-400 hover:text-white transition flex items-center gap-1"
        >
          ← 返回图鉴
        </button>
        <span v-if="spirit" class="text-xs text-gray-600">{{ spirit.spirit_no }}</span>
      </div>
    </header>

    <div class="max-w-4xl mx-auto px-4 py-6">
      <!-- Loading -->
      <div v-if="loading" class="text-center py-20">
        <div class="inline-block w-8 h-8 border-3 border-gray-700 border-t-yellow-400 rounded-full animate-spin mb-3"></div>
        <p class="text-gray-500">加载中...</p>
      </div>

      <!-- Not Found -->
      <div v-else-if="!spirit" class="text-center py-20 text-gray-500">
        <p class="text-4xl mb-3">❌</p>
        <p>精灵不存在</p>
        <button @click="goBack" class="mt-4 px-4 py-2 bg-gray-800 rounded-lg text-sm hover:bg-gray-700 transition">
          返回图鉴
        </button>
      </div>

      <template v-else>
        <!-- 基础信息 -->
        <div class="bg-gray-900 rounded-xl border border-gray-800 p-5 mb-5">
          <div class="flex flex-col sm:flex-row gap-5">
            <!-- 图片 -->
            <div class="w-36 h-36 sm:w-44 sm:h-44 flex-shrink-0 flex items-center justify-center bg-gray-800/50 rounded-xl overflow-hidden mx-auto sm:mx-0">
              <img
                v-if="getImageUrl(spirit)"
                :src="getImageUrl(spirit)"
                :alt="spirit.base_name"
                class="w-[90%] h-[90%] object-contain"
              />
              <span v-else class="text-5xl opacity-30">❓</span>
            </div>

            <!-- 信息 -->
            <div class="flex-1 text-center sm:text-left">
              <div class="flex items-baseline gap-2 justify-center sm:justify-start mb-2">
                <span class="text-sm text-gray-500">{{ spirit.spirit_no }}</span>
                <h1 class="text-2xl font-bold">{{ spirit.display_name || spirit.base_name }}</h1>
              </div>

              <!-- 标签 -->
              <div class="flex flex-wrap gap-2 justify-center sm:justify-start mb-3">
                <span
                  v-if="spirit.primary_attribute"
                  class="text-xs px-2 py-1 rounded bg-yellow-500/20 text-yellow-400 font-medium"
                >
                  {{ spirit.primary_attribute }}
                </span>
                <span
                  v-if="spirit.secondary_attribute"
                  class="text-xs px-2 py-1 rounded bg-green-500/20 text-green-400 font-medium"
                >
                  {{ spirit.secondary_attribute }}
                </span>
                <span
                  v-if="spirit.form_name"
                  class="text-xs px-2 py-1 rounded bg-gray-700 text-gray-400"
                >
                  {{ spirit.form_name }}
                </span>
                <span
                  v-if="!spirit.can_breed"
                  class="text-xs px-2 py-1 rounded bg-red-900/30 text-red-400"
                >
                  不可孵蛋
                </span>
                <span
                  v-if="spirit.has_shiny_variant"
                  class="text-xs px-2 py-1 rounded bg-purple-900/30 text-purple-400"
                >
                  ✨ 有异色
                </span>
              </div>

              <!-- 基础数据 -->
              <div class="grid grid-cols-2 gap-x-6 gap-y-1 text-sm text-gray-400 mb-3">
                <div v-if="spirit.height_text">📏 身高：{{ spirit.height_text }}</div>
                <div v-if="spirit.weight_text">⚖️ 体重：{{ spirit.weight_text }}</div>
                <div v-if="spirit.stage_name">📊 阶段：{{ spirit.stage_name }}</div>
                <div v-if="spirit.race_total" class="text-yellow-400 font-medium">⭐ 种族值：{{ spirit.race_total }}</div>
              </div>

              <!-- 蛋组 -->
              <div v-if="spirit.egg_groups?.length" class="text-sm mb-2">
                <span class="text-gray-500">蛋组：</span>
                <span
                  v-for="g in spirit.egg_groups"
                  :key="g"
                  class="inline-block text-xs px-2 py-0.5 rounded bg-yellow-900/20 text-yellow-400/80 mr-1"
                >
                  {{ g }}
                </span>
              </div>

              <!-- 描述 -->
              <p v-if="spirit.description" class="text-sm text-gray-500 mt-2 leading-relaxed">
                {{ spirit.description }}
              </p>
            </div>
          </div>
        </div>

        <!-- 特性 -->
        <div v-if="spirit.trait_name" class="bg-gray-900 rounded-xl border border-gray-800 p-5 mb-5">
          <h2 class="text-base font-bold mb-2 flex items-center gap-2">
            💡 特性
          </h2>
          <div class="flex items-start gap-3">
            <span class="text-sm font-medium text-yellow-400 bg-yellow-900/20 px-3 py-1 rounded-lg">
              {{ spirit.trait_name }}
            </span>
            <span v-if="spirit.trait_effect" class="text-sm text-gray-400 leading-relaxed">
              {{ spirit.trait_effect }}
            </span>
          </div>
        </div>

        <!-- 种族值 -->
        <div v-if="spirit.race_total" class="bg-gray-900 rounded-xl border border-gray-800 p-5 mb-5">
          <h2 class="text-base font-bold mb-4 flex items-center gap-2">
            📊 种族值
            <span class="text-sm text-yellow-400 font-normal">总和 {{ spirit.race_total }}</span>
          </h2>
          <div class="space-y-2.5">
            <div v-for="stat in stats" :key="stat.key" class="flex items-center gap-3">
              <span class="w-10 text-xs text-gray-500 text-right">{{ stat.label }}</span>
              <div class="flex-1 h-5 bg-gray-800 rounded-full overflow-hidden">
                <div
                  class="h-full rounded-full transition-all duration-500"
                  :style="{
                    width: Math.min((stat.value || 0) / 150 * 100, 100) + '%',
                    backgroundColor: stat.color
                  }"
                ></div>
              </div>
              <span class="w-8 text-xs font-semibold text-right" :style="{ color: stat.color }">
                {{ stat.value || 0 }}
              </span>
            </div>
          </div>
        </div>

        <!-- 进化链 -->
        <div v-if="spirit.evolution_chain?.length > 1" class="bg-gray-900 rounded-xl border border-gray-800 p-5 mb-5">
          <h2 class="text-base font-bold mb-4">🔄 进化链</h2>
          <div class="flex items-center flex-wrap gap-2">
            <template v-for="(evo, idx) in spirit.evolution_chain" :key="evo.spirit_id">
              <!-- 箭头 -->
              <div v-if="idx > 0" class="flex flex-col items-center px-1">
                <span class="text-gray-600 text-lg">→</span>
                <span v-if="evo.evolution_level_text" class="text-[10px] text-gray-500">
                  Lv.{{ evo.evolution_level_text }}
                </span>
              </div>

              <!-- 进化节点 -->
              <router-link
                :to="`/compendium/${evo.spirit_id}`"
                :class="[
                  'flex flex-col items-center p-2 rounded-lg transition min-w-[80px]',
                  evo.spirit_id === spirit.spirit_id
                    ? 'bg-yellow-900/20 border border-yellow-500/30'
                    : 'hover:bg-gray-800'
                ]"
              >
                <div class="w-14 h-14 flex items-center justify-center bg-gray-800/50 rounded-lg overflow-hidden mb-1">
                  <img
                    v-if="evo.image"
                    :src="evo.image"
                    :alt="evo.base_name"
                    class="w-12 h-12 object-contain"
                    loading="lazy"
                  />
                  <span v-else class="text-2xl opacity-30">❓</span>
                </div>
                <span class="text-xs font-medium">{{ evo.base_name }}</span>
                <span class="text-[10px] text-gray-500">{{ evo.spirit_no }}</span>
                <span v-if="evo.form_name" class="text-[10px] text-gray-600">{{ evo.form_name }}</span>
              </router-link>
            </template>
          </div>
        </div>

        <!-- 其他形态 -->
        <div v-if="spirit.forms?.length > 1" class="bg-gray-900 rounded-xl border border-gray-800 p-5 mb-5">
          <h2 class="text-base font-bold mb-4">🎭 其他形态</h2>
          <div class="flex flex-wrap gap-2">
            <router-link
              v-for="form in spirit.forms"
              :key="form.spirit_id"
              :to="`/compendium/${form.spirit_id}`"
              :class="[
                'px-3 py-2 rounded-lg text-sm transition border',
                form.spirit_id === spirit.spirit_id
                  ? 'bg-yellow-900/20 border-yellow-500/30 text-yellow-400'
                  : 'bg-gray-800 border-gray-700 text-gray-300 hover:border-gray-600'
              ]"
            >
              {{ form.display_name || form.base_name }}
              <span v-if="form.form_name" class="text-xs text-gray-500 ml-1">({{ form.form_name }})</span>
            </router-link>
          </div>
        </div>

        <!-- 出没地点 -->
        <div v-if="spirit.locations?.length" class="bg-gray-900 rounded-xl border border-gray-800 p-5 mb-5">
          <h2 class="text-base font-bold mb-3">📍 出没地点</h2>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="loc in spirit.locations"
              :key="loc"
              class="text-xs px-2 py-1 rounded bg-gray-800 text-gray-400"
            >
              {{ loc }}
            </span>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>
