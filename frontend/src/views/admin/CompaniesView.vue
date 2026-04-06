<template>
<DashboardLayout role="admin">
    <div class="admin-dashboard">
        <header class="dashboard-header">
            <div class="header-content">
                <div class="headder-tag">
                    MANAGEMENT CONSOLE
                </div>
                <h1>Company Management</h1>
            </div>
            <div class="header-actions">
                <button class="btn-primary">
                    <i class="fas fa-download"></i>
                    Export List
                </button>
            </div>
        </header>

        <!-- Stats Grid -->
        <div class="row g-4 mb-5">
            <div v-for="(stat, key) in statConfig" :key="key" class="col-sm-6 col-xl-4">
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

        <div class="dashboard-content-grid">
            <section class="upcoming-drives card">
                <div class="card-header">
                    <h3>Pending Approvals</h3>
                    <p class="text-muted small mb-0">Companies awaiting admin approval.</p>
                </div>
                <div class="table-head">
                    <span>COMPANY</span>
                    <span>INDUSTRY</span>
                    <span>EMAIL</span>
                    <span>STATUS</span>
                    <span>ACTION</span>
                </div>
                <div class="drive-list">
                    <div v-if="pendingCompanies.length === 0" class="empty-state">
                        Approval queue is empty.
                    </div>
                    <div v-for="company in paginatedPending" :key="company.id" class="drive-item">
                        <div class="company-col d-flex align-items-center gap-3">
                            <div class="drive-logo">
                                {{ company.icon || '🏢' }}
                            </div>
                            <div class="drive-details">
                                <h4>{{ company.name }}</h4>
                            </div>
                        </div>
                        <div class="industry-col">
                            <span class="text-muted small fw-medium">{{ company.industry || 'Technology' }}</span>
                        </div>
                        <div class="email-col">
                            <span class="text-muted small">{{ company.email }}</span>
                        </div>
                        <div class="status-col">
                            <span class="status-badge pending">Approval Pending</span>
                        </div>
                        <div class="action-col">
                            <button class="btn-action approve-btn" @click="approveCompany(company.id)">
                                <i class="fas fa-check-circle"></i> Approve
                            </button>
                        </div>
                    </div>
                </div>
                
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
                    <h3>Active Recruiters</h3>
                </div>
                <div class="table-head">
                    <span>COMPANY</span>
                    <span>INDUSTRY</span>
                    <span>EMAIL</span>
                    <span>STATUS</span>
                    <span>ACTION</span>
                </div>
                <div class="drive-list">
                    <div v-if="activeCompanies.length === 0" class="empty-state">
                        There are no active companies. 
                    </div>
                    <div v-for="company in paginatedActive" :key="company.id" class="drive-item">
                        <div class="company-col d-flex align-items-center gap-3">
                            <div class="drive-logo">
                                {{ company.icon || '🏢' }}
                            </div>
                            <div class="drive-details">
                                <h4>{{ company.name }}</h4>
                            </div>
                        </div>
                        <div class="industry-col">
                            <span class="text-muted small fw-medium">{{ company.industry || 'Technology' }}</span>
                        </div>
                        <div class="email-col">
                            <span class="text-muted small">{{ company.email }}</span>
                        </div>
                        <div class="status-col">
                            <span class="status-badge approved">Approved</span>
                        </div>
                        <div class="action-col">
                            <button class="btn-action revoke-btn" @click="revokeCompany(company.id)">
                                <i class="fas fa-times-circle"></i> Revoke
                            </button>
                        </div>
                    </div>
                </div>
                
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

const companies = ref([])
const errorMsg = ref('')

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
    bgClass: 'bg-pink-soft',
    textClass: 'text-pink',
  },
  approvals: {
    label: 'Pending Approvals',
    icon: 'fas fa-hourglass-half',
    bgClass: 'bg-emerald-soft',
    textClass: 'text-emerald',
  },
  blacklisted: {
    label: 'Blacklisted',
    icon: 'fas fa-ban',
    bgClass: 'bg-orange-soft',
    textClass: 'text-orange',
  }
}

// -- Fetch companies on mount --
onMounted(async () => {
    const token = localStorage.getItem("token")

    try {
        const res = await fetch('http://127.0.0.1:5555/api/admin/companies', {
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
})

// Stats computation
const totalCompaniesCount = computed(() => companies.value.length)
const pendingCompanies = computed(() => companies.value.filter(c => !c.approved))
const pendingCompaniesCount = computed(() => pendingCompanies.value.length)
const activeCompanies = computed(() => companies.value.filter(c => c.approved))
const blacklistedCompaniesCount = computed(() => companies.value.filter(c => c.isBlacklisted).length)

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
    try {
        const token = localStorage.getItem("token")

            if (!token) {
                console.error("No token found")
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

        // update UI
        companies.value = companies.value.map(c => {
        if (c.id === companyId) {
            return { ...c, approved: true }
        }
        return c
        })

    } catch (error) {
    console.error("Error:", error.response?.data || error.message)
  }
}

const revokeCompany = (id) => {
    console.log("Revoke company:", id)
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

.table-head {
    display: grid;
    grid-template-columns: 2fr 1fr 2fr 1fr 1fr;
    gap: 16px;
    padding: 12px 16px;
    border-bottom: 2px solid #eee;
    font-weight: 600;
    color: #555;
    font-size: 0.85rem;
    text-transform: uppercase;
}

.drive-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.drive-item {
    display: grid;
    grid-template-columns: 2fr 1fr 2fr 1fr 1fr;
    align-items: center;
    gap: 16px;
    padding: 12px 16px;
    border-radius: 12px;
    background: #fafafa;
    transition: all 0.2s ease;
}

.drive-item:hover {
    background: #f0f0f0;
}

.company-col, .industry-col, .email-col, .status-col, .action-col {
    display: flex;
    align-items: center;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
}

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
}

.drive-details {
    flex: 1;
    overflow: hidden;
}

.drive-details h4 {
    margin: 0;
    font-size: 1rem;
    color: #333;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.drive-details p {
    margin: 4px 0 0 0;
    font-size: 0.875rem;
    color: #777;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
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
</style>