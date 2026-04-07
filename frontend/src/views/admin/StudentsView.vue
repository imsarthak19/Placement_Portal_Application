<template>
<DashboardLayout role="admin">
<div class="admin-dashboard">

    <!-- Headings and stuff -->
    <header class="dashboard-header">
        <div class="header-content">
            <div class="header-tag">    MANAGEMENT CONSOLE  </div>
            <h1>Student Management</h1>
        </div>
        <div class="header-actions">
            <button class="btn-primary"><i class="fas fa-download"></i>Export List</button>
        </div>
    </header>
  
    <!-- Alert Messages -->
    <div class="flash-container">
        <transition name="fade">
            <div v-if="flashMsg" class="alert alert-success flash-msg d-flex align-items-center gap-2 border-0 shadow-sm rounded-3 py-3 px-4" role="alert">
                <i class="fas fa-check-circle"></i>
                <div>{{ flashMsg }}</div>
            </div>
        </transition>
        <transition name="fade">
            <div v-if="flashMsgError" class="alert alert-danger flash-msg d-flex align-items-center gap-2 border-0 shadow-sm rounded-3 py-3 px-4" role="alert">
                <i class="fas fa-exclamation-circle"></i>
                <div>{{ flashMsgError }}</div>
            </div>
        </transition>
    </div>
  
    <!-- Stats Grid -->
    <div class="row g-4 mb-5">
        <div v-for="(stat, key) in statConfig" :key="key" class="col-sm-6 col-xl-4">
            <StatCard 
                :label="stat.label" 
                :value="stats[key] || 0" 
                :icon="stat.icon" 
                :bgClass="stat.bgClass" 
                :textClass="stat.textClass" 
                :change="stat.change" 
                :changeClass="stat.changeClass" 
            />
        </div>
    </div>
  
    <!-- Main Content -->
    <div class="dashboard-content-grid">
        <!-- All Students Table -->
        <section class="upcoming-drives card my-4">
            <div class="card-header">
                <h3>All Registered Students</h3>
                <p class="text-muted small mb-0">Complete list of registered students.</p>
            </div>
                  
            <Table :columns="companyColumns" :data="students">
                <template #row="{ item: student }">

                    <td class="py-3 px-4">
                        <div class="fw-bold text-dark">{{ student.name }}</div>
                    </td>

                    <td class="py-3 px-3">
                        <div class="fw-medium text-dark"><i class="fas fa-envelope text-primary me-1 opacity-75"></i> {{ student.email }}</div>
                    </td>

                    <td class="py-3 px-3 text-muted">
                        <i class="fas text-secondary me-1 opacity-75"></i> {{ student.branch }}
                    </td>

                    <td class="py-3 px-4 text-center">
                        <span 
                            class="badge px-3 py-2 fw-medium shadow-sm"
                            :class="{
                                'bg-success': !student.blacklisted,
                                'bg-danger': student.blacklisted
                            }"
                            >
                            {{ !student.blacklisted ? 'Active' : 'blacklisted' }}
                        </span>
                    </td>

                    <td class="py-3 px-4 text-center">
                        <button v-if="!student.blacklisted" class="btn-action revoke-btn" @click="revokeStudent(student.id)">
                            <i class="fas fa-times-circle"></i> Blacklist
                        </button>
                        <button v-else-if="student.blacklisted" class="btn-action approve-btn" @click="whitelistStudent(student.id)">
                            <i class="fas fa-check-circle"></i> Whitelist
                        </button>
                        <span v-else class="text-muted small">N/A</span>
                    </td>

                </template>

                <!-- If there is no data to show -->
                <template #empty>
                    <td colspan="7" class="text-center py-5 text-muted">
                        <div class="fs-1 mb-3 opacity-50">📋</div>
                        <h5 class="fw-bold">No drives available.</h5>
                    </td>
                </template>
            </Table>
                  
            <!-- Page All -->
            <div v-if="allTotalPages > 1" class="pagination-controls mt-4">
                <button class="btn-pagination" :disabled="allCurrentPage === 1" @click="allCurrentPage--">
                    <i class="fas fa-chevron-left"></i>
                </button>

                <button v-for="page in allTotalPages" :key="page"
                    :class="['btn-pagination-number', { active: allCurrentPage === page }]"
                    @click="allCurrentPage = page">
                    {{ page }}
                </button>

                <button class="btn-pagination" :disabled="allCurrentPage === allTotalPages" @click="allCurrentPage++">
                    <i class="fas fa-chevron-right"></i>
                </button>
            </div>

        </section>
</div>
</div>
</DashboardLayout>
</template>


<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from "axios"
import DashboardLayout from '@/components/sidebar/DashboardLayout.vue'
import Table from '@/components/ui/Table.vue'
import StatCard from '@/components/ui/StatCard.vue'

const students = ref([])
const flashMsg = ref('')
const flashMsgError = ref('')

const showFlash = (message) => {
    flashMsg.value = message
    setTimeout(() => {
        flashMsg.value = ""
    }, 2000)
}

const errorMsg = (message) => {
    flashMsgError.value = message
    setTimeout(() => {
        flashMsgError.value = ""
    }, 2000)
}

// Table Columns
const companyColumns = [
    { key: 'title', label: 'Name', class: 'py-3 px-4 text-secondary fw-semibold text-uppercase' },
    { key: 'company', label: 'Email', class: 'py-3 px-3 text-secondary fw-semibold text-uppercase' },
    { key: 'location', label: 'Branch', class: 'py-3 px-3 text-secondary fw-semibold text-uppercase' },
    { key: 'status', label: 'Status', class: 'py-3 px-4 text-center text-secondary fw-semibold text-uppercase' },
    { key: 'actions', label: 'Actions', class: 'py-3 px-4 text-center text-secondary fw-semibold text-uppercase' }
]

// Stats Data Computation
const stats = computed(() => ({
    total: students.value.length,
    blacklisted: students.value.filter(s => s.blacklisted).length,
}))

const statConfig = {
    total: {
        label: 'Total Students',
        icon: 'fas fa-users',
        bgClass: 'bg-primary-soft border border-primary border-opacity-10',
        textClass: 'text-primary',
    },
    blacklisted: {
        label: 'Blocked Students',
        icon: 'fas fa-user-times',
        bgClass: 'bg-danger-soft border border-danger border-opacity-25',
        textClass: 'text-danger',
    }
}

// -- Fetch drives on mount --
const fetchStudents = async () => {
    const token = localStorage.getItem("token")

    try {
        const res = await fetch('http://127.0.0.1:5555/api/admin/all-students', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        })
        if (!res.ok) throw new Error("Failed to fetch")
        const data = await res.json()
        students.value = data
        console.log("STUDENTS", data)
    } 
    catch (err) {
        errorMsg('Server error. Please try again later.')
    }
}

onMounted(() => {
    fetchStudents()
})

const revokeStudent = async (studentId) => {
    flashMsg.value = ''
    try {
        const token = localStorage.getItem("token")

            if (!token) {
                console.error("No token found")
                errorMsg('Authentication error. Please log in again.')
                return
                }

        await axios.put(
            `http://127.0.0.1:5555/api/admin/blacklist_student/${studentId}`,
            {},
            {
                headers: {
                Authorization: `Bearer ${token}`
                }
            }
        )

        console.log("Student Blacklisted!")
        showFlash('Student blacklisted successfully.')

        // update UI
        students.value = students.value.map(s => {
        if (s.id === studentId) {
            return { ...s, blacklisted: true }
        }
        return s
        })

    } catch (error) {
    console.error("Error:", error.response?.data || error.message)
    errorMsg('Failed to blacklist student. Please try again.')
  }
}

const whitelistStudent = async (studentId) => {
    flashMsg.value = ''
    try {
        const token = localStorage.getItem("token")

            if (!token) {
                console.error("No token found")
                errorMsg('Authentication error. Please log in again.')
                return
                }

        await axios.put(
            `http://127.0.0.1:5555/api/admin/whitelist_student/${studentId}`,
            {},
            {
                headers: {
                Authorization: `Bearer ${token}`
                }
            }
        )

        console.log("Student Whitelisted!")
        showFlash('Student whitelisted successfully.')

        // update UI
        students.value = students.value.map(s => {
        if (s.id === studentId) {
            return { ...s, blacklisted: false }
        }
        return s
        })

    } catch (error) {
    console.error("Error:", error.response?.data || error.message)
    errorMsg('Failed to whitelist company. Please try again.')
  }
}

// Stats computation
const totalStudentsCount = computed(() => students.value.length)
const blacklistedStudentsCount = computed(() => students.value.filter(s => s.blacklisted).length)

// Pagination logic
const itemsPerPage = 5

// All Drives Pagination
const allCurrentPage = ref(1)
const allTotalPages = computed(() => Math.ceil(students.value.length / itemsPerPage) || 1)
const paginatedAll = computed(() => {
    const start = (allCurrentPage.value - 1) * itemsPerPage
    return students.value.slice(start, start + itemsPerPage)
})
</script>

<style scoped>
.admin-dashboard {
    max-width: 1200px;
    margin: 0 auto;
}

/* Header */
.dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 32px;
}

.header-tag {
    color: var(--color-primary);
    font-weight: 800;
    font-size: 0.8rem;
    letter-spacing: 1px;
    opacity: 0.7;
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

.btn-primary:hover, .approve-btn:hover {
    opacity: 0.9;
    transform: translateY(-1px);
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

/* Buttons */
.btn-action {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    height: 36px;
    padding: 0 16px;
    border-radius: 8px;
    font-size: 0.85rem;
    font-weight: 600;
    border: 1px solid transparent;
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.approve-btn {
    background-color: #10b981;
    color: #ffffff;
    border-color: #10b981;
}

.approve-btn:hover {
    background-color: #059669;
    border-color: #059669;
    transform: translateY(-1px);
    box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.4), 0 2px 4px -1px rgba(16, 185, 129, 0.2);
}

.revoke-btn {
    background-color: #ef4444;
    color: #ffffff;
    border-color: #ef4444;
}

.revoke-btn:hover {
    background-color: #dc2626;
    border-color: #dc2626;
    transform: translateY(-1px);
    box-shadow: 0 4px 6px -1px rgba(239, 68, 68, 0.4), 0 2px 4px -1px rgba(239, 68, 68, 0.2);
}

.btn-action:active {
    transform: translateY(0);
    box-shadow: none;
}

.status-badge {
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    white-space: nowrap;
}

.pending {
    background-color: #f8d7da;
    color: #721c24;
}

/* Pagination Styles */
.pagination-controls {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.btn-pagination {
    background: #fff;
    border: 1px solid #e2e8f0;
    color: #64748b;
    width: 32px;
    height: 32px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
}

.btn-pagination:hover:not(:disabled) {
    background: #f1f5f9;
    color: #334155;
}

.btn-pagination:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.btn-pagination-number {
    background: transparent;
    border: none;
    color: #64748b;
    width: 32px;
    height: 32px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-weight: 500;
    transition: all 0.2s ease;
}

.btn-pagination-number:hover {
    background: #f1f5f9;
}

.btn-pagination-number.active {
    background: var(--color-primary);
    color: white;
    font-weight: 600;
}

.bg-primary-soft { background-color: rgba(13, 110, 253, 0.1); }
.bg-warning-soft { background-color: rgba(255, 193, 7, 0.15); }
.bg-success-soft { background-color: rgba(25, 135, 84, 0.1); }

/* Notifications */
.flash-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.flash-msg {
    min-width: 250px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>