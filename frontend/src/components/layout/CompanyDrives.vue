<template>
    <div class="mt-4">
        <Table :columns="tableColumns" :data="drives">
            <template #row="{ item: drive }">
                <td class="py-3 px-4">
                    <router-link :to="`/${rolePrefix}/drive/${drive.id}`" class="text-decoration-none">
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
                <td class="py-3 px-3 text-muted">
                    <span class="d-flex align-items-center gap-1">
                        <i class="far fa-calendar-alt opacity-75"></i> {{ formatDate(drive.created_at) }}
                    </span>
                </td>
                <td class="py-3 px-4 text-center">
                    <span class="badge px-3 py-2 fw-medium shadow-sm"
                          :class="{
                              'bg-success': drive.status === 'Active',
                              'bg-secondary': drive.status === 'Closed',
                              'bg-warning text-dark': drive.status === 'Unapproved'
                          }">
                        {{ drive.status }}
                    </span>
                </td>
                <td class="py-3 px-4 text-center">
                    <div class="d-flex gap-2 justify-content-center">
                        <router-link :to="`/${rolePrefix}/drive/${drive.id}`" class="btn btn-sm btn-primary border-0 shadow-sm px-3 py-2 rounded-3 view-btn">
                            <i class="fas fa-eye me-1"></i> View
                        </router-link>
                        <button v-if="role === 'recruiter'" @click="navigateToEdit(drive.id)" class="btn btn-sm btn-outline-secondary shadow-sm px-3 py-2 rounded-3 edit-btn">
                            <i class="fas fa-edit me-1"></i> Edit
                        </button>
                        <button v-if="role === 'recruiter' && drive.status === 'Active'" @click="handleCloseDrive(drive.id)" class="btn btn-sm btn-danger border-0 shadow-sm px-3 py-2 rounded-3 close-btn">
                            <i class="fas fa-times-circle me-1"></i> Close
                        </button>
                    </div>
                </td>
            </template>
            <template #empty>
                <td colspan="8" class="text-center py-5 text-muted">
                    <div class="fs-1 mb-3 opacity-50">📋</div>
                    <h5 class="fw-bold">No drives posted yet</h5>
                    <p class="mb-0">Once the company posts hiring drives, they will appear here.</p>
                </td>
            </template>
        </Table>

        <!-- Edit Drive Modal Removed -->
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import Table from '@/components/ui/Table.vue'

const props = defineProps({
    companyId: {
        type: [String, Number],
        required: true
    },
    role: {
        type: String,
        default: 'admin' // or 'company'
    }
})

const router = useRouter()
const drives = ref([])

const navigateToEdit = (id) => {
    if (props.role === 'admin') {
        router.push(`/admin/drive/${id}/edit`)
    } else {
        router.push(`/company/drive/${id}/edit`)
    }
}
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

const rolePrefix = computed(() => props.role === 'admin' ? 'admin' : 'company')

onMounted(async () => {
    await fetchDrives()
})

const fetchDrives = async () => {
    const token = localStorage.getItem("token")
    try {
        const res = await fetch(
            `http://127.0.0.1:5555/api/company/all-drives/${props.companyId}`,
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
        drives.value = data
    } catch (err) {
        console.error("Drives error:", err)
    }
}

const handleCloseDrive = async (id) => {
    if (!confirm('Are you sure you want to close this drive?')) return
    
    const token = localStorage.getItem("token")
    try {
        const res = await fetch(`http://127.0.0.1:5555/api/company/close-drive/${id}`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        
        if (res.ok) {
            await fetchDrives()
        } else {
            const data = await res.json()
            alert(data.error || 'Failed to close drive')
        }
    } catch (err) {
        console.error('Error closing drive:', err)
        alert('An error occurred')
    }
}

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
.icon-square {
    width: 32px;
    height: 32px;
    font-size: 1rem;
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

.edit-btn {
    font-size: 0.8rem;
    font-weight: 600;
    border-color: #e2e8f0;
    background-color: #fff;
}

.edit-btn:hover {
    background-color: #f8fafc;
    border-color: #cbd5e1;
    transform: translateY(-1px);
}

.close-btn {
    font-size: 0.8rem;
    font-weight: 600;
}

.close-btn:hover {
    background-color: #dc2626;
    transform: translateY(-1px);
}

.hover-primary:hover {
    color: var(--color-primary) !important;
}
</style>
