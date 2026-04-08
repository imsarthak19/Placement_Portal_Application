<template>
<DashboardLayout role="admin">
    <div class="admin-dashboard">
        <header class="dashboard-header">
            <div class="header-content w-100 d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-4">
                <div>
                    <div class="header-tag">MANAGEMENT CONSOLE</div>
                    <h1>Drive Management</h1>
                </div>
                <Search v-model="searchQuery" placeholder="Search drives by title, company, location..." />
            </div>
            <div class="header-actions">
                <!-- <button class="btn-primary">
                    <i class="fas fa-download"></i>Export List</button> -->
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
  
        <div class="dashboard-content-grid">
            <section class="upcoming-drives card">
                <div class="card-header">
                    <h3>Pending Approvals</h3>
                    <p class="text-muted small mb-0">Drives awaiting admin approval.</p>
                </div>
                  
                <Table :columns="driveColumns" :data="paginatedPending">
                    <template #row="{ item: drive }">

                        <td class="py-3 px-4">
                            <router-link :to="`/admin/drive/${drive.id}`" class="text-decoration-none">
                                <div class="fw-bold text-dark hover-primary" style="transition: color 0.2s ease;">{{ drive.title }}</div>
                            </router-link>
                        </td>

                        <td class="py-3 px-3">
                            <div class="fw-medium text-dark"><i class="fas fa-building text-primary me-1 opacity-75"></i> {{ drive.company_name }}</div>
                        </td>

                        <td class="py-3 px-3 text-muted">
                            <i class="fas fa-map-marker-alt text-secondary me-1 opacity-75"></i> {{ drive.location }}
                        </td>

                        <td class="py-3 px-3">
                            <span class="badge bg-light text-dark border border-secondary border-opacity-25 px-2 py-1 d-inline-flex align-items-center gap-1">
                                <i class="fas" :class="drive.workMode === 'Remote' ? 'fa-home' : (drive.workMode === 'Hybrid' ? 'fa-sync-alt' : 'fa-building')"></i> {{ drive.workMode }}
                              </span>
                        </td>

                        <td class="py-3 px-3 text-success fw-bold">{{ drive.payScale }}</td>

                        <td class="py-3 px-3 text-dark fw-medium text-center">{{ drive.positions }}</td>

                        <td class="py-3 px-4 text-center">
                            <span class="status-badge pending">Pending</span>
                        </td>

                        <td class="py-3 px-4 text-center">
                            <router-link :to="`/admin/drive/${drive.id}`" class="btn-action mb-1 view-btn text-decoration-none me-2">
                                <i class="fas fa-eye"></i> View
                            </router-link>
                            <button class="btn-action approve-btn" @click="approveDrive(drive.id)">
                                <i class="fas fa-check-circle"></i> Approve
                            </button>
                        </td>
                    </template>

                    <template #empty>

                        <td colspan="8" class="text-center py-5 text-muted">
                            <div class="fs-1 mb-3 opacity-50">📋</div>
                            <h5 class="fw-bold">Approval queue is empty.</h5>
                        </td>

                    </template>
                </Table>
                  
                <!-- Page Pending -->
                <div v-if="pendingTotalPages > 1" class="pagination-controls mt-4">
                    <button class="btn-pagination" :disabled="pendingCurrentPage === 1" @click="pendingCurrentPage--">
                        <i class="fas fa-chevron-left"></i>
                    </button>
                    <button v-for="page in pendingTotalPages" :key="page"
                            :class="['btn-pagination-number', { active: pendingCurrentPage === page }]"
                            @click="pendingCurrentPage = page">
                        {{ page }}
                    </button>
                    <button class="btn-pagination" :disabled="pendingCurrentPage === pendingTotalPages" @click="pendingCurrentPage++">
                        <i class="fas fa-chevron-right"></i>
                    </button>
                </div>
            </section>
  
            <section class="upcoming-drives card my-4">
                <div class="card-header">
                    <h3>All Drives</h3>
                    <p class="text-muted small mb-0">Complete list of registered hiring drives.</p>
                </div>
                  
                <Table :columns="allDriveColumns" :data="paginatedAll">
                    <template #row="{ item: drive }">
                        <td class="py-3 px-4">
                            <router-link :to="`/admin/drive/${drive.id}`" class="text-decoration-none">
                                <div class="fw-bold text-dark hover-primary" style="transition: color 0.2s ease;">{{ drive.title }}</div>
                            </router-link>
                        </td>

                        <td class="py-3 px-3">
                            <div class="fw-medium text-dark"><i class="fas fa-building text-primary me-1 opacity-75"></i> {{ drive.company_name }}</div>
                        </td>

                        <td class="py-3 px-3 text-muted">
                            <i class="fas fa-map-marker-alt text-secondary me-1 opacity-75"></i> {{ drive.location }}
                        </td>

                        <td class="py-3 px-3">
                            <span class="badge bg-light text-dark border border-secondary border-opacity-25 px-2 py-1 d-inline-flex align-items-center gap-1">
                                <i class="fas" :class="drive.workMode === 'Remote' ? 'fa-home' : (drive.workMode === 'Hybrid' ? 'fa-sync-alt' : 'fa-building')"></i> {{ drive.workMode }}
                            </span>
                        </td>

                        <td class="py-3 px-4 text-center">
                            <span class="badge px-3 py-2 fw-medium shadow-sm"
                                :class="{
                                    'bg-success': drive.status === 'Active',
                                    'bg-secondary': drive.status === 'Closed',
                                    'bg-warning text-dark': drive.status === 'Unapproved' || drive.status === 'uapproved',
                                    'bg-danger': drive.status === 'Rejected',
                                    'bg-info text-dark': drive.status === 'Hired'
                                }">
                                {{ drive.status === 'uapproved' ? 'Unapproved' : drive.status }}
                            </span>
                        </td>

                        <td class="py-3 px-4 text-center">
                            <router-link :to="`/admin/drive/${drive.id}`" class="btn-action view-btn text-decoration-none me-2">
                                <i class="fas fa-eye"></i> View
                            </router-link>
                            <button v-if="drive.status === 'Active'" class="btn-action revoke-btn"@click="rejectDrive(drive.id)">
                                <i class="fas fa-times-circle"></i> Reject
                            </button>
                            <button v-else-if="drive.status === 'Rejected'" class="btn-action approve-btn" @click="approveDrive(drive.id)">
                                <i class="fas fa-check-circle"></i> Approve
                            </button>
                        </td>
                    </template>

                    <template #empty>
                        <td colspan="7" class="text-center py-5 text-muted">
                            <div class="fs-1 mb-3 opacity-50">📋</div>
                            <h5 class="fw-bold">No drives available.</h5>
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
import { ref, onMounted, computed } from 'vue'
import axios from "axios"
import DashboardLayout from '@/components/sidebar/DashboardLayout.vue'
import Table from '@/components/ui/Table.vue'
import StatCard from '@/components/ui/StatCard.vue'
import Search from '@/components/ui/Search.vue'

const drives = ref([])
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

const driveColumns = [
    { key: 'title', label: 'Title', class: 'py-3 px-4 text-secondary fw-semibold text-uppercase' },
    { key: 'company', label: 'Company', class: 'py-3 px-3 text-secondary fw-semibold text-uppercase' },
    { key: 'location', label: 'Location' },
    { key: 'workMode', label: 'Work Mode' },
    { key: 'payScale', label: 'Payscale' },
    { key: 'positions', label: 'Positions', class: 'py-3 px-3 text-secondary fw-semibold text-uppercase text-center' },
    { key: 'status', label: 'Status', class: 'py-3 px-4 text-secondary fw-semibold text-uppercase text-center' },
    { key: 'action', label: 'Action', class: 'py-3 px-4 text-secondary fw-semibold text-uppercase text-center' }
]

const allDriveColumns = [
    { key: 'title', label: 'Title', class: 'py-3 px-4 text-secondary fw-semibold text-uppercase' },
    { key: 'company', label: 'Company', class: 'py-3 px-3 text-secondary fw-semibold text-uppercase' },
    { key: 'location', label: 'Location' },
    { key: 'workMode', label: 'Work Mode' },
    { key: 'status', label: 'Status', class: 'py-3 px-4 text-secondary fw-semibold text-uppercase text-center' },
    { key: 'action', label: 'Action', class: 'py-3 px-4 text-secondary fw-semibold text-uppercase text-center' }
]

// -- Stats Data --
const stats = computed(() => ({
    total: totalDrivesCount.value,
    approvals: pendingDrivesCount.value,
    active: activeDrivesCount.value
}))

const statConfig = {
    total: {
        label: 'Total Drives',
        icon: 'fas fa-briefcase',
        bgClass: 'bg-primary-soft border border-primary border-opacity-10',
        textClass: 'text-primary',
    },
    approvals: {
        label: 'Pending Approvals',
        icon: 'fas fa-hourglass-half',
        bgClass: 'bg-warning-soft border border-warning border-opacity-25',
        textClass: 'text-warning',
    },
    active: {
        label: 'Active Drives',
        icon: 'fas fa-check-circle',
        bgClass: 'bg-success-soft border border-success border-opacity-25',
        textClass: 'text-success',
    }
}

// -- Fetch drives --
const fetchDrives = async (search = '') => {
    const token = localStorage.getItem("token")

    try {
        const url = new URL('http://127.0.0.1:5555/api/admin/all-drives')
        if (search) url.searchParams.append('search', search)

        const res = await fetch(url.toString(), {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        })
        if (!res.ok) throw new Error("Failed to fetch")
        const data = await res.json()
        drives.value = data
        console.log("DRIVES", data)
    } 
    catch (err) {
        errorMsg('Server error. Please try again later.')
    }
}

// Debounced search
let searchTimeout = null
import { watch } from 'vue'
watch(searchQuery, (newVal) => {
    if (searchTimeout) clearTimeout(searchTimeout)
    searchTimeout = setTimeout(() => {
        pendingCurrentPage.value = 1
        allCurrentPage.value = 1
        fetchDrives(newVal)
    }, 500)
})

onMounted(() => {
    fetchDrives()
})

// Stats computation
const totalDrivesCount = computed(() => drives.value.length)
const pendingDrives = computed(() => drives.value.filter(d => d.status === 'uapproved' || d.status === 'Unapproved'))
const pendingDrivesCount = computed(() => pendingDrives.value.length)
const activeDrivesCount = computed(() => drives.value.filter(d => d.status === 'Active').length)

// Pagination logic
const itemsPerPage = 5

// Pending Drives Pagination
const pendingCurrentPage = ref(1)
const pendingTotalPages = computed(() => Math.ceil(pendingDrivesCount.value / itemsPerPage) || 1)
const paginatedPending = computed(() => {
    const start = (pendingCurrentPage.value - 1) * itemsPerPage
    return pendingDrives.value.slice(start, start + itemsPerPage)
})

// All Drives Pagination
const allCurrentPage = ref(1)
const allTotalPages = computed(() => Math.ceil(drives.value.length / itemsPerPage) || 1)
const paginatedAll = computed(() => {
    const start = (allCurrentPage.value - 1) * itemsPerPage
    return drives.value.slice(start, start + itemsPerPage)
})

const approveDrive = async (driveId) => {
    flashMsg.value = ''
    try {
        const token = localStorage.getItem("token")

        if (!token) {
            errorMsg('Authentication error. Please log in again.')
            return
        }

        await axios.put(
            `http://127.0.0.1:5555/api/admin/approve_drive/${driveId}`,
            {},
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        )

        showFlash('Drive approved successfully.')

        // update UI
        drives.value = drives.value.map(d => {
            if (d.id === driveId) return { ...d, status: 'Active' }
            return d
        })

    } catch (error) {
        errorMsg('Failed to approve drive. Please try again.')
    }
}

const rejectDrive = async (driveId) => {
    flashMsg.value = ''
    try {
        const token = localStorage.getItem("token")

        if (!token) {
            errorMsg('Authentication error. Please log in again.')
            return
        }

        await axios.put(
            `http://127.0.0.1:5555/api/admin/reject_drive/${driveId}`,
            {},
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        )

        showFlash('Drive rejected successfully.')

        // update UI
        drives.value = drives.value.map(d => {
            if (d.id === driveId) return { ...d, status: 'Rejected' }
            return d
        })

    } catch (error) {
        errorMsg('Failed to reject drive. Please try again.')
    }
}
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

.btn-primary {
    background-color: var(--color-primary);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}

.btn-primary:hover, .approve-btn:hover {
    opacity: 0.9;
    transform: translateY(-1px);
}

.card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    border: 1px solid #f0f0f0;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.card-header h3 {
    font-size: 1.25rem;
    margin: 0;
    color: var(--color-text);
}

/* Buttons */
.btn-action {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    height: 36px;
    padding: 0 16px;
    border-radius: 8px;
    font-size: 0.85rem;
    font-weight: 600;
    border: 1px solid transparent;
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.approve-btn {
    background-color: #10b981;
    color: #ffffff;
    border-color: #10b981;
}

.approve-btn:hover {
    background-color: #059669;
    border-color: #059669;
    transform: translateY(-1px);
    box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.4), 0 2px 4px -1px rgba(16, 185, 129, 0.2);
}

.revoke-btn {
    background-color: #ef4444;
    color: #ffffff;
    border-color: #ef4444;
}

.revoke-btn:hover {
    background-color: #dc2626;
    border-color: #dc2626;
    transform: translateY(-1px);
    box-shadow: 0 4px 6px -1px rgba(239, 68, 68, 0.4), 0 2px 4px -1px rgba(239, 68, 68, 0.2);
}

.view-btn {
    background-color: #3b82f6;
    color: #ffffff;
    border-color: #3b82f6;
}

.view-btn:hover {
    background-color: #2563eb;
    border-color: #2563eb;
    transform: translateY(-1px);
    box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.4), 0 2px 4px -1px rgba(59, 130, 246, 0.2);
}

.hover-primary:hover {
    color: var(--color-primary) !important;
}

.btn-action:active {
    transform: translateY(0);
    box-shadow: none;
}

.status-badge {
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    white-space: nowrap;
}

.pending {
    background-color: #f8d7da;
    color: #721c24;
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