<template>
    <DriveProfile :driveId="driveId" />
</template>

<script setup>
import { useRoute } from 'vue-router';
import DriveProfile from '@/components/layout/DriveProfile.vue';

const route = useRoute();
const driveId = route.params.id;

</script>

<style scoped>

</style>
