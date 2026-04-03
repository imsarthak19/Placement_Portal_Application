// import { createRouter, createWebHistory } from 'vue-router'

// const router = createRouter({
//   history: createWebHistory(import.meta.env.BASE_URL),
//   routes: [],
// })

// export default router


import { createRouter, createWebHistory } from 'vue-router'
import SignupView from '../views/SignupView.vue'

const routes = [
  {
    path: '/signup',
    name: 'Signup',
    component: SignupView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router