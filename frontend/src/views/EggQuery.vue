<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import '../styles/dark-theme.css'

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
  { key: 'magic', label: '神奇的蛋' },
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
  <div class="garden dark-page">
    <div class="garden__box">
      <div class="garden__hd">
        <h1><img src="/favicon.png" alt="神奇的蛋" class="title-egg"> 孵蛋查询</h1>
        <p class="garden__sub">洛克王国：世界</p>
      </div>

      <!-- 表单 -->
      <div class="garden__card dark-card">
        <div class="eq-row">
          <div class="eq-ipt">
            <label>身高 (m)</label>
            <input v-model.number="height" type="number" step="0.01" min="0" placeholder="0.24" class="eq-input dark-input">
          </div>
          <div class="eq-ipt">
            <label>体重 (kg)</label>
            <input v-model.number="weight" type="number" step="0.001" min="0" placeholder="1.600" class="eq-input dark-input">
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
        <button class="query-btn dark-btn dark-btn--accent" :disabled="loading" @click="queryEgg">
          {{ loading ? '查询中...' : '查询' }}
        </button>
      </div>

      <!-- 错误提示 -->
      <div v-if="error" class="error-msg">{{ error }}</div>

      <!-- 结果 -->
      <div v-if="hasQueried && results.length" class="garden__card garden__result dark-card">
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
      <div v-else-if="hasQueried && !results.length" class="garden__card garden__result dark-card" style="text-align:center">
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
/* ===== 组件专属布局样式（深色主题由 dark-theme.css 提供） ===== */

/* 页面内边距 */
.garden { padding: 16px 16px 80px; }

/* 容器 */
.garden__box { max-width: 420px; margin: 0 auto; position: relative; z-index: 1; }
.garden__hd { text-align: center; padding: 24px 0 20px; }
.garden__hd h1 { font-size: 22px; font-weight: 700; margin: 0 0 6px; display: flex; align-items: center; justify-content: center; gap: 6px; color: #fff; }
.title-egg { width: 28px; height: 28px; vertical-align: middle; }
.garden__sub { font-size: 13px; margin: 0; color: rgba(255, 255, 255, 0.75); }

/* 卡片内边距/间距（背景/边框/圆角由 .dark-card 提供） */
.garden__card { padding: 16px; margin-bottom: 12px; }
.garden__result { display: flex; flex-direction: column; }

/* 查询按钮（宽度为组件专属，其余由 .dark-btn 提供） */
.query-btn { width: 100%; }

/* 错误提示 */
.error-msg {
  background: var(--dt-error-bg);
  color: var(--dt-error-text);
  padding: 12px 16px;
  border-radius: 14px;
  font-size: 14px;
  text-align: center;
  margin-bottom: 12px;
  border: 1px solid rgba(231, 76, 60, 0.2);
}

/* 表单行 */
.eq-row { display: flex; gap: 12px; margin-bottom: 12px; }
.eq-ipt { flex: 1; }
.eq-ipt label { display: block; font-size: 12px; color: var(--dt-text-muted); margin-bottom: 6px; }
/* 输入框只保留 font-weight，其余由 .dark-input 提供 */
.eq-input { font-weight: 500; }

/* 标签 */
.eq-tags { display: flex; gap: 8px; margin-bottom: 12px; flex-wrap: wrap; }
.eq-tag {
  padding: 7px 14px;
  border-radius: 20px;
  font-size: 13px;
  border: 1.5px solid var(--dt-tag-border);
  background: var(--dt-tag-bg);
  color: var(--dt-tag-text);
  cursor: pointer;
  transition: .2s;
  user-select: none;
}
.eq-tag--on { border-color: var(--dt-accent); background: var(--dt-accent); color: #fff; }

/* 标签页 */
.eq-tabs { display: flex; background: rgba(255, 255, 255, 0.06); border-radius: 10px; padding: 3px; margin-bottom: 8px; }
.eq-tb {
  flex: 1;
  padding: 8px 0;
  text-align: center;
  border-radius: 8px;
  font-size: 13px;
  color: var(--dt-text-muted);
  cursor: pointer;
  border: none;
  background: none;
  transition: .2s;
}
.eq-tb--on { background: rgba(255, 255, 255, 0.1); color: #fff; font-weight: 600; }
.eq-n { font-weight: 700; color: var(--dt-accent); }

/* R值 */
.eq-rval { text-align: center; font-size: 10px; color: var(--dt-accent); margin: 4px 0; font-weight: 500; }

/* 3列网格 */
.grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }

/* 精灵卡片 */
.pc {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  padding: 28px 4px 8px;
  text-align: center;
  transition: .15s;
  position: relative;
  overflow: hidden;
  cursor: pointer;
}
.pc:hover { border-color: var(--dt-accent-glow); box-shadow: 0 8px 24px rgba(139, 61, 255, 0.15); }
.pc:active { transform: scale(.96); }
.pc--precious {
  background: rgba(255, 215, 0, 0.08);
  border-color: rgba(255, 215, 0, 0.2);
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
  background: rgba(139, 61, 255, 0.15);
  overflow: hidden;
}
.pc--precious .pc__ico { background: rgba(255, 215, 0, 0.15); }
.pc__img { width: 48px; height: 48px; object-fit: contain; }
.pc__emoji { font-size: 20px; }
.pc__name {
  font-size: 11px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.2;
  max-width: 100%;
  padding: 0 2px;
}
.pc__range { font-size: 9px; color: var(--dt-text-muted); margin-top: 1px; opacity: 0.8; }
.pc__rval { font-size: 9px; color: var(--dt-accent); font-weight: 500; margin-top: 1px; }
.pc__rdiff { font-size: 9px; color: #ff9800; font-weight: 500; margin-top: 1px; }

/* 底部 */
.eq-ft { text-align: center; padding: 16px 0 8px; font-size: 11px; color: var(--dt-text-muted); }
.eq-ft a { color: rgba(255, 255, 255, 0.6); }

/* 弹窗遮罩 */
.eq-tip {
  display: none;
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  z-index: 100;
  justify-content: center;
  align-items: center;
}
.eq-tip--on { display: flex; }
/* 弹窗内容复用 .dark-card，仅补充组件专属间距 */
.eq-tip--box {
  padding: 24px;
  width: 85%;
  max-width: 320px;
}
.eq-tip--box h3 { font-size: 16px; margin-bottom: 12px; }
.eq-tip--box p { font-size: 13px; line-height: 1.8; }
.eq-tip--box button { margin-top: 16px; width: 100%; padding: 10px; border-radius: 8px; font-size: 14px; }
</style>
