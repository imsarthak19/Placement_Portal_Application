<template>
    <input type="date" v-model="selecteddate">
    <button @click="fetchDrives">Search</button>

    <div v-if="drives.length === 0">No Drives To Show</div>
    <div class="fs-4">Filter Date: {{ selecteddate }}</div>
    <div v-for="d in drives" :key="d.id">
        <div class="m-5">
            <div>Drive Title: {{ d.Title }}</div>
            <div>Organisation: {{ d.Company }}</div>
            <div>Job Description: {{ d.Description }}</div>
            <div>Deadline: {{ d.Deadline }}</div>
        </div>
        
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
const selecteddate = ref('')
const drives = ref([])

const fetchDrives= async() => {
    const res = await fetch(`http://127.0.0.1:5555/api/viva/drives?date=${selecteddate.value}`

    )

    const data = await res.json()
    console.log(data)
    drives.value=data
}

onMounted(() => {
})

</script>