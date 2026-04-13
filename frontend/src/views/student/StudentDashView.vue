<template>
  <DashboardLayout role="student">
    <div class="admin-dashboard">
      <!-- Header Section -->
      <header class="d-md-flex justify-content-between align-items-start mb-5">
        <div class="header-content mb-3 mb-md-0">
          <h1 class="h2 fw-bold text-dark mb-1">Student Dashboard</h1>
          <p class="text-muted mb-0">Welcome back, Here's what's happening today.</p>
        </div>
      </header>

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
import StatCard from '@/components/ui/StatCard.vue'
import DashboardLayout from '@/components/sidebar/DashboardLayout.vue'
import CompanyProfile from '@/components/layout/CompanyProfile.vue'

const stats = ref({
  active_drives: 0,
  active_recruiters: 0,
  applied_at: 0,
  shortlisted: 0,
  interviews: 0,
  offers_received: 0
})

const user = JSON.parse(localStorage.getItem('user') || '{}')
const companyId = user.id

const statConfig = {
  active_drives: {
    label: 'Active Drives',
    icon: 'fas fa-briefcase',
    bgClass: 'bg-indigo-soft',
    textClass: 'text-indigo',
  },
  active_recruiters: {
    label: 'Active Recruiters',
    icon: 'fas fa-building',
    bgClass: 'bg-pink-soft',
    textClass: 'text-pink',
  },
  applied_at: {
    label: 'Applied At',
    icon: 'fas fa-paper-plane',
    bgClass: 'bg-blue-soft',
    textClass: 'text-blue',
  },
  shortlisted: {
    label: 'Shortlisted',
    icon: 'fas fa-file-alt',
    bgClass: 'bg-emerald-soft',
    textClass: 'text-emerald',
  },
  interviews: {
    label: 'Interviews',
    icon: 'fas fa-calendar-check',
    bgClass: 'bg-orange-soft',
    textClass: 'text-orange',
  },
  offers_received: {
    label: 'Offers Received',
    icon: 'fas fa-award',
    bgClass: 'bg-gold-soft',
    textClass: 'text-gold',
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