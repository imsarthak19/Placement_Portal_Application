<template>
<DashboardLayout role="admin">
<div class="admin-dashboard">
    <!-- Page header -->
    <header class="dashboard-header">
        <div class="header-content w-100 d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-4">
            <div>
                <div class="headder-tag">MANAGEMENT CONSOLE</div>
                <h1>Company Management</h1>
            </div>
            <Search v-model="searchQuery" placeholder="Search companies by name, email, industry..." />
        </div>
    </header>

    <!-- Alert Messages -->
    <div class="flash-container">
    <transition name="fade">
        <div 
            v-if="flashMsg" 
            class="alert alert-success flash-msg d-flex align-items-center gap-2 border-0 shadow-sm rounded-3 py-3 px-4" 
            role="alert">
            <i class="fas fa-check-circle"></i>
            <div>{{ flashMsg }}</div>
        </div>
    </transition>
    <transition name="fade">
        <div 
            v-if="flashMsgError" 
            class="alert alert-danger flash-msg d-flex align-items-center gap-2 border-0 shadow-sm rounded-3 py-3 px-4" 
            role="alert">
            
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

        <!-- Unapproved Companies -->
        <section class="upcoming-drives card">
            <div class="card-header">
                <h3>Pending Approvals</h3>
                <p class="text-muted small mb-0">Companies awaiting admin approval.</p>
            </div>

            <Table :columns="companyColumns" :data="paginatedPending">
                <template #row="{ item: company }">
                
                    <td class="py-3 px-4">
                        <router-link :to="`/admin/company/${company.id}`" class="text-decoration-none">
                        <div class="d-flex align-items-center gap-3">
                            <div class="drive-logo">{{ company.icon || '🏢' }}</div>
                            <div>
                                <h6 class="mb-0 fw-bold text-dark">{{ company.name }}</h6>
                            </div>
                        </div>
                    </router-link>
                    </td>
                        
                    <td class="py-3 px-3">
                        <span class="text-muted fw-medium">{{ company.industry || 'Technology' }}</span>
                    </td>

                    <td class="py-3 px-3 text-muted">
                        {{ company.email }}
                        
                    </td>

                    <td class="py-3 px-3 text-center">
                        <span class="status-badge pending rounded-pill">Approval Pending</span>
                    </td>
                        
                    <td class="py-3 px-4 text-center">
                            
                        <button class="btn-action approve-btn" @click="approveCompany(company.id)">
                            <i class="fas fa-check-circle"></i> Approve
                        </button>
                    </td>
                </template>

                <!-- If there is no data to show -->
                <template #empty>
                    <td colspan="5" class="text-center py-5 text-muted">
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

        <!-- All cmpanies Section -->
        <section class="upcoming-drives card my-4">
            <div class="card-header">
                <h3>Active Recruiters</h3>
            </div>

            <Table :columns="companyColumns" :data="paginatedActive">
                <template #row="{ item: company }">

                    <td class="py-3 px-4">
                    <router-link :to="`/admin/company/${company.id}`" class="text-decoration-none">
                        <div class="d-flex align-items-center gap-3">
                            <div class="drive-logo">
                                <img v-if="company.icon" :src="company.icon" alt="Logo" class="img-fluid rounded-3" style="width: 100%; height: 100%; object-fit: contain;">
                                <span v-else>🏢</span>
                            </div>
                            <div>
                                <h6 class="mb-0 fw-bold text-dark hover-primary" style="transition: color 0.2s ease;">{{ company.name }}</h6>
                            </div>
                        </div>
                    </router-link>
                    </td>

                    <td class="py-3 px-3">
                        <span class="text-muted fw-medium">{{ company.industry }}</span>
                    </td>

                    <td class="py-3 px-3 text-muted">{{ company.email }}</td>

                    <td class="py-3 px-3 text-center">
                        <span v-if="!company.blacklisted" class="status-badge rounded-pill approved">
                            Active
                        </span>
                        <span v-else class="status-badge rounded-pill blacklisted">
                            Blacklisted
                        </span>
                    </td>

                    <td class="py-3 px-4 text-center">
                        <router-link :to="`/admin/company/${company.id}`" class="btn-action view-btn text-decoration-none me-2">
                            <i class="fas fa-eye"></i> View
                        </router-link>
                        <button v-if="company.blacklisted" class="btn-action approve-btn" @click="whitelistCompany(company.id)">
                            <i class="fas fa-check-circle"></i> Whitelist
                        </button>
                        <button v-else class="btn-action revoke-btn" @click="revokeCompany(company.id)">
                            <i class="fas fa-times-circle"></i> Blacklist
                        </button>
                    </td>
                </template>

                <template #empty>
                    <td colspan="5" class="text-center py-5 text-muted">
                        <div class="fs-1 mb-3 opacity-50">📋</div>
                        <h5 class="fw-bold">There are no active companies.</h5>
                    </td>
                </template>
                </Table>
                
                <!-- Page Active -->
                <div v-if="activeTotalPages > 1" class="pagination-controls mt-4">
                    <button class="btn-pagination" :disabled="activeCurrentPage === 1" @click="activeCurrentPage--">
                        <i class="fas fa-chevron-left"></i>
                    </button>
                    <button v-for="page in activeTotalPages" :key="page"
                        :class="['btn-pagination-number', { active: activeCurrentPage === page }]"
                        @click="activeCurrentPage = page">
                        {{ page }}
                    </button>
                    <button class="btn-pagination" :disabled="activeCurrentPage === activeTotalPages" @click="activeCurrentPage++">
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

const companyColumns = [
    { key: 'company', label: 'Company', class: 'py-3 px-4 text-secondary fw-semibold text-uppercase' },
    { key: 'industry', label: 'Industry', class: 'py-3 px-3 text-secondary fw-semibold text-uppercase' },
    { key: 'email', label: 'Email', class: 'py-3 px-3 text-secondary fw-semibold text-uppercase' },
    { key: 'status', label: 'Status', class: 'py-3 px-3 text-secondary fw-semibold text-uppercase text-center' },
    { key: 'action', label: 'Action', class: 'py-3 px-4 text-secondary fw-semibold text-uppercase text-center' }
]

const companies = ref([])
const searchQuery = ref('')

const flashMsg = ref('')
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

// -- Stats Data --
const stats = computed(() => ({
    companies: totalCompaniesCount.value,
    approvals: pendingCompaniesCount.value,
    blacklisted: blacklistedCompaniesCount.value
}))

const statConfig = {
    companies: {
        label: 'Total Companies',
        icon: 'fas fa-building',
        bgClass: 'bg-primary-soft border border-primary border-opacity-10',
        textClass: 'text-primary',
    },
    approvals: {
        label: 'Pending Approvals',
        icon: 'fas fa-hourglass-half',
        bgClass: 'bg-warning-soft border border-warning border-opacity-25',
        textClass: 'text-warning',
    },
    blacklisted: {
        label: 'Blocked Companies',
        icon: 'fas fa-user-times',
        bgClass: 'bg-danger-soft border border-danger border-opacity-25',
        textClass: 'text-danger',
    }
}

// -- Fetch companies --
const fetchCompanies = async (search = '') => {
    const token = localStorage.getItem("token")

    try {
        const url = new URL('http://127.0.0.1:5555/api/admin/companies')
        if (search) url.searchParams.append('search', search)

        const res = await fetch(url.toString(), {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        })
        const data = await res.json()
        companies.value = data
        console.log(data)
    } 
    catch (err) {
        errorMsg.value = 'Server error. Please try again later.'
    }
}

// Debounced search
let searchTimeout = null
import { watch } from 'vue'
import router from '@/router'
watch(searchQuery, (newVal) => {
    if (searchTimeout) clearTimeout(searchTimeout)
    searchTimeout = setTimeout(() => {
        pendingCurrentPage.value = 1
        activeCurrentPage.value = 1
        fetchCompanies(newVal)
    }, 500)
})

onMounted(() => {
    fetchCompanies()
})

// Stats computation
const totalCompaniesCount = computed(() => companies.value.length)
const pendingCompanies = computed(() => companies.value.filter(c => !c.approved))
const pendingCompaniesCount = computed(() => pendingCompanies.value.length)
const activeCompanies = computed(() => companies.value.filter(c => c.approved))
const blacklistedCompaniesCount = computed(() => companies.value.filter(c => c.blacklisted).length)

// Pagination logic
const itemsPerPage = 5

// Pending Companies Pagination
const pendingCurrentPage = ref(1)
const pendingTotalPages = computed(() => Math.ceil(pendingCompaniesCount.value / itemsPerPage) || 1)
const paginatedPending = computed(() => {
    const start = (pendingCurrentPage.value - 1) * itemsPerPage
    return pendingCompanies.value.slice(start, start + itemsPerPage)
})

// Active Companies Pagination
const activeCurrentPage = ref(1)
const activeTotalPages = computed(() => Math.ceil(activeCompanies.value.length / itemsPerPage) || 1)
const paginatedActive = computed(() => {
    const start = (activeCurrentPage.value - 1) * itemsPerPage
    return activeCompanies.value.slice(start, start + itemsPerPage)
})

const approveCompany = async (companyId) => {
    flashMsg.value = ''
    try {
        const token = localStorage.getItem("token")

            if (!token) {
                console.error("No token found")
                errorMsg('Authentication error. Please log in again.')
                return
                }

        await axios.put(
            `http://127.0.0.1:5555/api/admin/approve_company/${companyId}`,
            {},
            {
                headers: {
                Authorization: `Bearer ${token}`
                }
            }
        )

        console.log("Approved!")
        showFlash('Company approved successfully.')

        // update UI
        companies.value = companies.value.map(c => {
        if (c.id === companyId) {
            return { ...c, approved: true }
        }
        return c
        })

    } catch (error) {
    console.error("Error:", error.response?.data || error.message)
    errorMsg('Failed to approve company. Please try again.')
  }
}

const revokeCompany = async (companyId) => {
    flashMsg.value = ''
    try {
        const token = localStorage.getItem("token")

            if (!token) {
                console.error("No token found")
                errorMsg('Authentication error. Please log in again.')
                return
                }

        await axios.put(
            `http://127.0.0.1:5555/api/admin/blacklist_company/${companyId}`,
            {},
            {
                headers: {
                Authorization: `Bearer ${token}`
                }
            }
        )

        console.log("Company Blacklisted!")
        showFlash('Company blacklisted successfully.')

        // update UI
        companies.value = companies.value.map(c => {
        if (c.id === companyId) {
            return { ...c, blacklisted: true }
        }
        return c
        })

    } catch (error) {
    console.error("Error:", error.response?.data || error.message)
    errorMsg('Failed to blacklist company. Please try again.')
  }
}

const whitelistCompany = async (companyId) => {
    flashMsg.value = ''
    try {
        const token = localStorage.getItem("token")

            if (!token) {
                console.error("No token found")
                errorMsg('Authentication error. Please log in again.')
                return
                }

        await axios.put(
            `http://127.0.0.1:5555/api/admin/whitelist_company/${companyId}`,
            {},
            {
                headers: {
                Authorization: `Bearer ${token}`
                }
            }
        )

        console.log("Company Whitelisted!")
        showFlash('Company whitelisted successfully.')

        // update UI
        companies.value = companies.value.map(c => {
        if (c.id === companyId) {
            return { ...c, blacklisted: false }
        }
        return c
        })

    } catch (error) {
    console.error("Error:", error.response?.data || error.message)
    errorMsg('Failed to whitelist company. Please try again.')
  }
}

</script>

<style scoped>
.admin-dashboard {
    max-width: 1200px;
    margin: 0 auto;
}

/* Header + Stats */
.dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 32px;
}

.headder-tag{
    color:var(--color-primary);
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

.btn-primary, .approve-btn:hover {
    opacity: 0.9;
    transform: translateY(-1px);
}

@media (max-width: 1024px) {
    .dashboard-content-grid {
        grid-template-columns: 1fr;
    }
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

.btn-text {
    background: none;
    border: none;
    color: var(--color-primary);
    font-weight: 600;
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 4px;
}

.btn-text:hover {
    background: #f8f8f8;
}

/* Tables */

.drive-logo {
    width: 44px;
    height: 44px;
    background: white;
    border: 1px solid #eee;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    color: var(--color-primary);
    font-size: 1.2rem;
    flex-shrink: 0;
    overflow: hidden;
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

.blacklisted{
    background-color: #ffe5e5;
    color: #c53030;
}

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

.btn-action:active {
    transform: translateY(0);
    box-shadow: none;
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

.approved {
    background-color: #d4edda;
    color: #155724;
}

.pending {
    background-color: #f8d7da;
    color: #721c24;
}

.status-badge.open { background: #ecfdf5; color: #059669; }
.status-badge.upcoming { background: #eff6ff; color: #2563eb; }
.status-badge.draft { background: #f3f4f6; color: #4b5563; }

.empty-state {
    text-align: center;
    padding: 40px;
    color: #999;
    font-style: italic;
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

.flash-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;

    display: flex;
    flex-direction: column;
    gap: 10px; /* space between messages */
}

.flash-msg {
    min-width: 250px;
}

/* transition animations */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>