<template>
    <CompanyProfile :companyId="companyId" />
</template>

<script setup>
import { useRoute } from 'vue-router';
const route = useRoute();
const companyId = route.params.id;

import CompanyProfile from '@/components/layout/CompanyProfile.vue';
</script>

<style scoped>

</style>