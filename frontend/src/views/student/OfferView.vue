<template>
<DashboardLayout role="student">
    <div class="offerview-container p-4">
        <header class="mb-5 d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3 d-print-none">
            <div>
                <router-link to="/student/applications" class="btn btn-light rounded-pill px-4 shadow-sm border mb-3">
                    <i class="fas fa-arrow-left me-2"></i> Back to Applications
                </router-link>
                <h1 class="h3 fw-bold text-dark mb-1">Official Appointment Document</h1>
                <div class="d-flex align-items-center gap-2">
                    <p class="text-muted small mb-0">This is your legally binding recruitment document from the company.</p>
                    <span v-if="offer?.status.toLowerCase() === 'placed'" class="badge bg-success-soft text-success px-3 rounded-pill">
                        <i class="fas fa-check-circle me-1"></i> Already Accepted
                    </span>
                </div>
            </div>
            <div v-if="offer && offer.status.toLowerCase() === 'offered'" class="header-actions">
                <button @click="handleAcceptOffer" :disabled="accepting" class="btn btn-emerald px-4 py-2 rounded-pill fw-bold shadow-sm d-flex align-items-center gap-2">
                    <span v-if="accepting" class="spinner-border spinner-border-sm" role="status"></span>
                    <i v-else class="fas fa-check"></i>
                    {{ accepting ? 'Accepting...' : 'Accept Appointment' }}
                </button>
            </div>
        </header>

        <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>

        <div v-else-if="!offer" class="text-center py-5">
            <div class="display-3 mb-4 opacity-25"></div>
            <h4 class="fw-bold">Document Unavailable</h4>
            <p class="text-muted">This document is no longer available or was never issued.</p>
        </div>

        <div v-else class="offer-display animate-offer">
            <OfferLetter 
                :studentName="userName"
                :companyName="offer.company_name"
                :companyLogo="offer.company_logo"
                :driveTitle="offer.drive_title"
                :location="offer.location"
                :payScale="offer.payScale"
                :workMode="offer.workMode"
            />
        </div>
    </div>
</DashboardLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import DashboardLayout from '@/components/sidebar/DashboardLayout.vue'
import OfferLetter from '@/components/layout/OfferLetter.vue'

const route = useRoute()
const appId = route.params.id
const loading = ref(true)
const accepting = ref(false)
const offer = ref(null)

const user = JSON.parse(localStorage.getItem('user') || '{}')
const userName = user.name || 'Student'

const fetchOffer = async () => {
    loading.value = true
    try {
        const token = localStorage.getItem('token')
        const res = await axios.get('http://127.0.0.1:5555/api/student/applications', {
            headers: { Authorization: `Bearer ${token}` }
        })
        const app = res.data.find(a => a.id == appId)
        if (app && (app.status.toLowerCase() === 'offered' || app.status.toLowerCase() === 'placed' || app.status.toLowerCase() === 'hired')) {
            offer.value = app
        }
    } catch (err) {
        console.error('Error fetching offer:', err)
    } finally {
        loading.value = false
    }
}

const handleAcceptOffer = async () => {
    if (!confirm('Are you sure you want to accept this offer? This action is legally binding.')) return

    accepting.value = true
    try {
        const token = localStorage.getItem('token')
        await axios.post(`http://127.0.0.1:5555/api/student/accept-offer/${appId}`, {}, {
            headers: { Authorization: `Bearer ${token}` }
        })
        // Refresh offer data
        await fetchOffer()
        alert('Congratulations! You have successfully accepted the offer and are now placed.')
    } catch (err) {
        console.error('Error accepting offer:', err)
        alert(err.response?.data?.message || 'Failed to accept offer. Please try again.')
    } finally {
        accepting.value = false
    }
}

onMounted(fetchOffer)
</script>

<style scoped>
.offerview-container {
    animation: fadeIn 0.4s ease-out;
}

.btn-emerald {
    background: #10b981;
    color: white;
    border: none;
    transition: all 0.3s ease;
}

.btn-emerald:hover:not(:disabled) {
    background: #059669;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.bg-success-soft {
    background-color: rgba(16, 185, 129, 0.1);
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.animate-offer {
    animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes slideUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

@media print {
    body * {
        visibility: hidden;
    }

    #print-section, #print-section * {
        visibility: visible;
    }

    #print-section {
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
    }
}
</style>
