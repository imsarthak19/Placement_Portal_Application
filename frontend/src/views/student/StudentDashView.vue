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

      <!-- Stats Grid -->
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

      <!-- Recent Opportunities Section -->
      <div class="row mb-4">
        <div class="col-12 d-flex justify-content-between align-items-center">
            <h4 class="fw-bold text-dark mb-0">Recent Opportunities</h4>
            <router-link to="/student/drives" class="btn btn-link text-decoration-none fw-bold p-0">View All</router-link>
        </div>
      </div>

      <div class="row g-4">
          <div v-if="recentDrives.length === 0" class="col-12 py-4 text-center text-muted">
              No recent drives found.
          </div>
          <div v-for="drive in recentDrives" :key="drive.id" class="col-md-4">
              <div class="card border-0 shadow-sm rounded-4 h-100 drive-card overflow-hidden">
                  <div class="card-body p-4">
                      <div class="d-flex align-items-center gap-3 mb-3">
                          <div class="logo-box bg-light rounded-3 d-flex align-items-center justify-content-center border" style="width: 50px; height: 50px;">
                              <img v-if="drive.company_logo" :src="drive.company_logo" class="img-fluid rounded-2 p-1" style="max-height: 40px;">
                              <i v-else class="fas fa-building text-muted"></i>
                          </div>
                          <div>
                              <h6 class="fw-bold mb-0 text-truncate" style="max-width: 150px;">{{ drive.company_name }}</h6>
                              <small class="text-muted"><i class="fas fa-map-marker-alt"></i> {{ drive.location }}</small>
                          </div>
                      </div>
                      <h5 class="fw-bold mb-2">{{ drive.title }}</h5>
                      <div class="d-flex justify-content-between align-items-center mt-3">
                          <span class="badge bg-primary bg-opacity-10 text-primary rounded-pill px-3">{{ drive.payScale }}</span>
                          <router-link :to="'/student/drive/' + drive.id" class="btn btn-sm btn-outline-primary rounded-pill px-3">Details</router-link>
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

const recentDrives = ref([])

const user = ref(JSON.parse(localStorage.getItem('user') || '{}'))

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

// Fetch dashboard stats
const fetchStats = async () => {
    const token = localStorage.getItem("token")
    try {
        const res = await axios.get('http://127.0.0.1:5555/api/student/stats', {
            headers: { 'Authorization': `Bearer ${token}` }
        })
        stats.value = res.data
    } catch (err) {
        console.error("Fetch stats error:", err)
    }
}

// Fetch a glimpse of available drives
const fetchRecentDrives = async () => {
    const token = localStorage.getItem("token")
    try {
        const res = await axios.get('http://127.0.0.1:5555/api/student/active-drives', {
            headers: { 'Authorization': `Bearer ${token}` }
        })
        // Show only the 3 most recent drives
        recentDrives.value = res.data.slice(0, 3)
    } catch (err) {
        console.error("Fetch drives error:", err)
    }
}

onMounted(async () => {
  await fetchStats()
  await fetchRecentDrives()
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