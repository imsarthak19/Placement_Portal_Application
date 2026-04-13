<template>
<DashboardLayout role="student">
    <div class="my-applications">
        <header class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-4 mb-5">
            <div>
                <h1 class="h2 fw-bold text-dark mb-1">My Applications</h1>
                <p class="text-muted mb-0">Track the status of your placement applications.</p>
            </div>
            <div class="d-flex align-items-center gap-2">
                <Search v-model="searchQuery" placeholder="Search applications..." />
                <button @click="exportHistory" class="btn btn-outline-primary rounded-pill px-4 fw-bold shadow-sm d-none d-md-flex align-items-center gap-2" style="white-space: nowrap;">
                    <i class="fas fa-file-export"></i> Export History
                </button>
            </div>
        </header>

        <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>

        <div v-else-if="filteredApplications.length === 0" class="card border-0 shadow-sm rounded-4 py-5 text-center bg-white">
            <div class="card-body">
                <div class="display-1 mb-4 opacity-25">📄</div>
                <h3 class="fw-bold text-dark">No applications yet</h3>
                <p class="text-muted mx-auto mb-4" style="max-width: 400px;">You haven't applied to any drives yet. Exploration awaits!</p>
                <router-link to="/student/drives" class="btn btn-primary rounded-pill px-4">
                    Explore Available Drives
                </router-link>
            </div>
        </div>

        <div v-else class="row g-4">
            <div v-for="app in filteredApplications" :key="app.id" class="col-12">
                <div class="card application-card border-0 shadow-sm rounded-4 overflow-hidden position-relative">
                    <div class="card-body p-0">
                        <div class="row g-0">
                            <!-- Left Section: Company & Status -->
                            <div class="col-md-4 p-4 border-end bg-light-subtle">
                                <div class="d-flex align-items-center gap-3 mb-4">
                                    <div class="company-logo bg-white rounded-3 d-flex align-items-center justify-content-center p-2 border shadow-xs">
                                        <img v-if="app.company_logo" :src="app.company_logo" :alt="app.company_name" class="img-fluid rounded-2">
                                        <i v-else class="fas fa-building text-secondary opacity-50 fs-4"></i>
                                    </div>
                                    <div>
                                        <h6 class="text-primary fw-bold mb-0">{{ app.company_name }}</h6>
                                        <div class="text-muted small d-flex align-items-center gap-1">
                                            <i class="fas fa-map-marker-alt"></i> {{ app.location }}
                                        </div>
                                    </div>
                                </div>

                                <div class="status-indicator">
                                    <label class="text-muted small fw-bold text-uppercase mb-2 d-block opacity-75">Current Status</label>
                                    <span class="badge rounded-pill px-4 py-2 fs-6 shadow-xs border d-inline-flex align-items-center gap-2"
                                          :class="statusClasses(app.status)">
                                        <i class="fas fa-circle" style="font-size: 0.5rem;"></i>
                                        {{ formatStatus(app.status) }}
                                    </span>
                                </div>
                            </div>

                            <!-- Right Section: Details & Notes -->
                            <div class="col-md-8 p-4 d-flex flex-column justify-content-between">
                                <div>
                                    <div class="d-flex justify-content-between align-items-start mb-3">
                                        <h5 class="fw-bold text-dark mb-0">{{ app.drive_title }}</h5>
                                        <div class="text-muted small">
                                            <i class="far fa-calendar-alt me-1"></i> Applied: {{ formatDate(app.applied_at) }}
                                        </div>
                                    </div>

                                    <div class="d-flex gap-4 mb-4">
                                        <div class="info-pill">
                                            <i class="fas fa-users-cog text-primary"></i>
                                            <span><strong>{{ app.interviews_scheduled }}</strong> Interviews Scheduled</span>
                                        </div>
                                    </div>

                                    <!-- Rejection Message / Notes -->
                                    <div v-if="app.status.toLowerCase() === 'rejected' || app.comment" 
                                         class="notes-wrapper p-3 rounded-3 border-start border-4"
                                         :class="app.status.toLowerCase() === 'rejected' ? 'bg-danger-subtle border-danger' : 'bg-primary-subtle border-primary'">
                                        <div class="d-flex align-items-center gap-2 mb-2">
                                            <i class="fas" :class="app.status.toLowerCase() === 'rejected' ? 'fa-exclamation-triangle text-danger' : 'fa-info-circle text-primary'"></i>
                                            <span class="fw-bold small text-uppercase">
                                                {{ app.status.toLowerCase() === 'rejected' ? 'Rejection Feedback' : 'Recruiter Note' }}
                                            </span>
                                        </div>
                                        <p class="mb-0 text-dark small fst-italic">
                                            {{ app.comment || 'No feedback provided by the recruiter.' }}
                                        </p>
                                    </div>
                                    <div v-else-if="app.status.toLowerCase() === 'interviewing'" class="text-muted small p-3 bg-primary-subtle rounded-3 d-flex align-items-center gap-2 border-start border-4 border-primary">
                                        <i class="fas fa-calendar-check text-primary"></i>
                                        An interview has been scheduled.
                                    </div>
                                    <div v-else class="text-muted small p-3 bg-light rounded-3 d-flex align-items-center gap-2">
                                        <i class="fas fa-history"></i>
                                        Your application is currently under review.
                                    </div>
                                </div>

                                <div class="mt-4 pt-3 border-top d-flex justify-content-end align-items-center">
                                    <router-link 
                                        v-if="app.status.toLowerCase() === 'offered' || app.status.toLowerCase() === 'hired'"
                                        :to="`/student/offer-letter/${app.id}`"
                                        class="btn btn-success btn-sm rounded-pill px-4 fw-bold me-3 shadow-sm border-0"
                                    >
                                        <i class="fas fa-file-signature me-1"></i> Show Offer Letter
                                    </router-link>
                                    <router-link :to="`/student/drive/${app.drive_id}`" class="btn btn-outline-primary btn-sm rounded-pill px-4 fw-bold">
                                        View Drive Details
                                    </router-link>
                                </div>
                            </div>
                        </div>
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
import Search from '@/components/ui/Search.vue'

const applications = ref([])
const loading = ref(true)
const searchQuery = ref('')

const user = JSON.parse(localStorage.getItem('user') || '{}')
const userName = user.name || 'Student'

const fetchApplications = async () => {
    loading.value = true
    try {
        const token = localStorage.getItem('token')
        const res = await axios.get('http://127.0.0.1:5555/api/student/applications', {
            headers: { Authorization: `Bearer ${token}` }
        })
        applications.value = res.data
    } catch (err) {
        console.error('Error fetching applications:', err)
    } finally {
        loading.value = false
    }
}

const filteredApplications = computed(() => {
    if (!searchQuery.value) return applications.value
    const q = searchQuery.value.toLowerCase()
    return applications.value.filter(app => 
        app.drive_title.toLowerCase().includes(q) || 
        app.company_name.toLowerCase().includes(q) ||
        app.status.toLowerCase().includes(q)
    )
})

const statusClasses = (status) => {
    const s = status.toLowerCase()
    if (['hired', 'placed', 'offered', 'selected'].includes(s)) return 'bg-success bg-opacity-10 text-success border-success border-opacity-25'
    if (s === 'rejected') return 'bg-danger bg-opacity-10 text-danger border-danger border-opacity-25'
    if (s === 'shortlisted' || s === 'interviewing') return 'bg-primary bg-opacity-10 text-primary border-primary border-opacity-25'
    return 'bg-secondary bg-opacity-10 text-secondary border-secondary border-opacity-25'
}

const formatStatus = (status) => {
    return status.charAt(0).toUpperCase() + status.slice(1)
}

const formatDate = (dateStr) => {
    if (!dateStr) return 'N/A'
    const date = new Date(dateStr)
    return date.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}

const exportHistory = async () => {
    try {
        const token = localStorage.getItem('token')
        const res = await axios.post('http://127.0.0.1:5555/api/student/export-csv', {}, {
            headers: { Authorization: `Bearer ${token}` }
        })
        alert(res.data.message)
    } catch (err) {
        console.error('Error exporting history:', err)
        alert('Failed to trigger export.')
    }
}

onMounted(fetchApplications)
</script>

<style scoped>
.application-card {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.application-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px -8px rgba(0, 0, 0, 0.1) !important;
}

.company-logo {
    width: 64px;
    height: 64px;
}

.shadow-xs {
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.info-pill {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.9rem;
    color: var(--bs-gray-700);
}

.notes-wrapper {
    animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.search-wrapper {
    min-width: 320px;
}
</style>
