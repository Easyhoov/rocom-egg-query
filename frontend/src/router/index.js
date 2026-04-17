import { createRouter, createWebHistory } from 'vue-router'
import EggQuery from '../views/EggQuery.vue'

const routes = [
  {
    path: '/',
    name: 'EggQuery',
    component: EggQuery
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
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
