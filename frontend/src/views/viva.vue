<template>
    Hello World
    <div>Total Companies Registered: {{ comapnies.length }}</div>
    <div v-for="c in comapnies" :key="c.id" :class="{ 'highlighted': c.industry === 'Technology'}">
        <router-link :to="`/viva/${c.id}`" class="text-decoration-none">
            <div class="m-4">
                <div>Company Name: <b>{{ c.name }}</b></div>
            </div>
        </router-link>
        
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const comapnies = ref([])

const fetchCompanyList = async() => {

    const res = await fetch(`http://127.0.0.1:5555/viva`,{
        method: 'GET'
    })

    const data = await res.json()
    console.log(data)
    comapnies.value = data

}

onMounted(() => {
    fetchCompanyList()
})
</script>

<style scoped>

.highlighted{
    background-color: lightblue;
}

</style>