<template>
    <DriveProfile :key="driveId" :driveId="driveId" :role="role" />
</template>

<script setup>
import { useRoute } from 'vue-router';
import { computed } from 'vue';
import DriveProfile from '@/components/layout/DriveProfile.vue';

const route = useRoute();
const driveId = computed(() => route.params.id);
const role = computed(() => {
    if (route.path.startsWith('/admin')) return 'admin';
    if (route.path.startsWith('/student')) return 'student';
    return 'company';
});
</script>

<style scoped>

</style>
