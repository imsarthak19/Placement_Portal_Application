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
                <span :class="['small fw-semibold mt-1 d-block', stat.changeClass]">{{ stat.change }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content Grid -->
      <div class="row g-4">
        <!-- Recent Activity Section -->
        <div class="col-lg-5">
          <section class="card h-100 border-0 shadow-sm rounded-4">
            <div class="card-header bg-white border-0 py-4 px-4 d-flex justify-content-between align-items-center">
              <h5 class="mb-0 fw-bold">Recent Activity</h5>
              <button class="btn btn-link btn-sm text-brand-primary fw-bold text-decoration-none">View All</button>
            </div>
            <div class="card-body px-4 pb-4">
              <div v-if="activities.length === 0" class="text-center py-5 text-muted fst-italic">
                No recent activity found.
              </div>
              <div class="activity-timeline">
                <div v-for="activity in activities" :key="activity.id" class="activity-item d-flex gap-3 mb-4 last-child-mb-0">
                  <div class="timeline-dot-wrapper mt-1">
                    <div class="dot bg-brand-primary rounded-circle"></div>
                    <div class="line bg-light mx-auto"></div>
                  </div>
                  <div class="activity-info">
                    <p class="mb-1 text-dark small fw-medium">{{ activity.text }}</p>
                    <span class="text-muted smaller fst-italic">{{ activity.time }}</span>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </div>

        <!-- Upcoming Drives Section -->
        <div class="col-lg-7">
          <section class="card h-100 border-0 shadow-sm rounded-4">
            <div class="card-header bg-white border-0 py-4 px-4 d-flex justify-content-between align-items-center">
              <h5 class="mb-0 fw-bold">Upcoming Drives</h5>
              <button class="btn btn-link btn-sm text-brand-primary fw-bold text-decoration-none">Manage</button>
            </div>
            <div class="card-body px-4 pb-4">
              <div v-if="upcomingDrives.length === 0" class="text-center py-5 text-muted fst-italic">
                No upcoming drives scheduled.
              </div>
              <div class="drive-list d-grid gap-3">
                <div v-for="drive in upcomingDrives" :key="drive.id" class="drive-row p-3 rounded-3 bg-light d-flex align-items-center gap-3 transition-all">
                  <div class="drive-avatar bg-white border rounded-3 d-flex align-items-center justify-content-center fw-bold text-brand-primary shadow-sm" style="width: 48px; height: 48px;">
                    {{ drive.companyCode }}
                  </div>
                  <div class="flex-grow-1 overflow-hidden">
                    <h6 class="mb-1 fw-bold text-dark text-truncate">{{ drive.title }}</h6>
                    <p class="mb-0 text-muted small text-truncate">{{ drive.companyName }} • {{ drive.date }}</p>
                  </div>
                  <span :class="['badge rounded-pill px-3 py-2', getStatusBadgeClass(drive.status)]">
                    {{ drive.status }}
                  </span>
                </div>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DashboardLayout from '@/components/sidebar/DashboardLayout.vue'

const stats = ref({
  students: 1240,
  companies: 42,
  drives: 15,
  applications: 856
})

const statConfig = {
  students: {
    label: 'Total Students',
    icon: 'fas fa-user-graduate',
    bgClass: 'bg-indigo-soft',
    textClass: 'text-indigo',
    change: '+12% from last month',
    changeClass: 'text-success'
  },
  companies: {
    label: 'Total Companies',
    icon: 'fas fa-building',
    bgClass: 'bg-pink-soft',
    textClass: 'text-pink',
    change: '+5 new this week',
    changeClass: 'text-success'
  },
  drives: {
    label: 'Active Drives',
    icon: 'fas fa-briefcase',
    bgClass: 'bg-emerald-soft',
    textClass: 'text-emerald',
    change: '4 closing soon',
    changeClass: 'text-warning'
  },
  applications: {
    label: 'Total Applications',
    icon: 'fas fa-file-alt',
    bgClass: 'bg-orange-soft',
    textClass: 'text-orange',
    change: '+48 today',
    changeClass: 'text-success'
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

onMounted(async () => {
  // Here will Fetch real data later
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