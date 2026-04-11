<template>
<div class="modal fade show d-block" tabindex="-1" style="background: rgba(0,0,0,0.5);">
    <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content border-0 rounded-4 shadow-lg overflow-hidden">
            <div class="modal-header border-0 bg-primary text-white p-4">
                <h5 class="modal-title fw-bold">
                    <i class="fas fa-edit"></i> Edit Company Profile
                </h5>
                <button type="button" class="btn-close btn-close-white" @click="$emit('close')"></button>
            </div>
            <div class="modal-body p-4 bg-light bg-opacity-50">

                <!-- Form to edit the profile -->
                <form @submit.prevent="handleSubmit" class="row g-3">
                    
                    <!-- Company Name -->
                    <div class="col-md-6">
                        <label class="form-label fw-semibold">Company Name <span class="text-danger">*</span></label>
                        <input v-model="formData.name" type="text" class="form-control rounded-3 border-0 shadow-sm px-3 py-2" required>
                    </div>

                    <!-- Industry -->
                    <div class="col-md-6">
                        <label class="form-label fw-semibold">Industry</label>
                        <input v-model="formData.industry" type="text" class="form-control rounded-3 border-0 shadow-sm px-3 py-2" placeholder="e.g. Technology, Finance">
                    </div>

                    <!-- Company Scale and Website -->
                    <div class="col-md-6">
                        <label class="form-label fw-semibold">Company Scale</label>
                        <input v-model="formData.scale" type="text" class="form-control rounded-3 border-0 shadow-sm px-3 py-2" placeholder="e.g. 500-1000 employees">
                    </div>
                    <div class="col-md-6">
                        <label class="form-label fw-semibold">Website URL</label>
                        <input v-model="formData.website" type="url" class="form-control rounded-3 border-0 shadow-sm px-3 py-2" placeholder="https://example.com">
                    </div>

                    <!-- Head Office and Logo URL -->
                    <div class="col-md-6">
                        <label class="form-label fw-semibold">Head Office Location</label>
                        <input v-model="formData.headOffice" type="text" class="form-control rounded-3 border-0 shadow-sm px-3 py-2" placeholder="City, Country">
                    </div>
                    <div class="col-md-6">
                        <label class="form-label fw-semibold">Logo Image URL</label>
                        <input v-model="formData.logo" type="text" class="form-control rounded-3 border-0 shadow-sm px-3 py-2" placeholder="https://link-to-logo.png">
                    </div>

                    <hr class="my-4 text-muted opacity-25">
                    <h6 class="fw-bold mb-0">Point of Contact Details</h6>

                    <!-- POC Name and POC Email -->
                    <div class="col-md-6">
                        <label class="form-label fw-semibold">POC Name</label>
                        <input v-model="formData.pocName" type="text" class="form-control rounded-3 border-0 shadow-sm px-3 py-2">
                    </div>
                    <div class="col-md-6">
                        <label class="form-label fw-semibold">POC Email</label>
                        <input v-model="formData.pocEmail" type="email" class="form-control rounded-3 border-0 shadow-sm px-3 py-2">
                    </div>

                    <!-- Description -->
                    <div class="col-12">
                        <label class="form-label fw-semibold">Company Description</label>
                        <textarea v-model="formData.description" class="form-control rounded-4 border-0 shadow-sm px-3 py-2" rows="4" placeholder="Briefly describe what your company does..."></textarea>
                    </div>

                    <div class="col-12 mt-4 d-flex justify-content-end gap-2">
                        <button type="button" class="btn btn-light px-4 py-2 rounded-3 fw-medium" @click="$emit('close')">Cancel</button>
                        <button type="submit" class="btn btn-primary px-4 py-2 rounded-3 fw-medium d-flex align-items-center gap-2" :disabled="loading">
                            <i v-if="loading" class="fas fa-spinner fa-spin"></i>
                            Save Changes
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
    companyId: {
        type: [Number, String],
        required: true
    },
    initialData: {
        type: Object,
        default: () => ({})
    },
    isAdmin: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits(['close', 'success'])

const loading = ref(false)
const formData = ref({
    name: '',
    industry: '',
    scale: '',
    website: '',
    headOffice: '',
    logo: '',
    pocName: '',
    pocEmail: '',
    description: ''
})

onMounted(() => {
    if (props.initialData && Object.keys(props.initialData).length > 0) {
        // Map icon to logo if needed, based on common.py output
        formData.value = { 
            ...props.initialData,
            logo: props.initialData.logo || props.initialData.icon || ''
        }
    }
})

const handleSubmit = async () => {
    loading.value = true
    const token = localStorage.getItem('token')
    
    // Choose endpoint based on who is editing
    const url = props.isAdmin 
        ? `http://127.0.0.1:5555/api/admin/update-company/${props.companyId}`
        : 'http://127.0.0.1:5555/api/company/update-profile'

    try {
        const res = await fetch(url, {
            method: 'PUT',
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
        console.error('Error updating profile:', err)
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
