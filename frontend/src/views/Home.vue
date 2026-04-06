<template>
  <div class="vh-100 d-flex align-items-center justify-content-center hero-bg">
    <div class="texture-overlay"></div>
    <div class="container overflow-hidden">
      <div class="row justify-content-center align-items-center h-100">
        <div class="col-lg-6 text-center animate-fade-up">

          <div class="mb-5">
            <h1 class="display-1 fw-extrabold main-logo mb-3">
              <span class="text-accent">Campus</span><span class="text-white">Bridge</span>
            </h1>
            <p class="lead text-white-50 fs-4 mb-0 ls-wide fw-medium">
              Revolutionizing the Bridge between Students and Global Careers.
            </p>
          </div>

          <div class="d-flex flex-column flex-sm-row gap-4 justify-content-center px-4">
            <router-link to="/signup" class="btn btn-brand-primary btn-lg px-5 py-3 rounded-pill fw-bold shadow-lg transition-transform">
              <i class="fas fa-rocket me-2"></i>CREATE ACCOUNT
            </router-link>
            <router-link to="/login" class="btn btn-brand-outline btn-lg px-5 py-3 rounded-pill fw-bold shadow-lg transition-transform">
              <i class="fas fa-sign-in-alt me-2"></i>LOG IN
            </router-link>
          </div>

          <div class="mt-5 pt-5 opacity-75">
            <div class="d-flex align-items-center justify-content-center gap-4 text-white-50 small fw-bold text-uppercase ls-wider">
              <span>50+ Corporations</span>
              <span class="dot-separator">•</span>
              <span>Premium Career Management</span>
              <span class="dot-separator">•</span>
              <span>Al-Driven Matching</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <p class="brand-footer">© 2024 CampusBridge | Developed & Maintained by Sarthak Chaudhary</p>
  </div>
</template>

<script setup>
</script>

<style scoped>
.hero-bg {
  position: relative;
  width: 100%;
  height: 100%;
  background-color: var(--color-primary);
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  font-family: 'Inter', sans-serif;
}

.texture-overlay {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.07) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.07) 1px, transparent 1px);
  background-size: 36px 36px;
  pointer-events: none;
  z-index: 0;
}

.texture-overlay::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    radial-gradient(circle, rgba(255,255,255,0.065) 1px, transparent 1px);
  background-size: 36px 36px;
  background-position: 18px 18px;
  pointer-events: none;
}

.main-logo {
  letter-spacing: -2px;
  font-family: 'Inter', sans-serif;
  line-height: 1;
}

.fw-extrabold {
  font-weight: 800;
}

.text-accent {
  color: var(--color-secondary, #d6a650);
}

.ls-wide {
  letter-spacing: 0.05rem;
}

.ls-wider {
  letter-spacing: 0.15rem;
}

.btn-brand-primary {
  background-color: var(--color-secondary, #d6a650);
  color: var(--color-primary, #781f19);
  border: 2px solid var(--color-secondary, #d6a650);
}

.btn-brand-primary:hover {
  background-color: transparent;
  color: var(--color-secondary, #d6a650);
  transform: translateY(-4px);
}

.btn-brand-outline {
  background-color: transparent;
  color: #ffffff;
  border: 2px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(5px);
}

.btn-brand-outline:hover {
  background-color: rgba(255, 255, 255, 0.15);
  border-color: #ffffff;
  color: #ffffff;
  transform: translateY(-4px);
}

.transition-transform {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.dot-separator {
  color: var(--color-secondary, #d6a650);
  font-size: 1.2rem;
}

.brand-footer {
  position: absolute;
  bottom: 24px;
  left: 0;
  right: 0;
  text-align: center;
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.55);
  z-index: 1;
  letter-spacing: 0.2px;
}

/* Entry animation */
.animate-fade-up {
  animation: fadeUp 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) both;
}

@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 576px) {
  .display-1 {
    font-size: 4rem;
  }
  .lead {
    font-size: 1.1rem;
  }
}
</style>