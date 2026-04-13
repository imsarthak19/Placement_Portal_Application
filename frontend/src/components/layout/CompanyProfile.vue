<template>
  <component :is="hideLayout ? 'div' : DashboardLayout" :role="userRole">
    <div :class="hideLayout ? '' : 'container-fluid py-4 px-md-4'">
        <!-- Page Header (Only if not hidden) -->
        <div v-if="!hideLayout" class="d-flex justify-content-between align-items-center mb-4">
            <div>
                <h1 class="h3 fw-bold mb-1" style="color: var(--color-text);">Company Profile</h1>
                <p class="text-muted mb-0">{{ isEditing ? 'Edit the details of this company below.' : 'View detailed information about this registered company.' }}</p>
            </div>
            <div class="d-flex gap-2">
                <button v-if="canEdit && !isEditing" class="btn btn-primary shadow-sm border-0 d-flex align-items-center gap-2 fw-medium px-4 rounded-pill" @click="toggleEdit">
                    <i class="fas fa-edit"></i> Edit Profile
                </button>
                <button v-if="isEditing" class="btn btn-success shadow-sm border-0 d-flex align-items-center gap-2 fw-medium px-4 rounded-pill" @click="saveProfile">
                    <i class="fas fa-save"></i> Save Changes
                </button>
                <button v-if="isEditing" class="btn btn-outline-secondary shadow-sm d-flex align-items-center gap-2 fw-medium px-4 rounded-pill" @click="toggleEdit">
                    <i class="fas fa-times"></i> Cancel
                </button>
                <button v-if="!isEditing" class="btn btn-light shadow-sm border d-flex align-items-center gap-2 fw-medium px-3 rounded-pill" @click="$router.go(-1)">
                    <i class="fas fa-arrow-left"></i> Back
                </button>
            </div>
        </div>

        <div v-if="!hideLayout" class="flash-container z-3">
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
                                <h2 v-if="!isEditing" class="fw-bold mb-1 d-flex align-items-center gap-2 text-dark">
                                    {{ company.name || 'Company Name' }}
                                    <i class="fas fa-check-circle text-primary fs-5 mt-1" v-if="company.approved" title="Verified Company"></i>
                                </h2>
                                <div v-else class="mb-2">
                                    <label class="form-label small fw-bold text-muted text-uppercase mb-1">Company Name</label>
                                    <input type="text" v-model="editForm.name" class="form-control fw-bold fs-5 rounded-3 border-light shadow-sm" placeholder="Enter Company Name">
                                </div>

                                <div v-if="!isEditing">
                                    <span class="badge bg-primary bg-opacity-10 text-primary border border-primary border-opacity-25 px-3 py-2 rounded-pill mt-2 fw-semibold shadow-sm d-inline-flex align-items-center gap-1">
                                        <i class="fas fa-building"></i> {{ company.industry || 'General Industry' }}
                                    </span>
                                    <span class="badge bg-primary bg-opacity-10 text-primary border border-primary border-opacity-25 px-3 py-2 rounded-pill mt-2 fw-semibold shadow-sm d-inline-flex align-items-center gap-1 mx-2">
                                        <i class="fas fa-users"></i> {{ company.scale }}
                                    </span>
                                </div>
                                <div v-else class="row g-2 mt-1">
                                    <div class="col-md-6">
                                        <label class="form-label small fw-bold text-muted text-uppercase mb-1">Industry</label>
                                        <input type="text" v-model="editForm.industry" class="form-control form-control-sm rounded-3 shadow-sm border-light" placeholder="e.g. Technology">
                                    </div>
                                    <div class="col-md-6">
                                        <label class="form-label small fw-bold text-muted text-uppercase mb-1">Scale</label>
                                        <input type="text" v-model="editForm.scale" class="form-control form-control-sm rounded-3 shadow-sm border-light" placeholder="e.g. 1000+ Employees">
                                    </div>
                                </div>
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
                            About {{ isEditing ? 'the Company' : (company?.name || 'the Company') }}
                        </h5>
                        <div class="text-body-secondary fs-6 company-description">
                            <div v-if="!isEditing">
                                <p v-if="company?.description">{{ company.description }}</p>
                                <p v-else class="text-muted fst-italic">
                                    This company has not provided a detailed description yet. More information will be available here once they update their profile.
                                </p>
                            </div>
                            <div v-else>
                                <textarea v-model="editForm.description" class="form-control rounded-4 shadow-sm border-light" rows="10" placeholder="Describe the company's mission, values, and work culture..."></textarea>
                            </div>
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
                                    <small class="text-muted d-block fw-medium mb-1 text-uppercase" style="font-size: 0.75rem; letter-spacing: 0.5px;">COMPANY POC NAME</small>
                                    <div v-if="!isEditing">
                                        <div v-if="company">
                                            <span class="text-dark fw-bold text-truncate d-block">{{ company.pocName || 'N/A' }}</span>
                                        </div>
                                        <div v-else class="placeholder-glow"><span class="placeholder col-8 rounded"></span></div>
                                    </div>
                                    <div v-else>
                                        <input type="text" v-model="editForm.pocName" class="form-control form-control-sm rounded-3 shadow-sm border-light" placeholder="Enter POC Name">
                                    </div>
                                </div>
                            </div>

                            <div class="d-flex align-items-start mb-4">
                                <div class="icon-circle bg-white shadow-sm border text-primary flex-shrink-0 d-flex align-items-center justify-content-center mt-1">
                                    <i class="fas fa-envelope"></i>
                                </div>
                                <div class="ms-3 overflow-hidden w-100">
                                    <small class="text-muted d-block fw-medium mb-1 text-uppercase" style="font-size: 0.75rem; letter-spacing: 0.5px;">COMPANY POC EMAIL</small>
                                    <div v-if="!isEditing">
                                        <div v-if="company">
                                            <a :href="'mailto:' + company.pocEmail" class="text-dark fw-bold text-decoration-none text-truncate d-block contact-link">{{ company.pocEmail || 'N/A' }}</a>
                                        </div>
                                        <div v-else class="placeholder-glow"><span class="placeholder col-8 rounded"></span></div>
                                    </div>
                                    <div v-else>
                                        <input type="email" v-model="editForm.pocEmail" class="form-control form-control-sm rounded-3 shadow-sm border-light" placeholder="Enter POC Email">
                                    </div>
                                </div>
                            </div>

                            <div class="d-flex align-items-start mb-4">
                                <div class="icon-circle bg-white shadow-sm border text-primary flex-shrink-0 d-flex align-items-center justify-content-center mt-1">
                                    <i class="fas fa-globe"></i>
                                </div>
                                <div class="ms-3 overflow-hidden w-100">
                                    <small class="text-muted d-block fw-medium mb-1 text-uppercase" style="font-size: 0.75rem; letter-spacing: 0.5px;">Website</small>
                                    <div v-if="!isEditing">
                                        <div v-if="company">
                                            <a v-if="company.website" :href="company.website" target="_blank" class="text-primary fw-bold text-decoration-none text-truncate d-block contact-link">{{ company.website }}</a>
                                            <span v-else class="text-dark fw-bold">N/A</span>
                                        </div>
                                        <div v-else class="placeholder-glow"><span class="placeholder col-8 rounded"></span></div>
                                    </div>
                                    <div v-else>
                                        <input type="text" v-model="editForm.website" class="form-control form-control-sm rounded-3 shadow-sm border-light" placeholder="Enter Website URL">
                                    </div>
                                </div>
                            </div>

                            <div v-if="isEditing" class="d-flex align-items-start mb-4">
                                <div class="icon-circle bg-white shadow-sm border text-primary flex-shrink-0 d-flex align-items-center justify-content-center mt-1">
                                    <i class="fas fa-image"></i>
                                </div>
                                <div class="ms-3 overflow-hidden w-100">
                                    <small class="text-muted d-block fw-medium mb-1 text-uppercase" style="font-size: 0.75rem; letter-spacing: 0.5px;">Logo URL</small>
                                    <div>
                                        <input type="text" v-model="editForm.icon" class="form-control form-control-sm rounded-3 shadow-sm border-light" placeholder="Enter Logo Image URL">
                                    </div>
                                </div>
                            </div>
                            
                            <div class="d-flex align-items-start">
                                <div class="icon-circle bg-white shadow-sm border text-primary flex-shrink-0 d-flex align-items-center justify-content-center mt-1">
                                    <i class="fas fa-map-marker-alt"></i>
                                </div>
                                <div class="ms-3 overflow-hidden w-100">
                                    <small class="text-muted d-block fw-medium mb-1 text-uppercase" style="font-size: 0.75rem; letter-spacing: 0.5px;">Head Office</small>
                                    <div v-if="!isEditing">
                                        <div v-if="company">
                                            <span class="text-dark fw-bold d-block">{{ company.headOffice || 'Global Headquarters' }}</span>
                                        </div>
                                        <div v-else class="placeholder-glow"><span class="placeholder col-6 rounded"></span></div>
                                    </div>
                                    <div v-else>
                                        <input type="text" v-model="editForm.headOffice" class="form-control form-control-sm rounded-3 shadow-sm border-light" placeholder="Enter Head Office Location">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <!-- Independent Drives Component -->
            <CompanyDrives v-if="showDrives" :companyId="resolvedCompanyId" :role="userRole" />
        </div>

        <!-- Edit Profile Modal Removed -->
    </div>
  </component>
</template>

<script setup>
    import { ref, onMounted, computed } from 'vue'
    import { useRoute, useRouter } from 'vue-router'
    import DashboardLayout from '@/components/sidebar/DashboardLayout.vue'
    import CompanyDrives from '@/components/layout/CompanyDrives.vue'

    const props = defineProps({
        companyId: [String, Number],
        showDrives: {
            type: Boolean,
            default: false
        },
        hideLayout: {
            type: Boolean,
            default: false
        }
    })
    const route = useRoute()
    const router = useRouter()

    const user = JSON.parse(localStorage.getItem('user') || '{}')
    const userRole = user.type === 'admin' ? 'admin' : 'recruiter'
    
    const resolvedCompanyId = computed(() => props.companyId || route.params.id || user.id)
    
    const company = ref(null)
    const isEditing = ref(false)
    const editForm = ref({
        name: '',
        description: '',
        industry: '',
        scale: '',
        headOffice: '',
        website: '',
        icon: '',
        pocName: '',
        pocEmail: ''
    })
    const flashMsg = ref('')
    const flashMsgError = ref('')

    const canEdit = computed(() => {
        if (user.type === 'admin') return true
        if (user.type === 'recruiter' && user.id == resolvedCompanyId.value) return true
        return false
    })

    const showFlash = (message) => {
        flashMsg.value = message
        setTimeout(() => { flashMsg.value = "" }, 2000)
    }
    
    const errorMsg = (message) => {
        flashMsgError.value = message
        setTimeout(() => { flashMsgError.value = "" }, 2000)
    }

    onMounted(async () => {
        await fetchCompany()
    })

    const fetchCompany = async () => {
        const token = localStorage.getItem("token")
        const id = resolvedCompanyId.value
        if (!id) return

        try {
            const res = await fetch(
                `http://127.0.0.1:5555/api/company-profile/${id}`,
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
            company.value = data
            // Populate edit form
            editForm.value = {
                name: data.name || '',
                description: data.description || '',
                industry: data.industry || '',
                scale: data.scale || '',
                headOffice: data.headOffice || '',
                website: data.website || '',
                icon: data.icon || '',
                pocName: data.pocName || '',
                pocEmail: data.pocEmail || ''
            }
        } catch (err) {
            console.error("Error:", err)
            errorMsg('Server error. Please try again later.')
        }
    }
    
    const toggleEdit = () => {
        isEditing.value = !isEditing.value
        if (!isEditing.value && company.value) {
            // Reset form if cancelled
            editForm.value = {
                name: company.value.name || '',
                description: company.value.description || '',
                industry: company.value.industry || '',
                scale: company.value.scale || '',
                headOffice: company.value.headOffice || '',
                website: company.value.website || '',
                icon: company.value.icon || '',
                pocName: company.value.pocName || '',
                pocEmail: company.value.pocEmail || ''
            }
        }
    }

    const saveProfile = async () => {
        const token = localStorage.getItem("token")
        const id = resolvedCompanyId.value
        
        // Admin uses a different endpoint than Recruiter
        const url = user.type === 'admin' 
            ? `http://127.0.0.1:5555/api/admin/update-company/${id}`
            : 'http://127.0.0.1:5555/api/company/update-profile'

        try {
            const res = await fetch(url, {
                method: 'POST', // Backend currently accepts POST for these updates
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(editForm.value)
            })

            const data = await res.json()

            if (res.ok) {
                showFlash(data.message || 'Profile updated successfully!')
                isEditing.value = false
                await fetchCompany()
            } else {
                errorMsg(data.error || 'Failed to update profile')
            }
        } catch (err) {
            console.error("Save error:", err)
            errorMsg('Server error. Please try again later.')
        }
    }
</script>

<style scoped>
.custom-card {
    transition: all 0.3s ease;
}

.company-logo-wrapper {
    width: 130px;
    height: 130px;
    overflow: hidden;
}

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

.fade-enter-active,
.fade-leave-active {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
    transform: translateY(-10px) scale(0.95);
}
</style>