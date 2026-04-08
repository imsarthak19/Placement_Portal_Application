<template>
  <div class="search-container">
    <div class="search-wrapper shadow-sm">
      <i class="fas fa-search search-icon text-muted"></i>
      <input 
        type="text" 
        class="search-input" 
        :placeholder="placeholder"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
      >
      <button 
        v-if="modelValue" 
        class="clear-btn" 
        @click="$emit('update:modelValue', '')"
        title="Clear search"
      >
        <i class="fas fa-times-circle"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: 'Search...'
  }
})

defineEmits(['update:modelValue'])
</script>

<style scoped>
.search-container {
  width: 100%;
  max-width: 400px;
  position: relative;
}

.search-wrapper {
  display: flex;
  align-items: center;
  background: #ffffff;
  border-radius: 12px;
  padding: 8px 16px;
  border: 1px solid #e2e8f0;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  gap: 12px;
}

.search-wrapper:focus-within {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1) !important;
  transform: translateY(-1px);
}

.search-icon {
  font-size: 0.9rem;
  opacity: 0.6;
}

.search-input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 0.95rem;
  color: #1e293b;
  outline: none;
  padding: 4px 0;
}

.search-input::placeholder {
  color: #94a3b8;
  font-weight: 400;
}

.clear-btn {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s ease;
  border-radius: 50%;
}

.clear-btn:hover {
  color: #64748b;
  background: #f1f5f9;
}

/* Dark mode anticipation */
@media (prefers-color-scheme: dark) {
  /* .search-wrapper { background: #1e293b; border-color: #334155; } */
  /* .search-input { color: #f1f5f9; } */
}
</style>
