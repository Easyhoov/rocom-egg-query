<script setup>
import { ref, onMounted } from 'vue'

const loading = ref(true)
const error = ref('')
const merchant = ref(null)

function onImgError(e) {
  const img = e.target
  img.style.display = 'none'
  const wrap = img.parentElement
  const fallback = wrap.querySelector('.m-fallback')
  if (fallback) fallback.style.display = 'flex'
}

async function fetchMerchant(refresh = false) {
  loading.value = true
  error.value = ''
  try {
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), 15000)
    const url = refresh ? '/api/merchant/info?refresh=true' : '/api/merchant/info'
    const res = await fetch(url, { signal: controller.signal })
    clearTimeout(timeout)
    if (!res.ok) {
      if (res.status === 404) throw new Error('接口不存在，请检查服务是否正常运行')
      if (res.status >= 500) throw new Error(`服务器错误(${res.status})，请稍后重试`)
      throw new Error(`请求失败(${res.status})`)
    }
    const data = await res.json()
    if (data.success) {
      merchant.value = data.merchant
    } else {
      throw new Error(data.error || '获取数据失败')
    }
  } catch (e) {
    if (e.name === 'AbortError') error.value = '请求超时，请检查网络后重试'
    else if (e.name === 'TypeError' && e.message.includes('Failed to fetch')) error.value = '网络连接失败'
    else error.value = e.message || '查询失败，请稍后重试'
  } finally {
    loading.value = false
  }
}

onMounted(() => fetchMerchant())
</script>

<template>
  <div class="m-page">
    <div class="m-bg"></div>
    <div class="m-content">
      <!-- Loading -->
      <div v-if="loading" class="m-loading">
        <div class="m-spinner"></div>
        <p>加载中...</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="m-empty">
        <p style="font-size: 48px; margin-bottom: 8px;">😵</p>
        <p>{{ error }}</p>
        <button class="m-retry" @click="fetchMerchant(true)">重试</button>
      </div>

      <template v-else>
        <!-- Header -->
        <div class="m-header">
          <div class="m-header-left">
            <div class="m-title-row">
              <span class="m-icon">🛒</span>
              <span class="m-title">远行商人</span>
            </div>
            <div class="m-subtitle">洛克王国 · 今日特供</div>
          </div>
          <div class="m-header-right">
            <div class="m-chip">当前商品数 <strong>{{ merchant?.goods_count || 0 }}</strong></div>
            <div class="m-round-row">
              <span class="m-round-pill" v-if="merchant?.round?.is_open">
                第 {{ merchant.round.current }} / {{ merchant.round.total }} 轮
              </span>
              <span class="m-round-pill" v-else>已打烊</span>
              <span class="m-countdown-pill" v-if="merchant?.round?.is_open">
                剩余 {{ merchant.round.countdown }}
              </span>
            </div>
          </div>
        </div>

        <!-- Products Grid -->
        <div class="m-grid">
          <div v-for="(g, i) in merchant?.goods || []" :key="i" class="m-card">
            <div class="m-card-img-wrap">
              <img :src="g.icon" :alt="g.name" class="m-card-img"
                   @error="onImgError" />
              <span class="m-fallback" style="display:none">🧪</span>
            </div>
            <div class="m-card-body">
              <div class="m-card-name">{{ g.name }}</div>
              <div class="m-card-sub">远行商人当期商品</div>
              <div class="m-card-time">⏰ {{ g.time_label }}</div>
            </div>
            <div class="m-card-side">
              <span class="m-card-slot">第{{ Math.ceil((i + 1) / 3) || 1 }}轮</span>
            </div>
          </div>

          <!-- Empty state -->
          <div v-if="!merchant?.goods?.length" class="m-empty-card">
            本轮暂无商品，稍后再来看看。
          </div>
        </div>

        <!-- Refresh button -->
        <div class="m-ft">
          <button class="m-refresh" @click="fetchMerchant(true)">🔄 刷新数据</button>
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.m-page {
  position: relative;
  min-height: 100vh;
  width: 100%;
  max-width: 860px;
  margin: 0 auto;
  overflow: hidden;
  background: #ece3d3;
  font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
  color: #332719;
}

.m-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, #f5efe6 0%, #ece3d3 100%);
  opacity: 0.5;
}

.m-content {
  position: relative;
  z-index: 1;
  padding: 80px 18px 100px;
}

/* Header */
.m-header {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  padding: 22px 24px;
  border: 1px solid rgba(118, 97, 74, 0.22);
  border-radius: 24px;
  background: linear-gradient(135deg, rgba(255,255,255,0.86), rgba(245,236,221,0.9));
  box-shadow: 0 14px 36px rgba(58, 39, 21, 0.08);
}

.m-header-left {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.m-title-row {
  display: flex;
  align-items: center;
  gap: 14px;
}

.m-icon {
  font-size: 40px;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.m-title {
  font-size: 38px;
  font-weight: 900;
  letter-spacing: 2px;
}

.m-subtitle {
  color: #6b5846;
  font-size: 16px;
}

.m-header-right {
  min-width: 280px;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: center;
  gap: 14px;
}

.m-chip {
  padding: 10px 18px;
  border-radius: 999px;
  background: rgba(255,255,255,0.72);
  border: 1px solid rgba(179, 123, 45, 0.2);
  color: #6b5846;
  font-size: 16px;
}
.m-chip strong {
  color: #a0631d;
  font-size: 26px;
  margin-left: 8px;
}

.m-round-row {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.m-round-pill, .m-countdown-pill {
  padding: 8px 16px;
  border-radius: 999px;
  font-size: 15px;
  font-weight: 700;
}
.m-round-pill {
  background: rgba(179, 123, 45, 0.12);
  color: #8b5e2b;
}
.m-countdown-pill {
  background: rgba(191, 95, 63, 0.08);
  color: #bf5f3f;
}

/* Grid */
.m-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
  margin-top: 18px;
}

.m-card {
  display: grid;
  grid-template-columns: 120px 1fr auto;
  gap: 16px;
  align-items: center;
  min-height: 140px;
  padding: 16px 20px;
  border: 1px solid rgba(118, 97, 74, 0.14);
  border-radius: 22px;
  background: linear-gradient(135deg, rgba(255,255,255,0.72), rgba(244,236,224,0.88));
  box-shadow: 0 10px 26px rgba(58, 39, 21, 0.06);
}

.m-card-img-wrap {
  width: 120px;
  height: 120px;
  border-radius: 16px;
  background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.94), rgba(239,228,210,0.92));
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.m-card-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.m-fallback {
  font-size: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.m-card-body {
  min-width: 0;
}

.m-card-name {
  font-size: 28px;
  font-weight: 800;
  line-height: 1.2;
  word-break: break-word;
}

.m-card-sub {
  margin-top: 8px;
  color: #6b5846;
  font-size: 15px;
}

.m-card-time {
  display: inline-flex;
  margin-top: 12px;
  padding: 6px 12px;
  border-radius: 999px;
  background: rgba(255, 214, 153, 0.4);
  color: #9a5f19;
  font-size: 14px;
  font-weight: 700;
}

.m-card-side {
  align-self: stretch;
  display: flex;
  align-items: center;
}

.m-card-slot {
  padding: 8px 12px;
  border-radius: 14px;
  background: rgba(255,255,255,0.72);
  border: 1px solid rgba(179, 123, 45, 0.18);
  color: #8b5e2b;
  font-size: 15px;
  font-weight: 700;
}

.m-empty-card {
  grid-column: 1 / -1;
  text-align: center;
  padding: 30px 18px;
  border-radius: 22px;
  border: 1px dashed rgba(120, 102, 81, 0.35);
  color: #5c4a37;
  font-size: 20px;
  background: rgba(255,255,255,0.52);
}

/* Loading */
.m-loading {
  text-align: center;
  padding: 60px 0;
  color: #999;
}
.m-spinner {
  width: 32px; height: 32px;
  border: 3px solid rgba(118, 97, 74, 0.15);
  border-top-color: #a0631d;
  border-radius: 50%;
  animation: spin .8s linear infinite;
  margin: 0 auto 12px;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Empty / Error */
.m-empty {
  text-align: center;
  padding: 60px 0;
  color: #999;
}
.m-retry, .m-refresh {
  margin-top: 16px;
  padding: 10px 24px;
  border-radius: 999px;
  border: 1px solid rgba(179, 123, 45, 0.25);
  background: rgba(255,255,255,0.72);
  color: #8b5e2b;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
}
.m-retry:active, .m-refresh:active {
  transform: scale(.96);
}
.m-ft {
  text-align: center;
  margin-top: 24px;
}

/* Responsive */
@media (max-width: 760px) {
  .m-content { padding: 70px 12px 90px; }
  .m-header {
    flex-direction: column;
    gap: 10px;
    padding: 14px 16px;
  }
  .m-header-right {
    min-width: 0;
    align-items: flex-start;
  }
  .m-round-row { justify-content: flex-start; }
  .m-icon { font-size: 32px; width: 48px; height: 48px; }
  .m-title { font-size: 28px; }
  .m-card {
    grid-template-columns: 80px 1fr;
    min-height: 0;
    padding: 12px 14px;
  }
  .m-card-img-wrap { width: 80px; height: 80px; }
  .m-card-name { font-size: 22px; }
  .m-card-side { grid-column: 1 / -1; justify-content: flex-start; padding-left: 96px; }
}
</style>
