import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/egg-query',
    name: 'EggQuery',
    component: () => import('../views/EggQuery.vue'),
  },
  {
    path: '/compendium',
    name: 'Compendium',
    component: () => import('../views/CompendiumPage.vue'),
  },
  {
    path: '/compendium/:id',
    name: 'SpiritDetail',
    component: () => import('../views/SpiritDetail.vue'),
  },
  {
    path: '/egg-group',
    name: 'EggGroup',
    component: () => import('../views/EggGroup.vue'),
  },
  {
    path: '/garden',
    name: 'Garden',
    component: () => import('../views/Garden.vue'),
  },
  {
    path: '/merchant',
    name: 'Merchant',
    component: () => import('../views/Merchant.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
