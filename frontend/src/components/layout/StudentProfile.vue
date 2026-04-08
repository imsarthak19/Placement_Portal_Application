<template>
  <DashboardLayout role="admin">
    <div class="container-fluid py-4 px-md-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
                <h1 class="h3 fw-bold mb-1" style="color: var(--color-text);">Student Profile</h1>
                <p class="text-muted mb-0">View detailed information and application history of this student.</p>
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
                        <span class="display-3 text-secondary opacity-50">🎓</span>
                    </div>

                    <div class="ms-md-4 mt-3 mt-md-0 mb-2 flex-grow-1">
                        <div v-if="student" class="d-flex flex-column flex-md-row align-items-md-center justify-content-between w-100">
                            <div>
                                <h2 class="fw-bold mb-1 d-flex align-items-center gap-2 text-dark">
                                    {{ student.name || 'Student Name' }}
                                </h2>
                                <span class="badge bg-primary bg-opacity-10 text-primary border border-primary border-opacity-25 px-3 py-2 rounded-pill mt-2 fw-semibold shadow-sm d-inline-flex align-items-center gap-1">
                                    <i class="fas fa-id-badge"></i> {{ student.roll_number || 'N/A' }}
                                </span>
                                <span class="badge bg-primary bg-opacity-10 text-primary border border-primary border-opacity-25 px-3 py-2 rounded-pill mt-2 fw-semibold shadow-sm d-inline-flex align-items-center gap-1 mx-2">
                                    <i class="fas fa-graduation-cap"></i> {{ student.branch || 'Branch' }}
                                </span>
                            </div>
                            
                            <div class="d-flex gap-2 mt-3 mt-md-0 status-badges">
                                <span class="badge rounded-pill bg-success fw-medium px-4 py-2 shadow-sm fs-6" v-if="!student.blacklisted">
                                    <i class="fas fa-check-circle me-1"></i> Active
                                </span>
                                <span v-if="student.blacklisted" class="badge rounded-pill bg-danger fw-medium px-4 py-2 shadow-sm fs-6">
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
                    <!-- Left Side Panel (Academics & Applications) -->
                    <div class="col-lg-8 pe-lg-5">
                        <h5 class="fw-bold text-dark mt-2 mb-4 d-flex align-items-center gap-2 pb-2 border-bottom">
                            <div class="icon-square text-primary bg-primary bg-opacity-10 rounded shadow-sm d-flex align-items-center justify-content-center p-2 mb-1 me-1">
                                <i class="fas fa-file-alt"></i>
                            </div>
                            Applications History
                        </h5>
                        
                        <Table :columns="tableColumns" :data="applications">
                            <template #row="{ item: app }">
                                <td class="py-3 px-4">
                                    <div class="fw-bold text-dark">{{ app.company_name }}</div>
                                </td>
                                <td class="py-3 px-3 text-muted">
                                    <i class="fas fa-briefcase text-secondary me-1 opacity-75"></i> {{ app.drive_title }}
                                </td>
                                <td class="py-3 px-3 text-dark fw-medium text-center">
                                    <span class="badge bg-light text-dark border border-secondary border-opacity-25 px-2 py-1">
                                        {{ app.interviews_scheduled }}
                                    </span>
                                </td>
                                <td class="py-3 px-3 text-muted"><span class="d-flex align-items-center gap-1"><i class="far fa-calendar-alt opacity-75"></i> {{ formatDate(app.applied_at) }}</span></td>
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
                                    <div class="fs-1 mb-3 opacity-50">📋</div>
                                    <h5 class="fw-bold">No applications found.</h5>
                                    <p class="mb-0">This student has not applied to any drives yet.</p>
                                </td>
                            </template>
                        </Table>
                    </div>
                    
                    <!-- Right Side Panel  -->
                    <div class="col-lg-4">
                        <div class="bg-light p-4 rounded-4 border border-1 custom-contact-card h-100 shadow-sm">
                            <h6 class="fw-bold text-secondary text-uppercase mb-4 pb-2 border-bottom border-secondary border-opacity-10 d-flex justify-content-between align-items-center">
                                Academic & Contact
                                <i class="fas fa-id-card text-muted opacity-50"></i>
                            </h6>
                            
                            <div class="d-flex align-items-start mb-4">
                                <div class="icon-circle bg-white shadow-sm border text-primary flex-shrink-0 d-flex align-items-center justify-content-center mt-1">
                                    <i class="fas fa-envelope"></i>
                                </div>
                                <div class="ms-3 overflow-hidden w-100">
                                    <small class="text-muted d-block fw-medium mb-1 text-uppercase" style="font-size: 0.75rem; letter-spacing: 0.5px;">Email Address</small>
                                    <div v-if="student">
                                        <a :href="'mailto:' + student.email" class="text-dark fw-bold text-decoration-none text-truncate d-block contact-link">{{ student.email || 'N/A' }}</a>
                                    </div>
                                    <div v-else class="placeholder-glow"><span class="placeholder col-8 rounded"></span></div>
                                </div>
                            </div>

                            <div class="d-flex align-items-start mb-4">
                                <div class="icon-circle bg-white shadow-sm border text-primary flex-shrink-0 d-flex align-items-center justify-content-center mt-1">
                                    <i class="fas fa-calendar-alt"></i>
                                </div>
                                <div class="ms-3 overflow-hidden w-100">
                                    <small class="text-muted d-block fw-medium mb-1 text-uppercase" style="font-size: 0.75rem; letter-spacing: 0.5px;">Year of Study</small>
                                    <div v-if="student">
                                        <span class="text-dark fw-bold text-truncate d-block">{{ student.year_of_study || 'N/A' }}</span>
                                    </div>
                                    <div v-else class="placeholder-glow"><span class="placeholder col-8 rounded"></span></div>
                                </div>
                            </div>

                            <div class="d-flex align-items-start mb-4">
                                <div class="icon-circle bg-white shadow-sm border text-primary flex-shrink-0 d-flex align-items-center justify-content-center mt-1">
                                    <i class="fas fa-star"></i>
                                </div>
                                <div class="ms-3 overflow-hidden w-100">
                                    <small class="text-muted d-block fw-medium mb-1 text-uppercase" style="font-size: 0.75rem; letter-spacing: 0.5px;">CGPA</small>
                                    <div v-if="student">
                                        <span class="text-success fw-bold text-truncate d-block fs-5">{{ student.cgpa || 'N/A' }}</span>
                                    </div>
                                    <div v-else class="placeholder-glow"><span class="placeholder col-8 rounded"></span></div>
                                </div>
                            </div>

                            <div class="d-flex align-items-start mb-4">
                                <div class="icon-circle bg-white shadow-sm border text-primary flex-shrink-0 d-flex align-items-center justify-content-center mt-1">
                                    <i class="fas fa-file-pdf"></i>
                                </div>
                                <div class="ms-3 overflow-hidden w-100">
                                    <small class="text-muted d-block fw-medium mb-1 text-uppercase" style="font-size: 0.75rem; letter-spacing: 0.5px;">Resume</small>
                                    <div v-if="student">
                                        <a v-if="student.resume" :href="student.resume" target="_blank" class="text-primary fw-bold text-decoration-none text-truncate d-block contact-link"><i class="fas fa-external-link-alt me-1"></i> View Resume</a>
                                        <span v-else class="text-dark fw-bold">Not Uploaded</span>
                                    </div>
                                    <div v-else class="placeholder-glow"><span class="placeholder col-8 rounded"></span></div>
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
    import axios from "axios"
    import DashboardLayout from '@/components/sidebar/DashboardLayout.vue'
    import Table from '@/components/ui/Table.vue'

    const props = defineProps({
        studentId: {
            type: [String, Number],
            required: true
        }
    })

    const tableColumns = [
        { key: 'company', label: 'Company', class: 'py-3 px-4 text-secondary fw-semibold text-uppercase' },
        { key: 'drive', label: 'Drive' },
        { key: 'interviews', label: 'Interviews', class: 'py-3 px-3 text-secondary fw-semibold text-uppercase text-center' },
        { key: 'appliedAt', label: 'Applied At' },
        { key: 'status', label: 'Status', class: 'py-3 px-4 text-secondary fw-semibold text-uppercase text-center' }
    ]

    const student = ref(null)
    const applications = ref([])
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

    onMounted(async () => {
        await fetchStudent()
        await fetchApplications()
    })

    const fetchStudent = async () => {
        const token = localStorage.getItem("token")

        try {
            const res = await fetch(
            `http://127.0.0.1:5555/api/admin/student-profile/${props.studentId}`,
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
            student.value = data

        } catch (err) {
            console.error("Error:", err)
            errorMsg('Server error. Please try again later.')
        }
    }

    const fetchApplications = async () => {
        const token = localStorage.getItem("token")

        try {
            const res = await fetch(
            `http://127.0.0.1:5555/api/admin/student-applications/${props.studentId}`,
            {
                method: 'GET',
                headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
                }
            }
            )

            if (!res.ok) {
                console.error("Applications fetch failed:", res.status)
                return
            }

            const data = await res.json()
            applications.value = data

        } catch (err) {
            console.error("Applications error:", err)
        }
    }

    // Formatting Date
    const formatDate = (isoString) => {
        if (!isoString) return 'N/A'
        const date = new Date(isoString)
        const day = String(date.getDate()).padStart(2, '0')
        const month = String(date.getMonth() + 1).padStart(2, '0')
        const year = String(date.getFullYear()).slice(-2)

        return `${day}-${month}-${year}`
    }

</script>

<style scoped>

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
</style>
