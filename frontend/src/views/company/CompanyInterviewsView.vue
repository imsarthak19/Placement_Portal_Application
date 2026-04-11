<template>
<DashboardLayout role="recruiter">
    <div class="mt-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
                <h1 class="h3 fw-bold mb-1" style="color: var(--color-text);">Scheduled Interviews</h1>
                <p class="text-muted mb-0">Track and manage all your upcoming and past interview sessions.</p>
            </div>
            <div class="stats-pills d-flex gap-3">
                <div class="stat-pill text-primary px-3 py-2 rounded-3 border border-indigo border-opacity-25 d-flex align-items-center gap-2">
                    <i class="fas fa-calendar-alt"></i>
                    <span class="fw-bold">{{ upcomingInterviews.length }}</span>
                    <span class="small opacity-75">Upcoming</span>
                </div>
            </div>
        </div>

        <!-- Filter Tabs -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="btn-group bg-white p-1 rounded-4 shadow-sm">
                    <button @click="currentFilter = 'all'" :class="['btn rounded-3 px-4 py-2 fw-medium border-0', currentFilter === 'all' ? 'btn-primary text-white shadow-sm' : 'btn-light text-muted']">All Sessions</button>
                    <button @click="currentFilter = 'upcoming'" :class="['btn rounded-3 px-4 py-2 fw-medium border-0', currentFilter === 'upcoming' ? 'btn-primary text-white shadow-sm' : 'btn-light text-muted']">Upcoming</button>
                </div>
            </div>
        </div>

        <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>

        <div v-else-if="filteredInterviews.length === 0" class="card border-0 shadow-sm rounded-4 py-5 text-center">
            <div class="card-body">
                <div class="display-3 mb-4 opacity-25">🗓️</div>
                <h4 class="fw-bold">No interviews found</h4>
                <p class="text-muted">You haven't scheduled any interviews for this category yet.</p>
            </div>
        </div>

        <div v-else class="row g-4">
            <div v-for="interview in filteredInterviews" :key="interview.id" class="col-md-6 col-xl-4">
                <div class="card border-0 shadow-sm rounded-4 h-100 interview-card overflow-hidden">
                    <div class="card-header border-0 bg-transparent p-4 pb-0">
                        <div class="d-flex justify-content-between align-items-start mb-3">
                            <span :class="['badge rounded-pill px-3 py-2 fw-medium', isUpcoming(interview.scheduled_at) ? 'bg-success bg-opacity-10 text-success' : 'bg-secondary bg-opacity-10 text-secondary']">
                                <i :class="['fas me-1', isUpcoming(interview.scheduled_at) ? 'fa-clock' : 'fa-check-circle']"></i>
                                {{ isUpcoming(interview.scheduled_at) ? 'Upcoming' : 'Completed' }}
                            </span>
                            <div class="text-muted small">ID: #{{ interview.id }}</div>
                        </div>
                        <h5 class="fw-bold mb-1">{{ interview.student_name }}</h5>
                        <p class="text-muted small mb-0"><i class="fas fa-briefcase me-1"></i> {{ interview.drive_title }}</p>
                    </div>
                    <div class="card-body p-4">
                        <div class="bg-light rounded-4 p-3 mb-3 d-flex align-items-center gap-3">
                            <div class="date-box bg-white rounded-3 shadow-sm p-2 text-center" style="min-width: 60px;">
                                <div class="small fw-bold text-uppercase text-primary">{{ formatMonth(interview.scheduled_at) }}</div>
                                <div class="h4 fw-bold mb-0">{{ formatDay(interview.scheduled_at) }}</div>
                            </div>
                            <div>
                                <div class="fw-bold text-dark">{{ formatTime(interview.scheduled_at) }}</div>
                                <div class="small text-muted">{{ interview.mode }} Interview</div>
                            </div>
                        </div>

                        <div class="location-details small mb-3">
                            <div v-if="interview.mode === 'Online'" class="d-flex align-items-center gap-2 text-primary">
                                <i class="fas fa-link"></i>
                                <a :href="interview.meeting_link" target="_blank" class="text-decoration-none text-truncate fw-medium">{{ interview.meeting_link || 'Link not provided' }}</a>
                            </div>
                            <div v-else class="d-flex align-items-center gap-2 text-muted">
                                <i class="fas fa-map-marker-alt"></i>
                                <span class="fw-medium text-truncate">{{ interview.location || 'Location not specified' }}</span>
                            </div>
                        </div>
                    </div>
                    <div class="card-footer border-0 bg-light p-3 d-flex gap-2">
                        <router-link :to="`/company/student/${interview.student_id}`" class="btn btn-outline-primary btn-sm flex-grow-1 rounded-3">
                            <i class="fas fa-user me-1"></i> View Profile
                        </router-link>
                        <!-- <button v-if="isUpcoming(interview.scheduled_at)" class="btn btn-primary btn-sm flex-grow-1 rounded-3">
                            <i class="fas fa-edit me-1"></i> Reschedule
                        </button> -->
                    </div>
                </div>
            </div>
        </div>
    </div>
</DashboardLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import DashboardLayout from '@/components/sidebar/DashboardLayout.vue'
import axios from 'axios'

const interviews = ref([])
const loading = ref(true)
const currentFilter = ref('upcoming')

const fetchInterviews = async () => {
    loading.value = true
    try {
        const token = localStorage.getItem('token')
        const res = await axios.get('http://127.0.0.1:5555/api/company/interviews', {
            headers: { Authorization: `Bearer ${token}` }
        })
        interviews.value = res.data
    } catch (err) {
        console.error('Error fetching interviews:', err)
    } finally {
        loading.value = false
    }
}

const isUpcoming = (dateStr) => {
    return new Date(dateStr) > new Date()
}

const filteredInterviews = computed(() => {
    if (currentFilter.value === 'all') return interviews.value
    return interviews.value.filter(i => {
        const upcoming = isUpcoming(i.scheduled_at)
        return currentFilter.value === 'upcoming' ? upcoming : !upcoming
    })
})

const upcomingInterviews = computed(() => interviews.value.filter(i => isUpcoming(i.scheduled_at)))

const formatMonth = (dateStr) => {
    return new Date(dateStr).toLocaleString('en-US', { month: 'short' })
}

const formatDay = (dateStr) => {
    return new Date(dateStr).getDate()
}

const formatTime = (dateStr) => {
    return new Date(dateStr).toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: true 
    })
}

onMounted(fetchInterviews)
</script>

<style scoped>
.interview-card {
    transition: all 0.3s ease;
}

.interview-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 1rem 3rem rgba(0, 0, 0, 0.1) !important;
}

.bg-indigo { background-color: #6366f1; }
.text-indigo { color: #4338ca; }

.btn-primary {
    background-color: var(--color-primary, #781f19);
    border: none;
}

.btn-primary:hover {
    background-color: #5d1712;
}

.btn-outline-primary {
    color: var(--color-primary);
    border-color: var(--color-primary);
}

.btn-outline-primary:hover {
    background-color: var(--color-primary);
    color: white;
}
</style>
