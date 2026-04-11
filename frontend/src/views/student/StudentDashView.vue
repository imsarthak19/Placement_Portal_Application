<template>
  <DashboardLayout role="recruiter">
    <div class="admin-dashboard">
      <!-- Header Section -->
      <header class="d-md-flex justify-content-between align-items-start mb-5">
        <div class="header-content mb-3 mb-md-0">
          <h1 class="h2 fw-bold text-dark mb-1">Student Dashboard</h1>
          <p class="text-muted mb-0">Welcome back, Here's what's happening today.</p>
        </div>
        <div class="header-actions">
          <button class="btn btn-brand-primary px-4 py-2 rounded-3 fw-bold shadow-sm">
            <i class="fas fa-file-alt me-2"></i>Generate Report
          </button>
        </div>
      </header>

      <!-- Stats Grid -->
      <div class="row g-4 mb-5">
        <div v-for="(stat, key) in statConfig" :key="key" class="col-sm-6 col-xl-3">
          <div class="card h-100 border-0 shadow-sm rounded-4 p-2">
            <div class="card-body d-flex align-items-center gap-3">
              <div :class="['stat-icon-wrapper rounded-3 d-flex align-items-center justify-content-center flex-shrink-0', stat.bgClass]">
                <i :class="[stat.icon, stat.textClass, 'fs-4']"></i>
              </div>
              <div class="overflow-hidden">
                <span class="text-muted small fw-bold text-uppercase ls-wide d-block mb-1">{{ stat.label }}</span>
                <h3 class="mb-0 fw-extrabold h4">{{ stats[key] || 0 }}</h3>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import DashboardLayout from '@/components/sidebar/DashboardLayout.vue'
import CompanyProfile from '@/components/layout/CompanyProfile.vue'

const stats = ref({
  students: 0,
  companies: 0,
  drives: 0,
  applications: 0
})

const user = JSON.parse(localStorage.getItem('user') || '{}')
const companyId = user.id

const statConfig = {
  students: {
    label: 'Active Drives',
    icon: 'fas fa-briefcase',
    bgClass: 'bg-indigo-soft',
    textClass: 'text-success',
    change: '+12% from last month',
  },
  companies: {
    label: 'Actiive Recruiters',
    icon: 'fas fa-building',
    bgClass: 'bg-pink-soft',
    textClass: 'text-warning',
  },
  applications: {
    label: 'Shortlisted Applications',
    icon: 'fas fa-file-alt',
    bgClass: 'bg-orange-soft',
    textClass: 'text-orange',
  },
  hired: {
    label: 'Interviews Scheduled',
    icon: 'fas fa-users-cog',
    bgClass: 'bg-orange-soft',
    textClass: 'text-orange',
  }
}

const fetchStats = async () => {
    const token = localStorage.getItem("token")
    try {
        const res = await axios.get('http://127.0.0.1:5555/api/student/stats', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        stats.value = res.data
    } catch (err) {
        console.error("Fetch stats error:", err)
    }
}

onMounted(async () => {
  await fetchStats()
})
</script>

<style scoped>
.btn-brand-primary {
  background-color: var(--color-primary, #781f19);
  color: #ffffff;
  border: none;
  transition: all 0.2s ease;
}

.btn-brand-primary:hover {
  background-color: #5d1712;
  color: white;
  transform: translateY(-2px);
}

.text-brand-primary {
  color: var(--color-primary, #781f19);
}

.ls-wide {
  letter-spacing: 0.05rem;
}

.fw-extrabold {
  font-weight: 800;
}

/* Custom Stat Icon Colors (Soft Backgrounds) */
.bg-indigo-soft { background-color: rgb(200, 223, 201); }
.text-indigo { color: #4f46e5; }
.bg-pink-soft { background-color: #fff7e3; }
.text-pink { color: #e2ce87; }
.bg-emerald-soft { background-color: #ecfdf5; }
.text-emerald { color: #059669; }
.bg-orange-soft { background-color: #fff7ed; }
.text-orange { color: #ea580c; }

.stat-icon-wrapper {
  width: 52px;
  height: 52px;
}

.smaller {
  font-size: 0.75rem;
}

.transition-all {
  transition: all 0.2s ease;
}
</style>