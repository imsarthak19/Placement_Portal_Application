<template>
    <DriveProfile :driveId="driveId" :role="role" />
</template>

<script setup>
import { useRoute } from 'vue-router';
import { computed } from 'vue';
import DriveProfile from '@/components/layout/DriveProfile.vue';

const route = useRoute();
const driveId = route.params.id;
const role = computed(() => route.path.startsWith('/admin') ? 'admin' : 'company');
</script>

<style scoped>

</style>
