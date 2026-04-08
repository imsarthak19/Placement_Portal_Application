<template>
  <div class="reports-container">
    <div class="card shadow-sm border-0 rounded-4 p-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h3 class="fw-bold mb-1">System Reports</h3>
          <p class="text-muted small mb-0">Export platform data and analytics</p>
        </div>
        <div class="report-actions">
          <slot name="actions"></slot>
        </div>
      </div>

      <div class="report-content py-5 text-center">
        <div class="empty-state">
          <div class="fs-1 mb-3 opacity-50">📊</div>
          <h5 class="fw-bold">Report generation</h5>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

</script>

<style scoped>
.reports-container {
  max-width: 100%;
}

.empty-state {
  max-width: 400px;
  margin: 0 auto;
}
</style>
