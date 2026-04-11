<template>
<div class="modal fade show d-block" tabindex="-1" style="background: rgba(0,0,0,0.5);">
    <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content border-0 rounded-4 shadow-lg overflow-hidden">
            <div class="modal-header border-0 bg-primary text-white p-4">
                <h5 class="modal-title fw-bold">
                    <i class="fas" :class="driveId ? 'fa-edit' : 'fa-plus-circle'"></i>
                    {{ driveId ? 'Edit Hiring Drive' : 'Create New Hiring Drive' }}
                </h5>
                <button type="button" class="btn-close btn-close-white" @click="$emit('close')"></button>
            </div>
            <div class="modal-body p-4 bg-light bg-opacity-50">
                <form @submit.prevent="handleSubmit" class="row g-3">
                    <!-- Title -->
                    <div class="col-12">
                        <label class="form-label fw-semibold">Drive Title <span class="text-danger">*</span></label>
                        <input v-model="formData.title" type="text" class="form-control rounded-3 border-0 shadow-sm px-3 py-2" placeholder="e.g. Software Engineer Intern - Summer 2024" required>
                    </div>

                    <!-- Work Mode and Location -->
                    <div class="col-md-6">
                        <label class="form-label fw-semibold">Work Mode</label>
                        <select v-model="formData.workMode" class="form-select rounded-3 border-0 shadow-sm px-3 py-2">
                            <option value="In-Office">In-Office</option>
                            <option value="Remote">Remote</option>
                            <option value="Hybrid">Hybrid</option>
                        </select>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label fw-semibold">Location</label>
                        <input v-model="formData.location" type="text" class="form-control rounded-3 border-0 shadow-sm px-3 py-2" placeholder="e.g. Bangalore, Mumbai">
                    </div>

                    <!-- Pay Scale and Positions -->
                    <div class="col-md-6">
                        <label class="form-label fw-semibold">Pay Scale / Package</label>
                        <input v-model="formData.payScale" type="text" class="form-control rounded-3 border-0 shadow-sm px-3 py-2" placeholder="e.g. 12 LPA - 15 LPA">
                    </div>
                    <div class="col-md-6">
                        <label class="form-label fw-semibold">Total Positions</label>
                        <input v-model="formData.positions" type="number" class="form-control rounded-3 border-0 shadow-sm px-3 py-2" placeholder="e.g. 10">
                    </div>

                    <!-- Batch and Branches -->
                    <div class="col-md-6">
                        <label class="form-label fw-semibold">Eligible Batches</label>
                        <input v-model="formData.batch" type="text" class="form-control rounded-3 border-0 shadow-sm px-3 py-2" placeholder="e.g. 2024, 2025">
                    </div>
                    <div class="col-md-6">
                        <label class="form-label fw-semibold">Eligible Branches</label>
                        <input v-model="formData.branches" type="text" class="form-control rounded-3 border-0 shadow-sm px-3 py-2" placeholder="e.g. CSE, ECE, EE">
                    </div>

                    <!-- Eligibility and Deadline -->
                    <div class="col-md-6">
                        <label class="form-label fw-semibold">Eligibility Criteria</label>
                        <input v-model="formData.eligibility" type="text" class="form-control rounded-3 border-0 shadow-sm px-3 py-2" placeholder="e.g. 7.5 CGPA and above">
                    </div>
                    <div class="col-md-6">
                        <label class="form-label fw-semibold">Application Deadline</label>
                        <input v-model="formData.deadline" type="date" class="form-control rounded-3 border-0 shadow-sm px-3 py-2">
                    </div>

                    <!-- Interview Rounds -->
                    <div class="col-12">
                        <label class="form-label fw-semibold">Interview Rounds</label>
                        <input v-model="formData.interviewRounds" type="text" class="form-control rounded-3 border-0 shadow-sm px-3 py-2" placeholder="e.g. OA + 2 Technical + 1 HR">
                    </div>

                    <!-- Skills Required -->
                    <div class="col-12">
                        <label class="form-label fw-semibold">Required Skills</label>
                        <input v-model="formData.skillsRequired" type="text" class="form-control rounded-3 border-0 shadow-sm px-3 py-2" placeholder="e.g. Python, SQL, React, AWS">
                    </div>

                    <!-- Description -->
                    <div class="col-12">
                        <label class="form-label fw-semibold">Job Description</label>
                        <textarea v-model="formData.description" class="form-control rounded-4 border-0 shadow-sm px-3 py-2" rows="4" placeholder="Detailed description of the role, responsibilities, etc."></textarea>
                    </div>

                    <div class="col-12 mt-4 d-flex justify-content-end gap-2">
                        <button type="button" class="btn btn-light px-4 py-2 rounded-3 fw-medium" @click="$emit('close')">Cancel</button>
                        <button type="submit" class="btn btn-primary px-4 py-2 rounded-3 fw-medium d-flex align-items-center gap-2" :disabled="loading">
                            <i v-if="loading" class="fas fa-spinner fa-spin"></i>
                            {{ driveId ? 'Update Drive' : 'Create Drive' }}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
    driveId: {
        type: [Number, String],
        default: null
    }
})

const emit = defineEmits(['close', 'success'])

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
    if (props.driveId) {
        await fetchDriveDetails()
    }
})

const fetchDriveDetails = async () => {
    loading.value = true
    const token = localStorage.getItem('token')
    try {
        const res = await fetch(`http://127.0.0.1:5555/api/company/drive-details/${props.driveId}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        if (res.ok) {
            const data = await res.json()
            // Format deadline date for input type="date"
            let deadline = ''
            if (data.deadline) {
                deadline = data.deadline.split('T')[0]
            }
            formData.value = { ...data, deadline }
        }
    } catch (err) {
        console.error('Error fetching drive details:', err)
    } finally {
        loading.value = false
    }
}

const handleSubmit = async () => {
    loading.value = true
    const token = localStorage.getItem('token')
    const url = props.driveId 
        ? `http://127.0.0.1:5555/api/company/update-drive/${props.driveId}`
        : 'http://127.0.0.1:5555/api/company/create-drive'
    
    // Method for update should be PUT or POST based on backend implementation
    // I implemented both PUT and POST for update in company.py
    const method = props.driveId ? 'POST' : 'POST' 

    try {
        const res = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(formData.value)
        })

        if (res.ok) {
            emit('success')
            emit('close')
        } else {
            const error = await res.json()
            alert(error.error || 'Something went wrong')
        }
    } catch (err) {
        console.error('Error saving drive:', err)
        alert('Network error')
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
}

.modal-content {
    animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.form-control:focus, .form-select:focus {
    box-shadow: 0 0 0 3px rgba(120, 31, 25, 0.15);
    border-color: var(--color-primary, #781f19);
}

.form-label {
    color: #4a5568;
    font-size: 0.9rem;
}
</style>
