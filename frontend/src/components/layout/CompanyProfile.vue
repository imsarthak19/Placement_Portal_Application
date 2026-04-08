<template>
  <DashboardLayout role="admin">
    <div class="container-fluid py-4 px-md-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
                <h1 class="h3 fw-bold mb-1" style="color: var(--color-text);">Company Profile</h1>
                <p class="text-muted mb-0">View detailed information about this registered company.</p>
            </div>
            <button class="btn btn-light shadow-sm border d-flex align-items-center gap-2 fw-medium px-3" @click="$router.go(-1)">
                <i class="fas fa-arrow-left"></i> Back
            </button>
        </div>

        <div class="flash-container z-3">
            <transition name="fade">
                <div v-if="flashMsg" class="alert alert-success d-flex align-items-center gap-3 shadow border-0 rounded-4 py-3 px-4" role="alert">
                    <i class="fas fa-check-circle fs-4"></i>
                    <div class="fw-medium">{{ flashMsg }}</div>
                </div>
            </transition>
            <transition name="fade">
                <div v-if="flashMsgError" class="alert alert-danger d-flex align-items-center gap-3 shadow border-0 rounded-4 py-3 px-4" role="alert">
                    <i class="fas fa-exclamation-circle fs-4"></i>
                    <div class="fw-medium">{{ flashMsgError }}</div>
                </div>
            </transition>
        </div>

        <div class="card shadow-sm border-0 bg-white rounded-4 overflow-hidden mb-4 custom-card">
            <div class="card-body p-4 position-relative">
                <div class="d-flex flex-column flex-md-row align-items-md-center mb-5 profile-header-wrapper">
                    <div class="company-logo-wrapper bg-white p-2 rounded-4 shadow-sm border z-1 flex-shrink-0 d-flex align-items-center justify-content-center">
                        <img v-if="company && company.icon" :src="company.icon" alt="Company Logo" class="img-fluid rounded-3 w-100 h-100 object-fit-contain">
                        <span v-else class="display-3 text-secondary opacity-50">🏢</span>
                    </div>

                    <div class="ms-md-4 mt-3 mt-md-0 mb-2 flex-grow-1">
                        <div v-if="company" class="d-flex flex-column flex-md-row align-items-md-center justify-content-between w-100">
                            <div>
                                <h2 class="fw-bold mb-1 d-flex align-items-center gap-2 text-dark">
                                    {{ company.name || 'Company Name' }}
                                    <i class="fas fa-check-circle text-primary fs-5 mt-1" v-if="company.approved" title="Verified Company"></i>
                                </h2>
                                <span class="badge bg-primary bg-opacity-10 text-primary border border-primary border-opacity-25 px-3 py-2 rounded-pill mt-2 fw-semibold shadow-sm d-inline-flex align-items-center gap-1">
                                    <i class="fas fa-building"></i> {{ company.industry || 'General Industry' }}
                                </span>
                                <span class="badge bg-primary bg-opacity-10 text-primary border border-primary border-opacity-25 px-3 py-2 rounded-pill mt-2 fw-semibold shadow-sm d-inline-flex align-items-center gap-1 mx-2">
                                    <i class="fas fa-users"></i> {{ company.scale }}
                                </span>
                            </div>
                            
                            <div class="d-flex gap-2 mt-3 mt-md-0 status-badges">
                                <span class="badge rounded-pill bg-success fw-medium px-4 py-2 shadow-sm fs-6" v-if="company.approved">
                                    <i class="fas fa-check me-1"></i> Approved
                                </span>
                                <span class="badge rounded-pill bg-warning text-dark fw-medium px-4 py-2 shadow-sm fs-6" v-else>
                                    <i class="fas fa-clock me-1"></i> Pending
                                </span>
                                <span v-if="company.blacklisted" class="badge rounded-pill bg-danger fw-medium px-4 py-2 shadow-sm fs-6">
                                    <i class="fas fa-ban me-1"></i> Blacklisted
                                </span>
                            </div>
                        </div>
                        <div v-else class="placeholder-glow w-100">
                            <h2 class="placeholder col-6 rounded bg-secondary opacity-25"></h2>
                            <p class="placeholder col-3 rounded mt-2 bg-secondary opacity-25"></p>
                        </div>
                    </div>
                </div>

                <div class="row g-4 pt-3 border-top">
                    <div class="col-lg-8 pe-lg-5">
                        <h5 class="fw-bold text-dark mb-4 d-flex align-items-center gap-2 pb-2 border-bottom">
                            <div class="icon-square text-primary bg-primary bg-opacity-10 rounded shadow-sm d-flex align-items-center justify-content-center p-2 mb-1 me-1">
                                <i class="fas fa-info-circle"></i>
                            </div>
                            About {{ company?.name || 'the Company' }}
                        </h5>
                        <div class="text-body-secondary fs-6 company-description">
                            <p v-if="company?.description">{{ company.description }}</p>
                            <p v-else class="text-muted fst-italic">
                                This company has not provided a detailed description yet. More information will be available here once they update their profile.
                            </p>
                        </div>
                    </div>
                    
                    <!-- Right Side Panel  -->
                    <div class="col-lg-4">
                        <div class="bg-light p-4 rounded-4 border border-1 custom-contact-card h-100 shadow-sm">
                            <h6 class="fw-bold text-secondary text-uppercase mb-4 pb-2 border-bottom border-secondary border-opacity-10 d-flex justify-content-between align-items-center">
                                Contact Details
                                <i class="fas fa-id-card text-muted opacity-50"></i>
                            </h6>
                            
                            <div class="d-flex align-items-start mb-4">
                                <div class="icon-circle bg-white shadow-sm border text-primary flex-shrink-0 d-flex align-items-center justify-content-center mt-1">
                                    <i class="fas fa-user"></i>
                                </div>
                                <div class="ms-3 overflow-hidden w-100">
                                    <small class="text-muted d-block fw-medium mb-1 text-uppercase" style="font-size: 0.75rem; letter-spacing: 0.5px;">COMPANY POC</small>
                                    <div v-if="company">
                                        
                                        <a :href="'mailto:' + company.pocName" class="text-dark fw-bold text-decoration-none text-truncate d-block contact-link">{{ company.pocName || 'N/A' }}</a>
                                    </div>
                                    <div v-else class="placeholder-glow"><span class="placeholder col-8 rounded"></span></div>
                                </div>
                            </div>

                            <div class="d-flex align-items-start mb-4">
                                <div class="icon-circle bg-white shadow-sm border text-primary flex-shrink-0 d-flex align-items-center justify-content-center mt-1">
                                    <i class="fas fa-envelope"></i>
                                </div>
                                <div class="ms-3 overflow-hidden w-100">
                                    <small class="text-muted d-block fw-medium mb-1 text-uppercase" style="font-size: 0.75rem; letter-spacing: 0.5px;">COMPANY POC EMAIL</small>
                                    <div v-if="company">
                                        
                                        <a :href="'mailto:' + company.pocEmail" class="text-dark fw-bold text-decoration-none text-truncate d-block contact-link">{{ company.pocEmail || 'N/A' }}</a>
                                    </div>
                                    <div v-else class="placeholder-glow"><span class="placeholder col-8 rounded"></span></div>
                                </div>
                            </div>

                            <div class="d-flex align-items-start mb-4">
                                <div class="icon-circle bg-white shadow-sm border text-primary flex-shrink-0 d-flex align-items-center justify-content-center mt-1">
                                    <i class="fas fa-envelope"></i>
                                </div>
                                <div class="ms-3 overflow-hidden w-100">
                                    <small class="text-muted d-block fw-medium mb-1 text-uppercase" style="font-size: 0.75rem; letter-spacing: 0.5px;">Email Address</small>
                                    <div v-if="company">
                                        <a :href="'mailto:' + company.email" class="text-dark fw-bold text-decoration-none text-truncate d-block contact-link">{{ company.email || 'N/A' }}</a>
                                    </div>
                                    <div v-else class="placeholder-glow"><span class="placeholder col-8 rounded"></span></div>
                                </div>
                            </div>

                            <div class="d-flex align-items-start mb-4">
                                <div class="icon-circle bg-white shadow-sm border text-primary flex-shrink-0 d-flex align-items-center justify-content-center mt-1">
                                    <i class="fas fa-globe"></i>
                                </div>
                                <div class="ms-3 overflow-hidden w-100">
                                    <small class="text-muted d-block fw-medium mb-1 text-uppercase" style="font-size: 0.75rem; letter-spacing: 0.5px;">Website</small>
                                    <div v-if="company">
                                        <a v-if="company.website" :href="company.website" target="_blank" class="text-primary fw-bold text-decoration-none text-truncate d-block contact-link">{{ company.website }}</a>
                                        <span v-else class="text-dark fw-bold">N/A</span>
                                    </div>
                                    <div v-else class="placeholder-glow"><span class="placeholder col-8 rounded"></span></div>
                                </div>
                            </div>
                            
                            <div class="d-flex align-items-start">
                                <div class="icon-circle bg-white shadow-sm border text-primary flex-shrink-0 d-flex align-items-center justify-content-center mt-1">
                                    <i class="fas fa-map-marker-alt"></i>
                                </div>
                                <div class="ms-3 overflow-hidden w-100">
                                    <small class="text-muted d-block fw-medium mb-1 text-uppercase" style="font-size: 0.75rem; letter-spacing: 0.5px;">Head Office</small>
                                    <div v-if="company">
                                        <span class="text-dark fw-bold d-block">{{ company.headOffice || 'Global Headquarters' }}</span>
                                    </div>
                                    <div v-else class="placeholder-glow"><span class="placeholder col-6 rounded"></span></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <h5 class="fw-bold text-dark mt-5 mb-4 d-flex align-items-center gap-2 pb-2 border-bottom">
                    <div class="icon-square text-primary bg-primary bg-opacity-10 rounded shadow-sm d-flex align-items-center justify-content-center p-2 mb-1 me-1">
                        <i class="fas fa-briefcase"></i>
                    </div>
                Drives by {{ company?.name || 'the Company' }}
                </h5>
                
                <Table :columns="tableColumns" :data="drives">
                    <template #row="{ item: drive }">
                        <td class="py-3 px-4">
                            <router-link :to="`/admin/drive/${drive.id}`" class="text-decoration-none">
                                <div class="fw-bold text-dark hover-primary" style="transition: color 0.2s ease;">{{ drive.title }}</div>
                            </router-link>
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
                        <td class="py-3 px-3 text-muted"><span class="d-flex align-items-center gap-1"><i class="far fa-calendar-alt opacity-75"></i> {{ formatDate(drive.created_at) }}</span></td>
                        <td class="py-3 px-4 text-center">
                            <span class="badge px-3 py-2 fw-medium shadow-sm"
                                  :class="{
                                      'bg-success': drive.status === 'Active',
                                      'bg-secondary': drive.status === 'Closed',
                                      'bg-warning text-dark': drive.status === 'Unapproved',
                                      'bg-danger': drive.status === 'Rejected',
                                      'bg-info text-dark': drive.status === 'Hired'
                                  }">
                                {{ drive.status }}
                            </span>
                        </td>
                        <td class="py-3 px-4 text-center">
                            <router-link :to="`/admin/drive/${drive.id}`" class="btn btn-sm btn-primary border-0 shadow-sm px-3 py-2 rounded-3 view-btn">
                                <i class="fas fa-eye me-1"></i> View
                            </router-link>
                        </td>
                    </template>
                    <template #empty>
                        <td colspan="7" class="text-center py-5 text-muted">
                            <div class="fs-1 mb-3 opacity-50">📋</div>
                            <h5 class="fw-bold">No drives posted yet</h5>
                            <p class="mb-0">Once the company posts hiring drives, they will appear here.</p>
                        </td>
                    </template>
                </Table>

                </div>
        </div>
    </div>
</DashboardLayout>
</template>

<script setup>
    import { ref, onMounted, computed } from 'vue'
    import { useRoute } from 'vue-router'
    import axios from "axios"
    import DashboardLayout from '@/components/sidebar/DashboardLayout.vue'
    import Table from '@/components/ui/Table.vue'

    const tableColumns = [
        { key: 'title', label: 'Title', class: 'py-3 px-4 text-secondary fw-semibold text-uppercase' },
        { key: 'location', label: 'Location' },
        { key: 'workMode', label: 'Mode' },
        { key: 'payScale', label: 'Payscale' },
        { key: 'positions', label: 'Positions', class: 'py-3 px-3 text-secondary fw-semibold text-uppercase text-center' },
        { key: 'createdAt', label: 'Created' },
        { key: 'status', label: 'Status', class: 'py-3 px-4 text-secondary fw-semibold text-uppercase text-center' },
        { key: 'action', label: 'Action', class: 'py-3 px-4 text-secondary fw-semibold text-uppercase text-center' }
    ]

    const route = useRoute()
    const companyId = route.params.id
    const company = ref(null)
    const drives = ref([])
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

    // -- Fetch company & Drive details on mount --
    onMounted(async () => {
        console.log("Company ID:", companyId)

        await fetchCompany()
        await fetchDrives()
    })

    const fetchCompany = async () => {
        console.log("Company ID:", companyId)
        const token = localStorage.getItem("token")

        try {
            const res = await fetch(
            `http://127.0.0.1:5555/api/company-profile/${companyId}`,
            {
                method: 'GET',
                headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
                }
            }
            )

            if (!res.ok) {
            console.error("Request failed:", res.status)
            return
            }

            const data = await res.json()
            console.log("COMPANY DATA:", data)

            company.value = data

        } catch (err) {
            console.error("Error:", err)
            errorMsg.value = 'Server error. Please try again later.'
        }
    }

    const fetchDrives = async () => {
        const token = localStorage.getItem("token")

        try {
            const res = await fetch(
            `http://127.0.0.1:5555/api/company/all-drives/${companyId}`,
            {
                method: 'GET',
                headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
                }
            }
            )

            if (!res.ok) {
            console.error("Drives fetch failed:", res.status)
            return
            }

            const data = await res.json()
            console.log("DRIVES:", data)

            drives.value = data

        } catch (err) {
            console.error("Drives error:", err)
        }
    }

    // Formatting Date
    const formatDate = (isoString) => {
    const date = new Date(isoString)

    const day = String(date.getDate()).padStart(2, '0')
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const year = String(date.getFullYear()).slice(-2)

    return `${day}-${month}-${year}`
}

    // Pending Companies Pagination
    const pendingCurrentPage = ref(1)
    const pendingTotalPages = computed(() => Math.ceil(pendingCompaniesCount.value / itemsPerPage) || 1)
    const paginatedPending = computed(() => {
        const start = (pendingCurrentPage.value - 1) * itemsPerPage
        return pendingCompanies.value.slice(start, start + itemsPerPage)
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

</script><style scoped>

/* Page Layout */
.custom-card {
    transition: all 0.3s ease;
}


.company-logo-wrapper {
    width: 130px;
    height: 130px;
    overflow: hidden;
}

/* Icons & Sidebar */
.icon-circle {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    font-size: 1.1rem;
    transition: transform 0.2s ease;
}
.custom-contact-card:hover .icon-circle {
    transform: scale(1.05);
}
.custom-table tbody tr:last-child {
    border-bottom: 0 !important;
}
.icon-square {
    width: 32px;
    height: 32px;
    font-size: 1rem;
}
.contact-link {
    transition: color 0.2s ease;
}
.contact-link:hover {
    color: var(--color-primary) !important;
}
.company-description {
    line-height: 1.8;
    color: #4b5563;
}

/* Notifications */
.flash-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    gap: 12px;
    min-width: 300px;
    pointer-events: none;
}
.flash-container > div {
    pointer-events: auto;
}

/* Vue Transitions */
.fade-enter-active,
.fade-leave-active {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.fade-enter-from,
.fade-leave-to {
    opacity: 0;
    transform: translateY(-10px) scale(0.95);
}

.view-btn {
    background-color: #3b82f6;
    font-size: 0.8rem;
    font-weight: 600;
}

.view-btn:hover {
    background-color: #2563eb;
    transform: translateY(-1px);
}

.hover-primary:hover {
    color: var(--color-primary) !important;
}
</style>