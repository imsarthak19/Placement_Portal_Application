<template>
    Hello

    <child
        v-for="u in users"
        :key="u.name",
        :user="u"
    />

</template>

<script setup>
import child from '@/components/layout/child.vue';

const users=[
    { name: 'Sarthak', score: 90 },
    { name: 'Tanisha', score:95 }
]
</script>