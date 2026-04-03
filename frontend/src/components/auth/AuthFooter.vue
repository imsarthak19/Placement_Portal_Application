<template>
  <div class="auth-footer">
    <p class="footer-text">
      Already have an account?&nbsp;
      <a href="#" class="sign-in-link">Sign In</a>
    </p>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

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
</style>