<template>
  <DashboardLayout role="admin">
    <div class="admin-reports">
      <!-- Headings -->
      <header class="dashboard-header mb-5">
        <div class="header-tag">ADMINISTRATION</div>
        <h1>Reports Console</h1>
      </header>

      <!-- Main Content -->
      <div class="reports-view-content">
        <Reports />
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import DashboardLayout from '@/components/sidebar/DashboardLayout.vue'
import Reports from '@/components/ui/Reports.vue'
</script>

<style scoped>
.admin-reports {
  max-width: 1200px;
  margin: 0 auto;
}

.header-tag {
  color: var(--color-primary);
  font-weight: 800;
  font-size: 0.8rem;
  letter-spacing: 1px;
  opacity: 0.7;
}

.dashboard-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
}
</style>
