<template>
<DashboardLayout :role="isAdmin ? 'admin' : 'recruiter'">
    <div class="container-fluid py-4 px-md-4">
        <!-- Page Header -->
        <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
                <h1 class="h3 fw-bold mb-1" style="color: var(--color-text);">Edit Company Profile</h1>
                <p class="text-muted mb-0">Update company information and branding details.</p>
            </div>
            <button class="btn btn-light shadow-sm border d-flex align-items-center gap-2 fw-medium px-3 rounded-3" @click="$router.go(-1)">
                <i class="fas fa-arrow-left"></i> Back
            </button>
        </div>

        <!-- Main Form -->
        <div class="row justify-content-center">
            <div class="col-lg-10 col-xl-8">
                <div class="card border-0 rounded-4 shadow-sm overflow-hidden">
                    <div class="card-header border-0 bg-primary text-white p-4">
                        <h5 class="mb-0 fw-bold">
                            <i class="fas fa-edit me-2"></i> Company Information
                        </h5>
                    </div>
                    <div class="card-body p-4 bg-white">
                        <form @submit.prevent="handleSubmit" class="row g-4">
                            <!-- Company Name -->
                            <div class="col-md-6">
                                <label class="form-label fw-semibold text-secondary small text-uppercase">Company Name <span class="text-danger">*</span></label>
                                <input v-model="formData.name" type="text" class="form-control rounded-3 border-light shadow-sm px-3 py-2.5" required>
                            </div>

                            <!-- Industry -->
                            <div class="col-md-6">
                                <label class="form-label fw-semibold text-secondary small text-uppercase">Industry</label>
                                <input v-model="formData.industry" type="text" class="form-control rounded-3 border-light shadow-sm px-3 py-2.5" placeholder="e.g. Technology, Finance">
                            </div>

                            <!-- Company Scale and Website -->
                            <div class="col-md-6">
                                <label class="form-label fw-semibold text-secondary small text-uppercase">Company Scale</label>
                                <input v-model="formData.scale" type="text" class="form-control rounded-3 border-light shadow-sm px-3 py-2.5" placeholder="e.g. 500-1000 employees">
                            </div>
                            <div class="col-md-6">
                                <label class="form-label fw-semibold text-secondary small text-uppercase">Website URL</label>
                                <input v-model="formData.website" type="url" class="form-control rounded-3 border-light shadow-sm px-3 py-2.5" placeholder="https://example.com">
                            </div>

                            <!-- Head Office and Logo URL -->
                            <div class="col-md-6">
                                <label class="form-label fw-semibold text-secondary small text-uppercase">Head Office Location</label>
                                <input v-model="formData.headOffice" type="text" class="form-control rounded-3 border-light shadow-sm px-3 py-2.5" placeholder="City, Country">
                            </div>
                            <div class="col-md-6">
                                <label class="form-label fw-semibold text-secondary small text-uppercase">Logo Image URL</label>
                                <input v-model="formData.logo" type="text" class="form-control rounded-3 border-light shadow-sm px-3 py-2.5" placeholder="https://link-to-logo.png">
                            </div>

                            <hr class="my-4 opacity-10">
                            <h6 class="fw-bold mb-1 text-dark">Point of Contact Details</h6>
                            <p class="text-muted small mb-3">These details are used for official communication.</p>

                            <!-- POC Name and POC Email -->
                            <div class="col-md-6">
                                <label class="form-label fw-semibold text-secondary small text-uppercase">POC Name</label>
                                <input v-model="formData.pocName" type="text" class="form-control rounded-3 border-light shadow-sm px-3 py-2.5">
                            </div>
                            <div class="col-md-6">
                                <label class="form-label fw-semibold text-secondary small text-uppercase">POC Email</label>
                                <input v-model="formData.pocEmail" type="email" class="form-control rounded-3 border-light shadow-sm px-3 py-2.5">
                            </div>

                            <!-- Description -->
                            <div class="col-12 mt-4">
                                <label class="form-label fw-semibold text-secondary small text-uppercase">Company Description</label>
                                <textarea v-model="formData.description" class="form-control rounded-4 border-light shadow-sm px-3 py-2.5" rows="6" placeholder="Briefly describe what your company does..."></textarea>
                            </div>

                            <div class="col-12 mt-5 d-flex justify-content-end gap-3 pb-2">
                                <button type="button" class="btn btn-light px-4 py-2.5 rounded-3 fw-semibold border shadow-sm" @click="$router.go(-1)">Cancel</button>
                                <button type="submit" class="btn btn-primary px-5 py-2.5 rounded-3 fw-semibold shadow d-flex align-items-center gap-2" :disabled="loading">
                                    <i v-if="loading" class="fas fa-spinner fa-spin"></i>
                                    <i v-else class="fas fa-save"></i>
                                    Save Profile Changes
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
import DashboardLayout from '@/components/sidebar/DashboardLayout.vue'

// This one loads the data into the edit form
const route = useRoute()
// This one saves data after editing
const router = useRouter()

const user = JSON.parse(localStorage.getItem('user') || '{}')
const isAdmin = computed(() => user.type === 'admin')
const companyId = computed(() => route.params.id || user.id)

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

onMounted(async () => {
    await fetchCompanyData()
})

// # Fetch Company Profile 
const fetchCompanyData = async () => {
    loading.value = true
    const token = localStorage.getItem('token')
    const id = companyId.value
    if (!id) return

    try {
        const res = await fetch(`http://127.0.0.1:5555/api/company-profile/${id}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        if (res.ok) {
            const data = await res.json()
            formData.value = {
                ...data,
                logo: data.logo || data.icon || ''
            }
        }
    } catch (err) {
        console.error('Error fetching company data:', err)
    } finally {
        loading.value = false
    }
}

// #Updates the company details 
const handleSubmit = async () => {
    loading.value = true
    const token = localStorage.getItem('token')
    
    // Choose endpoint based on who is editing, Admin can edit or company itsef can edit their profile!
    const url = isAdmin.value 
        ? `http://127.0.0.1:5555/api/admin/update-company/${companyId.value}`
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
            router.go(-1)
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
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(120, 31, 25, 0.2) !important;
}

.form-control:focus {
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

input::placeholder, textarea::placeholder {
    color: #a0aec0;
    font-size: 0.9rem;
}
</style>