<template>
<DashboardLayout role="recruiter">
    <div class="mt-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
                <h1 class="h3 fw-bold mb-1" style="color: var(--color-text);">Drive Management</h1>
                <p class="text-muted mb-0">Manage and track all your hiring drives in one place.</p>
            </div>
            <button @click="navigateToCreate" class="btn btn-primary shadow-sm border-0 d-flex align-items-center gap-2 fw-medium px-4 rounded-3">
                <i class="fas fa-plus-circle"></i> Create Drive
            </button>
        </div>

        <div class="card shadow-sm border-0 bg-white rounded-4 overflow-hidden mb-4">
            <div class="card-body p-4">
                <CompanyDrives :key="refreshKey" :companyId="companyId" role="recruiter" />
            </div>
        </div>
    </div>
</DashboardLayout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()
import DashboardLayout from '@/components/sidebar/DashboardLayout.vue'
import CompanyDrives from '@/components/layout/CompanyDrives.vue'

const user = JSON.parse(localStorage.getItem('user') || '{}')
const companyId = user.id

const showCreateModal = ref(false)
const refreshKey = ref(0)

const handleSuccess = () => {
    refreshKey.value++
}

const navigateToCreate = () => {
        router.push(`/company/drive/create`)
    }

</script>


<style scoped>
.btn-primary {
    background-color: var(--color-primary, #781f19);
    border: none;
    transition: all 0.2s ease;
}

.btn-primary:hover {
    background-color: #5a1712;
    transform: translateY(-1px);
}
</style>