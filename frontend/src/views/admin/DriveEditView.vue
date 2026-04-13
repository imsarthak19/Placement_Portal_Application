<template>
<DashboardLayout :role="isAdmin ? 'admin' : 'recruiter'">
    <div class="container-fluid py-4 px-md-4">
        <!-- Page Header -->
        <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
                <h1 class="h3 fw-bold mb-1" style="color: var(--color-text);">
                    {{ driveId ? 'Edit Hiring Drive' : 'Create New Hiring Drive' }}
                </h1>
                <p class="text-muted mb-0">Manage job details, eligibility criteria, and application settings.</p>
            </div>
            <button class="btn btn-light shadow-sm border d-flex align-items-center gap-2 fw-medium px-3 rounded-3" @click="$router.go(-1)">
                <i class="fas fa-arrow-left"></i> Back
            </button>
        </div>

        <div class="row justify-content-center">
            <div class="col-lg-10 col-xl-8">
                <div class="card border-0 rounded-4 shadow-sm overflow-hidden mb-5">
                    <div class="card-header border-0 bg-primary text-white p-4">
                        <h5 class="mb-0 fw-bold">
                            <i class="fas" :class="driveId ? 'fa-edit' : 'fa-plus-circle'"></i>
                            {{ driveId ? 'Drive Specifics' : 'Drive Details' }}
                        </h5>
                    </div>
                    <div class="card-body p-4 bg-white">
                        <form @submit.prevent="handleSubmit" class="row g-4">
                            <!-- Title -->
                            <div class="col-12">
                                <label class="form-label fw-semibold text-secondary small text-uppercase">Drive Title <span class="text-danger">*</span></label>
                                <input v-model="formData.title" type="text" class="form-control rounded-3 border-light shadow-sm px-3 py-2.5" placeholder="e.g. Software Engineer Intern - Summer 2024" required>
                            </div>

                            <!-- Work Mode and Location -->
                            <div class="col-md-6">
                                <label class="form-label fw-semibold text-secondary small text-uppercase">Work Mode</label>
                                <select v-model="formData.workMode" class="form-select rounded-3 border-light shadow-sm px-3 py-2.5">
                                    <option value="In-Office">In-Office</option>
                                    <option value="Remote">Remote</option>
                                    <option value="Hybrid">Hybrid</option>
                                </select>
                            </div>
                            <div class="col-md-6">
                                <label class="form-label fw-semibold text-secondary small text-uppercase">Location</label>
                                <input v-model="formData.location" type="text" class="form-control rounded-3 border-light shadow-sm px-3 py-2.5" placeholder="e.g. Bangalore, Mumbai">
                            </div>

                            <!-- Pay Scale and Positions -->
                            <div class="col-md-6">
                                <label class="form-label fw-semibold text-secondary small text-uppercase">Pay Scale / Package</label>
                                <input v-model="formData.payScale" type="text" class="form-control rounded-3 border-light shadow-sm px-3 py-2.5" placeholder="e.g. 12 LPA - 15 LPA">
                            </div>
                            <div class="col-md-6">
                                <label class="form-label fw-semibold text-secondary small text-uppercase">Total Positions</label>
                                <input v-model="formData.positions" type="number" class="form-control rounded-3 border-light shadow-sm px-3 py-2.5" placeholder="e.g. 10">
                            </div>

                            <hr class="my-3 opacity-10">
                            <h6 class="fw-bold mb-0 text-dark">Candidate Requirements</h6>

                            <!-- Batch and Branches -->
                            <div class="col-md-6">
                                <label class="form-label fw-semibold text-secondary small text-uppercase">Eligible Batches</label>
                                <input v-model="formData.batch" type="text" class="form-control rounded-3 border-light shadow-sm px-3 py-2.5" placeholder="e.g. 2024, 2025">
                            </div>
                            <div class="col-md-6">
                                <label class="form-label fw-semibold text-secondary small text-uppercase">Eligible Branches</label>
                                <input v-model="formData.branches" type="text" class="form-control rounded-3 border-light shadow-sm px-3 py-2.5" placeholder="e.g. CSE, ECE, EE">
                            </div>

                            <!-- Eligibility and Deadline -->
                            <div class="col-md-6">
                                <label class="form-label fw-semibold text-secondary small text-uppercase">Eligibility Criteria</label>
                                <input v-model="formData.eligibility" type="text" class="form-control rounded-3 border-light shadow-sm px-3 py-2.5" placeholder="e.g. 7.5 CGPA and above">
                            </div>
                            <div class="col-md-6">
                                <label class="form-label fw-semibold text-secondary small text-uppercase">Application Deadline</label>
                                <input v-model="formData.deadline" type="date" class="form-control rounded-3 border-light shadow-sm px-3 py-2.5">
                            </div>

                            <!-- Interview Rounds -->
                            <div class="col-12">
                                <label class="form-label fw-semibold text-secondary small text-uppercase">Interview Rounds</label>
                                <input v-model="formData.interviewRounds" type="text" class="form-control rounded-3 border-light shadow-sm px-3 py-2.5" placeholder="e.g. OA + 2 Technical + 1 HR">
                            </div>

                            <!-- Skills Required -->
                            <div class="col-12">
                                <label class="form-label fw-semibold text-secondary small text-uppercase">Required Skills</label>
                                <input v-model="formData.skillsRequired" type="text" class="form-control rounded-3 border-light shadow-sm px-3 py-2.5" placeholder="e.g. Python, SQL, React, AWS">
                            </div>

                            <!-- Description -->
                            <div class="col-12">
                                <label class="form-label fw-semibold text-secondary small text-uppercase">Job Description</label>
                                <textarea v-model="formData.description" class="form-control rounded-4 border-light shadow-sm px-3 py-2.5" rows="6" placeholder="Detailed description of the role, responsibilities, etc."></textarea>
                            </div>

                            <div class="col-12 mt-5 d-flex justify-content-end gap-3 pb-2">
                                <button type="button" class="btn btn-light px-4 py-2.5 rounded-3 fw-semibold border shadow-sm" @click="$router.go(-1)">Cancel</button>
                                <button type="submit" class="btn btn-primary px-5 py-2.5 rounded-3 fw-semibold shadow d-flex align-items-center gap-2" :disabled="loading">
                                    <i v-if="loading" class="fas fa-spinner fa-spin"></i>
                                    <i v-else class="fas fa-check-circle"></i>
                                    {{ driveId ? 'Update Hiring Drive' : 'Create Hiring Drive' }}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</DashboardLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import DashboardLayout from '@/components/sidebar/DashboardLayout.vue'

const route = useRoute()
const router = useRouter()

const user = JSON.parse(localStorage.getItem('user') || '{}')
const isAdmin = computed(() => user.type === 'admin')
const driveId = computed(() => route.params.id)

const loading = ref(false)
const formData = ref({
    title: '',
    description: '',
    eligibility: '',
    batch: '',
    branches: '',
    skillsRequired: '',
    payScale: '',
    location: '',
    workMode: 'In-Office',
    interviewRounds: '',
    positions: null,
    deadline: ''
})

onMounted(async () => {
    if (driveId.value) {
        await fetchDriveDetails()
    }
})

// Fetch drive details for editing
const fetchDriveDetails = async () => {
    loading.value = true
    const token = localStorage.getItem('token')
    try {
        const res = await fetch(`http://127.0.0.1:5555/api/company/drive-details/${driveId.value}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        
        if (res.ok) {
            const data = await res.json()
            let deadline = ''
            if (data.deadline) {
                deadline = data.deadline.split('T')[0]
            }
            // Populate form with fetched data
            formData.value = { 
                title: data.title || '',
                description: data.description || '',
                eligibility: data.eligibility || '',
                batch: data.batch || '',
                branches: data.branches || '',
                skillsRequired: data.skillsRequired || '',
                payScale: data.payScale || '',
                location: data.location || '',
                workMode: data.workMode || 'In-Office',
                interviewRounds: data.interviewRounds || '',
                positions: data.positions || null,
                deadline: deadline
            }
        } else {
            const errData = await res.json()
            alert('Failed to load drive: ' + (errData.error || 'Server error'))
        }
    } catch (err) {
        console.error('Error fetching drive details:', err)
        alert('Network error while loading data')
    } finally {
        loading.value = false
    }
}

// Updated the drives either by company or admin
const handleSubmit = async () => {
    loading.value = true
    const token = localStorage.getItem('token')
    
    const url = driveId.value 
        ? `http://127.0.0.1:5555/api/company/update-drive/${driveId.value}`
        : 'http://127.0.0.1:5555/api/company/create-drive'
    
    const method = driveId.value ? 'put' : 'post'

    try {
        const res = await axios({
            url: url,
            method: method,
            headers: {
                'Authorization': `Bearer ${token}`
            },
            data: formData.value
        })

        if (res.status === 200 || res.status === 201) {
            router.go(-1)
        }
    } catch (err) {
        console.error('Error saving drive:', err)
        alert(err.response?.data?.error || 'Failed to save drive details')
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
.bg-primary {
    background-color: var(--color-primary, #781f19) !important;
}

.btn-primary {
    background-color: var(--color-primary, #781f19);
    border: none;
}

.btn-primary:hover {
    background-color: #5a1712;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(120, 31, 25, 0.2) !important;
}

.form-control:focus, .form-select:focus {
    border-color: var(--color-primary, #781f19);
    box-shadow: 0 0 0 0.25rem rgba(120, 31, 25, 0.1);
}

.card {
    transition: all 0.3s ease;
}

.form-label {
    letter-spacing: 0.5px;
    margin-bottom: 0.5rem;
}
</style>
