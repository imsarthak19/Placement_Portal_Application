<template>
  <DashboardLayout role="admin">
    <div class="admin-dashboard">
        <header class="dashboard-header">
            <div class="header-content">
                <h1>Manage Companies</h1>
            </div>
            <div class="header-actions">
                <button class="btn-primary">Export CSV</button>
            </div>
        </header>

        <div class="dashboard-content-grid">
            <section class="upcoming-drives card">
                <div class="card-header">
                    <h3>Unapproved Companies</h3>
                </div>
                <div class="drive-list">
                    <div v-if="upcomingDrives.length === 0" class="empty-state">
                        Approval queue is empty.
                    </div>
                    <div v-for="drive in upcomingDrives" :key="drive.id" class="drive-item">
                    <div class="drive-logo">
                        {{ drive.companyCode }}
                    </div>
                    <div class="drive-details">
                        <h4>{{ drive.title }}</h4>
                        <p>{{ drive.companyName }} • {{ drive.date }}</p>
                    </div>
                    <span :class="['status-badge', drive.status]">{{ drive.status }}</span>
                    </div>
                </div>
            </section>

            <section class="upcoming-drives card">
                <div class="card-header">
                    <h3>approved Companies</h3>
                </div>
                <div class="drive-list">
                    <div v-if="upcomingDrives.length === 0" class="empty-state">
                        There are no approved companies.
                    </div>
                    <div v-for="drive in upcomingDrives" :key="drive.id" class="drive-item">
                    <div class="drive-logo">
                        {{ drive.companyCode }}
                    </div>
                    <div class="drive-details">
                        <h4>{{ drive.title }}</h4>
                        <p>{{ drive.companyName }} • {{ drive.date }}</p>
                    </div>
                    <span :class="['status-badge', drive.status]">{{ drive.status }}</span>
                    </div>
                </div>
            </section>
        </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DashboardLayout from '@/components/sidebar/DashboardLayout.vue'

const upcomingDrives = ref([
    { id: 1, title: 'Software Engineer Intern', companyName: 'Google', companyCode: 'G', date: 'Oct 15, 2026', status: 'open' },
    { id: 2, title: 'Product Manager', companyName: 'Microsoft', companyCode: 'M', date: 'Oct 18, 2026', status: 'upcoming' },
    { id: 3, title: 'Data Scientist', companyName: 'Meta', companyCode: 'F', date: 'Oct 20, 2026', status: 'draft' }
])

onMounted(async () => {
  // Fetch real stats from API in future
})
</script>

<style scoped>
.admin-dashboard {
    max-width: 1200px;
    margin: 0 auto;
}

.dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 32px;
}

.header-content h1 {
    font-size: 2rem;
    font-weight: 700;
    color: var(--color-text);
    margin: 0 0 8px 0;
}

.btn-primary {
    background-color: var(--color-primary);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}

.btn-primary:hover {
    opacity: 0.9;
    transform: translateY(-1px);
}

@media (max-width: 1024px) {
    .dashboard-content-grid {
        grid-template-columns: 1fr;
    }
}

.card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    border: 1px solid #f0f0f0;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.card-header h3 {
    font-size: 1.25rem;
    margin: 0;
    color: var(--color-text);
}

.btn-text {
    background: none;
    border: none;
    color: var(--color-primary);
    font-weight: 600;
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 4px;
}

.btn-text:hover {
    background: #f8f8f8;
}

.drive-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.drive-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 12px;
    border-radius: 12px;
    background: #fafafa;
    transition: all 0.2s ease;
}

.drive-item:hover {
    background: #f0f0f0;
}

.drive-logo {
    width: 44px;
    height: 44px;
    background: white;
    border: 1px solid #eee;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    color: var(--color-primary);
    font-size: 1.2rem;
}

.drive-details {
    flex: 1;
}

.drive-details h4 {
    margin: 0;
    font-size: 1rem;
    color: #333;
}

.drive-details p {
    margin: 4px 0 0 0;
    font-size: 0.875rem;
    color: #777;
}

.status-badge {
    font-size: 0.75rem;
    padding: 4px 10px;
    border-radius: 20px;
    text-transform: capitalize;
    font-weight: 600;
}

.status-badge.open { background: #ecfdf5; color: #059669; }
.status-badge.upcoming { background: #eff6ff; color: #2563eb; }
.status-badge.draft { background: #f3f4f6; color: #4b5563; }

.empty-state {
    text-align: center;
    padding: 40px;
    color: #999;
    font-style: italic;
}
</style>