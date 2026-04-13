<template>
  <div class="d-flex min-vh-100 bg-light">
    <!-- Sidebar Component -->
    <Sidebar :user="user" :isOpen="isSidebarOpen" @toggle="toggleSidebar" />

    <!-- Mobile Header -->
    <div class="mobile-header d-lg-none position-fixed top-0 start-0 w-100 bg-white border-bottom px-4 d-flex align-items-center justify-content-between z-3 shadow-xs" style="height: 60px;">
        <h2 class="h5 fw-bold mb-0">
            <span style="color: var(--color-secondary, #781f19);">Campus</span><span style="color: var(--color-primary, #d6a650);">Bridge</span>
        </h2>
        <button @click="toggleSidebar" class="btn border-0 p-0 text-primary fs-3">
            <i class="fas fa-bars"></i>
        </button>
    </div>

    <!-- Main Content Area -->
    <main class="flex-grow-1 p-4 dashboard-main" :class="{'mobile-mt': true}">
      <!-- Overlay for mobile -->
      <div v-show="isSidebarOpen" @click="toggleSidebar" class="sidebar-overlay d-lg-none"></div>
      
      <div class="container-fluid py-2">
        <slot />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Sidebar from './Sidebar.vue'

const props = defineProps({
  user: Object
})

const user = ref(props.user || JSON.parse(localStorage.getItem('user') || '{}'))
const isSidebarOpen = ref(false)

const toggleSidebar = () => {
    isSidebarOpen.value = !isSidebarOpen.value
}

onMounted(() => {
  if (!props.user) {
    const savedUser = localStorage.getItem('user')
    if (savedUser) {
      user.value = JSON.parse(savedUser)
    }
  }
})
</script>

<style scoped>
.dashboard-main {
  /* Offset for fixed sidebar width (230px) */
  margin-left: 230px;
  transition: all 0.3s ease;
  overflow-x: hidden;
}

.sidebar-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.5);
    z-index: 1045;
    backdrop-filter: blur(2px);
}

@media (max-width: 991.98px) {
  .dashboard-main {
    margin-left: 0;
    padding: 1rem !important;
  }
  .mobile-mt {
      margin-top: 60px !important;
  }
}
</style>