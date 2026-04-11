<template>
  <DashboardLayout role="recruiter">
    <div class="company-dashboard">
      <header class="dashboard-header mb-4">
        <div class="header-content d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-4">
          <div>
            <div class="header-tag">RECRUITER CONSOLE</div>
            <h1>Applications Management</h1>
            <p class="text-muted mb-0">Track and manage all candidate applications across your drives.</p>
          </div>
          <Search v-model="searchQuery" placeholder="Search by student, drive or status..." />
        </div>
      </header>

      <div class="flash-container">
        <transition name="fade">
          <div v-if="flashMsg" class="alert alert-success flash-msg d-flex align-items-center gap-2 border-0 shadow-sm rounded-3 py-3 px-4" role="alert">
            <i class="fas fa-check-circle"></i>
            <div>{{ flashMsg }}</div>
          </div>
        </transition>
        <transition name="fade">
          <div v-if="flashMsgError" class="alert alert-danger flash-msg d-flex align-items-center gap-2 border-0 shadow-sm rounded-3 py-3 px-4" role="alert">
            <i class="fas fa-exclamation-circle"></i>
            <div>{{ flashMsgError }}</div>
          </div>
        </transition>
      </div>

      <div class="row g-4 mb-5">
        <div v-for="(stat, key) in statConfig" :key="key" class="col-sm-6 col-xl-4">
          <StatCard 
            :label="stat.label" 
            :value="stats[key] || 0" 
            :icon="stat.icon" 
            :bgClass="stat.bgClass" 
            :textClass="stat.textClass" 
          />
        </div>
      </div>

      <div class="card shadow-sm border-0 rounded-4 overflow-hidden mb-4">
        <div class="card-header border-0 bg-white py-4 px-4">
          <div class="d-flex justify-content-between align-items-center">
            <h5 class="fw-bold mb-0">Applications</h5>
            <span class="badge bg-primary bg-opacity-10 text-primary border border-primary border-opacity-10 px-3 py-2 rounded-pill fw-semibold">{{ filteredApplications.length }} Total</span>
          </div>
        </div>
        
        <Table :columns="applicationColumns" :data="paginatedApplications">
          <template #row="{ item: app }">
            <td class="py-3 px-4">
              <router-link :to="`/company/student/${app.student_id}`" class="text-decoration-none">
                <div class="fw-bold text-dark hover-primary">{{ app.student_name }}</div>
                <small class="text-muted">{{ app.roll_number }}</small>
              </router-link>
            </td>
            <td class="py-3 px-3">
              <router-link :to="`/company/drive/${app.drive_id}`" class="text-decoration-none">
                <div class="fw-medium text-dark hover-primary">
                  <i class="fas fa-briefcase text-secondary me-1 opacity-75"></i> {{ app.drive_title }}
                </div>
              </router-link>
            </td>
            <td class="py-3 px-3">
              <span class="badge bg-light text-dark border px-2 py-1 fw-medium">{{ app.branch }}</span>
            </td>
            <td class="py-3 px-3 text-center fw-bold text-success">{{ app.cgpa }}</td>
            <td class="py-3 px-3 text-center">
              <span 
                class="badge rounded-pill px-3 py-2 fw-medium shadow-sm text-capitalize border"
                :class="{
                  'bg-success bg-opacity-10 text-success border-success border-opacity-25': ['offered', 'placed', 'hired', 'selected'].includes(app.status.toLowerCase()),
                  'bg-info bg-opacity-10 text-info border-info border-opacity-25': app.status.toLowerCase() === 'applied',
                  'bg-warning bg-opacity-10 text-warning border-warning border-opacity-25': app.status.toLowerCase() === 'shortlisted',
                  'bg-primary bg-opacity-10 text-primary border-primary border-opacity-25': app.status.toLowerCase() === 'interviewing',
                  'bg-danger bg-opacity-10 text-danger border-danger border-opacity-25': app.status.toLowerCase() === 'rejected'
                }"
              >
                {{ app.status }}
              </span>
            </td>
            <td class="py-3 px-4 text-center">
              <div v-if="app.status === 'applied'" class="d-flex justify-content-center gap-2">
                <button class="btn btn-sm btn-outline-success rounded-pill px-3" @click="handleStatusUpdate(app.id, 'shortlisted')" title="Shortlist">
                  <i class="fas fa-user-check"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger rounded-pill px-3" @click="openRejectModal(app)" title="Reject">
                  <i class="fas fa-user-times"></i>
                </button>
              </div>
              <div v-else class="text-muted small">
                 <i class="fas fa-info-circle me-1"></i> Already processed
              </div>
            </td>
          </template>
          <template #empty>
            <td colspan="6" class="text-center py-5 text-muted">
              <div class="fs-1 mb-3 opacity-50">📋</div>
              <h5 class="fw-bold">No applications found.</h5>
              <p class="mb-0">Candidate applications for your drives will appear here.</p>
            </td>
          </template>
        </Table>

        <div v-if="totalPages > 1" class="card-footer bg-white border-0 py-4">
          <div class="pagination-controls">
            <button class="btn-pagination" :disabled="currentPage === 1" @click="currentPage--">
              <i class="fas fa-chevron-left"></i>
            </button>
            <button v-for="page in totalPages" :key="page"
              :class="['btn-pagination-number', { active: currentPage === page }]"
              @click="currentPage = page">
              {{ page }}
            </button>
            <button class="btn-pagination" :disabled="currentPage === totalPages" @click="currentPage++">
              <i class="fas fa-chevron-right"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Reject Modal -->
    <div v-if="showRejectModal" class="modal-backdrop fade show" @click="closeRejectModal"></div>
    <div v-if="showRejectModal" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg rounded-4">
          <div class="modal-header border-0 pb-0">
            <h5 class="modal-title fw-bold">Reject Application</h5>
            <button type="button" class="btn-close" @click="closeRejectModal"></button>
          </div>
          <div class="modal-body py-4">
            <p class="text-muted border-start border-4 border-danger ps-3">
              Are you sure you want to reject <strong>{{ selectedApp?.student_name }}</strong>? This action cannot be undone.
            </p>
            <div class="mt-4">
              <label class="form-label small fw-bold text-uppercase opacity-75">Reason for Rejection (Optional)</label>
              <textarea v-model="rejectComment" class="form-control rounded-3" rows="3" placeholder="Explain why the candidate is being rejected..."></textarea>
            </div>
          </div>
          <div class="modal-footer border-0 pt-0">
            <button type="button" class="btn btn-light rounded-pill px-4" @click="closeRejectModal">Cancel</button>
            <button type="button" class="btn btn-danger rounded-pill px-4" @click="submitRejection" :disabled="updating">
               <i v-if="updating" class="fas fa-spinner fa-spin me-2"></i> Confirm Rejection
            </button>
          </div>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import axios from "axios"
import DashboardLayout from '@/components/sidebar/DashboardLayout.vue'
import Table from '@/components/ui/Table.vue'
import StatCard from '@/components/ui/StatCard.vue'
import Search from '@/components/ui/Search.vue'

const applications = ref([])
const searchQuery = ref('')
const flashMsg = ref('')
const flashMsgError = ref('')
const currentPage = ref(1)
const itemsPerPage = 8
const updating = ref(false)

const showRejectModal = ref(false)
const selectedApp = ref(null)
const rejectComment = ref('')

const applicationColumns = [
  { key: 'student', label: 'Candidate', class: 'py-3 px-4 text-secondary fw-semibold text-uppercase' },
  { key: 'drive', label: 'Drive', class: 'py-3 px-3 text-secondary fw-semibold text-uppercase' },
  { key: 'branch', label: 'Branch', class: 'py-3 px-3 text-secondary fw-semibold text-uppercase' },
  { key: 'cgpa', label: 'CGPA', class: 'py-3 px-3 text-center text-secondary fw-semibold text-uppercase' },
  { key: 'status', label: 'Status', class: 'py-3 px-3 text-center text-secondary fw-semibold text-uppercase' },
  { key: 'actions', label: 'Actions', class: 'py-3 px-4 text-center text-secondary fw-semibold text-uppercase' }
]

const stats = computed(() => ({
  total: applications.value.length,
  hired: applications.value.filter(a => ['hired', 'placed', 'offered', 'selected'].includes(a.status.toLowerCase())).length,
  active: applications.value.filter(a => ['applied', 'interviewing', 'shortlisted'].includes(a.status.toLowerCase())).length
}))

const statConfig = {
  total: {
    label: 'Total Applicants',
    icon: 'fas fa-users',
    bgClass: 'bg-primary-soft border border-primary border-opacity-10',
    textClass: 'text-primary'
  },
  hired: {
    label: 'Selected/Hired',
    icon: 'fas fa-check-double',
    bgClass: 'bg-success-soft border border-success border-opacity-25',
    textClass: 'text-success'
  },
  active: {
    label: 'Active Pipeline',
    icon: 'fas fa-spinner',
    bgClass: 'bg-warning-soft border border-warning border-opacity-25',
    textClass: 'text-warning'
  }
}

const filteredApplications = computed(() => {
  if (!searchQuery.value) return applications.value
  const q = searchQuery.value.toLowerCase()
  return applications.value.filter(app => 
    app.student_name.toLowerCase().includes(q) || 
    app.drive_title.toLowerCase().includes(q) || 
    app.status.toLowerCase().includes(q) ||
    app.roll_number.toLowerCase().includes(q) ||
    app.branch.toLowerCase().includes(q)
  )
})

const totalPages = computed(() => Math.ceil(filteredApplications.value.length / itemsPerPage) || 1)
const paginatedApplications = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return filteredApplications.value.slice(start, start + itemsPerPage)
})

const fetchApplications = async () => {
  const token = localStorage.getItem("token")
  try {
    const res = await axios.get('http://127.0.0.1:5555/api/company/all-applications', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    applications.value = res.data
  } catch (err) {
    console.error("Fetch Applications Error:", err)
    flashMsgError.value = "Failed to load applications."
  }
}

const handleStatusUpdate = async (appId, status, comment = null) => {
  updating.value = true
  const token = localStorage.getItem("token")
  try {
    await axios.post(`http://127.0.0.1:5555/api/company/update-application-status/${appId}`, {
      status,
      comment
    }, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    
    flashMsg.value = `Candidate successfully ${status}!`
    setTimeout(() => { flashMsg.value = "" }, 2500)
    await fetchApplications()
  } catch (err) {
    console.error("Status Update Error:", err)
    flashMsgError.value = err.response?.data?.error || "Failed to update status."
    setTimeout(() => { flashMsgError.value = "" }, 2500)
  } finally {
    updating.value = false
  }
}

const openRejectModal = (app) => {
  selectedApp.value = app
  rejectComment.value = ''
  showRejectModal.value = true
}

const closeRejectModal = () => {
  showRejectModal.value = false
  selectedApp.value = null
  rejectComment.value = ''
}

const submitRejection = async () => {
  if (!selectedApp.value) return
  await handleStatusUpdate(selectedApp.value.id, 'rejected', rejectComment.value)
  closeRejectModal()
}

onMounted(fetchApplications)

watch(searchQuery, () => {
  currentPage.value = 1
})

const formatDate = (isoString) => {
  if (!isoString) return 'N/A'
  const date = new Date(isoString)
  return date.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}
</script>

<style scoped>
.company-dashboard { max-width: 1200px; margin: 0 auto; }
.header-tag { color: var(--color-primary); font-weight: 800; font-size: 0.8rem; letter-spacing: 1px; opacity: 0.7; }
.hover-primary:hover { color: var(--color-primary) !important; }
.bg-primary-soft { background-color: rgba(13, 110, 253, 0.1); }
.bg-warning-soft { background-color: rgba(255, 193, 7, 0.15); }
.bg-success-soft { background-color: rgba(25, 135, 84, 0.1); }

.pagination-controls { display: flex; align-items: center; justify-content: center; gap: 8px; }
.btn-pagination { background: #fff; border: 1px solid #e2e8f0; color: #64748b; width: 32px; height: 32px; border-radius: 6px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s ease; }
.btn-pagination:hover:not(:disabled) { background: #f1f5f9; color: #334155; }
.btn-pagination:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-pagination-number { background: transparent; border: none; color: #64748b; width: 32px; height: 32px; border-radius: 6px; display: flex; align-items: center; justify-content: center; cursor: pointer; font-weight: 500; transition: all 0.2s ease; }
.btn-pagination-number.active { background: var(--color-primary); color: white; font-weight: 600; }

.flash-container { position: fixed; top: 20px; right: 20px; z-index: 9999; display: flex; flex-direction: column; gap: 10px; }
.flash-msg { min-width: 250px; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
