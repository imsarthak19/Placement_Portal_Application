<template>
  <DashboardLayout role="recruiter">
    <div class="admin-dashboard">
      <!-- Header Section -->
      <header class="d-md-flex justify-content-between align-items-start mb-5">
        <div class="header-content mb-3 mb-md-0">
          <h1 class="h2 fw-bold text-dark mb-1">Company Dashboard</h1>
          <p class="text-muted mb-0">Welcome back, <span class="text-dark">{{ company?.name || 'Company Representative' }}</span>. Here's what's happening today.</p>
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

      <!-- Upcoming Interviews Section -->
      <div class="row mb-4">
        <div class="col-12 d-flex justify-content-between align-items-center">
            <h4 class="fw-bold text-dark mb-0">Upcoming Interviews</h4>
            <router-link to="/company/interviews" class="btn btn-link text-decoration-none fw-bold p-0">View All</router-link>
        </div>
      </div>

      <div class="row g-4 mb-5">
          <div v-if="upcomingInterviews.length === 0" class="col-12 py-5 text-center text-muted card border-0 shadow-sm rounded-4">
              <div class="card-body">
                  <i class="fas fa-calendar-times display-4 mb-3 opacity-25"></i>
                  <p class="mb-0">No upcoming interviews scheduled.</p>
              </div>
          </div>
          <div v-for="interview in upcomingInterviews" :key="interview.id" class="col-md-4">
              <div class="card border-0 shadow-sm rounded-4 h-100 interview-card transition-all">
                  <div class="card-body p-4">
                      <!-- Date Badge -->
                      <div class="d-flex justify-content-between align-items-start mb-3">
                          <div class="date-badge rounded-3 text-center p-2 bg-light border">
                              <div class="small fw-bold text-primary text-uppercase">{{ formatDateMonth(interview.scheduled_at) }}</div>
                              <div class="h5 fw-bold mb-0 text-dark">{{ formatDateDay(interview.scheduled_at) }}</div>
                          </div>
                          <span class="badge rounded-pill px-3" :class="interview.mode === 'Virtual' ? 'bg-info bg-opacity-10 text-info' : 'bg-primary bg-opacity-10 text-primary'">
                              {{ interview.mode }}
                          </span>
                      </div>
                      
                      <!-- Candidate Info -->
                      <div class="mb-4">
                          <h6 class="text-muted small fw-bold text-uppercase mb-1 ls-wide">Candidate</h6>
                          <h5 class="fw-bold text-dark mb-1">{{ interview.student_name }}</h5>
                          <p class="text-muted small mb-0"><i class="fas fa-briefcase me-1"></i> {{ interview.drive_title }}</p>
                      </div>

                      <div class="d-flex justify-content-between align-items-center pt-3 border-top">
                          <div class="small text-muted">
                              <i class="far fa-clock me-1"></i> {{ formatTime(interview.scheduled_at) }}
                          </div>
                          <router-link to="/company/interviews" class="btn btn-sm btn-outline-primary rounded-pill px-3 fw-bold">Manage</router-link>
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
import StatCard from '@/components/ui/StatCard.vue'

const stats = ref({
  total_drives: 0,
  active_drives: 0,
  total_applications: 0,
  shortlisted: 0,
  hired: 0,
  interviews: 0
})

const upcomingInterviews = ref([])
const company = JSON.parse(localStorage.getItem('user') || '{}')

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
    bgClass: 'bg-gold-soft',
    textClass: 'text-gold',
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

// Fetch dashboard stats
const fetchStats = async () => {
    const token = localStorage.getItem("token")
    try {
        const res = await axios.get('http://127.0.0.1:5555/api/company/stats', {
            headers: { 'Authorization': `Bearer ${token}` }
        })
        stats.value = res.data
    } catch (err) {
        console.error("Fetch stats error:", err)
    }
}

// Fetch upcoming interviews
const fetchInterviews = async () => {
    const token = localStorage.getItem("token")
    try {
        const res = await axios.get('http://127.0.0.1:5555/api/company/interviews', {
            headers: { 'Authorization': `Bearer ${token}` }
        })
        
        const now = new Date()
        // Sort and filter only future interviews
        upcomingInterviews.value = res.data
            .filter(i => new Date(i.scheduled_at) > now)
            .sort((a, b) => new Date(a.scheduled_at) - new Date(b.scheduled_at))
            .slice(0, 5) // Show top 5
            
    } catch (err) {
        console.error("Fetch interviews error:", err)
    }
}

// Formatters
const formatDateMonth = (dateStr) => {
    return new Date(dateStr).toLocaleDateString(undefined, { month: 'short' })
}

const formatDateDay = (dateStr) => {
    return new Date(dateStr).toLocaleDateString(undefined, { day: '2-digit' })
}

const formatTime = (dateStr) => {
    return new Date(dateStr).toLocaleTimeString(undefined, { 
        hour: '2-digit', minute: '2-digit' 
    })
}

onMounted(async () => {
  await fetchStats()
  await fetchInterviews()
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
  transition: all 0.3s ease;
}

.interview-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;
}

.date-badge {
    min-width: 50px;
    line-height: 1.2;
}
</style>