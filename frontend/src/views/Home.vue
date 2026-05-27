<script setup>
const imgBase = '/img/'

const features = [
  {
    icon: '/img/favicon.png',
    title: '孵蛋查询',
    desc: '输入身高体重，查询可能孵化的精灵',
    href: '/egg-query',
  },
  {
    icon: '/img/icon-decorative-book.6KbZJc7F.png',
    title: '精灵图鉴',
    desc: '468只精灵数据，属性/蛋组筛选',
    href: '/compendium',
  },
  {
    icon: '🎯',
    title: '蛋组配对',
    desc: '查看各蛋组可繁殖精灵，同组可互相配对',
    href: '/egg-group',
  },
  {
    icon: '/img/peach-icon.png',
    title: '家园炼金',
    desc: '种花、做饭、炼球最优方案推荐',
    href: '/garden',
  },
  {
    icon: '/img/yuanxingshangren.png',
    title: '远行商人',
    desc: '查看远行商人当前轮次商品',
    href: '/merchant',
  },
]
</script>

<template>
  <div class="page">
    <div class="bg-layer"></div>
    <div class="content">
      <!-- 标题区 -->
      <div class="header">
        <div class="header-bg"></div>
        <div class="header-inner">
          <img class="title-logo" :src="imgBase + '洛克王国大标题-白.png'" alt="洛克王国" />
          <div class="title-sub">孵蛋查询工具</div>
        </div>
      </div>

      <!-- 功能入口 -->
      <div class="section">
        <div class="section-label">
          <span class="label-bar"></span>
          功能
        </div>
        <div class="card-list">
          <a
            v-for="f in features"
            :key="f.title"
            :href="f.href"
            class="card"
          >
            <img v-if="f.icon.startsWith('/')" class="card-icon-img" :src="f.icon" :alt="f.title" />
            <div v-else class="card-icon">{{ f.icon }}</div>
            <div class="card-body">
              <div class="card-title">{{ f.title }}</div>
              <div class="card-desc">{{ f.desc }}</div>
            </div>
            <div class="card-arrow">›</div>
          </a>
        </div>
      </div>

      <!-- 装饰图（已移至背景） -->
      <div class="xiaoluoke" style="display:none">
        <img :src="imgBase + 'pokemon-camp.jpg'" alt="宝可梦露营" />
      </div>

      <!-- 底部 -->
      <div class="footer">
        <div class="footer-links">
          <a href="https://github.com/Easyhoov/rocom-egg-query" target="_blank">GitHub</a>
          <span class="dot">·</span>
          <span>数据 RocomUID</span>
          <span class="dot">·</span>
          <span>AstrBot</span>
        </div>
        <div class="footer-sub">WeGame · 洛克王国世界</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page {
  min-height: 100vh;
  background: #1a1a2e;
  position: relative;
  overflow: hidden;
}

.bg-layer {
  position: absolute;
  inset: 0;
  background: url('/img/pokemon-camp.jpg') center center / cover no-repeat;
  opacity: 0.4;
  pointer-events: none;
}

.content {
  position: relative;
  z-index: 1;
  max-width: 420px;
  margin: 0 auto;
  padding: 24px 16px 60px;
}

/* Header */
.header {
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  margin-bottom: 24px;
}

.header-bg {
  position: absolute;
  inset: 0;
  border-radius: 20px;
}

.header-bg::after {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(20, 20, 40, 0.3);
  border-radius: 20px;
}

.header-inner {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 28px 20px 24px;
}

.title-logo {
  height: 48px;
  width: auto;
  object-fit: contain;
  filter: brightness(1.2);
}

.title-sub {
  font-size: 15px;
  color: rgba(255, 255, 255, 0.9);
  margin-top: 8px;
  letter-spacing: 2px;
}

/* Section */
.section {
  margin-bottom: 20px;
}

.section-label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 14px;
  padding-left: 4px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.label-bar {
  display: block;
  width: 4px;
  height: 18px;
  background: #c97926;
  border-radius: 2px;
}

/* Cards */
.card-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px;
  background: rgba(20, 20, 40, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 18px;
  text-decoration: none;
  color: #fff;
  transition: all 0.15s;
  cursor: pointer;
  backdrop-filter: blur(8px);
}

.card:active {
  transform: scale(0.97);
  background: rgba(20, 20, 40, 0.8);
}

.card-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  background: linear-gradient(135deg, rgba(255,240,210,0.6), rgba(245,225,185,0.4));
  border-radius: 14px;
  flex-shrink: 0;
}

.card-icon-img {
  width: 48px;
  height: 48px;
  object-fit: contain;
  border-radius: 14px;
  flex-shrink: 0;
  background: linear-gradient(135deg, rgba(255,240,210,0.6), rgba(245,225,185,0.4));
  padding: 4px;
}

.card-body {
  flex: 1;
  min-width: 0;
}

.card-title {
  font-size: 17px;
  font-weight: 800;
  color: #fff;
  margin-bottom: 3px;
}

.card-desc {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.75);
  line-height: 1.4;
}

.card-arrow {
  font-size: 24px;
  color: rgba(255, 255, 255, 0.6);
  font-weight: 300;
  flex-shrink: 0;
  opacity: 0.8;
}

/* 小洛克装饰 */
/* 装饰图 */
.xiaoluoke {
  text-align: center;
  margin: 20px 0;
  opacity: 0.6;
  pointer-events: none;
  border-radius: 12px;
  overflow: hidden;
}

.xiaoluoke img {
  width: 100%;
  max-width: 400px;
  height: auto;
  border-radius: 12px;
}

/* Footer */
.footer {
  text-align: center;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-links {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
}

.footer-links a {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
}

.footer-links a:hover {
  color: rgba(255, 255, 255, 0.9);
}

.dot {
  margin: 0 6px;
  color: rgba(255, 255, 255, 0.4);
}

.footer-sub {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.5);
  margin-top: 6px;
}
</style>
