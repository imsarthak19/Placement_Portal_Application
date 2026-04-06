<template>
  <div class="signup-container mx-auto">
    <!-- Header Section -->
    <div class="text-start mb-4">
      <h1 class="fs-3 fw-extrabold text-dark mb-2">Create your account</h1>
      <p class="text-muted mb-0">Join the premium placement management ecosystem.</p>
    </div>

    <!-- Error/Success Alerts -->
    <div class="mb-4">
      <transition name="fade">
        <div v-if="errorMsg" class="alert alert-danger d-flex align-items-center gap-2 border-0 shadow-sm rounded-3 py-3 px-4" role="alert">
          <i class="fas fa-exclamation-triangle"></i>
          <div>{{ errorMsg }}</div>
        </div>
      </transition>
      
      <transition name="fade">
        <div v-if="registered" class="alert alert-success d-flex align-items-center gap-2 border-0 shadow-sm rounded-3 py-3 px-4" role="alert">
          <i class="fas fa-check-circle"></i>
          <div>Registration successful! You can now <router-link to="/login" class="fw-bold text-brand-primary">login</router-link>.</div>
        </div>
      </transition>
    </div>

    <!-- Form Fields -->
    <div class="d-grid gap-3 mb-4">
      <BaseInput label="Full Name" placeholder="Your Name" v-model="name" />
      <BaseInput label="Username" placeholder="Choose a username min 4 characters" v-model="username" />
      <BaseInput label="Institutional Email" placeholder="Your Institutional Email" type="email" v-model="email" />
      <BaseInput label="Password" type="password" placeholder="Min 8 characters" v-model="password" />
      <BaseInput label="Confirm Password" type="password" placeholder="Re-enter your password" v-model="confirmPassword" />
    </div>

    <!-- Submit Button -->
    <div class="mb-4">
      <BaseButton 
        :text="loading ? 'Creating Account...' : 'CREATE ACCOUNT →'" 
        @click="handleSubmit" 
        :disabled="loading"
        class="w-100 py-3"
      />
    </div>

    <!-- Footer Links -->
    <div class="text-center">
      <p class="text-muted small mb-2">
        Already have an account? 
        <router-link to="/login" class="text-brand-primary fw-bold text-decoration-none hover-underline">Login</router-link>
      </p>
      <p class="text-muted small mb-0">
        Signing up as a recruiter? 
        <router-link to="/company-signup" class="text-brand-primary fw-bold text-decoration-none hover-underline">Recruiter Signup</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import BaseInput from '../ui/BaseInput.vue'
import BaseButton from '../ui/BaseButton.vue'

const name = ref('')
const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const registered = ref(false)
const loading = ref(false)
const errorMsg = ref('')

//  Front End Validations 
function validate() {
  if (!name.value.trim()) return 'Name is required.'
  if (!email.value.trim()) return 'Email is required.'
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
  registered.value = false

  const validationError = validate()
  if (validationError) {
    errorMsg.value = validationError
    return
  }

  loading.value = true
  try {
    const res = await fetch('http://127.0.0.1:5555/api/student-register', {
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
      // Clear fields on success
      name.value = ''
      username.value = ''
      email.value = ''
      password.value = ''
      confirmPassword.value = ''
    }
  } catch (err) {
    errorMsg.value = 'Network error. Please check your connection.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.signup-container {
  max-width: 420px;
}

.fw-extrabold {
  font-weight: 800;
}

.text-brand-primary {
  color: var(--color-primary, #781f19);
}

.hover-underline:hover {
  text-decoration: underline !important;
}

/* Alert styling overrides */
.alert-danger {
  background-color: #fff5f5;
  color: #c53030;
}

.alert-success {
  background-color: #f0fff4;
  color: #2f855a;
}

/* Auth Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>