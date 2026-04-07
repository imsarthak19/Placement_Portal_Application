<template>
  <aside class="sidebar position-fixed start-0 top-0 vh-100 d-flex flex-column border-end shadow-sm">
    <!-- Brand Logo -->
    <div class="logo-container py-4 px-4 mb-1">
      <h2 class="h4 fw-bold mb-0 ls-tight dash-logo">
        <span class="logo-accent">Campus</span><span class="text-white">Bridge</span>
      </h2>
    </div>

    <!-- User Profile Card -->
    <div class="user-profile py-3 px-4 mb-3 d-flex align-items-center gap-3 profile-divider">
      <div class="avatar-box bg-brand-secondary rounded-circle d-flex align-items-center justify-content-center flex-shrink-0 shadow-sm">
        <i class="fas fa-user-shield text-brand-primary" v-if="role === 'admin'"></i>
        <i class="fas fa-building text-brand-primary" v-else-if="role === 'recruiter'"></i>
        <i class="fas fa-user-graduate text-brand-primary" v-else></i>
      </div>
      <div class="user-details overflow-hidden">
        <h6 class="mb-0 fw-semibold text-white text-truncate small">{{ user?.username }}</h6>
        <span class="text-secondary text-white opacity-75 fw-bold text-uppercase user-role-text">{{ user?.type }}</span>
      </div>
    </div>

    <!-- Scrollable Menu -->
    <div class="flex-grow-1 custom-scrollbar">
      <SidebarMenu :user="user" />
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import SidebarMenu from '@/components/sidebar/SidebarMenu.vue'

const props = defineProps({
  user: Object
})

const role = computed(() => props.user?.type)
</script>

<style scoped>
.sidebar {
  width: 230px;
  background-color: var(--color-primary, #781f19);
  z-index: 1050;
  transition: transform 0.3s ease;
}

.dash-logo {
  font-size: 1.5rem;
  letter-spacing: -0.5px;
}

.logo-accent {
  color: var(--color-secondary, #d6a650);
}

.profile-divider {
  border-bottom: 2px solid rgba(214, 166, 80, 0.3);
}

.avatar-box {
  width: 42px;
  height: 42px;
}

.bg-brand-secondary{
  background-color: var(--color-secondary);
}

.text-brand-primary {
  color: var(--color-primary, #781f19);
}

.user-role-text {
  font-size: 0.65rem;
  letter-spacing: 0.05rem;
}

.ls-tight {
  letter-spacing: -0.025em;
}

.custom-scrollbar {
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.2) transparent;
}

/* Responsive: Hide sidebar on small screens or use a drawer */
@media (max-width: 991.98px) {
  .sidebar {
    transform: translateX(-100%);
  }
}
</style>