<template>
  <DashboardLayout role="admin">
    <div class="container-fluid py-4 px-md-4">
        <!-- Page Header -->
        <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
                <h1 class="h3 fw-bold mb-1" style="color: var(--color-text);">Drive Detail</h1>
                <p class="text-muted mb-0">View comprehensive details and applicant history for this placement drive.</p>
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

        <!-- Drive Main Card -->
        <div class="card shadow-sm border-0 bg-white rounded-4 overflow-hidden mb-4 custom-card">
            <div class="card-body p-4 position-relative">
                <!-- Header Section -->
                <div class="d-flex flex-column flex-md-row align-items-md-center mb-5 profile-header-wrapper">
                    <div class="company-logo-wrapper bg-white p-2 rounded-4 shadow-sm border z-1 flex-shrink-0 d-flex align-items-center justify-content-center">
                        <img v-if="drive?.company_logo" :src="drive.company_logo" alt="Company Logo" class="img-fluid rounded-3" style="width: 100%; height: 100%; object-fit: contain;">
                        <span v-else class="display-3 text-secondary opacity-50">🏢</span>
                    </div>

                    <div class="ms-md-4 mt-3 mt-md-0 mb-2 flex-grow-1">
                        <div v-if="drive" class="d-flex flex-column flex-md-row align-items-md-center justify-content-between w-100">
                            <div>
                                <h2 class="fw-bold mb-1 d-flex align-items-center gap-2 text-dark">
                                    {{ drive.title || 'Drive Title' }}
                                </h2>
                                <router-link :to="`/admin/company/${drive.company_id}`" class="text-decoration-none">
                                    <span class="text-primary fw-semibold h5 mb-0 hover-opacity">
                                        <i class="fas fa-building me-1"></i> {{ drive.company_name || 'Company Name' }}
                                    </span>
                                </router-link>
                                <div class="mt-2 d-flex flex-wrap gap-2">
                                    <span class="badge bg-light text-dark border px-3 py-2 rounded-pill fw-medium shadow-sm d-inline-flex align-items-center gap-1">
                                        <i class="fas fa-map-marker-alt text-danger"></i> {{ drive.location || 'N/A' }}
                                    </span>
                                    <span class="badge bg-light text-dark border px-3 py-2 rounded-pill fw-medium shadow-sm d-inline-flex align-items-center gap-1">
                                        <i class="fas fa-briefcase text-primary"></i> {{ drive.workMode || 'N/A' }}
                                    </span>
                                </div>
                            </div>
                            
                            <div class="d-flex flex-column align-items-md-end gap-2 mt-3 mt-md-0">
                                <span class="badge rounded-pill fw-medium px-4 py-2 shadow-sm fs-6"
                                      :class="{
                                          'bg-success': drive.status === 'Active',
                                          'bg-warning text-dark': drive.status === 'Unapproved',
                                          'bg-danger': drive.status === 'Rejected' || drive.status === 'Closed'
                                      }">
                                    <i class="fas fa-circle me-1" style="font-size: 0.5rem; vertical-align: middle;"></i> {{ drive.status }}
                                </span>
                                <small class="text-muted fw-medium">Posted on {{ formatDate(drive.created_at) }}</small>
                            </div>
                        </div>
                        <div v-else class="placeholder-glow w-100">
                            <h2 class="placeholder col-6 rounded bg-secondary opacity-25"></h2>
                            <p class="placeholder col-3 rounded mt-2 bg-secondary opacity-25"></p>
                        </div>
                    </div>
                </div>

                <!-- Content Grid -->
                <div class="row g-4 pt-3 border-top">
                    <!-- Left: Description & Applicants -->
                    <div class="col-lg-8 pe-lg-5 border-end">
                        <div class="mb-5">
                            <h5 class="fw-bold text-dark d-flex align-items-center gap-2 mb-4">
                                <div class="icon-square text-primary bg-primary bg-opacity-10 rounded shadow-sm d-flex align-items-center justify-content-center p-2">
                                    <i class="fas fa-align-left"></i>
                                </div>
                                Role Description
                            </h5>
                            <div v-if="drive" class="text-muted lh-base drive-description" v-html="drive.description"></div>
                            <div v-else class="placeholder-glow">
                                <p class="placeholder col-12 rounded"></p>
                                <p class="placeholder col-12 rounded"></p>
                                <p class="placeholder col-8 rounded"></p>
                            </div>
                        </div>

                        <div class="mb-2">
                            <h5 class="fw-bold text-dark d-flex align-items-center justify-content-between gap-2 mb-4">
                                <span class="d-flex align-items-center gap-2">
                                    <div class="icon-square text-primary bg-primary bg-opacity-10 rounded shadow-sm d-flex align-items-center justify-content-center p-2">
                                        <i class="fas fa-users"></i>
                                    </div>
                                    Applicants List
                                </span>
                                <span class="badge bg-primary rounded-pill px-3 py-2 fw-medium" v-if="applications.length > 0">
                                    {{ applications.length }} Total
                                </span>
                            </h5>
                            
                            <Table :columns="tableColumns" :data="applications">
                                <template #row="{ item: app }">
                                    <td class="py-3 px-4">
                                        <router-link :to="`/admin/student/${app.student_id}`" class="text-decoration-none">
                                            <div class="fw-bold text-dark hover-primary">{{ app.student_name }}</div>
                                            <small class="text-muted">{{ app.roll_number }}</small>
                                        </router-link>
                                    </td>
                                    <td class="py-3 px-3 text-muted">
                                        <span class="badge bg-light text-dark border fw-medium">{{ app.branch }}</span>
                                    </td>
                                    <td class="py-3 px-3 text-center fw-bold text-success">
                                        {{ app.cgpa }}
                                    </td>
                                    <td class="py-3 px-3 text-muted text-center"><small>{{ formatDate(app.applied_at) }}</small></td>
                                    <td class="py-3 px-4 text-center">
                                        <span class="badge rounded-pill px-3 py-2 fw-medium shadow-sm"
                                              :class="{
                                                  'bg-info text-dark': app.status.toLowerCase() === 'applied',
                                                  'bg-primary': app.status.toLowerCase() === 'interviewing',
                                                  'bg-success': app.status.toLowerCase() === 'hired' || app.status.toLowerCase() === 'selected',
                                                  'bg-danger': app.status.toLowerCase() === 'rejected'
                                              }">
                                            {{ app.status }}
                                        </span>
                                    </td>
                                </template>
                                <template #empty>
                                    <td colspan="5" class="text-center py-5 text-muted">
                                        <div class="fs-1 mb-3 opacity-50">👥</div>
                                        <h5 class="fw-bold">No applicants yet.</h5>
                                        <p class="mb-0">Applications will appear here once students start applying.</p>
                                    </td>
                                </template>
                            </Table>
                        </div>
                    </div>
                    
                    <!-- Right Sidebar: Stats & Criteria -->
                    <div class="col-lg-4 ps-lg-4">
                        <div class="bg-light p-4 rounded-4 border border-1 custom-stats-card shadow-sm mb-4">
                            <h6 class="fw-bold text-secondary text-uppercase mb-4 pb-2 border-bottom border-secondary border-opacity-10 d-flex justify-content-between align-items-center">
                                Drive Overview
                                <i class="fas fa-info-circle text-muted opacity-50"></i>
                            </h6>
                            
                            <!-- Stat Items -->
                            <div class="d-flex align-items-start mb-4">
                                <div class="icon-circle bg-white shadow-sm border text-success flex-shrink-0 d-flex align-items-center justify-content-center mt-1">
                                    <i class="fas fa-money-bill-wave"></i>
                                </div>
                                <div class="ms-3">
                                    <small class="text-muted d-block fw-medium mb-1 text-uppercase" style="font-size: 0.75rem; letter-spacing: 0.5px;">Pay Scale</small>
                                    <span v-if="drive" class="text-dark fw-bold fs-5">{{ drive.payScale || 'N/A' }}</span>
                                    <div v-else class="placeholder-glow"><span class="placeholder col-8 rounded"></span></div>
                                </div>
                            </div>

                            <div class="d-flex align-items-start mb-4">
                                <div class="icon-circle bg-white shadow-sm border text-primary flex-shrink-0 d-flex align-items-center justify-content-center mt-1">
                                    <i class="fas fa-chair"></i>
                                </div>
                                <div class="ms-3">
                                    <small class="text-muted d-block fw-medium mb-1 text-uppercase" style="font-size: 0.75rem; letter-spacing: 0.5px;">Open Positions</small>
                                    <span v-if="drive" class="text-dark fw-bold fs-5">{{ drive.positions || '0' }}</span>
                                    <div v-else class="placeholder-glow"><span class="placeholder col-8 rounded"></span></div>
                                </div>
                            </div>

                            <div class="d-flex align-items-start mb-4">
                                <div class="icon-circle bg-white shadow-sm border text-warning flex-shrink-0 d-flex align-items-center justify-content-center mt-1">
                                    <i class="fas fa-graduation-cap"></i>
                                </div>
                                <div class="ms-3">
                                    <small class="text-muted d-block fw-medium mb-1 text-uppercase" style="font-size: 0.75rem; letter-spacing: 0.5px;">Eligible Batch</small>
                                    <span v-if="drive" class="text-dark fw-bold">{{ drive.batch || 'All' }}</span>
                                    <div v-else class="placeholder-glow"><span class="placeholder col-8 rounded"></span></div>
                                </div>
                            </div>
                        </div>

                        <!-- Requirements Card -->
                        <div class="bg-white p-4 rounded-4 border border-1 shadow-sm h-auto">
                            <h6 class="fw-bold text-secondary text-uppercase mb-4 pb-2 border-bottom border-secondary border-opacity-10">
                                Requirements
                            </h6>
                            
                            <div class="mb-4">
                                <small class="text-muted d-block mb-2 fw-bold text-uppercase" style="font-size: 0.7rem;">Education Criteria</small>
                                <p v-if="drive" class="text-dark small mb-0">{{ drive.educationCriteria || 'Not specified' }}</p>
                                <div v-else class="placeholder-glow"><span class="placeholder col-12 rounded"></span></div>
                            </div>

                            <div class="mb-0">
                                <small class="text-muted d-block mb-2 fw-bold text-uppercase" style="font-size: 0.7rem;">Skills Required</small>
                                <div v-if="drive" class="d-flex flex-wrap gap-2">
                                    <template v-if="drive.skillsRequired">
                                        <span v-for="skill in drive.skillsRequired.split(',')" :key="skill" class="badge bg-primary bg-opacity-10 text-primary border border-primary border-opacity-10 px-2 py-1 fw-medium">
                                            {{ skill.trim() }}
                                        </span>
                                    </template>
                                    <span v-else class="text-muted small">Not specified</span>
                                </div>
                                <div v-else class="placeholder-glow d-flex gap-2"><span class="placeholder col-3 rounded"></span><span class="placeholder col-4 rounded"></span></div>
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
    import { ref, onMounted } from 'vue'
    import axios from "axios"
    import DashboardLayout from '@/components/sidebar/DashboardLayout.vue'
    import Table from '@/components/ui/Table.vue'

    const props = defineProps({
        driveId: {
            type: [String, Number],
            required: true
        }
    })

    const tableColumns = [
        { key: 'student', label: 'Candidate', class: 'py-3 px-4 text-secondary fw-semibold text-uppercase' },
        { key: 'branch', label: 'Branch', class: 'py-3 px-3 text-secondary fw-semibold text-uppercase' },
        { key: 'cgpa', label: 'CGPA', class: 'py-3 px-3 text-secondary fw-semibold text-uppercase text-center' },
        { key: 'appliedAt', label: 'Applied Date', class: 'py-3 px-3 text-secondary fw-semibold text-uppercase text-center' },
        { key: 'status', label: 'Status', class: 'py-3 px-4 text-secondary fw-semibold text-uppercase text-center' }
    ]

    const drive = ref(null)
    const applications = ref([])
    const flashMsg = ref('')
    const flashMsgError = ref('')

    const errorMsg = (message) => {
        flashMsgError.value = message
        setTimeout(() => { flashMsgError.value = "" }, 2500)
    }

    onMounted(async () => {
        await fetchDrive()
        await fetchApplications()
    })

    const fetchDrive = async () => {
        const token = localStorage.getItem("token")
        try {
            const res = await axios.get(`http://127.0.0.1:5555/api/admin/drive-details/${props.driveId}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            })
            drive.value = res.data
        } catch (err) {
            console.error("Drive Fetch Error:", err)
            errorMsg('Failed to load drive details.')
        }
    }

    const fetchApplications = async () => {
        const token = localStorage.getItem("token")
        try {
            const res = await axios.get(`http://127.0.0.1:5555/api/admin/drive-applications/${props.driveId}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            })
            applications.value = res.data
        } catch (err) {
            console.error("Apps Fetch Error:", err)
        }
    }

    const formatDate = (isoString) => {
        if (!isoString) return 'N/A'
        const date = new Date(isoString)
        return date.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
    }
</script>

<style scoped>
.custom-card { transition: all 0.3s ease; }
.company-logo-wrapper { width: 120px; height: 120px; }
.icon-circle { width: 42px; height: 42px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
.icon-square { width: 36px; height: 36px; border-radius: 8px; }
.drive-description :deep(p) { margin-bottom: 1rem; }
.hover-opacity:hover { opacity: 0.8; }
.hover-primary:hover { color: var(--color-primary) !important; }

.flash-container { position: fixed; top: 20px; right: 20px; z-index: 9999; display: flex; flex-direction: column; gap: 12px; min-width: 300px; pointer-events: none; }
.flash-container > div { pointer-events: auto; }

.fade-enter-active, .fade-leave-active { transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translateY(-10px) scale(0.95); }
</style>
