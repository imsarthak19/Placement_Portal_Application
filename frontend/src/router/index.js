import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/Home.vue'

import SignupView from '@/views/SignupView.vue'
import CompanySignupView from '@/views/CompanySignupView.vue'
import LoginView from '@/views/LoginView.vue'

import AdminDashView from '@/views/admin/AdminDashView.vue'
import CompaniesView from '@/views/admin/CompaniesView.vue'
import CompanyDetailView from '@/views/admin/CompanyDetailView.vue'
import StudentsView from '@/views/admin/StudentsView.vue'
import StudentDetailView from '@/views/admin/StudentDetailView.vue'
import DrivesView from '@/views/admin/DrivesView.vue'
import DriveDetailView from '@/views/admin/DriveDetailView.vue'
import ApplicationsView from '@/views/admin/ApplicationsView.vue'
import ReportsView from '@/views/admin/ReportsView.vue'


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
    path: '/admin/companies',
    name: 'Companies',
    component: CompaniesView
  },

  {
    path: '/admin/company/:id',
    name: 'CompanyDetails',
    component: CompanyDetailView
  },

  {
    path: '/admin/students',
    name: 'Students',
    component: StudentsView
  },

  {
    path: '/admin/student/:id',
    name: 'StudentDetails',
    component: StudentDetailView
  },

  {
    path: '/admin/drive/:id',
    name: 'DriveDetails',
    component: DriveDetailView
  },

  {
    path: '/admin/drives',
    name: 'AllDrives',
    component: DrivesView
  },

  {
    path: '/admin/applications',
    name: 'AllApplications',
    component: ApplicationsView
  },

  {
    path: '/admin/reports',
    name: 'Reports',
    component: ReportsView
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

router.beforeEach((to, from, next) => {
  const user = JSON.parse(localStorage.getItem('user'))

  const publicPages = ['/', '/login', '/signup', '/company-signup']
  const authRequired = !publicPages.includes(to.path)

  if (authRequired && !user) {
    return next('/login')
  }

  // Role-based protection
  if (to.path.startsWith('/company-dash') && user?.type !== 'recruiter') {
    return next('/login')
  }

  if (to.path.startsWith('/admin-dash') && user?.type !== 'admin') {
    return next('/login')
  }

  if (to.path.startsWith('/student-dash') && user?.type !== 'student') {
    return next('/login')
  }

  next()
})

export default router