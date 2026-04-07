<template>
  <div class="d-flex min-vh-100 bg-light">
    <!-- Sidebar Component -->
    <Sidebar :user="user" />

    <!-- Main Content Area -->
    <main class="flex-grow-1 p-4 dashboard-main">
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
}

@media (max-width: 991.98px) {
  .dashboard-main {
    margin-left: 0;
    padding: 1rem !important;
  }
}
</style>