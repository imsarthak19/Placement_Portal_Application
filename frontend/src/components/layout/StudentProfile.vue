<template>
  <DashboardLayout :role="userType">
    <div class="container-fluid py-4 px-md-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
                <h1 class="h3 fw-bold mb-1" style="color: var(--color-text);">{{ isOwner ? 'My Profile' : 'Student Profile' }}</h1>
                <p class="text-muted mb-0">View {{ isOwner ? 'and manage your' : 'detailed information and application history of this' }} student profile.</p>
            </div>
            <div class="d-flex gap-2">
                <button v-if="isOwner && !isEditing" class="btn btn-primary shadow-sm d-flex align-items-center gap-2 fw-medium px-4 rounded-pill" @click="toggleEdit">
                    <i class="fas fa-edit"></i> Edit Profile
                </button>
                <button v-if="isEditing" class="btn btn-success shadow-sm d-flex align-items-center gap-2 fw-medium px-4 rounded-pill" @click="saveProfile">
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
                                <div v-if="!isEditing">
                                    <span class="badge bg-primary bg-opacity-10 text-primary border border-primary border-opacity-25 px-3 py-2 rounded-pill mt-2 fw-semibold shadow-sm d-inline-flex align-items-center gap-1">
                                        <i class="fas fa-id-badge"></i> {{ student.roll_number || 'Roll Number Not Set' }}
                                    </span>
                                    <span class="badge bg-primary bg-opacity-10 text-primary border border-primary border-opacity-25 px-3 py-2 rounded-pill mt-2 fw-semibold shadow-sm d-inline-flex align-items-center gap-1 mx-2">
                                        <i class="fas fa-graduation-cap"></i> {{ student.branch || 'Branch Not Set' }}
                                    </span>
                                </div>
                                <div v-else class="mt-3">
                                    <div class="row g-3">
                                        <div class="col-md-6">
                                            <label class="form-label small fw-bold text-muted text-uppercase">Roll Number</label>
                                            <input type="text" v-model="editForm.roll_number" class="form-control rounded-3" placeholder="Enter Roll Number">
                                        </div>
                                        <div class="col-md-6">
                                            <label class="form-label small fw-bold text-muted text-uppercase">Branch</label>
                                            <input type="text" v-model="editForm.branch" class="form-control rounded-3" placeholder="Enter Branch (e.g. CSE)">
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="d-flex gap-2 mt-3 mt-md-0 status-badges align-self-start">
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
                    <div class="col-lg-7 pe-lg-4">
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
                                        {{ app.interviews_scheduled || 0 }}
                                    </span>
                                </td>
                                <td class="py-3 px-3 text-muted"><span class="d-flex align-items-center gap-1"><i class="far fa-calendar-alt opacity-75"></i> {{ formatDate(app.applied_at) }}</span></td>
                                <td class="py-3 px-4 text-center">
                                    <span class="badge rounded-pill px-3 py-2 fw-medium shadow-sm border"
                                          :class="{
                                              'bg-info bg-opacity-10 text-info border-info border-opacity-25': app.status.toLowerCase() === 'applied' || app.status.toLowerCase() === 'pending',
                                              'bg-warning bg-opacity-10 text-warning border-warning border-opacity-25': app.status.toLowerCase() === 'shortlisted',
                                              'bg-primary bg-opacity-10 text-primary border-primary border-opacity-25': app.status.toLowerCase() === 'interviewing',
                                              'bg-success bg-opacity-10 text-success border-success border-opacity-25': ['hired', 'selected', 'offered', 'placed'].includes(app.status.toLowerCase()),
                                              'bg-danger bg-opacity-10 text-danger border-danger border-opacity-25': app.status.toLowerCase() === 'rejected'
                                          }">
                                        {{ app.status }}
                                    </span>
                                </td>
                            </template>
                            <template #empty>
                                <td colspan="5" class="text-center py-5 text-muted">
                                    <div class="fs-1 mb-3 opacity-50">📋</div>
                                    <h5 class="fw-bold">{{ isOwner ? "You haven't applied yet" : "No applications found" }}</h5>
                                    <p class="mb-0">{{ isOwner ? "Start applying for drives to see them here." : "This student has not applied to any drives yet." }}</p>
                                </td>
                            </template>
                        </Table>
                    </div>
                    
                    <!-- Right Side Panel  -->
                    <div class="col-lg-5">
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
                                    <small class="text-muted d-block fw-medium mb-1 text-uppercase" style="font-size: 0.75rem; letter-spacing: 0.5px;">Year of Graduation</small>
                                    <div v-if="!isEditing">
                                        <div v-if="student">
                                            <span class="text-dark fw-bold text-truncate d-block">{{ student.year_of_study || 'N/A' }}</span>
                                        </div>
                                        <div v-else class="placeholder-glow"><span class="placeholder col-8 rounded"></span></div>
                                    </div>
                                    <div v-else>
                                        <select v-model="editForm.year_of_study" class="form-select form-select-sm rounded-3">
                                            <option value="">Select Year</option>
                                            <option v-for="year in [2022, 2023, 2024, 2025, 2026, 2027]" :key="year" :value="year">{{ year }}</option>
                                        </select>
                                    </div>
                                </div>
                            </div>

                            <div class="d-flex align-items-start mb-4">
                                <div class="icon-circle bg-white shadow-sm border text-primary flex-shrink-0 d-flex align-items-center justify-content-center mt-1">
                                    <i class="fas fa-star"></i>
                                </div>
                                <div class="ms-3 overflow-hidden w-100">
                                    <small class="text-muted d-block fw-medium mb-1 text-uppercase" style="font-size: 0.75rem; letter-spacing: 0.5px;">CGPA</small>
                                    <div v-if="!isEditing">
                                        <div v-if="student">
                                            <span class="text-success fw-bold text-truncate d-block fs-5">{{ student.cgpa || 'N/A' }}</span>
                                        </div>
                                        <div v-else class="placeholder-glow"><span class="placeholder col-8 rounded"></span></div>
                                    </div>
                                    <div v-else>
                                        <input type="number" step="0.01" min="0" max="10" v-model="editForm.cgpa" class="form-control form-control-sm rounded-3" placeholder="Enter CGPA">
                                    </div>
                                </div>
                            </div>

                            <div class="d-flex align-items-start mb-4">
                                <div class="icon-circle bg-white shadow-sm border text-primary flex-shrink-0 d-flex align-items-center justify-content-center mt-1">
                                    <i class="fas fa-file-pdf"></i>
                                </div>
                                <div class="ms-3 overflow-hidden w-100">
                                    <small class="text-muted d-block fw-medium mb-1 text-uppercase" style="font-size: 0.75rem; letter-spacing: 0.5px;">Resume Link</small>
                                    <div v-if="!isEditing">
                                        <div v-if="student">
                                            <a v-if="student.resume" :href="student.resume" target="_blank" class="text-primary fw-bold text-decoration-none text-truncate d-block contact-link"><i class="fas fa-external-link-alt me-1"></i> View Resume</a>
                                            <span v-else class="text-dark fw-bold">Not Uploaded</span>
                                        </div>
                                        <div v-else class="placeholder-glow"><span class="placeholder col-8 rounded"></span></div>
                                    </div>
                                    <div v-else>
                                        <input type="text" v-model="editForm.resume" class="form-control form-control-sm rounded-3" placeholder="Enter Resume URL">
                                    </div>
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
    import { useRouter } from 'vue-router'
    import axios from "axios"
    import DashboardLayout from '@/components/sidebar/DashboardLayout.vue'
    import Table from '@/components/ui/Table.vue'

    const props = defineProps({
        studentId: {
            type: [String, Number],
            required: false,
            default: null
        }
    })

    const router = useRouter()

    const tableColumns = [
        { key: 'company', label: 'Company', class: 'py-3 px-4 text-secondary fw-semibold text-uppercase' },
        { key: 'drive', label: 'Drive' },
        { key: 'interviews', label: 'Interviews', class: 'py-3 px-3 text-secondary fw-semibold text-uppercase text-center' },
        { key: 'appliedAt', label: 'Applied At' },
        { key: 'status', label: 'Status', class: 'py-3 px-4 text-secondary fw-semibold text-uppercase text-center' }
    ]

    const student = ref(null)
    const editForm = ref({
        roll_number: '',
        branch: '',
        year_of_study: '',
        cgpa: '',
        resume: ''
    })
    const isEditing = ref(false)
    const applications = ref([])
    const flashMsg = ref('')
    const flashMsgError = ref('')
    const currentUser = JSON.parse(localStorage.getItem('user'))
    const userType = currentUser?.type || 'student'
    const isOwner = computed(() => userType === 'student' && (!props.studentId || props.studentId == currentUser.id))

    const showFlash = (message) => {
        flashMsg.value = message
        setTimeout(() => { flashMsg.value = "" }, 3000)
    }

    const errorMsg = (message) => {
        flashMsgError.value = message
        setTimeout(() => { flashMsgError.value = "" }, 3000)
    }

    onMounted(async () => {
        await fetchStudent()
        await fetchApplications()
    })

    const fetchStudent = async () => {
        const token = localStorage.getItem("token")
        let url = `http://127.0.0.1:5555/api/admin/student-profile/${props.studentId}`
        
        if (userType === 'student') {
            url = `http://127.0.0.1:5555/api/student/profile`
        }

        try {
            const res = await fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            })

            if (!res.ok) {
                console.error("Request failed:", res.status)
                if (res.status === 404 && userType === 'student') {
                    // Profile doesn't exist yet, that's fine for students
                    student.value = { name: currentUser.username, email: '', roll_number: '', branch: '', year_of_study: '', cgpa: '', resume: '' }
                    return
                }
                return
            }

            const data = await res.json()
            student.value = data
            // Initialize edit form
            editForm.value = {
                roll_number: data.roll_number || '',
                branch: data.branch || '',
                year_of_study: data.year_of_study || '',
                cgpa: data.cgpa || '',
                resume: data.resume || ''
            }

        } catch (err) {
            console.error("Error:", err)
            errorMsg('Server error. Please try again later.')
        }
    }

    const fetchApplications = async () => {
        const token = localStorage.getItem("token")
        let url = `http://127.0.0.1:5555/api/admin/student-applications/${props.studentId}`
        
        if (userType === 'student') {
            url = `http://127.0.0.1:5555/api/student/applications`
        }

        try {
            const res = await fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            })

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

    const toggleEdit = () => {
        isEditing.value = !isEditing.value
        if (!isEditing.value) {
            // Reset form if cancelled
            editForm.value = {
                roll_number: student.value.roll_number || '',
                branch: student.value.branch || '',
                year_of_study: student.value.year_of_study || '',
                cgpa: student.value.cgpa || '',
                resume: student.value.resume || ''
            }
        }
    }

    const saveProfile = async () => {
        const token = localStorage.getItem("token")
        
        try {
            const res = await fetch('http://127.0.0.1:5555/api/student/profile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(editForm.value)
            })

            const data = await res.json()

            if (res.ok) {
                showFlash(data.message)
                isEditing.value = false
                await fetchStudent()
            } else {
                errorMsg(data.message || 'Failed to update profile')
            }
        } catch (err) {
            console.error("Save error:", err)
            errorMsg('Server error. Please try again later.')
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
