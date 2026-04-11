<template>
<DashboardLayout role="recruiter">
    <div class="mt-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
                <h1 class="h3 fw-bold mb-1" style="color: var(--color-text);">Shortlisted Candidates</h1>
                <p class="text-muted mb-0">Manage interviews for candidates you've shortlisted.</p>
            </div>
            <div class="stats-pills d-flex gap-3">
                <div class="stat-pill bg-warning bg-opacity-10 text-warning px-3 py-2 rounded-3 border border-warning border-opacity-25 d-flex align-items-center gap-2">
                    <i class="fas fa-user-clock"></i>
                    <span class="fw-bold">{{ candidates.length }}</span>
                    <span class="small opacity-75">Pending Interview</span>
                </div>
            </div>
        </div>

        <!-- Search and Filter -->
        <div class="card shadow-sm border-0 bg-white rounded-4 mb-4">
            <div class="card-body p-3">
                <div class="row g-3">
                    <div class="col-md-8">
                        <div class="input-group border rounded-3 bg-light overflow-hidden">
                            <span class="input-group-text border-0 bg-transparent text-muted ms-2"><i class="fas fa-search"></i></span>
                            <input v-model="searchQuery" type="text" class="form-control border-0 bg-transparent py-2" placeholder="Search by name, roll number, or drive...">
                        </div>
                    </div>
                    <div class="col-md-4">
                        <select v-model="filterDrive" class="form-select border rounded-3 py-2 bg-light">
                            <option value="">All Drives</option>
                            <option v-for="drive in uniqueDrives" :key="drive" :value="drive">{{ drive }}</option>
                        </select>
                    </div>
                </div>
            </div>
        </div>

        <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>

        <div v-else-if="filteredCandidates.length === 0" class="card border-0 shadow-sm rounded-4 py-5 text-center">
            <div class="card-body">
                <h4 class="fw-bold">No shortlisted candidates found</h4>
                <p class="text-muted">You haven't shortlisted any candidates yet or no matches found.</p>
            </div>
        </div>

        <Table v-else :columns="tableColumns" :data="filteredCandidates">
            <template #row="{ item: candidate }">
                <td class="py-3 px-4">
                    <div class="d-flex align-items-center gap-3">
                        <div class="avatar bg-primary bg-opacity-10 text-primary rounded-circle d-flex align-items-center justify-content-center fw-bold" style="width: 40px; height: 40px;">
                            {{ candidate.student_name.charAt(0) }}
                        </div>
                        <div>
                            <div class="fw-bold text-dark">{{ candidate.student_name }}</div>
                            <div class="small text-muted">{{ candidate.roll_number }}</div>
                        </div>
                    </div>
                </td>
                <td class="py-3 px-3">
                    <div class="text-dark fw-medium">{{ candidate.drive_title }}</div>
                    <div class="small text-muted">{{ candidate.branch }}</div>
                </td>
                <td class="py-3 px-3">
                    <div class="text-success fw-bold">{{ candidate.cgpa }} CGPA</div>
                </td>
                <td class="py-3 px-3">
                    <div v-if="candidate.interviews.length > 0">
                        <span class="badge bg-success bg-opacity-10 text-success border border-success border-opacity-25 px-2 py-1 mb-1 d-block w-fit">
                            <i class="fas fa-calendar-check me-1"></i> Scheduled
                        </span>
                        <div class="small text-muted">{{ formatDate(candidate.interviews[0].scheduled_at) }}</div>
                    </div>
                    <span v-else class="badge bg-warning bg-opacity-10 text-warning border border-warning border-opacity-25 px-2 py-1">
                        <i class="fas fa-clock me-1"></i> Waiting
                    </span>
                </td>
                <td class="py-3 px-4 text-end">
                    <div class="d-flex gap-2 justify-content-end">
                        <button @click="openScheduleModal(candidate)" class="btn btn-sm btn-primary border-0 shadow-sm px-3 rounded-3 d-flex align-items-center gap-1">
                            <i class="fas fa-calendar-alt"></i> {{ candidate.interviews.length > 0 ? 'Reschedule' : 'Schedule' }}
                        </button>
                        <router-link :to="`/company/student/${candidate.student_id}`" class="btn btn-sm btn-light border shadow-sm px-3 rounded-3">
                            <i class="fas fa-user"></i>
                        </router-link>
                    </div>
                </td>
            </template>
        </Table>
    </div>

    <!-- Schedule Interview Modal -->
    <div v-if="showModal" class="modal-overlay d-flex align-items-center justify-content-center z-3">
        <div class="modal-container bg-white rounded-4 shadow-lg p-4 w-100 mx-3" style="max-width: 500px;">
            <div class="d-flex justify-content-between align-items-center mb-4 pb-2 border-bottom">
                <h5 class="fw-bold mb-0">Schedule Interview</h5>
                <button @click="showModal = false" class="btn-close"></button>
            </div>
            
            <div class="mb-4">
                <div class="d-flex align-items-center gap-3 bg-light p-3 rounded-3">
                    <div class="avatar bg-white rounded-circle d-flex align-items-center justify-content-center fw-bold text-primary shadow-sm" style="width: 45px; height: 45px;">
                        {{ selectedCandidate?.student_name.charAt(0) }}
                    </div>
                    <div>
                        <div class="fw-bold">{{ selectedCandidate?.student_name }}</div>
                        <div class="small text-muted">{{ selectedCandidate?.drive_title }}</div>
                    </div>
                </div>
            </div>

            <form @submit.prevent="handleSchedule">
                <div class="mb-3">
                    <label class="form-label small fw-bold text-muted text-uppercase">Interview Date & Time</label>
                    <input v-model="form.scheduled_at" type="datetime-local" class="form-control rounded-3 border-light shadow-sm" required>
                </div>

                <div class="mb-3">
                    <label class="form-label small fw-bold text-muted text-uppercase">Interview Mode</label>
                    <div class="d-flex gap-3">
                        <div class="form-check custom-check">
                            <input v-model="form.mode" class="form-check-input" type="radio" value="Online" id="modeOnline" required>
                            <label class="form-check-label" for="modeOnline">Online</label>
                        </div>
                        <div class="form-check custom-check">
                            <input v-model="form.mode" class="form-check-input" type="radio" value="In-Person" id="modeOffline">
                            <label class="form-check-label" for="modeOffline">In-Person</label>
                        </div>
                    </div>
                </div>

                <div v-if="form.mode === 'Online'" class="mb-3">
                    <label class="form-label small fw-bold text-muted text-uppercase">Meeting Link</label>
                    <div class="input-group rounded-3 shadow-sm border-light overflow-hidden">
                        <span class="input-group-text border-0 bg-white"><i class="fas fa-link text-muted"></i></span>
                        <input v-model="form.meeting_link" type="url" class="form-control border-0" placeholder="https://meet.google.com/...">
                    </div>
                </div>

                <div v-else class="mb-3">
                    <label class="form-label small fw-bold text-muted text-uppercase">Location</label>
                    <div class="input-group rounded-3 shadow-sm border-light overflow-hidden">
                        <span class="input-group-text border-0 bg-white"><i class="fas fa-map-marker-alt text-muted"></i></span>
                        <input v-model="form.location" type="text" class="form-control border-0" placeholder="e.g. Conference Room A, 4th Floor">
                    </div>
                </div>

                <div class="d-flex gap-2 mt-5">
                    <button type="button" @click="showModal = false" class="btn btn-light rounded-3 fw-bold flex-grow-1 border">Cancel</button>
                    <button type="submit" class="btn btn-primary rounded-3 fw-bold flex-grow-1 shadow" :disabled="submitting">
                        <span v-if="submitting" class="spinner-border spinner-border-sm me-1"></span>
                        {{ selectedCandidate?.interviews.length > 0 ? 'Reschedule' : 'Confirm & Send' }}
                    </button>
                </div>
            </form>
        </div>
    </div>
</DashboardLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import DashboardLayout from '@/components/sidebar/DashboardLayout.vue'
import Table from '@/components/ui/Table.vue'
import axios from 'axios'

const candidates = ref([])
const loading = ref(true)
const submitting = ref(false)
const searchQuery = ref('')
const filterDrive = ref('')

const showModal = ref(false)
const selectedCandidate = ref(null)
const form = ref({
    scheduled_at: '',
    mode: 'Online',
    meeting_link: '',
    location: ''
})

const tableColumns = [
    { key: 'name', label: 'Candidate', class: 'py-3 px-4 text-secondary fw-semibold text-uppercase' },
    { key: 'drive', label: 'Drive / Branch' },
    { key: 'cgpa', label: 'Academics' },
    { key: 'interview', label: 'Interview Status' },
    { key: 'action', label: 'Action', class: 'py-3 px-4 text-secondary fw-semibold text-uppercase text-end' }
]

const fetchCandidates = async () => {
    loading.value = true
    try {
        const token = localStorage.getItem('token')
        const res = await axios.get('http://127.0.0.1:5555/api/company/shortlisted-applications', {
            headers: { Authorization: `Bearer ${token}` }
        })
        candidates.value = res.data
    } catch (err) {
        console.error('Error fetching shortlisted candidates:', err)
    } finally {
        loading.value = false
    }
}

const uniqueDrives = computed(() => {
    const drives = candidates.value.map(c => c.drive_title)
    return [...new Set(drives)]
})

const filteredCandidates = computed(() => {
    return candidates.value.filter(c => {
        const matchesSearch = c.student_name.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
                             c.drive_title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                             c.roll_number.toLowerCase().includes(searchQuery.value.toLowerCase())
        const matchesDrive = !filterDrive.value || c.drive_title === filterDrive.value
        return matchesSearch && matchesDrive
    })
})

const openScheduleModal = (candidate) => {
    selectedCandidate.value = candidate
    if (candidate.interviews.length > 0) {
        const intv = candidate.interviews[0]
        form.value = {
            scheduled_at: intv.scheduled_at.substring(0, 16),
            mode: intv.mode,
            meeting_link: intv.meeting_link || '',
            location: intv.location || ''
        }
    } else {
        form.value = {
            scheduled_at: '',
            mode: 'Online',
            meeting_link: '',
            location: ''
        }
    }
    showModal.value = true
}

const handleSchedule = async () => {
    submitting.value = true
    try {
        const token = localStorage.getItem('token')
        const res = await axios.post(`http://127.0.0.1:5555/api/company/schedule-interview/${selectedCandidate.value.id}`, form.value, {
            headers: { Authorization: `Bearer ${token}` }
        })
        
        showModal.value = false
        await fetchCandidates()
        alert('Interview scheduled successfully!')
    } catch (err) {
        console.error('Error scheduling interview:', err)
        alert(err.response?.data?.error || 'Failed to schedule interview')
    } finally {
        submitting.value = false
    }
}

const formatDate = (dateStr) => {
    if (!dateStr) return 'N/A'
    const date = new Date(dateStr)
    return date.toLocaleString('en-GB', { 
        day: '2-digit', 
        month: 'short', 
        hour: '2-digit', 
        minute: '2-digit' 
    })
}

onMounted(fetchCandidates)
</script>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(4px);
}

.w-fit { width: fit-content; }

.custom-check .form-check-input:checked {
    background-color: var(--color-primary);
    border-color: var(--color-primary);
}

.btn-primary {
    background-color: var(--color-primary, #781f19);
}

.btn-primary:hover:not(:disabled) {
    background-color: #5d1712;
    transform: translateY(-1px);
}
</style>
