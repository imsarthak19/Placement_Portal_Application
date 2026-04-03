<template>
  <div class="signup-panel">

    <div class="signup-header">
      <h1 class="signup-title">Create your account</h1>
      <p class="signup-subtitle">Join the premium placement management ecosystem.</p>
    </div>

    <div class="form-fields">
      <BaseInput label="Full Name" placeholder="Your Name" v-model="name" />
      <BaseInput label="Institutional Email" placeholder="Your Institutional Email" type="email" v-model="email" />
      <BaseInput label="Password" type="password" v-model="password" />
      <BaseInput label="Confirm Password" type="password" v-model="confirmPassword" />
    </div>

    <BaseButton text="CREATE ACCOUNT →" @click="handleSubmit" />

    <GoogleLogin />

    <AuthFooter />

    <div class="bottom-links">
      <a href="#">Privacy Policy</a>
      <span class="dot">•</span>
      <a href="#">Terms of Use</a>
      <span class="dot">•</span>
      <a href="#">Support</a>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import BaseInput from '../ui/BaseInput.vue'
import BaseButton from '../ui/BaseButton.vue'
import GoogleLogin from './GoogleLogin.vue'
import AuthFooter from './AuthFooter.vue'

const name = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')

function handleSubmit() {
    
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.signup-panel {
  width: 420px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  font-family: 'Inter', sans-serif;
}

/* Header */
.signup-header {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.signup-title {
  font-size: 1.85rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0;
  line-height: 1.15;
}

.signup-subtitle {
  font-size: 0.9rem;
  color: #6b7280;
  margin: 0;
}

/* Form fields */
.form-fields {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

/* Bottom footer links */
.bottom-links {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-top: 4px;
}

.bottom-links a {
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.8px;
  text-transform: uppercase;
  color: #9ca3af;
  text-decoration: none;
  transition: color 0.2s ease;
}

.bottom-links a:hover {
  color: #374151;
}

.bottom-links .dot {
  color: #9ca3af;
  font-size: 0.6rem;
}
</style>