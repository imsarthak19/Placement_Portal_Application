<template>
  <div class="brand-panel">
    <div class="texture-overlay"></div>

    <!-- Logo -->
    <div class="brand-content">
      <div class="logo-card">
        <img src="../../assets/logo/logo1.png" alt="CampusBridge Logo" />
      </div>

      <h1 class="brand-name">CampusBridge</h1>

      <p class="brand-tagline">Connecting <span class="brand-tagline2">Talent</span> to <span class="brand-tagline2">Opportunity</span></p>

      <div class="gold-divider"></div>
    </div>

    <p class="brand-footer">© 2024 CampusBridge | Developed & Maintained by Sarthak Chaudhary</p>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

.brand-panel {
  position: relative;
  width: 45%;
  min-height: 100vh;
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

.brand-content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.logo-card {
  background: #ffffff;
  border: 3px solid var(--color-secondary);
  border-radius: 20px;
  padding: 18px 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow:
    0 0 0 6px rgba(201, 160, 62, 0.2),
    0 8px 32px rgba(0, 0, 0, 0.35);
  width: 160px;
  height: 110px;
}

.logo-card img {
  width: 130px;
  height: auto;
  object-fit: contain;
  display: block;
}

.brand-name {
  font-size: 2.4rem;
  font-weight: 800;
  color: #ffffff;
  margin: 0;
  letter-spacing: -0.5px;
  text-align: center;
}

.brand-tagline {
  font-size: 1rem;
  font-weight: 600;
  font-style: italic;
  color: rgba(255, 255, 255, 0.92);
  margin: 0;
  text-align: center;
  letter-spacing: 0.3px;
}

.brand-tagline2{
  color: var(--color-secondary);

}

.gold-divider {
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, #c9a03e, #e8c96d, #c9a03e);
  border-radius: 2px;
  margin-top: 4px;
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
</style>