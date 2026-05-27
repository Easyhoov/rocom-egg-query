<script setup>
import { ref, onMounted } from 'vue'

const level = ref(16)
const targetBall = ref('')
const loading = ref(false)
const result = ref(null)
const ballOptions = ref([])
const error = ref('')

const fetchBallOptions = async () => {
  try {
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), 15000)
    const res = await fetch('/api/garden/balls', { signal: controller.signal })
    clearTimeout(timeout)
    const data = await res.json()
    if (data.success) {
      ballOptions.value = data.balls
    }
  } catch (e) {
    console.error('获取球列表失败', e)
  }
}

const queryGarden = async () => {
  loading.value = true
  error.value = ''
  try {
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), 15000)
    let url = `/api/garden/query?level=${level.value}`
    if (targetBall.value) {
      url += `&target_ball=${encodeURIComponent(targetBall.value)}`
    }
    const res = await fetch(url, { signal: controller.signal })
    clearTimeout(timeout)
    if (!res.ok) {
      if (res.status === 404) throw new Error('接口不存在，请检查服务是否正常运行')
      if (res.status >= 500) throw new Error(`服务器错误(${res.status})，请稍后重试`)
      throw new Error(`请求失败(${res.status})`)
    }
    const data = await res.json()
    if (data.success) {
      result.value = data
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

const selectBall = (ballName) => {
  targetBall.value = ballName
  queryGarden()
}

onMounted(() => {
  fetchBallOptions()
})

const resetAll = () => {
  result.value = null
  targetBall.value = ''
  error.value = ''
}
</script>

<template>
  <div class="garden">
    <div class="garden__box">
      <div class="garden__hd">
        <h1>🌿 家园炼金方案查询</h1>
        <p class="garden__sub">根据家园等级推荐最优经验效率的炼金配方，支持按目标球查询</p>
      </div>

    <div class="garden__card">
      <div class="form-group">
        <label>🏠 家园等级 (1-25)</label>
        <input v-model.number="level" type="number" min="1" max="25" class="form-input" placeholder="输入家园等级">
      </div>

      <div class="form-group">
        <label>🎯 目标球 (可选)</label>
        <select v-model="targetBall" class="form-select">
          <option value="">全部（按经验效率排序）</option>
          <option v-for="ball in ballOptions" :key="ball.name" :value="ball.name">{{ ball.name }}</option>
        </select>
      </div>

      <button @click="queryGarden" class="query-btn" :disabled="loading">
        {{ loading ? '查询中...' : '🔍 查询推荐方案' }}
      </button>
      <button @click="resetAll" class="reset-btn" v-if="result">🔄 重置</button>
    </div>

    <div v-if="error" class="error-msg">{{ error }}</div>

    <!-- 摘要统计 -->
    <div v-if="result && result.summary" class="summary-row">
      <div class="summary-item">
        <div class="summary-val">{{ result.summary.available_count }}</div>
        <div class="summary-label">可种配方</div>
      </div>
      <div class="summary-item">
        <div class="summary-val">{{ result.summary.best_food }}</div>
        <div class="summary-label">推荐食物</div>
      </div>
      <div class="summary-item">
        <div class="summary-val">{{ result.summary.available_ball_count }}</div>
        <div class="summary-label">可直炼球</div>
      </div>
      <div class="summary-item">
        <div class="summary-val">{{ result.summary.best_exp_per_hour }}/h</div>
        <div class="summary-label">最优经验</div>
      </div>
    </div>

    <div v-if="result" class="result-section">
      <!-- 最优推荐 -->
      <div class="garden__card garden__result">
        <h2>⭐ 最优推荐方案 (Lv.{{ result.level }})</h2>
        <div class="recipe-grid">
          <div class="item-card">
            <img :src="result.best_recommendation.seed.icon_url" :alt="result.best_recommendation.seed.name" class="item-icon">
            <p class="item-name">{{ result.best_recommendation.seed.name }}</p>
            <span class="item-label">种子</span>
          </div>
          <div class="plus">+</div>
          <div class="item-card">
            <img :src="result.best_recommendation.material.icon_url" :alt="result.best_recommendation.material.name" class="item-icon">
            <p class="item-name">{{ result.best_recommendation.material.name }}</p>
            <span class="item-label">材料</span>
          </div>
          <div class="equal">=</div>
          <div class="item-card food-card">
            <img :src="result.best_recommendation.food.icon_url" :alt="result.best_recommendation.food.name" class="item-icon">
            <p class="item-name">{{ result.best_recommendation.food.name }}</p>
            <span class="item-label">{{ result.best_recommendation.food.duration_label }} · {{ result.best_recommendation.food.exp }} 经验</span>
            <span class="formula-tag">{{ result.best_recommendation.food.formula }}</span>
          </div>
        </div>
        <div class="exp-info">
          <span class="exp-badge">⏱️ 每小时经验: {{ result.best_recommendation.exp_per_hour }}</span>
          <span class="level-badge">🔓 解锁等级: Lv.{{ result.best_recommendation.unlock_level }}</span>
        </div>
      </div>

      <!-- 可炼制的球 -->
      <div class="garden__card garden__result">
        <h2>🎾 当前等级可炼制的球 (共{{ result.available_balls.length }}种)</h2>
        <div class="balls-grid">
          <div v-for="ball in result.available_balls" :key="ball.name" class="ball-card" @click="selectBall(ball.name)">
            <img :src="ball.icon_url" :alt="ball.name" class="ball-icon">
            <p class="ball-name">{{ ball.name }}</p>
          </div>
        </div>
      </div>

      <!-- 目标球配方列表 -->
      <div v-if="targetBall && result.ball_cards && result.ball_cards.length > 0" class="garden__card garden__result">
        <h2>📋 可炼制「{{ targetBall }}」的所有配方</h2>
        <div class="ball-recipe-list">
          <div v-for="(card, index) in result.ball_cards" :key="index" class="ball-recipe-card">
            <div class="recipe-rank">#{{ index + 1 }}</div>
            <div class="recipe-content">
              <div class="recipe-items">
                <span>{{ card.seed.name }}</span> + <span>{{ card.material.name }}</span> = <span class="food-name">{{ card.food.name }}</span>
              </div>
              <div class="recipe-meta">
                <span>⏱️ {{ card.food.duration_label }} · {{ card.exp_per_hour }} 经验/小时</span>
                <span>🧪 {{ card.ball.formula_label }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    </div>
    <div class="garden__ft">洛克王国：世界 · 家园炼金</div>
  </div>
</template>

<style scoped>
.garden {
  min-height: 100vh;
  background: linear-gradient(180deg, #f0ecff 0%, #ffffff 100%);
  padding: 16px 16px 80px;
}
.garden__box { max-width: 420px; margin: 0 auto; }

/* Header */
.garden__hd { text-align: center; padding: 24px 0 20px; }
.garden__hd h1 { font-size: 22px; color: #1a1a2e; font-weight: 700; margin: 0 0 6px; }
.garden__sub { font-size: 13px; color: #888; margin: 0; }

/* Card */
.garden__card {
  background: #fff;
  border-radius: 18px;
  padding: 16px;
  box-shadow: 0 4px 16px rgba(15,16,21,0.08);
  margin-bottom: 12px;
  display: flex;
  gap: 12px;
  align-items: flex-end;
  flex-wrap: wrap;
  transition: box-shadow .2s;
}
.garden__card:hover { box-shadow: 0 8px 24px rgba(139,61,255,0.12); }

/* Error */
.error-msg {
  background: #fff0f0;
  color: #e74c3c;
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
  text-align: center;
  margin-bottom: 16px;
}

.form-group {
  flex: 1;
  min-width: 180px;
}
.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #1a1a2e;
  font-size: 14px;
}
.form-input, .form-select {
  width: 100%;
  padding: 10px 14px;
  border: 1.5px solid #e8e8e8;
  border-radius: 10px;
  background: #fafafa;
  font-size: 15px;
  transition: .2s;
  box-sizing: border-box;
}
.form-input:focus, .form-select:focus {
  outline: none;
  border-color: #8b3dff;
  background: #fff;
}

.query-btn {
  padding: 10px 24px;
  background: #8b3dff;
  color: #fff;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: .2s;
  height: fit-content;
}
.query-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102,126,234,.4);
}
.query-btn:active { transform: scale(.97); }
.query-btn:disabled { opacity: .6; cursor: not-allowed; transform: none; }

.reset-btn {
  padding: 10px 16px;
  background: #f5f5f5;
  color: #888;
  border: 1.5px solid #e8e8e8;
  border-radius: 12px;
  font-size: 14px;
  cursor: pointer;
  transition: .2s;
  height: fit-content;
}
.reset-btn:hover { background: #eee; }

/* Summary row */
.summary-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  margin-bottom: 12px;
}
.summary-item {
  background: #fff;
  border-radius: 12px;
  padding: 12px 8px;
  text-align: center;
  box-shadow: 0 8px 24px rgba(15,16,21,0.08);
}
.summary-val {
  font-size: 16px;
  font-weight: 700;
  color: #8b3dff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.summary-label {
  font-size: 11px;
  color: #aaa;
  margin-top: 4px;
}

/* Result cards */
.result-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.garden__result {
  flex-direction: column;
  align-items: stretch;
  padding: 20px 16px;
}
.garden__result h2 {
  font-size: 16px;
  color: #1a1a2e;
  margin: 0 0 16px;
  font-weight: 700;
}

.recipe-grid {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}
.item-card {
  background: #f5f2ff;
  border-radius: 12px;
  padding: 14px;
  text-align: center;
  min-width: 100px;
  position: relative;
}
.food-card {
  background: #f0fff4;
  border: 1px solid #9ae6b4;
}
.item-icon {
  width: 56px;
  height: 56px;
  object-fit: contain;
  margin-bottom: 6px;
}
.item-name {
  font-weight: 600;
  color: #1a1a2e;
  margin-bottom: 2px;
  font-size: 14px;
}
.item-label {
  font-size: 12px;
  color: #888;
}
.formula-tag {
  position: absolute;
  top: 6px;
  right: 6px;
  background: #8b3dff;
  color: #fff;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 11px;
}
.plus, .equal {
  font-size: 20px;
  font-weight: bold;
  color: #8b3dff;
}

.exp-info {
  display: flex;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
}
.exp-badge, .level-badge {
  background: #f0ecff;
  color: #8b3dff;
  padding: 6px 14px;
  border-radius: 20px;
  font-weight: 500;
  font-size: 13px;
}

/* Balls */
.balls-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(90px, 1fr));
  gap: 12px;
}
.ball-card {
  background: #f5f2ff;
  border-radius: 12px;
  padding: 14px;
  text-align: center;
  cursor: pointer;
  transition: .2s;
  border: 2px solid transparent;
}
.ball-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102,126,234,.2);
  border-color: #8b3dff;
}
.ball-card:active { transform: scale(.97); }
.ball-icon {
  width: 42px;
  height: 42px;
  object-fit: contain;
  margin-bottom: 6px;
}
.ball-name {
  font-size: 13px;
  color: #1a1a2e;
  font-weight: 500;
}

/* Ball recipe list */
.ball-recipe-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.ball-recipe-card {
  background: #f5f2ff;
  border-radius: 12px;
  padding: 14px;
  display: flex;
  align-items: center;
  gap: 14px;
  transition: .2s;
}
.ball-recipe-card:hover { background: #f0ecff; }
.recipe-rank {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #8b3dff;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 13px;
  flex-shrink: 0;
}
.recipe-content { flex: 1; }
.recipe-items {
  font-size: 14px;
  color: #1a1a2e;
  margin-bottom: 4px;
  font-weight: 500;
}
.recipe-items .food-name { color: #8b3dff; }
.recipe-meta {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: #888;
}

@media (max-width: 768px) {
  .garden__card {
    flex-direction: column;
    align-items: stretch;
  }
  .query-btn { width: 100%; }
  .recipe-grid { flex-direction: column; }
  .plus, .equal { transform: rotate(90deg); }
}
.garden__ft { text-align: center; padding: 24px 0 16px; font-size: 11px; color: #ccc; }
</style>
