<template>
  <DashboardLayout role="admin">
    <div class="admin-dashboard">
      <!-- Header Section -->
      <header class="d-md-flex justify-content-between align-items-start mb-5">
        <div class="header-content mb-3 mb-md-0">
          <h1 class="h2 fw-bold text-dark mb-1">Admin Dashboard</h1>
          <p class="text-muted mb-0">Welcome back, Administrator. Here's what's happening today.</p>
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

const stats = ref({
  students: 0,
  companies: 0,
  drives: 0,
  applications: 0
})

const statConfig = {
  students: {
    label: 'Total Students',
    icon: 'fas fa-user-graduate',
    bgClass: 'bg-indigo-soft',
    textClass: 'text-indigo',
    change: '+12% from last month',
  },
  companies: {
    label: 'Total Companies',
    icon: 'fas fa-building',
    bgClass: 'bg-pink-soft',
    textClass: 'text-pink',
  },
  drives: {
    label: 'Active Drives',
    icon: 'fas fa-briefcase',
    bgClass: 'bg-emerald-soft',
    textClass: 'text-emerald',
  },
  applications: {
    label: 'Total Applications',
    icon: 'fas fa-file-alt',
    bgClass: 'bg-orange-soft',
    textClass: 'text-orange',
  }
}

const activities = ref([
  { id: 1, text: 'New company "TechCorp" registered', time: '2 mins ago' },
  { id: 2, text: 'Placement drive for "DataSystems" approved', time: '1 hour ago' },
  { id: 3, text: 'Student "Rahul Sharma" updated resume', time: '3 hours ago' },
  { id: 4, text: 'System backup completed successfully', time: '5 hours ago' }
])

const upcomingDrives = ref([
  { id: 1, title: 'Software Engineer Intern', companyName: 'Google', companyCode: 'G', date: 'Oct 15, 2026', status: 'open' },
  { id: 2, title: 'Product Manager', companyName: 'Microsoft', companyCode: 'M', date: 'Oct 18, 2026', status: 'upcoming' },
  { id: 3, title: 'Data Scientist', companyName: 'Meta', companyCode: 'F', date: 'Oct 20, 2026', status: 'draft' }
])

function getStatusBadgeClass(status) {
  const map = {
    open: 'bg-success text-white',
    upcoming: 'bg-primary text-white',
    draft: 'bg-secondary text-white'
  }
  return map[status] || 'bg-light text-dark'
}

const fetchStats = async () => {
    const token = localStorage.getItem("token")
    try {
        const res = await axios.get('http://127.0.0.1:5555/api/admin/stats', {
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
.bg-indigo-soft { background-color: #eef2ff; }
.text-indigo { color: #4f46e5; }
.bg-pink-soft { background-color: #fdf2f8; }
.text-pink { color: #db2777; }
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

/* Timeline Custom Styles */
.timeline-dot-wrapper {
  position: relative;
  width: 12px;
}

.dot {
  width: 12px;
  height: 12px;
  z-index: 1;
}

.line {
  width: 2px;
  height: 100%;
  position: absolute;
  top: 12px;
  left: 5px;
  z-index: 0;
}

.last-child-mb-0:last-child {
  margin-bottom: 0 !important;
}

.last-child-mb-0:last-child .line {
  display: none;
}

/* Drive Row Hover */
.drive-row:hover {
  background-color: #f0f0f0 !important;
  transform: translateX(5px);
  cursor: pointer;
}

.transition-all {
  transition: all 0.2s ease;
}
</style>