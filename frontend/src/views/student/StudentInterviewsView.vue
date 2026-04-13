<template>
<DashboardLayout role="student">
    <div class="student-interviews">
        <header class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-4 mb-5">
            <div>
                <h1 class="h2 fw-bold text-dark mb-1">My Interviews</h1>
                <p class="text-muted mb-0">Prepare yourself for the upcoming recruitment rounds.</p>
            </div>
            <div class="search-wrapper">
                <Search v-model="searchQuery" placeholder="Search by company or role..." />
            </div>
        </header>

        <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>

        <div v-else-if="filteredInterviews.length === 0" class="card border-0 shadow-sm rounded-4 py-5 text-center bg-white">
            <div class="card-body">
                <div class="display-1 mb-4 opacity-25">🎓</div>
                <h3 class="fw-bold text-dark">No interviews scheduled</h3>
                <p class="text-muted mx-auto" style="max-width: 400px;">Keep applying to drives and your interview calls will appear here!</p>
            </div>
        </div>

        <div v-else class="row g-4">
            <div v-for="interview in filteredInterviews" :key="interview.id" class="col-md-6 col-xl-4">
                <div class="card interview-card border-0 shadow-sm rounded-4 overflow-hidden h-100 position-relative">
                    <div class="card-header bg-white p-4 border-0 pb-0">
                        <div class="d-flex align-items-center gap-3 mb-3">
                            <div class="company-logo bg-light rounded-3 d-flex align-items-center justify-content-center p-2 border">
                                <img v-if="interview.company_logo" :src="interview.company_logo" :alt="interview.company_name" class="img-fluid rounded-2">
                                <i v-else class="fas fa-building text-secondary opacity-50 fs-4"></i>
                            </div>
                            <div>
                                <h6 class="text-primary fw-bold mb-0 text-truncate" style="max-width: 150px;">{{ interview.company_name }}</h6>
                                <div class="text-muted small">
                                    <i class="fas fa-briefcase me-1"></i> {{ interview.drive_title }}
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="card-body p-4 pt-2">
                        <!-- Date & Time Section -->
                        <div class="datetime-card p-3 rounded-4 bg-primary bg-opacity-10 border border-primary border-opacity-10 mb-4">
                            <div class="row align-items-center">
                                <div class="col-auto">
                                    <div class="calendar-icon text-center text-primary">
                                        <div class="day fw-bold">{{ formatDay(interview.scheduled_at) }}</div>
                                        <div class="month small text-uppercase">{{ formatMonth(interview.scheduled_at) }}</div>
                                    </div>
                                </div>
                                <div class="col ps-3">
                                    <h5 class="fw-bold text-dark mb-0 text-highlight">{{ formatTime(interview.scheduled_at) }}</h5>
                                    <small class="text-muted fw-medium">{{ formatFullDate(interview.scheduled_at) }}</small>
                                </div>
                            </div>
                        </div>

                        <!-- Details -->
                        <div class="d-flex flex-column gap-3 mb-4">
                            <div class="d-flex align-items-center gap-3">
                                <div class="detail-icon bg-light text-secondary rounded-circle d-flex align-items-center justify-content-center shadow-xs">
                                    <i class="fas" :class="interview.mode.toLowerCase().includes('virtual') ? 'fa-video' : 'fa-map-marker-alt'"></i>
                                </div>
                                <div>
                                    <label class="text-muted small fw-bold text-uppercase d-block mb-0 opacity-75">Interview Mode</label>
                                    <span class="text-dark fw-bold">{{ interview.mode }}</span>
                                </div>
                            </div>

                            <div v-if="interview.location" class="d-flex align-items-center gap-3">
                                <div class="detail-icon bg-light text-secondary rounded-circle d-flex align-items-center justify-content-center shadow-xs">
                                    <i class="fas fa-location-arrow"></i>
                                </div>
                                <div>
                                    <label class="text-muted small fw-bold text-uppercase d-block mb-0 opacity-75">Location / Venue</label>
                                    <span class="text-dark fw-bold small">{{ interview.location }}</span>
                                </div>
                            </div>

                            <div v-if="interview.meeting_link" class="d-flex align-items-center gap-3">
                                <div class="detail-icon bg-light text-secondary rounded-circle d-flex align-items-center justify-content-center shadow-xs">
                                    <i class="fas fa-link"></i>
                                </div>
                                <div>
                                    <label class="text-muted small fw-bold text-uppercase d-block mb-0 opacity-75">Meeting Link</label>
                                    <a :href="interview.meeting_link" target="_blank" class="text-primary fw-bold small text-decoration-none hover-underline text-truncate d-block" style="max-width: 180px;">
                                        Join Meeting <i class="fas fa-external-link-alt ms-1 text-highlight" style="font-size: 0.7rem;"></i>
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="card-footer bg-light p-3 border-0 mt-auto">
                         <div class="d-flex justify-content-between align-items-center">
                            <span class="badge rounded-pill bg-white text-dark shadow-xs border px-3 py-2 fw-medium">
                                <i class="fas fa-info-circle text-info me-1"></i> Action Required
                            </span>
                            <router-link :to="`/student/drive/${interview.drive_id}`" class="text-primary small fw-bold text-decoration-none">
                                View Drive <i class="fas fa-chevron-right ms-1"></i>
                            </router-link>
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
import axios from 'axios'
import DashboardLayout from '@/components/sidebar/DashboardLayout.vue'
import Search from '@/components/ui/Search.vue'

const interviews = ref([])
const loading = ref(true)
const searchQuery = ref('')

const fetchInterviews = async () => {
    loading.value = true
    try {
        const token = localStorage.getItem('token')
        const res = await axios.get('http://127.0.0.1:5555/api/student/interviews', {
            headers: { Authorization: `Bearer ${token}` }
        })
        interviews.value = res.data
    } catch (err) {
        console.error('Error fetching interviews:', err)
    } finally {
        loading.value = false
    }
}

const filteredInterviews = computed(() => {
    if (!searchQuery.value) return interviews.value
    const q = searchQuery.value.toLowerCase()
    return interviews.value.filter(i => 
        i.drive_title.toLowerCase().includes(q) || 
        i.company_name.toLowerCase().includes(q)
    )
})

const formatDay = (dateStr) => {
    if (!dateStr) return '-'
    const date = new Date(dateStr)
    return date.getDate()
}

const formatMonth = (dateStr) => {
    if (!dateStr) return '-'
    const date = new Date(dateStr)
    return date.toLocaleDateString('en-GB', { month: 'short' })
}

const formatTime = (dateStr) => {
    if (!dateStr) return '-'
    const date = new Date(dateStr)
    return date.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', hour12: true })
}

const formatFullDate = (dateStr) => {
    if (!dateStr) return '-'
    const date = new Date(dateStr)
    return date.toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })
}

onMounted(fetchInterviews)
</script>

<style scoped>
.student-interviews {
    animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.interview-card {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.interview-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 16px 32px -12px rgba(0, 0, 0, 0.1) !important;
}

.company-logo {
    width: 60px;
    height: 60px;
}

.calendar-icon {
    border-right: 2px solid rgba(120, 31, 25, 0.1);
    padding-right: 15px;
    min-width: 60px;
}

.day {
    font-size: 1.5rem;
    line-height: 1;
}

.month {
    letter-spacing: 0.1em;
    font-size: 0.7rem;
}

.detail-icon {
    width: 36px;
    height: 36px;
    flex-shrink: 0;
}

.hover-underline:hover {
    text-decoration: underline !important;
}

.shadow-xs {
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.search-wrapper {
    min-width: 320px;
}

.text-highlight {
    color: var(--color-primary, #781f19);
}
</style>
