<template>
  <button class="btn" @click="emit('click')">
    {{ text }}<slot />
  </button>
</template>

<script setup>
defineProps({
  text: String
})

const emit = defineEmits(['click'])
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@600;700&display=swap');

.btn {
  width: 100%;
  padding: 15px;
  background: var(--color-secondary, #d6a650);
  color: var(--color-primary, #781f19);
  border: none;
  border-radius: 8px;
  font-family: 'Inter', sans-serif;
  font-size: 0.875rem;
  font-weight: 700;
  letter-spacing: 1.2px;
  cursor: pointer;
  transition: background 0.25s ease, box-shadow 0.25s ease, transform 0.15s ease;
}

.btn:hover {
  background: #c9903a;
  box-shadow: 0 6px 20px rgba(214, 166, 80, 0.45);
  transform: translateY(-1px);
}

.btn:active {
  transform: translateY(0);
  box-shadow: none;
}
</style>