<template>
<DashboardLayout role="student">
    <div class="offerview-container p-4">
        <header class="mb-5 d-flex justify-content-between align-items-center d-print-none">
            <div>
                <router-link to="/student/applications" class="btn btn-light rounded-pill px-4 shadow-sm border mb-3">
                    <i class="fas fa-arrow-left me-2"></i> Back to Applications
                </router-link>
                <h1 class="h3 fw-bold text-dark">Official Appointment Document</h1>
                <p class="text-muted small">This is your legally binding recruitment document from the company.</p>
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
        // Find the specific application and verify it's an offer
        const app = res.data.find(a => a.id == appId)
        if (app && (app.status.toLowerCase() === 'offered' || app.status.toLowerCase() === 'hired')) {
            offer.value = app
        }
    } catch (err) {
        console.error('Error fetching offer:', err)
    } finally {
        loading.value = false
    }
}

onMounted(fetchOffer)
</script>

<style scoped>
.offerview-container {
    animation: fadeIn 0.4s ease-out;
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
