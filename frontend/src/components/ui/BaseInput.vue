<template>
  <div class="input-group">
    <label class="input-label">{{ label }}</label>
    <div class="input-wrapper" :class="{ focused }">
      <span class="input-icon">
        <!-- Password (confirm) icon -->
        <svg v-if="type === 'password' && label?.toLowerCase().includes('confirm')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/>
        </svg>
        <!-- Password icon -->
        <svg v-else-if="type === 'password'" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>
        </svg>
        <!-- Email icon -->
        <svg v-else-if="label?.toLowerCase().includes('email')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>
        </svg>
        <!-- Person / Name icon -->
        <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="8" r="4"/><path d="M20 21a8 8 0 1 0-16 0"/>
        </svg>
      </span>

      <input
        :type="showPassword ? 'text' : type"
        :placeholder="placeholder || label"
        :value="modelValue"
        @input="onInput"
        @focus="focused = true"
        @blur="focused = false"
        class="input-field"
      />

      <!-- Eye toggle for password fields -->
      <button
        v-if="type === 'password'"
        type="button"
        class="toggle-eye"
        @click="showPassword = !showPassword"
        tabindex="-1"
      >
        <svg v-if="!showPassword" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/>
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-10-8-10-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 10 8 10 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  label: String,
  placeholder: String,
  modelValue: String,
  type: {
    type: String,
    default: 'text'
  }
})

const emit = defineEmits(['update:modelValue'])
const focused = ref(false)
const showPassword = ref(false)

function onInput(event) {
  emit('update:modelValue', event.target.value)
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

.input-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.input-label {
  font-family: 'Inter', sans-serif;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.input-wrapper {
  display: flex;
  align-items: center;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  background: #fff;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  overflow: hidden;
}

.input-wrapper.focused {
  border-color: var(--color-primary, #781f19);
  box-shadow: 0 0 0 3px rgba(120, 31, 25, 0.1);
}

.input-icon {
  display: flex;
  align-items: center;
  padding: 0 12px;
  color: #9ca3af;
  flex-shrink: 0;
}

.input-icon svg {
  width: 16px;
  height: 16px;
}

.input-field {
  flex: 1;
  border: none;
  outline: none;
  padding: 11px 8px 11px 0;
  font-family: 'Inter', sans-serif;
  font-size: 0.9rem;
  color: #111827;
  background: transparent;
}

.input-field::placeholder {
  color: #9ca3af;
}

.toggle-eye {
  display: flex;
  align-items: center;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0 12px;
  color: #9ca3af;
  transition: color 0.2s ease;
  flex-shrink: 0;
}

.toggle-eye:hover {
  color: #6b7280;
}

.toggle-eye svg {
  width: 16px;
  height: 16px;
}
</style>