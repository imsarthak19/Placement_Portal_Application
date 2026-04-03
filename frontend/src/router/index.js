import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Home.vue'
import SignupView from '../views/SignupView.vue'
import CompanySignupView from '../views/CompanySignupView.vue'
import LoginView from '../views/LoginView.vue'
import AdminDashView from '@/views/AdminDashView.vue'
import CompanyDashView from '@/views/CompanyDashView.vue'
import StudentDashView from '@/views/StudentDashView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },

  {
    path: '/signup',
    name: 'Signup',
    component: SignupView
  },

  {
    path: '/company-signup',
    name: 'CompanySignup',
    component: CompanySignupView
  },

  {
    path: '/login',
    name: 'Login',
    component: LoginView
  },

  {
    path: '/admin-dash',
    name: 'AdminDashboard',
    component: AdminDashView
  },

  {
    path: '/company-dash',
    name: 'CompanyDashboard',
    component: CompanyDashView
  },

  {
    path: '/student-dash',
    name: 'StudentDashboard',
    component: StudentDashView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router