<template>
  <div class="auth-layout">
    <BrandPanel />
    <div class="auth-content">
      <slot />
    </div>
  </div>
</template>

<script setup>
import BrandPanel from './BrandPanel.vue'
</script>

<style scoped>
.auth-layout {
  display: flex;
  height: 100vh;
}

.auth-content {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>