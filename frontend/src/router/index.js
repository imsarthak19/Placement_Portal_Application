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
import DriveView from '@/views/admin/DrivesView.vue'
import DriveDetailView from '@/views/admin/DriveDetailView.vue'
import CompanyEditView from '@/views/admin/CompanyEditView.vue'
import DriveEditView from '@/views/admin/DriveEditView.vue'
import ApplicationsView from '@/views/admin/ApplicationsView.vue'
import ReportsView from '@/views/admin/ReportsView.vue'


import CompanyDashView from '@/views/company/CompanyDashView.vue'
import AllDrivesView from '@/views/company/AllDrivesView.vue'
import CompanyProfile from '@/views/company/CompanyProfileView.vue'
import CompanyApplicationsView from '@/views/company/CompanyApplicationsView.vue'
import CompanyShortlisted from '@/views/company/ShortlistedCandidatesView.vue'
import CompanyInterviews from '@/views/company/CompanyInterviewsView.vue'


import StudentDashView from '@/views/student/StudentDashView.vue'
import AvailableDrivesView from '@/views/student/AvailableDrivesView.vue'
import StudentProfileView from '@/views/student/StudentProfileView.vue'
import EditStudentProfileView from '@/views/student/EditStudentProfileView.vue'
import RecruiterDriveView from '@/views/student/RecruiterDriveView.vue'
import MyApplications from '@/views/student/MyApplications.vue'
import StudentInterviewsView from '@/views/student/StudentInterviewsView.vue'
import OfferView from '@/views/student/OfferView.vue'

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
    name: 'AdminCompanies',
    component: CompaniesView
  },

  {
    path: '/admin/company/:id',
    name: 'AdminCompanyDetail',
    component: CompanyDetailView
  },
  {
    path: '/admin/company/:id/edit',
    name: 'AdminCompanyEdit',
    component: CompanyEditView
  },

  {
    path: '/admin/students',
    name: 'AdminStudents',
    component: StudentsView
  },

  {
    path: '/admin/student/:id',
    name: 'AdminStudentDetail',
    component: StudentDetailView
  },

  {
    path: '/admin/drive/:id',
    name: 'AdminDriveDetail',
    component: DriveDetailView
  },
  {
    path: '/admin/drive/:id/edit',
    name: 'AdminDriveEdit',
    component: DriveEditView
  },
  {
    path: '/admin/drive/create',
    name: 'AdminDriveCreate',
    component: DriveEditView
  },

  {
    path: '/admin/drives',
    name: 'AdminDrives',
    component: DriveView
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
    path: '/company/profile',
    name: 'CompanyProfile',
    component: CompanyProfile
  },
  {
    path: '/company/profile/edit',
    name: 'CompanyProfileEdit',
    component: CompanyEditView
  },
  {
    path: '/company/all-drives',
    name: 'RecruiterAllDrives',
    component: AllDrivesView
  },
  {
    path: '/company/shortlisted',
    name: 'RecruiterShortlisted',
    component: CompanyShortlisted
  },
  {
    path: '/company/interviews',
    name: 'RecruiterInterviews',
    component: CompanyInterviews
  },
  {
    path: '/company/applications',
    name: 'RecruiterApplications',
    component: CompanyApplicationsView
  },
  {
    path: '/company/drive/:id',
    name: 'DriveDetailView',
    component: DriveDetailView
  },
  {
    path: '/company/student/:id',
    name: 'RecruiterStudentDetail',
    component: StudentDetailView
  },
  {
    path: '/company/drive/:id/edit',
    name: 'RecruiterDriveEdit',
    component: DriveEditView
  },
  {
    path: '/company/drive/create',
    name: 'RecruiterDriveCreate',
    component: DriveEditView
  },

  {
    path: '/student-dash',
    name: 'StudentDashboard',
    component: StudentDashView
  },
  {
    path: '/student/drives',
    name: 'StudentAvailableDrives',
    component: AvailableDrivesView
  },
  {
    path: '/student/drive/:id',
    name: 'RecruiterDriveView',
    component: RecruiterDriveView
  },
  {
    path: '/student/profile',
    name: 'StudentProfile',
    component: StudentProfileView
  },
  {
    path: '/student/profile/edit',
    name: 'StudentProfileEdit',
    component: EditStudentProfileView
  },
  {
    path: '/student/applications',
    name: 'StudentApplications',
    component: MyApplications
  },
  {
    path: '/student/interviews',
    name: 'StudentInterviews',
    component: StudentInterviewsView
  },
  {
    path: '/student/offer-letter/:id',
    name: 'StudentOfferLetter',
    component: OfferView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const user = JSON.parse(localStorage.getItem('user'))

  const publicPages = ['/', '/login', '/signup', '/company-signup']
  const authRequired = !publicPages.includes(to.path)

  if (authRequired && !user) {
    return '/login'
  }

  // Role-based protection
  if (to.path.startsWith('/admin') && user?.type !== 'admin') {
    return '/login'
  }

  if (to.path.startsWith('/company') && user?.type !== 'recruiter') {
    return '/login'
  }

  if (to.path.startsWith('/student') && user?.type !== 'student') {
    return '/login'
  }

  return true
})

export default router