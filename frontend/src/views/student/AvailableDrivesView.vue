<template>
<DashboardLayout role="student">
    <div class="student-drives">
        <header class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-4 mb-5">
            <div>
                <h1 class="h2 fw-bold text-dark mb-1">Available Hiring Drives</h1>
                <p class="text-muted mb-0">Discover and apply to the latest placement opportunities.</p>
            </div>
            <div class="search-wrapper">
                <Search v-model="searchQuery" placeholder="Search by role, company, or location..." />
            </div>
        </header>

        <div class="row g-4 mb-5">
             <div class="col-md-4">
                <StatCard 
                    label="Active Drives" 
                    :value="drives.length" 
                    icon="fas fa-briefcase" 
                    bgClass="bg-primary-soft" 
                    textClass="text-primary" 
                />
            </div>
            <div class="col-md-4">
                <StatCard 
                    label="Applied" 
                    :value="appliedCount" 
                    icon="fas fa-check-circle" 
                    bgClass="bg-success-soft" 
                    textClass="text-success" 
                />
            </div>
            <div class="col-md-4">
                <StatCard 
                    label="Upcoming Deadlines" 
                    :value="upcomingCount" 
                    icon="fas fa-clock" 
                    bgClass="bg-warning-soft" 
                    textClass="text-warning" 
                />
            </div>
        </div>

        <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>

        <div v-else-if="filteredDrives.length === 0" class="card border-0 shadow-sm rounded-4 py-5 text-center">
            <div class="card-body">
                <div class="display-1 mb-4 opacity-25">🔍</div>
                <h3 class="fw-bold text-dark">No active drives found</h3>
                <p class="text-muted mx-auto" style="max-width: 400px;">We couldn't find any active drives. Check back later!</p>
            </div>
        </div>

        <div v-else class="row g-4">
            <div v-for="drive in filteredDrives" :key="drive.id" class="col-md-6 col-xl-4">
                <div class="card drive-card border-0 shadow-sm h-100 rounded-4 overflow-hidden position-relative">
                    <div v-if="drive.hasApplied" class="applied-badge">
                        <i class="fas fa-check me-1"></i> Applied
                    </div>
                    
                    <div class="card-body p-4">
                        <div class="d-flex align-items-center gap-3 mb-4">
                            <div class="company-logo bg-light rounded-3 d-flex align-items-center justify-content-center p-2 border">
                                <img v-if="drive.company_logo" :src="drive.company_logo" :alt="drive.company_name" class="img-fluid rounded-2 shadow-sm">
                                <i v-else class="fas fa-building text-secondary opacity-50 fs-3"></i>
                            </div>
                            <div>
                                <h6 class="text-primary fw-bold mb-0 text-truncate" style="max-width: 150px;">{{ drive.company_name }}</h6>
                                <div class="text-muted small d-flex align-items-center gap-1">
                                    <i class="fas fa-map-marker-alt"></i> {{ drive.location }}
                                </div>
                            </div>
                        </div>

                        <h5 class="fw-bold mb-3 text-dark drive-title">{{ drive.title }}</h5>

                        <div class="d-flex flex-wrap gap-2 mb-4">
                            <span class="badge bg-light text-dark border px-2 py-1.5 rounded-pill fw-medium d-flex align-items-center gap-1">
                                <i class="fas fa-briefcase text-primary opacity-75"></i> {{ drive.workMode }}
                            </span>
                            <span class="badge bg-light text-dark border px-2 py-1.5 rounded-pill fw-medium d-flex align-items-center gap-1">
                                <i class="fas fa-money-bill-wave text-success opacity-75"></i> {{ drive.payScale }}
                            </span>
                        </div>

                        <div class="mt-auto pt-3 border-top d-flex justify-content-between align-items-center">
                            <div class="deadline small text-muted">
                                <i class="far fa-clock me-1"></i> Ends: {{ formatDate(drive.deadline) }}
                            </div>
                            <router-link :to="`/student/drive/${drive.id}`" class="btn btn-outline-primary btn-sm rounded-3 px-3 fw-bold">
                                View Details
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
import { ref, onMounted, computed, watch } from 'vue'
import axios from 'axios'
import DashboardLayout from '@/components/sidebar/DashboardLayout.vue'
import StatCard from '@/components/ui/StatCard.vue'
import Search from '@/components/ui/Search.vue'

const drives = ref([])
const loading = ref(true)
const searchQuery = ref('')

const fetchDrives = async () => {
    loading.value = true
    try {
        const token = localStorage.getItem('token')
        const res = await axios.get('http://127.0.0.1:5555/api/student/active-drives', {
            headers: { Authorization: `Bearer ${token}` }
        })
        drives.value = res.data
    } catch (err) {
        console.error('Error fetching drives:', err)
        console.log('Drives API response:', err.response ? err.response.data : 'No response data')
    } finally {
        loading.value = false
    }
}

const filteredDrives = computed(() => {
    if (!searchQuery.value) return drives.value
    const q = searchQuery.value.toLowerCase()
    return drives.value.filter(d => 
        d.title.toLowerCase().includes(q) || 
        d.company_name.toLowerCase().includes(q) || 
        d.location.toLowerCase().includes(q)
    )
})

const appliedCount = computed(() => drives.value.filter(d => d.hasApplied).length)
const upcomingCount = computed(() => {
    const today = new Date()
    return drives.value.filter(d => {
        if (!d.deadline) return false
        const deadline = new Date(d.deadline)
        const diffTime = deadline - today
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
        return diffDays > 0 && diffDays <= 7
    }).length
})

const formatDate = (dateStr) => {
    if (!dateStr) return 'N/A'
    const date = new Date(dateStr)
    return date.toLocaleDateString('en-GB', { day: '2-digit', month: 'short' })
}

onMounted(async () => {
    await fetchDrives()
})
</script>

<style scoped>
.text-brand-primary {
  color: var(--color-primary, #781f19);
}

.student-drives {
    position: relative;
}

.search-wrapper {
    min-width: 320px;
}

.bg-primary-soft { background-color: rgba(120, 31, 25, 0.08); }
.bg-success-soft { background-color: rgba(25, 135, 84, 0.08); }
.bg-warning-soft { background-color: rgba(255, 193, 7, 0.12); }

.drive-card {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.drive-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 24px -10px rgba(0, 0, 0, 0.15) !important;
}

.company-logo {
    width: 54px;
    height: 54px;
}

.drive-title {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    height: 3rem;
    line-height: 1.5rem;
}

.applied-badge {
    position: absolute;
    top: 0;
    right: 0;
    background-color: #10b981;
    color: white;
    padding: 6px 16px;
    font-size: 0.75rem;
    font-weight: 700;
    border-bottom-left-radius: 16px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.tracking-wider {
    letter-spacing: 0.05em;
}
</style>
