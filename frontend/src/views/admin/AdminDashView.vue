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

      <!-- Charts Section -->
      <div class="row g-4 mb-5">
        <!-- Application Status Distribution (Pie Chart) -->
        <div class="col-lg-6">
          <div class="card border-0 shadow-sm p-4 h-100 rounded-4">
            <h5 class="fw-bold mb-4 text-dark">Application Status</h5>
            <div id="status-chart" class="chart-container">
              <apexchart 
                type="donut" 
                height="350" 
                :options="statusChartOptions" 
                :series="statusSeries"
              ></apexchart>
            </div>
          </div>
        </div>

        <!-- Students by Branch (Bar Chart) -->
        <div class="col-lg-6">
          <div class="card border-0 shadow-sm p-4 h-100 rounded-4">
            <h5 class="fw-bold mb-4 text-dark">Students by Branch</h5>
            <div id="branch-chart" class="chart-container">
              <apexchart 
                type="bar" 
                height="350" 
                :options="branchChartOptions" 
                :series="branchSeries"
              ></apexchart>
            </div>
          </div>
        </div>

        <!-- Placement Trends (Line Chart) -->
        <div class="col-12">
          <div class="card border-0 shadow-sm p-4 rounded-4">
            <h5 class="fw-bold mb-4 text-dark">Placement Drive Trends (Last 6 Months)</h5>
            <div id="trend-chart" class="chart-container">
              <apexchart 
                type="area" 
                height="350" 
                :options="trendChartOptions" 
                :series="trendSeries"
              ></apexchart>
            </div>
          </div>
        </div>
      </div>

    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import DashboardLayout from '@/components/sidebar/DashboardLayout.vue'
import StatCard from '@/components/ui/StatCard.vue'
import VueApexCharts from 'vue3-apexcharts'

// Register ApexCharts locally
const apexchart = VueApexCharts

const stats = ref({
  students: 0,
  companies: 0,
  drives: 0,
  applications: 0,
  shortlisted: 0,
  interviews: 0
})

const chartsData = ref({
  application_status: {},
  student_branches: {},
  drives_trend: {}
})

const loading = ref(true)

// --- Chart Options & Series ---

// 1. Application Status Chart
const statusSeries = computed(() => Object.values(chartsData.value.application_status))
const statusChartOptions = computed(() => ({
  labels: Object.keys(chartsData.value.application_status).map(s => s.charAt(0).toUpperCase() + s.slice(1)),
  chart: {
    type: 'donut',
    fontFamily: "'Inter', sans-serif"
  },
  colors: ['#781f19', '#e63946', '#2a9d8f', '#e9c46a', '#f4a261', '#457b9d', '#1d3557'],
  legend: {
    position: 'bottom'
  },
  plotOptions: {
    pie: {
      donut: {
        size: '70%',
        labels: {
          show: true,
          total: {
            show: true,
            label: 'Total',
            formatter: (w) => w.globals.seriesTotals.reduce((a, b) => a + b, 0)
          }
        }
      }
    }
  },
  dataLabels: {
    enabled: false
  },
  responsive: [{
    breakpoint: 480,
    options: {
      chart: {
        width: 200
      },
      legend: {
        position: 'bottom'
      }
    }
  }]
}))

// 2. Branch Chart
const branchSeries = computed(() => [{
  name: 'Students',
  data: Object.values(chartsData.value.student_branches)
}])
const branchChartOptions = computed(() => ({
  chart: {
    type: 'bar',
    fontFamily: "'Inter', sans-serif",
    toolbar: { show: false }
  },
  plotOptions: {
    bar: {
      borderRadius: 8,
      horizontal: true,
      distributed: true,
    }
  },
  colors: ['#781f19', '#4f46e5', '#10b981', '#f59e0b', '#06b6d4', '#ec4899', '#8b5cf6'],
  dataLabels: {
    enabled: true,
    style: {
      fontSize: '12px',
      colors: ['#fff']
    }
  },
  xaxis: {
    categories: Object.keys(chartsData.value.student_branches),
  },
  legend: { show: false }
}))

// 3. Trend Chart
const trendSeries = computed(() => [{
  name: 'New Drives',
  data: Object.values(chartsData.value.drives_trend)
}])
const trendChartOptions = computed(() => ({
  chart: {
    type: 'area',
    height: 350,
    toolbar: { show: false },
    fontFamily: "'Inter', sans-serif",
    zoom: { enabled: false }
  },
  dataLabels: { enabled: false },
  stroke: {
    curve: 'smooth',
    width: 3,
    colors: ['#781f19']
  },
  fill: {
    type: 'gradient',
    gradient: {
      shadeIntensity: 1,
      opacityFrom: 0.4,
      opacityTo: 0.1,
      stops: [0, 90, 100],
      colorStops: [
        {
          offset: 0,
          color: "#781f19",
          opacity: 0.4
        },
        {
          offset: 100,
          color: "#781f19",
          opacity: 0.1
        }
      ]
    }
  },
  xaxis: {
    categories: Object.keys(chartsData.value.drives_trend),
  },
  colors: ['#781f19'],
  grid: {
    borderColor: '#f1f1f1',
  }
}))

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
        
        // Update Chart Data
        if (res.data.charts) {
          chartsData.value = res.data.charts
        }
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

.chart-container {
  min-height: 350px;
}

.rounded-4 {
  border-radius: 1.25rem !important;
}

.card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0,0,0,0.08) !important;
}

@media (max-width: 768px) {
  .chart-container {
    min-height: 300px;
  }
}
</style>