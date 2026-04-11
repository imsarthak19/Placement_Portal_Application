<template>
    <CompanyProfile :companyId="companyId" />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import CompanyProfile from '@/components/layout/CompanyProfile.vue'

const user = JSON.parse(localStorage.getItem('user') || '{}')
const companyId = ref(user.id)

onMounted(() => {
    if (!companyId.value) {
        console.error("No company ID found in localStorage")
    }
})
</script>

<style scoped>
</style>