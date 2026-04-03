<template>
  <div class="signup-panel">

    <div class="signup-header">
      <div class="company-badge">
        <span class="badge-icon">🏢</span>
        <span class="badge-label">Recruiter Portal</span>
      </div>
      <h1 class="signup-title">Partner with CampusBridge</h1>
      <p class="signup-subtitle">Create your recruiter account to start hiring our campus talent.</p>
    </div>

    <transition name="fade">
      <div v-if="errorMsg" class="alert alert-error">
        <span class="alert-icon">⚠️</span> {{ errorMsg }}
      </div>
    </transition>
    <transition name="fade">
      <div v-if="successMsg" class="alert alert-success">
        <span class="alert-icon">✅</span> {{ successMsg }}
      </div>
    </transition>

    <div v-if="registered" class="success-banner">
      <span class="success-banner-icon">✓</span>
      <span>Registration successful! You can now <router-link to="/login" class="success-link">login</router-link>.</span>
    </div>

    <div class="form-fields">
      <BaseInput label="Company Name" placeholder="Your Company Name" v-model="name" />
      <BaseInput label="Company Email" placeholder="company@example.com" type="email" v-model="email" id="company-email" />
      <BaseInput label="Username" placeholder="Choose a unique username" v-model="username" id="company-username" />
      <BaseInput label="Password" type="password" placeholder="Min 8 characters" v-model="password" id="company-password" />
      <BaseInput label="Confirm Password" type="password" placeholder="Re-enter your password" v-model="confirmPassword" />
    </div>

    <BaseButton
      :text="loading ? 'Creating Account...' : 'CREATE ACCOUNT →'"
      @click="handleSubmit"
      :disabled="loading"
    />

    <div class="auth-footer">
      <p class="footer-text">
        Already have an account?&nbsp;
        <router-link to="/login" class="sign-in-link">Login</router-link>
      </p>
      <p class="footer-text" style="margin-top: 6px;">
        Signing up as a student?&nbsp;
        <router-link to="/signup" class="sign-in-link">Student Signup</router-link>
      </p>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import BaseInput from '../ui/BaseInput.vue'
import BaseButton from '../ui/BaseButton.vue'

const name = ref('')
const email = ref('')
const username = ref('')
const password = ref('')
const confirmPassword = ref('')

const loading = ref(false)
const errorMsg = ref('')
const registered = ref(false)

function validate() {
  if (!name.value.trim()) return 'Company name is required.'
  if (!email.value.trim()) return 'Company email is required.'
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) return 'Please enter a valid email address.'
  if (!username.value.trim()) return 'Username is required.'
  if (username.value.trim().length < 4) return 'Username must be at least 4 characters.'
  if (!password.value) return 'Password is required.'
  if (password.value.length < 8) return 'Password must be at least 8 characters.'
  if (password.value !== confirmPassword.value) return 'Passwords do not match.'
  return null
}

async function handleSubmit() {
  errorMsg.value = ''

  const validationError = validate()
  if (validationError) {
    errorMsg.value = validationError
    return
  }

  loading.value = true
  try {
    const res = await fetch('http://127.0.0.1:5000/api/company-register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        name: name.value.trim(),
        email: email.value.trim(),
        username: username.value.trim(),
        password: password.value
      })
    })

    const data = await res.json()

    if (!res.ok) {
      errorMsg.value = data.error || 'Registration failed. Please try again.'
    } else {
      registered.value = true
    }
  } catch (err) {
    errorMsg.value = 'Network error. Please check your connection.'
  } finally {
    loading.value = false
  }
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

.signup-header {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.company-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #fff7ed;
  border: 1px solid #fed7aa;
  border-radius: 20px;
  padding: 4px 12px;
  width: fit-content;
}

.badge-icon {
  font-size: 0.85rem;
}

.badge-label {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.8px;
  text-transform: uppercase;
  color: #c2410c;
}

.signup-title {
  font-size: 1.85rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0;
  line-height: 1.15;
}

.signup-subtitle {
  font-size: 0.88rem;
  color: #6b7280;
  margin: 0;
  line-height: 1.5;
}

.form-fields {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.alert {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border-radius: 10px;
  font-size: 0.85rem;
  font-weight: 500;
  line-height: 1.4;
}

.alert-error {
  background: #fef2f2;
  border: 1px solid #fca5a5;
  color: #b91c1c;
}

.alert-success {
  display: none;
}

.alert-icon {
  font-size: 1rem;
  flex-shrink: 0;
}

.auth-footer {
  text-align: center;
}

.footer-text {
  font-family: 'Inter', sans-serif;
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0;
}

.sign-in-link {
  font-weight: 700;
  color: var(--color-primary, #781f19);
  text-decoration: none;
  transition: opacity 0.2s ease;
}

.sign-in-link:hover {
  opacity: 0.75;
  text-decoration: underline;
}

/* Transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}

.success-banner {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 11px 16px;
  border-left: 3px solid #008000;
  background: #e6ffe6;
  border-radius: 6px;
  font-family: 'Inter', sans-serif;
  font-size: 0.875rem;
  font-weight: 500;
  color: #0f172a;
}

.success-banner-icon {
  font-size: 1rem;
  font-weight: 700;
  color: #008000;
  flex-shrink: 0;
}

.success-link {
  font-weight: 700;
  color: var(--color-primary, #781f19);
  text-decoration: none;
}

.success-link:hover {
  text-decoration: underline;
}
</style>