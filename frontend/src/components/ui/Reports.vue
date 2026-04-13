<template>
  <div class="reports-container">
    <!-- Success Alert -->
        <div v-if="message" class="alert alert-success border-0 rounded-3 shadow-sm mb-2">
          <div class="d-flex align-items-center gap-3">
             <i class="fas fa-check-circle fs-4"></i>
             <div>{{ message }}</div>
          </div>
        </div>
    <div class="card shadow-sm border-0 rounded-4 p-4 mb-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h3 class="fw-bold mb-1">System Reports</h3>
          <p class="text-muted small mb-0">Export platform data and analytics</p>
        </div>
        <div class="report-actions">
           <button 
            @click="triggerReport" 
            :disabled="processing" 
            class="btn btn-brand-primary rounded-3 px-4 py-2 d-flex align-items-center gap-2"
           >
            <i v-if="processing" class="fas fa-spinner fa-spin"></i>
            <i v-else class="fas fa-file-export"></i>
            {{ processing ? 'Processing...' : 'Get Full Platform Report' }}
           </button>
        </div>
      </div>

      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading statistics...</span>
        </div>
      </div>

      <div v-else class="report-content">
        <!-- Visualization Row -->
        <div class="row g-4 mb-4">
          <div class="col-lg-6">
            <div class="chart-card bg-light p-3 rounded-4">
              <h6 class="fw-bold mb-3">Application Distribution</h6>
              <apexchart 
                type="donut" 
                height="300" 
                :options="statusChartOptions" 
                :series="statusSeries"
              ></apexchart>
            </div>
          </div>
          <div class="col-lg-6">
            <div class="chart-card bg-light p-3 rounded-4">
              <h6 class="fw-bold mb-3">Student Branches</h6>
              <apexchart 
                type="bar" 
                height="300" 
                :options="branchChartOptions" 
                :series="branchSeries"
              ></apexchart>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import VueApexCharts from 'vue3-apexcharts'

const apexchart = VueApexCharts
const loading = ref(true)
const processing = ref(false)
const message = ref('')

const chartsData = ref({
  application_status: {},
  student_branches: {},
  drives_trend: {}
})

// --- Chart Options & Series (Reused from AdminDash) ---

const statusSeries = computed(() => Object.values(chartsData.value.application_status))
const statusChartOptions = computed(() => ({
  labels: Object.keys(chartsData.value.application_status).map(s => s.charAt(0).toUpperCase() + s.slice(1)),
  chart: {
    type: 'donut',
    fontFamily: "'Inter', sans-serif"
  },
  colors: ['#781f19', '#e63946', '#2a9d8f', '#e9c46a', '#f4a261', '#457b9d', '#1d3557'],
  legend: { position: 'bottom' },
  dataLabels: { enabled: false },
  plotOptions: {
    pie: {
      donut: {
        size: '65%',
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
  }
}))

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
      borderRadius: 6,
      horizontal: true,
      distributed: true,
    }
  },
  colors: ['#781f19', '#4f46e5', '#10b981', '#f59e0b', '#06b6d4'],
  xaxis: {
    categories: Object.keys(chartsData.value.student_branches),
  },
  legend: { show: false }
}))

const fetchStats = async () => {
  const token = localStorage.getItem("token")
  if (!token) return
  
  loading.value = true
  try {
    const res = await axios.get('http://127.0.0.1:5555/api/admin/stats', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (res.data.charts) {
      chartsData.value = res.data.charts
    }
  } catch (err) {
    console.error("Fetch stats error:", err)
  } finally {
    loading.value = false
  }
}

const triggerReport = async () => {
    const token = localStorage.getItem("token")
    if (!token) return

    processing.value = true
    message.value = ''
    try {
        const res = await axios.post('http://127.0.0.1:5555/api/admin/trigger-platform-report', {}, {
            headers: { 'Authorization': `Bearer ${token}` }
        })
        message.value = res.data.message
    } catch (err) {
        console.error("Trigger report error:", err)
        alert("Failed to trigger report. Please try again.")
    } finally {
        processing.value = false
    }
}

onMounted(fetchStats)
</script>

<style scoped>
.reports-container {
  max-width: 100%;
}

.chart-card {
  transition: all 0.3s ease;
}

.chart-card:hover {
  background-color: #f8f9fa !important;
  box-shadow: 0 5px 15px rgba(0,0,0,0.05);
}

.btn-brand-primary {
  background-color: var(--color-primary, #781f19);
  color: white;
  border: none;
  font-weight: 600;
  transition: all 0.2s ease;
}

.btn-brand-primary:hover:not(:disabled) {
  background-color: #5d1712;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(120, 31, 25, 0.2);
}

.btn-brand-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.rounded-4 {
  border-radius: 1.25rem !important;
}
</style>
