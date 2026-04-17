<script setup>
const features = [
  {
    icon: '🔍',
    title: '孵蛋查询',
    desc: '输入身高体重，查询可能孵化的精灵',
    href: '/egg-query',
    done: true,
  },
  {
    icon: '📖',
    title: '精灵图鉴',
    desc: '468只精灵数据，属性/蛋组筛选',
    href: '/compendium',
    done: true,
  },
]

const upcoming = [
  { icon: '🎯', title: '蛋组配对查询', desc: '查看哪些精灵可以互相繁殖' },
  { icon: '🌈', title: '异色孵化路径', desc: '异色精灵的孵化概率与流程' },
  { icon: '📊', title: '六维雷达图', desc: '精灵属性六维可视化对比' },
  { icon: '🔗', title: '孵蛋↔图鉴联动', desc: '从图鉴详情直接跳转孵蛋查询' },
]
</script>

<template>
  <div class="home">
    <div class="home__box">
      <!-- 标题 -->
      <div class="home__hd">
        <div class="home__logo">🥚</div>
        <h1>洛克王国孵蛋查询</h1>
        <p class="home__sub">世界 · 1623条数据 · R值排序</p>
      </div>

      <!-- 功能入口 -->
      <div class="home__section">
        <div class="home__section-title">功能</div>
        <div class="home__cards">
          <a
            v-for="f in features"
            :key="f.title"
            :href="f.href"
            class="home__card home__card--active"
          >
            <div class="home__card-icon">{{ f.icon }}</div>
            <div class="home__card-body">
              <div class="home__card-title">{{ f.title }}</div>
              <div class="home__card-desc">{{ f.desc }}</div>
            </div>
            <div class="home__card-arrow">→</div>
          </a>
        </div>
      </div>

      <!-- 即将上线 -->
      <div class="home__section">
        <div class="home__section-title">即将上线</div>
        <div class="home__cards">
          <div
            v-for="f in upcoming"
            :key="f.title"
            class="home__card home__card--disabled"
          >
            <div class="home__card-icon">{{ f.icon }}</div>
            <div class="home__card-body">
              <div class="home__card-title">{{ f.title }}</div>
              <div class="home__card-desc">{{ f.desc }}</div>
            </div>
            <div class="home__card-badge">🚧</div>
          </div>
        </div>
      </div>

      <!-- 底部 -->
      <div class="home__ft">
        数据来源：github.com/jiluoQAQ/RocomUID
      </div>
    </div>
  </div>
</template>

<style scoped>
.home {
  min-height: 100vh;
  background: linear-gradient(180deg, #e8f0fe 0%, #f5f0ff 50%, #fff 100%);
  padding: 16px;
  padding-bottom: env(safe-area-inset-bottom, 16px);
}
.home__box {
  max-width: 420px;
  margin: 0 auto;
}
.home__hd {
  text-align: center;
  padding: 24px 0 20px;
}
.home__logo {
  font-size: 48px;
  margin-bottom: 8px;
}
.home__hd h1 {
  font-size: 22px;
  color: #1a1a2e;
  font-weight: 700;
}
.home__sub {
  font-size: 13px;
  color: #888;
  margin-top: 4px;
}
.home__section {
  margin-bottom: 20px;
}
.home__section-title {
  font-size: 12px;
  color: #aaa;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 10px;
  padding-left: 4px;
}
.home__cards {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.home__card {
  background: #fff;
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,.06);
  display: flex;
  align-items: center;
  gap: 14px;
  transition: all .2s;
  text-decoration: none;
  color: inherit;
}
.home__card--active {
  cursor: pointer;
}
.home__card--active:active {
  transform: scale(.97);
}
.home__card--active:hover {
  box-shadow: 0 4px 20px rgba(102,126,234,.15);
}
.home__card--disabled {
  opacity: .45;
  cursor: not-allowed;
}
.home__card--disabled .home__card-icon {
  filter: grayscale(1);
}
.home__card-icon {
  font-size: 32px;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0f2ff;
  border-radius: 14px;
  flex-shrink: 0;
}
.home__card-body {
  flex: 1;
  min-width: 0;
}
.home__card-title {
  font-size: 16px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 2px;
}
.home__card-desc {
  font-size: 12px;
  color: #999;
  line-height: 1.4;
}
.home__card-arrow {
  font-size: 18px;
  color: #667eea;
  font-weight: 600;
  flex-shrink: 0;
}
.home__card-badge {
  font-size: 14px;
  flex-shrink: 0;
}
.home__ft {
  text-align: center;
  padding: 24px 0 16px;
  font-size: 11px;
  color: #ccc;
}
.home__ft a {
  color: #999;
}
</style>
