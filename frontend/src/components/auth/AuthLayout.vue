<template>
  <div class="container-fluid p-0 vh-100 overflow-hidden">
    <div class="row g-0 h-100">
      <!-- Brand Panel Section (hidden on mobile, visible on lg+) -->
      <div class="col-lg-5 d-none d-lg-block h-100 p-0">
        <BrandPanel />
      </div>
      
      <!-- Content Section -->
      <div class="col-lg-7 d-flex align-items-center justify-content-center h-100 bg-white shadow-lg">
        <div class="auth-box w-100">
          <slot />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import BrandPanel from './BrandPanel.vue'
</script>

<style scoped>
.auth-box {
  max-width: 480px;
  padding: 1.5rem;
}

/* This Ensures child Slot content is centered on mobile too */
@media (max-width: 991.98px) {
  .auth-box {
    padding: 1rem;
    max-width: 100%;
  }
}
</style>