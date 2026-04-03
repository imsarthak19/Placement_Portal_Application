<template>
  <div class="signup-panel">
    <p v-if="errorMessage" class="error">
      {{ errorMessage }}
    </p>

    <div class="signup-header">
      <h1 class="signup-title">Login your account</h1>
      <p class="signup-subtitle">Welcome back! Enter your details to access your dashboard.</p>
    </div>

    <div class="form-fields">
      <BaseInput label="Institutional Email or Username" placeholder="Your Institutional Email or Username" type="text" v-model="email" />
      <BaseInput label="Password" type="password" v-model="password" />
    </div>

    <BaseButton text="LOGIN →" @click="handleLogin" />

    <GoogleLogin />

    <div class="auth-footer">
      <p class="footer-text">
        Don't have an account?&nbsp;
        <a href="" class="sign-up-link">Sign Up</a>
      </p>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import BaseInput from '../ui/BaseInput.vue'
import BaseButton from '../ui/BaseButton.vue'
import GoogleLogin from './GoogleLogin.vue'
import { useRouter } from 'vue-router'

const errorMessage = ref('')
const router = useRouter()

const email = ref('')
const password = ref('')

async function handleLogin() {
  errorMessage.value = '' // reset before request

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
        errorMessage.value = 'Unknown user type'
      }

    } else {
      errorMessage.value = data.message || 'Invalid credentials'
    }

  } catch (err) {
    errorMessage.value = 'Server error. Please try again later.'
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

.error {
  color: red;
  font-size: 14px;
  margin-bottom: 10px;
}
</style>