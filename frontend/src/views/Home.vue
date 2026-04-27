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
    icon: '🏡',
    title: '家园炼金',
    desc: '种花、做饭、炼球最优方案推荐',
    href: '/garden',
    done: true,
  },
  {
    icon: '📖',
    title: '精灵图鉴',
    desc: '468只精灵数据，属性/蛋组筛选',
    href: '/compendium',
    done: true,
  },
  {
    icon: '🎯',
    title: '蛋组配对',
    desc: '查看各蛋组可繁殖精灵，同组可互相配对',
    href: '/egg-group',
    done: true,
  },
]

const upcoming = [
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
      <div class="home__section" v-if="upcoming.length">
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
  background: linear-gradient(180deg, #f0ecff 0%, #ffffff 100%);
  padding: 16px 16px 80px;
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
  border-radius: 18px;
  padding: 16px;
  box-shadow: 0 4px 16px rgba(15,16,21,0.08);
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
  box-shadow: 0 8px 24px rgba(139,61,255,0.12);
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
  background: #f0ecff;
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
  color: #8b3dff;
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
