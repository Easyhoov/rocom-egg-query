import { createRouter, createWebHistory } from 'vue-router'
import EggQuery from '../views/EggQuery.vue'

const routes = [
  {
    path: '/',
    name: 'EggQuery',
    component: EggQuery
  },
  // 二期预留
  // {
  //   path: '/egg-group',
  //   name: 'EggGroup',
  //   component: () => import('../views/EggGroup.vue')
  // },
  // {
  //   path: '/breeding',
  //   name: 'Breeding',
  //   component: () => import('../views/Breeding.vue')
  // },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
