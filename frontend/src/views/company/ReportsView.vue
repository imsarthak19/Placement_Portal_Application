<template>
  <DashboardLayout role="recruiter">
    <div class="mt-4 animate-fade-in">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1 class="h3 fw-bold mb-1" style="color: var(--color-text);">Analytics & Reports</h1>
          <p class="text-muted mb-0">Visual insights into your recruitment performance.</p>
        </div>
        <div class="d-flex gap-2">
            <button @click="exportData" class="btn btn-outline-primary border-2 d-flex align-items-center gap-2 px-4 rounded-3 fw-bold">
                <i class="fas fa-file-export"></i> EXPORT DATA
            </button>
        </div>
      </div>

      <!-- Stats Overview -->
      <div class="row g-4 mb-5">
        <div v-for="stat in reportStats" :key="stat.label" class="col-md-3">
          <div class="card border-0 shadow-sm rounded-4 h-100 stat-hover">
            <div class="card-body p-4 text-center">
              <div :class="['icon-box rounded-circle mx-auto mb-3 d-flex align-items-center justify-content-center bg-opacity-10', stat.colorClass]">
                <i :class="[stat.icon, stat.textClass, 'fs-4']"></i>
              </div>
              <h3 class="fw-bold mb-1">{{ stat.value }}</h3>
              <p class="text-muted small text-uppercase fw-bold mb-0 opacity-75">{{ stat.label }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Analytics Section -->
      <div class="row g-4 mt-2">
          <!-- Selection Funnel -->
          <div class="col-lg-7">
              <div class="card border-0 shadow-sm rounded-4 h-100">
                  <div class="card-header bg-white border-0 p-4 pb-0">
                      <h5 class="fw-bold mb-0 d-flex align-items-center gap-2">
                          <i class="fas fa-filter text-primary"></i> Selection Funnel
                      </h5>
                  </div>
                  <div class="card-body p-4">
                      <div class="chart-container" style="position: relative; height:300px; width:100%">
                          <canvas id="funnelChart"></canvas>
                      </div>
                  </div>
              </div>
          </div>
          <!-- Drive Distribution -->
          <div class="col-lg-5">
              <div class="card border-0 shadow-sm rounded-4 h-100">
                  <div class="card-header bg-white border-0 p-4 pb-0">
                      <h5 class="fw-bold mb-0 d-flex align-items-center gap-2">
                          <i class="fas fa-chart-pie text-info"></i> Drive Distribution
                      </h5>
                  </div>
                  <div class="card-body p-4">
                      <div class="chart-container" style="position: relative; height:300px; width:100%">
                          <canvas id="distributionChart"></canvas>
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

const reportStats = ref([
    { label: 'Total Applications', value: '0', icon: 'fas fa-file-invoice', colorClass: 'bg-primary', textClass: 'text-primary' },
    { label: 'Shortlisted', value: '0', icon: 'fas fa-user-check', colorClass: 'bg-warning', textClass: 'text-warning' },
    { label: 'Hired Candidates', value: '0', icon: 'fas fa-award', colorClass: 'bg-success', textClass: 'text-success' },
    { label: 'Total Drives', value: '0', icon: 'fas fa-briefcase', colorClass: 'bg-info', textClass: 'text-info' }
])

const fetchReportData = async () => {
    try {
        const token = localStorage.getItem('token')
        const res = await axios.get('http://127.0.0.1:5555/api/company/stats', {
            headers: { Authorization: `Bearer ${token}` }
        })
        const stats = res.data
        
        reportStats.value[0].value = stats.total_applications || 0
        reportStats.value[1].value = stats.shortlisted || 0
        reportStats.value[2].value = stats.hired || 0
        reportStats.value[3].value = stats.total_drives || 0
        
        // Initialize charts with real data
        initCharts(stats)
        
    } catch (err) {
        console.error('Error fetching report stats:', err)
    }
}

const initCharts = (stats) => {
    // 1. Funnel Chart (Bar)
    const funnelCtx = document.getElementById('funnelChart').getContext('2d')
    new Chart(funnelCtx, {
        type: 'bar',
        data: {
            labels: ['Applications', 'Shortlisted', 'Hired'],
            datasets: [{
                label: 'Count',
                data: [stats.total_applications, stats.shortlisted, stats.hired],
                backgroundColor: ['#781f19', '#d6a650', '#22c55e'],
                borderRadius: 8,
                barThickness: 45
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { beginAtZero: true, grid: { display: false } },
                x: { grid: { display: false } }
            }
        }
    })

    // 2. Distribution Chart (Doughnut)
    const distCtx = document.getElementById('distributionChart').getContext('2d')
    new Chart(distCtx, {
        type: 'doughnut',
        data: {
            labels: ['Active Drives', 'Closed Drives'],
            datasets: [{
                data: [stats.active_drives, stats.total_drives - stats.active_drives],
                backgroundColor: ['#22c55e', '#e2e8f0'],
                borderWidth: 0,
                cutout: '70%'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom', labels: { usePointStyle: true, padding: 20 } }
            }
        }
    })
}

const exportData = async () => {
    try {
        const token = localStorage.getItem('token')
        const res = await axios.post('http://127.0.0.1:5555/api/company/export-csv', {}, {
            headers: { Authorization: `Bearer ${token}` }
        })
        alert(res.data.message)
    } catch (err) {
        console.error('Error triggering export:', err)
        alert(err.response?.data?.error || 'Failed to trigger export')
    }
}

onMounted(fetchReportData)
</script>

<style scoped>
.icon-box {
    width: 60px;
    height: 60px;
}
.stat-hover {
    transition: all 0.3s ease;
}
.stat-hover:hover {
    transform: translateY(-8px);
    box-shadow: 0 1rem 3rem rgba(0,0,0,0.1) !important;
}

.chart-placeholder {
    border: 3px dashed #f0f0f0;
    border-radius: 2rem;
}

.animate-fade-in {
    animation: fadeIn 0.8s ease-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.btn-outline-primary {
    color: var(--color-primary);
    border-color: var(--color-primary);
}
.btn-outline-primary:hover {
    background-color: var(--color-primary);
    color: white;
}
</style>
