<script setup>
import { ref, onMounted } from 'vue'
import '../styles/dark-theme.css'
import { useApi } from '../composables/useApi'

const level = ref(16)
const targetBall = ref('')
const result = ref(null)
const ballOptions = ref([])

const { fetchJson: fetchBalls } = useApi()
const { loading, error, fetchJson } = useApi()

const fetchBallOptions = async () => {
  const data = await fetchBalls('/api/garden/balls')
  if (data && data.success) {
    ballOptions.value = data.balls
  }
}

const queryGarden = async () => {
  let url = `/api/garden/query?level=${level.value}`
  if (targetBall.value) {
    url += `&target_ball=${encodeURIComponent(targetBall.value)}`
  }
  const data = await fetchJson(url)
  if (data) {
    if (data.success) {
      result.value = data
    } else {
      error.value = data.message || '查询失败'
    }
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
  <div class="garden dark-page">
    <div class="garden__box" style="position: relative; z-index: 1;">
      <div class="garden__hd">
        <h1><img :src="'/img/peach-icon.png'" class="garden__title-icon" alt="" /> 家园炼金方案查询</h1>
        <p class="garden__sub">根据家园等级推荐最优经验效率的炼金配方，支持按目标球查询</p>
      </div>

    <div class="garden__card dark-card">
      <div class="form-group">
        <label>🏠 家园等级 (1-25)</label>
        <input v-model.number="level" type="number" min="1" max="25" class="form-input dark-input" placeholder="输入家园等级">
      </div>

      <div class="form-group">
        <label>🎯 目标球 (可选)</label>
        <select v-model="targetBall" class="form-select dark-input">
          <option value="">全部（按经验效率排序）</option>
          <option v-for="ball in ballOptions" :key="ball.name" :value="ball.name">{{ ball.name }}</option>
        </select>
      </div>

      <button @click="queryGarden" class="query-btn dark-btn dark-btn--accent" :disabled="loading">
        {{ loading ? '查询中...' : '🔍 查询推荐方案' }}
      </button>
      <button @click="resetAll" class="reset-btn dark-btn" v-if="result">🔄 重置</button>
    </div>

    <div v-if="error" class="dt-error-msg">{{ error }}</div>

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
      <div class="garden__card garden__result dark-card">
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
      <div class="garden__card garden__result dark-card">
        <h2>🎾 当前等级可炼制的球 (共{{ result.available_balls.length }}种)</h2>
        <div class="balls-grid">
          <div v-for="ball in result.available_balls" :key="ball.name" class="ball-card" @click="selectBall(ball.name)">
            <img :src="ball.icon_url" :alt="ball.name" class="ball-icon">
            <p class="ball-name">{{ ball.name }}</p>
          </div>
        </div>
      </div>

      <!-- 目标球配方列表 -->
      <div v-if="targetBall && result.ball_cards && result.ball_cards.length > 0" class="garden__card garden__result dark-card">
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
/* ===== 深色主题 - 家园炼金页 ===== */
.garden {
  padding: 16px 16px 80px;
}
.garden__box { max-width: 420px; margin: 0 auto; position: relative; z-index: 1; }

/* 标题 */
.garden__hd { text-align: center; padding: 24px 0 20px; }
.garden__hd h1 { font-size: 22px; color: #fff; font-weight: 700; margin: 0 0 6px; display: flex; align-items: center; justify-content: center; gap: 8px; }
.garden__title-icon { width: 28px; height: 28px; object-fit: contain; }
.garden__sub { font-size: 13px; color: rgba(255, 255, 255, 0.6); margin: 0; }

/* 卡片 */
.garden__card {
  padding: 16px;
  margin-bottom: 12px;
  display: flex;
  gap: 12px;
  align-items: flex-end;
  flex-wrap: wrap;
  transition: box-shadow .2s;
}
.garden__card:hover { box-shadow: 0 8px 24px rgba(139, 61, 255, 0.15); }

.form-group {
  flex: 1;
  min-width: 180px;
}
.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.85);
  font-size: 14px;
}
.form-input, .form-select {
  width: 100%;
  padding: 10px 14px;
  border: 1.5px solid rgba(255, 255, 255, 0.15);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
  font-size: 15px;
  transition: .2s;
  box-sizing: border-box;
}
.form-input::placeholder { color: rgba(255, 255, 255, 0.35); }
.form-input:focus, .form-select:focus {
  outline: none;
  border-color: #8b3dff;
  background: rgba(255, 255, 255, 0.12);
}
.form-select option { background: #1a1a2e; color: #fff; }

.query-btn {
  padding: 10px 24px;
  background: rgba(139, 61, 255, 0.6);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(8px);
  border-radius: 12px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: .2s;
  height: fit-content;
}
.query-btn:hover {
  transform: translateY(-2px);
  background: rgba(139, 61, 255, 0.8);
}
.query-btn:active { transform: scale(.97); }
.query-btn:disabled { opacity: .6; cursor: not-allowed; transform: none; }

.reset-btn {
  padding: 10px 16px;
  background: rgba(255, 255, 255, 0.06);
  color: rgba(255, 255, 255, 0.7);
  border: 1.5px solid rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  font-size: 14px;
  cursor: pointer;
  transition: .2s;
  height: fit-content;
}
.reset-btn:hover { background: rgba(255, 255, 255, 0.12); }

/* 摘要统计 */
.summary-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  margin-bottom: 12px;
}
.summary-item {
  background: rgba(20, 20, 40, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(8px);
  border-radius: 12px;
  padding: 12px 8px;
  text-align: center;
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
  color: rgba(255, 255, 255, 0.5);
  margin-top: 4px;
}

/* 结果卡片 */
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
  color: #fff;
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
  background: rgba(139, 61, 255, 0.1);
  border: 1px solid rgba(139, 61, 255, 0.2);
  border-radius: 12px;
  padding: 14px;
  text-align: center;
  min-width: 100px;
  position: relative;
}
.food-card {
  background: rgba(46, 204, 113, 0.1);
  border: 1px solid rgba(46, 204, 113, 0.25);
}
.item-icon {
  width: 56px;
  height: 56px;
  object-fit: contain;
  margin-bottom: 6px;
}
.item-name {
  font-weight: 600;
  color: #fff;
  margin-bottom: 2px;
  font-size: 14px;
}
.item-label {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
}
.formula-tag {
  position: absolute;
  top: 6px;
  right: 6px;
  background: rgba(139, 61, 255, 0.7);
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
  background: rgba(139, 61, 255, 0.12);
  color: #8b3dff;
  padding: 6px 14px;
  border-radius: 20px;
  font-weight: 500;
  font-size: 13px;
  border: 1px solid rgba(139, 61, 255, 0.2);
}

/* 球列表 - 横向胶囊标签式 */
.balls-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.ball-card {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 50px;
  padding: 8px 16px 8px 8px;
  cursor: pointer;
  transition: .2s;
}
.ball-card:hover {
  border-color: rgba(139, 61, 255, 0.5);
  background: rgba(139, 61, 255, 0.15);
  box-shadow: 0 2px 8px rgba(139, 61, 255, 0.15);
}
.ball-card:active { transform: scale(.97); }
.ball-icon {
  width: 28px;
  height: 28px;
  object-fit: contain;
  border-radius: 50%;
  flex-shrink: 0;
}
.ball-name {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.85);
  font-weight: 500;
  white-space: nowrap;
}

/* 球配方列表 */
.ball-recipe-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.ball-recipe-card {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 12px;
  padding: 14px;
  display: flex;
  align-items: center;
  gap: 14px;
  transition: .2s;
}
.ball-recipe-card:hover { background: rgba(255, 255, 255, 0.08); }
.recipe-rank {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: rgba(139, 61, 255, 0.6);
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
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 4px;
  font-weight: 500;
}
.recipe-items .food-name { color: #8b3dff; }
.recipe-meta {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
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
.garden__ft { text-align: center; padding: 24px 0 16px; font-size: 11px; color: rgba(255, 255, 255, 0.3); }
</style>
