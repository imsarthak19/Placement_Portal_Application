<template>
  <div class="card h-100 border-0 shadow-sm rounded-4 p-2 custom-stat-card">
      <div class="card-body d-flex align-items-center gap-3">
          <div :class="['stat-icon-wrapper rounded-3 d-flex align-items-center justify-content-center flex-shrink-0', bgClass]">
              <i :class="[icon, textClass, 'fs-4']"></i>
          </div>
          <div class="overflow-hidden">
              <span class="text-muted small fw-bold text-uppercase ls-wide d-block mb-1">{{ label }}</span>
              <h3 class="mb-0 fw-extrabold h4">{{ value }}</h3>
              <span v-if="change" :class="['small fw-semibold mt-1 d-block', changeClass]">{{ change }}</span>
          </div>
      </div>
  </div>
</template>

<script setup>
defineProps({
    label: { type: String, required: true },
    value: { type: [Number, String], required: true },
    icon: { type: String, default: 'fas fa-chart-line' },
    bgClass: { type: String, default: 'bg-primary border border-primary border-opacity-10' },
    textClass: { type: String, default: 'text-primary' },
    change: { type: String, default: '' },
    changeClass: { type: String, default: '' }
})
</script>

<style>
.custom-stat-card {
    transition: all 0.3s ease;
}
.custom-stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05) !important;
}
.stat-icon-wrapper {
    width: 60px;
    height: 60px;
}
.ls-wide {
    letter-spacing: 0.05em;
}
.fw-extrabold {
    font-weight: 800;
}

/* Stat color utility classes */
.bg-indigo-soft { background-color: #d8e6fb; }
.text-indigo { color: #0d6eff; }
.bg-pink-soft { background-color: #fff7e3; }
.text-pink { color: #e2ce87; }
.bg-emerald-soft { background-color: #ecfdf5; }
.text-emerald { color: #059669; }
.bg-orange-soft { background-color: #fff7ed; }
.text-orange { color: #ea580c; }
.bg-blue-soft { background-color: #e0f2fe; }
.text-blue { color: #0369a1; }
.bg-gold-soft { background-color: #fefce8; }
.text-gold { color: #a16207; }

.bg-primary-soft { background-color: rgba(120, 31, 25, 0.08); }
.bg-success-soft { background-color: rgba(25, 135, 84, 0.08); }
.bg-warning-soft { background-color: rgba(255, 193, 7, 0.12); }
</style>
