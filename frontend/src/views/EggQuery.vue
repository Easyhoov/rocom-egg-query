<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const height = ref(null)
const weight = ref(null)
const eggType = ref('magic') // 'magic' | 'colorful' | 'all'
const loading = ref(false)
const error = ref('')
const results = ref([])
const total = ref(0)
const normalCount = ref(0)
const preciousCount = ref(0)
const userR = ref(0)
const tab = ref('all')
const showTip = ref(false)
const hasQueried = ref(false)

// URL hash 参数解析
function parseHash() {
  const h = location.hash
  if (!h) return
  const mh = h.match(/h=([\d.]+)/)
  const mw = h.match(/w=([\d.]+)/)
  if (mh) height.value = parseFloat(mh[1])
  if (mw) weight.value = parseFloat(mw[1])
}

// 蛋类型标签
const eggTags = [
  { key: 'magic', label: '🥚 神奇的蛋' },
  { key: 'colorful', label: '✨ 炫彩蛋' },
  { key: 'all', label: '📦 不限类型' },
]

// 查询
async function queryEgg() {
  if (!height.value || !weight.value) {
    error.value = '请输入身高和体重'
    return
  }
  loading.value = true
  error.value = ''
  try {
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), 15000)
    let url = `/api/query?height=${height.value}&weight=${weight.value}`
    if (eggType.value === 'magic') url += '&precious=0'
    else if (eggType.value === 'colorful') url += '&precious=1'
    const res = await fetch(url, { signal: controller.signal })
    clearTimeout(timeout)
    if (!res.ok) {
      if (res.status === 404) throw new Error('接口不存在，请检查服务是否正常运行')
      if (res.status >= 500) throw new Error(`服务器错误(${res.status})，请稍后重试`)
      throw new Error(`请求失败(${res.status})`)
    }
    const data = await res.json()
    if (data.success) {
      results.value = data.results
      total.value = data.total
      normalCount.value = data.normal_count
      preciousCount.value = data.precious_count
      userR.value = data.user_r || 0
      hasQueried.value = true
      await nextTick()
      document.querySelector('.garden__result')?.scrollIntoView({ behavior: 'smooth' })
    } else {
      throw new Error(data.message || '查询失败')
    }
  } catch (e) {
    if (e.name === 'AbortError') error.value = '请求超时，请检查网络后重试'
    else if (e.name === 'TypeError' && e.message.includes('Failed to fetch')) error.value = '网络连接失败'
    else error.value = e.message || '查询失败，请稍后重试'
  } finally {
    loading.value = false
  }
}

// Tab 筛选
const filteredResults = computed(() => {
  if (tab.value === 'normal') return results.value.filter(r => r.precious_type === 0)
  if (tab.value === 'special') return results.value.filter(r => r.precious_type > 0)
  return results.value
})

// Emoji fallback
function ico(name) {
  if (!name) return '🐾'
  const m = {
    '喵': '🐱', '水蓝': '💧', '火': '🔥', '迪莫': '✨', '鸟': '🐦',
    '鸭': '🦆', '鼠': '🐭', '犬': '🐕', '猫': '🐱', '虫': '🐛',
    '蝶': '🦋', '花': '🌸', '草': '🌿', '石': '🪨', '龙': '🐉',
    '蛇': '🐍', '兔': '🐰', '羊': '🐑', '猪': '🐷', '熊': '🐻',
    '狐': '🦊', '鱼': '🐟', '龟': '🐢', '蜂': '🐝', '蛛': '🕷️',
    '菇': '🍄', '树': '🌳', '冰': '❄️', '电': '⚡', '雪': '🌨️',
    '精灵': '🧚', '恶魔': '😈', '幽': '👻', '幻': '🔮', '甲': '🪲',
    '鹰': '🦅', '狼': '🐺',
  }
  for (const [k, v] of Object.entries(m)) if (name.includes(k)) return v
  return '🐾'
}

function imgError(e) {
  const item = e.target.closest('.pc')?.querySelector('.pc__ico')
  if (item) {
    const name = item.dataset.name || ''
    item.textContent = ico(name)
  }
}

function onKeydown(e) {
  if (e.key === 'Enter') queryEgg()
}

onMounted(() => {
  parseHash()
  document.addEventListener('keydown', onKeydown)
})
onUnmounted(() => {
  document.removeEventListener('keydown', onKeydown)
})
</script>

<template>
  <div class="garden">
    <div class="garden__box">
      <div class="garden__hd">
        <h1>🥚 孵蛋查询</h1>
        <p class="garden__sub">洛克王国：世界</p>
      </div>

      <!-- 表单 -->
      <div class="garden__card">
        <div class="eq-row">
          <div class="eq-ipt">
            <label>身高 (m)</label>
            <input v-model.number="height" type="number" step="0.01" min="0" placeholder="0.24" class="eq-input">
          </div>
          <div class="eq-ipt">
            <label>体重 (kg)</label>
            <input v-model.number="weight" type="number" step="0.001" min="0" placeholder="1.600" class="eq-input">
          </div>
        </div>
        <div class="eq-tags">
          <span
            v-for="t in eggTags" :key="t.key"
            class="eq-tag"
            :class="{ 'eq-tag--on': eggType === t.key }"
            @click="eggType = t.key"
          >{{ t.label }}</span>
        </div>
        <button class="query-btn" :disabled="loading" @click="queryEgg">
          {{ loading ? '查询中...' : '查询' }}
        </button>
      </div>

      <!-- 错误提示 -->
      <div v-if="error" class="error-msg">{{ error }}</div>

      <!-- 结果 -->
      <div v-if="hasQueried && results.length" class="garden__card garden__result">
        <div class="eq-tabs">
          <button class="eq-tb" :class="{ 'eq-tb--on': tab === 'all' }" @click="tab = 'all'">
            全部 <span class="eq-n">{{ total }}</span>
          </button>
          <button class="eq-tb" :class="{ 'eq-tb--on': tab === 'normal' }" @click="tab = 'normal'">
            🥚 神奇 <span class="eq-n">{{ normalCount }}</span>
          </button>
          <button class="eq-tb" :class="{ 'eq-tb--on': tab === 'special' }" @click="tab = 'special'">
            ✨ 炫彩 <span class="eq-n">{{ preciousCount }}</span>
          </button>
        </div>
        <div class="eq-rval">你的R值: {{ userR.toFixed(2) }}</div>
        <div v-if="filteredResults.length" class="grid">
          <div
            v-for="r in filteredResults" :key="r.name + '-' + r.spirit_id"
            class="pc"
            :class="{ 'pc--precious': r.precious_type > 0 }"
            @click="r.spirit_id && router.push('/compendium/' + r.spirit_id)"
          >
            <div class="pc__badge" :style="{ background: r.egg_type_color }">
              {{ r.egg_type_icon }} {{ (r.egg_type_name || '').replace('蛋', '') }}
            </div>
            <div class="pc__ico" :data-name="r.name">
              <img v-if="r.image" :src="r.image" class="pc__img" @error="e => { e.target.remove(); e.target.parentElement.textContent = ico(r.name) }" loading="lazy">
              <span v-else class="pc__emoji">{{ ico(r.name) }}</span>
            </div>
            <div class="pc__name" :title="r.name">{{ r.name }}</div>
            <div class="pc__range">{{ r.height_min?.toFixed(2) }}-{{ r.height_max?.toFixed(2) }}m</div>
            <div class="pc__rval">🎯R值: {{ r.r_value?.toFixed(2) || '-' }}</div>
            <div class="pc__rdiff">📏差值: {{ r.r_diff != null ? r.r_diff.toFixed(2) : '-' }}</div>
          </div>
        </div>
        <div v-else style="text-align:center;padding:20px 0">
          <div style="font-size:36px;margin-bottom:8px">🐣</div>
          <p style="color:#ccc;font-size:13px">该筛选下暂无结果</p>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else-if="hasQueried && !results.length" class="garden__card garden__result" style="text-align:center">
        <div style="font-size:48px;margin-bottom:8px">🐣</div>
        <p style="color:#ccc">暂无结果</p>
      </div>

      <!-- 底部 -->
      <div class="eq-ft">
        数据 <a href="https://github.com/jiluoQAQ/RocomUID" target="_blank">RocomUID</a> |
        <a href="javascript:void(0)" @click="showTip = true">R值说明</a>
      </div>
    </div>

    <!-- R值说明弹窗 -->
    <div class="eq-tip" :class="{ 'eq-tip--on': showTip }" @click="showTip = false">
      <div class="eq-tip--box" @click.stop>
        <h3>📊 R值说明</h3>
        <p>
          🎯 <b>R值公式</b> — R = 体重(kg) ÷ 身高(m)<br>
          📏 差值越小表示越接近你的精灵属性，匹配概率越高
        </p>
        <button @click="showTip = false">我知道了</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.garden {
  min-height: 100vh;
  background: linear-gradient(180deg, #f0ecff 0%, #ffffff 100%);
  padding: 16px 16px 80px;
}
.garden__box { max-width: 420px; margin: 0 auto; }
.garden__hd { text-align: center; padding: 24px 0 20px; }
.garden__hd h1 { font-size: 22px; color: #1a1a2e; font-weight: 700; margin: 0 0 6px; }
.garden__sub { font-size: 13px; color: #888; margin: 0; }
.garden__card {
  background: #fff;
  border-radius: 18px;
  padding: 16px;
  box-shadow: 0 4px 16px rgba(15,16,21,0.08);
  margin-bottom: 12px;
}
.garden__result {
  display: flex;
  flex-direction: column;
}
.query-btn {
  width: 100%;
  padding: 12px;
  background: #8b3dff;
  color: #fff;
  border: none;
  border-radius: 14px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: .15s;
}
.query-btn:active { transform: scale(.97); }
.query-btn:disabled { opacity: .5; cursor: not-allowed; }

/* Error */
.error-msg {
  background: #fff0f0;
  color: #e74c3c;
  padding: 12px 16px;
  border-radius: 14px;
  font-size: 14px;
  text-align: center;
  margin-bottom: 12px;
}

/* Form row */
.eq-row { display: flex; gap: 12px; margin-bottom: 12px; }
.eq-ipt { flex: 1; }
.eq-ipt label { display: block; font-size: 12px; color: #888; margin-bottom: 6px; }
.eq-input {
  width: 100%;
  padding: 12px;
  border: 1.5px solid #e8e8e8;
  border-radius: 10px;
  font-size: 17px;
  font-weight: 500;
  background: #fafafa;
  transition: .2s;
  box-sizing: border-box;
}
.eq-input:focus { outline: none; border-color: #8b3dff; background: #fff; }

/* Tags */
.eq-tags { display: flex; gap: 8px; margin-bottom: 12px; flex-wrap: wrap; }
.eq-tag {
  padding: 7px 14px;
  border-radius: 20px;
  font-size: 13px;
  border: 1.5px solid #e8e8e8;
  background: #fff;
  color: #666;
  cursor: pointer;
  transition: .2s;
  user-select: none;
}
.eq-tag--on { border-color: #8b3dff; background: #8b3dff; color: #fff; }

/* Tabs */
.eq-tabs { display: flex; background: #f5f5f5; border-radius: 10px; padding: 3px; margin-bottom: 8px; }
.eq-tb {
  flex: 1;
  padding: 8px 0;
  text-align: center;
  border-radius: 8px;
  font-size: 13px;
  color: #888;
  cursor: pointer;
  border: none;
  background: none;
  transition: .2s;
}
.eq-tb--on { background: #fff; color: #333; font-weight: 600; box-shadow: 0 1px 4px rgba(0,0,0,.08); }
.eq-n { font-weight: 700; color: #8b3dff; }

/* R值 */
.eq-rval { text-align: center; font-size: 10px; color: #8b3dff; margin: 4px 0; font-weight: 500; }

/* 3列网格 */
.grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }

/* Pet card */
.pc {
  background: #f5f2ff;
  border-radius: 10px;
  padding: 28px 4px 8px;
  text-align: center;
  border: 1.5px solid transparent;
  transition: .15s;
  position: relative;
  overflow: hidden;
  cursor: pointer;
}
.pc:hover { box-shadow: 0 8px 24px rgba(139,61,255,0.12); }
.pc:active { transform: scale(.96); }
.pc--precious {
  background: linear-gradient(135deg, #fffdf0, #fff8dc);
  border-color: rgba(102, 126, 234, 0.25);
}
.pc__badge {
  position: absolute;
  top: 3px;
  right: 3px;
  font-size: 9px;
  padding: 1px 5px;
  border-radius: 6px;
  font-weight: 600;
  color: #fff;
  max-width: 70px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.pc__ico {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  margin: 0 auto 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  background: linear-gradient(135deg, #f0ecff, #e2d6ff);
  overflow: hidden;
}
.pc--precious .pc__ico { background: linear-gradient(135deg, #fff3cd, #ffe082); }
.pc__img { width: 48px; height: 48px; object-fit: contain; }
.pc__emoji { font-size: 20px; }
.pc__name {
  font-size: 11px;
  font-weight: 600;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.2;
  max-width: 100%;
  padding: 0 2px;
}
.pc__range { font-size: 9px; color: #bbb; margin-top: 1px; }
.pc__rval { font-size: 9px; color: #8b3dff; font-weight: 500; margin-top: 1px; }
.pc__rdiff { font-size: 9px; color: #ff6d00; font-weight: 500; margin-top: 1px; }

/* Footer */
.eq-ft { text-align: center; padding: 16px 0 8px; font-size: 11px; color: #bbb; }
.eq-ft a { color: #999; }

/* Tip modal */
.eq-tip {
  display: none;
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,.4);
  z-index: 100;
  justify-content: center;
  align-items: center;
}
.eq-tip--on { display: flex; }
.eq-tip--box {
  background: #fff;
  border-radius: 18px;
  padding: 24px;
  width: 85%;
  max-width: 320px;
}
.eq-tip--box h3 { font-size: 16px; margin-bottom: 12px; }
.eq-tip--box p { font-size: 13px; color: #666; line-height: 1.8; }
.eq-tip--box button {
  margin-top: 16px;
  width: 100%;
  padding: 10px;
  border: none;
  background: #8b3dff;
  color: #fff;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
}
</style>
