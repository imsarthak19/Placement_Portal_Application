<template>
  <nav class="nav nav-pills flex-column px-3 h-100">
    <!-- Main Section -->
    <div class="menu-section mb-5">
      <p class="section-label ms-3 small mb-3 text-uppercase fw-bold text-white opacity-75">Main</p>
      <div class="d-grid gap-1">
        <router-link 
          v-for="item in currentMenu" 
          :key="item.path" 
          :to="item.path" 
          class="nav-link dashboard-link d-flex align-items-center gap-3 py-2 px-3"
          active-class="active"
        >
          <i :class="[item.icon, 'menu-icon']"></i>
          <span class="menu-text">{{ item.label }}</span>
        </router-link>
      </div>
    </div>

    <!-- Bottom Section -->
    <div class="mt-auto py-4 border-top border-white border-opacity-10">
      <div class="d-grid gap-1">
        <router-link 
          to="/settings" 
          class="nav-link dashboard-link d-flex align-items-center gap-3 py-2 px-3"
          active-class="active"
        >
          <i class="fas fa-cog menu-icon"></i>
          <span class="menu-text">Settings</span>
        </router-link>
        
        <button 
          @click="handleLogout" 
          class="nav-link dashboard-link logout-btn d-flex align-items-center gap-3 py-2 px-3 border-0 text-start w-100"
        >
          <i class="fas fa-sign-out-alt menu-icon"></i>
          <span class="menu-text">Logout</span>
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  user: Object
})

const router = useRouter()

const menuConfigs = {
  admin: [
    { label: 'Dashboard', path: '/admin-dash', icon: 'fas fa-th-large' },
    { label: 'Companies', path: '/admin/companies', icon: 'fas fa-building' },
    { label: 'Students', path: '/admin/students', icon: 'fas fa-user-graduate' },
    { label: 'Drives', path: '/admin/drives', icon: 'fas fa-briefcase' },
    { label: 'Applications', path: '/admin/applications', icon: 'fas fa-file-alt' },
    { label: 'Reports', path: '/admin/reports', icon: 'fas fa-chart-bar' }
  ],
  recruiter: [
    { label: 'Dashboard', path: '/company-dash', icon: 'fas fa-th-large' },
    { label: 'Our Drives', path: '/company/all-drives', icon: 'fas fa-briefcase' },
    { label: 'Shortlisted', path: '/company/shortlisted', icon: 'fas fa-user-check' },
    { label: 'Interviews', path: '/company/interviews', icon: 'fas fa-calendar-alt' },
    { label: 'Applications', path: '/company/applications', icon: 'fas fa-file-alt' },
    { label: 'Profile', path: '/company/profile', icon: 'fas fa-user-tie' }
  ],
  student: [
    { label: 'Dashboard', path: '/student-dash', icon: 'fas fa-th-large' },
    { label: 'Available Drives', path: '/student/drives', icon: 'fas fa-search' },
    { label: 'My Applications', path: '/student/applications', icon: 'fas fa-file-invoice' },
    { label: 'Interviews', path: '/student/interviews', icon: 'fas fa-calendar-alt' },
    { label: 'My Profile', path: '/student/profile', icon: 'fas fa-user' }
  ]
}

const currentMenu = computed(() => menuConfigs[props.user?.type] || [])

const handleLogout = () => {
  localStorage.removeItem('user')
  router.push('/login')
}
</script>

<style scoped>
.section-label {
  letter-spacing: 0.07rem;
}

.dashboard-link {
  color: var(--color-bg, #ffffff);
  font-weight: 500;
  font-size: 0.9rem;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.dashboard-link:hover {
  background-color: var(--color-secondary, #d6a650) !important;
  color: var(--color-primary, #781f19) !important;
  transform: translateX(4px);
}

.dashboard-link.active {
  background-color: var(--color-secondary, #d6a650) !important;
  color: var(--color-primary, #781f19) !important;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.menu-icon {
  width: 20px;
  text-align: center;
  font-size: 1.1rem;
}

.logout-btn {
  background: transparent;
  color: #ffb5b5; /* Light red */
}

.logout-btn:hover {
  background-color: #ff4d4d !important;
  color: white !important;
}

.menu-text {
  letter-spacing: 0.2px;
}
</style>
