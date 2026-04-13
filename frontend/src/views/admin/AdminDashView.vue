<template>
  <DashboardLayout role="admin">
    <div class="admin-dashboard">
      <!-- Header Section -->
      <header class="d-md-flex justify-content-between align-items-start mb-5">
        <div class="header-content mb-3 mb-md-0">
          <h1 class="h2 fw-bold text-dark mb-1">Admin Dashboard</h1>
          <p class="text-muted mb-0">Welcome back, Administrator. Here's what's happening today.</p>
        </div>
        <!-- Might add some other button here later -->
        <div class="header-actions">
           <div v-if="loading" class="spinner-border spinner-border-sm text-primary me-2" role="status">
             <span class="visually-hidden">Loading...</span>
           </div>
          <button class="btn btn-brand-primary px-4 py-2 rounded-3 fw-bold shadow-sm">
            <router-link to="/admin/reports" class="text-white text-decoration-none">
              <i class="fas fa-file-alt me-2"></i>Generate Report
            </router-link>
          </button>
        </div>
      </header>

      <!-- Stats Grid -->
      <!-- Future adds - Total Shortlisted, Total Hired, Total Rejected, etc. -->
      <div class="row g-4 mb-5">
        <div v-for="(stat, key) in statConfig" :key="key" class="col-sm-6 col-md-4">
          <StatCard 
            :label="stat.label"
            :value="stats[key] || 0"
            :icon="stat.icon"
            :bgClass="stat.bgClass"
            :textClass="stat.textClass"
          />
        </div>
      </div>

    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import DashboardLayout from '@/components/sidebar/DashboardLayout.vue'
import StatCard from '@/components/ui/StatCard.vue'
import router from '@/router'

const stats = ref({
  students: 0,
  companies: 0,
  drives: 0,
  applications: 0,
  shortlisted: 0,
  interviews: 0
})

const loading = ref(true)

const statConfig = {
  students: {
    label: 'Total Students',
    icon: 'fas fa-user-graduate',
    bgClass: 'bg-indigo-soft',
    textClass: 'text-indigo',
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
  },
  shortlisted: {
    label: 'Shortlisted',
    icon: 'fas fa-user-check',
    bgClass: 'bg-amber-soft',
    textClass: 'text-amber',
  },
  interviews: {
    label: 'Interviews',
    icon: 'fas fa-calendar-check',
    bgClass: 'bg-cyan-soft',
    textClass: 'text-cyan',
  }
}

// # Fetching Admin Stats
const fetchStats = async () => {
    const token = localStorage.getItem("token")
    if (!token) {
        console.error("No token found")
        return
    }
    loading.value = true
    try {
        const res = await axios.get('http://127.0.0.1:5555/api/admin/stats', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        console.log("Admin Stats Data:", res.data)
        // Update stats object
        Object.keys(res.data).forEach(key => {
            if (key in stats.value) {
                stats.value[key] = res.data[key]
            }
        })
    } catch (err) {
        console.error("Fetch stats error:", err)
    } finally {
        loading.value = false
    }
}

// Things to be done on mount
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

.stat-icon-wrapper {
  width: 58px;
  height: 58px;
  transition: all 0.3s ease;
}

.card:hover .stat-icon-wrapper {
  transform: scale(1.1) rotate(5deg);
}

.card {
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;
}

.smaller {
  font-size: 0.7rem;
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