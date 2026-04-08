<template>
    <StudentProfile :studentId="studentId" />
</template>

<script setup>
import { useRoute } from 'vue-router';
import StudentProfile from '@/components/layout/StudentProfile.vue';

const route = useRoute();
const studentId = route.params.id;

</script>

<style scoped>

</style>
