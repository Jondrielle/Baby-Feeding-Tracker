import { createRouter, createWebHistory } from 'vue-router'

import BabyCard from '../views/BabyCard.vue'

const routes = [
  { path: '/', component: BabyCard },
]

export const router = createRouter({
  history: createWebHistory(),  // <-- This is the fix
  routes,
})
