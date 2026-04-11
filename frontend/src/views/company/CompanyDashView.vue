<template>
  <DashboardLayout role="recruiter">
    <div class="admin-dashboard">
      <!-- Header Section -->
      <header class="d-md-flex justify-content-between align-items-start mb-5">
        <div class="header-content mb-3 mb-md-0">
          <h1 class="h2 fw-bold text-dark mb-1">Company Dashboard</h1>
          <p class="text-muted mb-0">Welcome back, <span class="text-dark">{{ company?.name || 'Company Representative' }}</span>. Here's what's happening today.</p>
        </div>
        <div class="header-actions">
          <button class="btn btn-brand-primary px-4 py-2 rounded-3 fw-bold shadow-sm">
            <i class="fas fa-file-alt me-2"></i>Generate Report
          </button>
        </div>
      </header>

      <!-- Stats Grid -->
      <div class="row g-4 mb-5">
        <div v-for="(config, key) in statConfig" :key="key" class="col-sm-6 col-md-4">
          <StatCard
            :label="config.label"
            :value="stats[key]"
            :icon="config.icon"
            :bgClass="config.bgClass"
            :textClass="config.textClass"
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

const stats = ref({
  total_drives: 0,
  active_drives: 0,
  total_applications: 0,
  shortlisted: 0,
  hired: 0,
  interviews: 0
})

const statConfig = {
  active_drives: {
    label: 'Active Drives',
    icon: 'fas fa-briefcase',
    bgClass: 'bg-indigo-soft',
    textClass: 'text-indigo',
  },
  total_applications: {
    label: 'Total Applications',
    icon: 'fas fa-file-alt',
    bgClass: 'bg-emerald-soft',
    textClass: 'text-emerald',
  },
  shortlisted: {
    label: 'Shortlisted Candidates',
    icon: 'fas fa-user-check',
    bgClass: 'bg-orange-soft',
    textClass: 'text-orange',
  },
  interviews: {
    label: 'Interviews Scheduled',
    icon: 'fas fa-calendar-alt',
    bgClass: 'bg-cyan-soft',
    textClass: 'text-cyan',
  },
  hired: {
    label: 'Hired Candidates',
    icon: 'fas fa-award',
    bgClass: 'bg-pink-soft',
    textClass: 'text-pink',
  },
  total_drives: {
    label: 'Total All Drives',
    icon: 'fas fa-archive',
    bgClass: 'bg-orange-soft',
    textClass: 'text-orange',
  }
}

const fetchStats = async () => {
    const token = localStorage.getItem("token")
    try {
        const res = await axios.get('http://127.0.0.1:5555/api/company/stats', {
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