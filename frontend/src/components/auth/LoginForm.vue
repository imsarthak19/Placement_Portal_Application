<template>
  <div class="login-container w-100">
    
    <!-- Error Message -->
    <transition name="fade">
        <div v-if="errorMsg" class="alert alert-danger d-flex align-items-center gap-2 border-0 shadow-sm rounded-3 py-3 px-4" role="alert">
          <i class="fas fa-exclamation-triangle"></i>
          <div>{{ errorMsg }}</div>
        </div>
    </transition>

    <!-- Header -->
    <div class="login-header mb-5">
      <h1 class="display-6 fw-bolder text-dark mb-2 ls-tight">Login to account</h1>
      <p class="text-muted mb-0">Welcome back! Please enter your details to access your dashboard.</p>
      <div class="brand-divider mt-3"></div>
    </div>

    <!-- Form Fields -->
    <div class="form-fields d-grid gap-4 mb-5">
      <BaseInput 
        label="Email or Username" 
        placeholder="Enter your email or username" 
        type="text" 
        v-model="email" 
      />
      <div class="password-field-wrapper">
        <BaseInput 
          label="Password" 
          placeholder="Enter your password"
          type="password" 
          v-model="password" 
        />
        <div class="text-end mt-2">
          <a href="#" class="forgot-password-link">Forgot password?</a>
        </div>
      </div>
    </div>

    <!-- Action Button -->
    <div class="action-section mb-5">
      <BaseButton text="SIGN IN TO DASHBOARD →" @click="handleLogin" />
    </div>

    <div class="auth-footer py-4 border-top border-light">
      <div class="row g-3">
        <div class="col-sm-6 text-center text-sm-start">
          <p class="text-muted small mb-1">New student?</p>
          <router-link to="/signup" class="brand-link">Student Signup</router-link>
        </div>
        <div class="col-sm-6 text-center text-sm-end">
          <p class="text-muted small mb-1">Hiring talent?</p>
          <router-link to="/company-signup" class="brand-link">Recruiter Signup</router-link>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import BaseInput from '../ui/BaseInput.vue'
import BaseButton from '../ui/BaseButton.vue'
import { useRouter } from 'vue-router'

const errorMsg = ref('')
const router = useRouter()

const email = ref('')
const password = ref('')

async function handleLogin() {
  errorMsg.value = '' // reset before request

  try {
    const res = await fetch('http://127.0.0.1:5000/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        identifier: email.value,
        password: password.value
      })
    })

    const data = await res.json()

    if (res.ok) {
      localStorage.setItem('user', JSON.stringify(data))

      const routeMap = {
        admin: '/admin-dash',
        recruiter: '/company-dash',
        student: '/student-dash'
      }

      const route = routeMap[data.type]

      if (route) {
        router.push(route)
      } else {
        errorMsg.value = 'Unknown user type'
      }

    } else {
      errorMsg.value = data.message || 'Invalid credentials'
    }

  } catch (err) {
    errorMsg.value = 'Server error. Please try again later.'
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.login-container {
  font-family: 'Inter', sans-serif;
}

.ls-tight {
  letter-spacing: -0.025em;
}

.brand-divider {
  width: 40px;
  height: 4px;
  background-color: var(--color-secondary, #d6a650);
  border-radius: 2px;
}

.brand-link {
  font-weight: 700;
  font-size: 0.9rem;
  color: var(--color-primary, #781f19);
  text-decoration: none;
  transition: all 0.2s ease;
  display: inline-block;
}

.brand-link:hover {
  color: #5a1712;
  transform: translateX(3px);
  text-decoration: underline;
}

.forgot-password-link {
  font-size: 0.8rem;
  font-weight: 600;
  color: #6b7280;
  text-decoration: none;
  transition: color 0.2s ease;
}

.forgot-password-link:hover {
  color: var(--color-primary, #781f19);
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

.fw-extrabold {
  font-weight: 800;
}
</style>