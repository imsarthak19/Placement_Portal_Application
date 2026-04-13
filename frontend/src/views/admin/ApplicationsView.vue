<template>
<DashboardLayout role="admin">
<div class="admin-dashboard">

    <!-- Headings and stuff -->
     <header class="dashboard-header">
        <div class="header-content w-100 d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-4">
            <div>
                <div class="header-tag">MANAGEMENT CONSOLE</div>
                <h1>Application Management</h1>
            </div>
            <Search v-model="searchQuery" placeholder="Search applications by student, company, drive or status..." />
        </div>
    </header>
  
    <!-- Alert Messages -->
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
  
    <!-- Stats Grid -->
    <div class="row g-4 mb-5">
        <div v-for="(stat, key) in statConfig" :key="key" class="col-sm-6 col-xl-4">
            <StatCard 
                :label="stat.label" 
                :value="stats[key] || 0" 
                :icon="stat.icon" 
                :bgClass="stat.bgClass" 
                :textClass="stat.textClass" 
                :change="stat.change" 
                :changeClass="stat.changeClass" 
            />
        </div>
    </div>
  
    <!-- Main Content -->
    <div class="dashboard-content-grid">
        <!-- All Applications Table -->
        <section class="upcoming-drives card my-4">
            <div class="card-header border-0 pb-0">
                <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-4 w-100">
                    <div>
                        <h3 class="mb-1">Recent Applications</h3>
                        <p class="text-muted small mb-0">Total list of all applications submitted.</p>
                    </div>
                </div>
            </div>
                  
            <Table :columns="applicationColumns" :data="paginatedAll">
                <template #row="{ item: app }">
                     
                    <td class="py-3 px-4">
                        <router-link :to="`/admin/student/${app.student_id}`" class="text-decoration-none">
                            <div class="fw-bold text-dark">{{ app.student_name }}</div>
                        </router-link>
                    </td>

                    <td class="py-3 px-3">
                        <div class="fw-medium text-dark"><i class="fas fa-building text-primary me-1 opacity-75"></i> {{ app.company_name }}</div>
                    </td>

                    <td class="py-3 px-3 text-muted">
                        <i class="fas fa-briefcase text-secondary me-1 opacity-75"></i> {{ app.drive_title }}
                    </td>

                    <td class="py-3 px-4 text-center">
                        <span 
                            class="badge px-3 py-2 fw-medium shadow-sm text-capitalize"
                            :class="{
                                'bg-success': app.status === 'offered' || app.status === 'placed',
                                'bg-primary': app.status === 'applied',
                                'bg-warning text-dark': app.status === 'interviewing' || app.status === 'shortlisted',
                                'bg-danger': app.status === 'rejected'
                            }"
                            >
                            {{ app.status }}
                        </span>
                    </td>

                    <td class="py-3 px-4 text-center">
                        <div class="text-muted small">
                            <i class="far fa-calendar-alt me-1"></i> {{ new Date(app.applied_at).toLocaleDateString() }}
                        </div>
                    </td>

                </template>

                <!-- If there is no data to show -->
                <template #empty>
                    <td colspan="5" class="text-center py-5 text-muted">
                        <div class="fs-1 mb-3 opacity-50">📋</div>
                        <h5 class="fw-bold">No applications found matching your criteria.</h5>
                    </td>
                </template>
            </Table>
                  
            <!-- Page All -->
            <div v-if="allTotalPages > 1" class="pagination-controls mt-4">
                <button class="btn-pagination" :disabled="allCurrentPage === 1" @click="allCurrentPage--">
                    <i class="fas fa-chevron-left"></i>
                </button>

                <button v-for="page in allTotalPages" :key="page"
                    :class="['btn-pagination-number', { active: allCurrentPage === page }]"
                    @click="allCurrentPage = page">
                    {{ page }}
                </button>

                <button class="btn-pagination" :disabled="allCurrentPage === allTotalPages" @click="allCurrentPage++">
                    <i class="fas fa-chevron-right"></i>
                </button>
            </div>

        </section>
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

const showFlash = (message) => {
    flashMsg.value = message
    setTimeout(() => {
        flashMsg.value = ""
    }, 2000)
}

const errorMsg = (message) => {
    flashMsgError.value = message
    setTimeout(() => {
        flashMsgError.value = ""
    }, 2000)
}

// Table Columns
const applicationColumns = [
    { key: 'student', label: 'Student', class: 'py-3 px-4 text-secondary fw-semibold text-uppercase' },
    { key: 'company', label: 'Company', class: 'py-3 px-3 text-secondary fw-semibold text-uppercase' },
    { key: 'drive', label: 'Drive', class: 'py-3 px-3 text-secondary fw-semibold text-uppercase' },
    { key: 'status', label: 'Status', class: 'py-3 px-4 text-center text-secondary fw-semibold text-uppercase' },
    { key: 'date', label: 'Applied On', class: 'py-3 px-4 text-center text-secondary fw-semibold text-uppercase' }
]

// Stats Data Computation
const stats = computed(() => ({
    total: applications.value.length,
    placed: applications.value.filter(a => a.status === 'placed' || a.status === 'offered').length,
    pending: applications.value.filter(a => a.status === 'applied' || a.status === 'interviewing' || a.status === 'shortlisted').length,
}))

const statConfig = {
    total: {
        label: 'Total Applications',
        icon: 'fas fa-file-alt',
        bgClass: 'bg-primary-soft border border-primary border-opacity-10',
        textClass: 'text-primary',
    },
    placed: {
        label: 'Offers/Placements',
        icon: 'fas fa-award',
        bgClass: 'bg-success-soft border border-success border-opacity-25',
        textClass: 'text-success',
    },
    pending: {
        label: 'Active Pipeline',
        icon: 'fas fa-spinner',
        bgClass: 'bg-warning-soft border border-warning border-opacity-25',
        textClass: 'text-warning',
    }
}

// -- Fetch applications on mount --
const fetchApplications = async (search = '') => {
    const token = localStorage.getItem("token")

    try {
        const res = await axios.get('http://127.0.0.1:5555/api/admin/all-applications', {
            params: { search },
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        applications.value = res.data
        console.log("APPLICATIONS", res.data)
    } 
    catch (err) {
        console.error("Fetch error:", err)
        errorMsg('Server error. Please try again later.')
    }
}

// Debounced search
let searchTimeout = null
watch(searchQuery, (newVal) => {
    if (searchTimeout) clearTimeout(searchTimeout)
    searchTimeout = setTimeout(() => {
        allCurrentPage.value = 1 // reset to first page on search
        fetchApplications(newVal)
    }, 500)
})

onMounted(() => {
    fetchApplications()
})

// Pagination logic
const itemsPerPage = 8

// All Applications Pagination
const allCurrentPage = ref(1)
const allTotalPages = computed(() => Math.ceil(applications.value.length / itemsPerPage) || 1)
const paginatedAll = computed(() => {
    const start = (allCurrentPage.value - 1) * itemsPerPage
    return applications.value.slice(start, start + itemsPerPage)
})
</script>

<style scoped>
.admin-dashboard {
    max-width: 1200px;
    margin: 0 auto;
}

/* Header */
.dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 32px;
}

.header-tag {
    color: var(--color-primary);
    font-weight: 800;
    font-size: 0.8rem;
    letter-spacing: 1px;
    opacity: 0.7;
}

.header-content h1 {
    font-size: 2rem;
    font-weight: 700;
    color: var(--color-text);
    margin: 0 0 8px 0;
}

.card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    border: 1px solid #f0f0f0;
}

.card-header {
    margin-bottom: 20px;
}

.card-header h3 {
    font-size: 1.25rem;
    margin: 0;
    color: var(--color-text);
}

/* Pagination Styles */
.pagination-controls {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.btn-pagination {
    background: #fff;
    border: 1px solid #e2e8f0;
    color: #64748b;
    width: 32px;
    height: 32px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
}

.btn-pagination:hover:not(:disabled) {
    background: #f1f5f9;
    color: #334155;
}

.btn-pagination:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.btn-pagination-number {
    background: transparent;
    border: none;
    color: #64748b;
    width: 32px;
    height: 32px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-weight: 500;
    transition: all 0.2s ease;
}

.btn-pagination-number:hover {
    background: #f1f5f9;
}

.btn-pagination-number.active {
    background: var(--color-primary);
    color: white;
    font-weight: 600;
}

.bg-primary-soft { background-color: rgba(13, 110, 253, 0.1); }
.bg-warning-soft { background-color: rgba(255, 193, 7, 0.15); }
.bg-success-soft { background-color: rgba(25, 135, 84, 0.1); }

/* Notifications */
.flash-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.flash-msg {
    min-width: 250px;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>
