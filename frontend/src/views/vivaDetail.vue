<template>
    <div class="errorMsg" v-if="errorMsg">{{ errorMsg }}</div>
    Hello World
    <div>Company Profile</div>
    <div v-for="c in company" :class="{ 'highlighted': c.id > 1, 'normal': c.id == 1}">
        <div class="m-4">
            <div class="top-profile">
                <div><img :src="c.logo" alt="" class="logo"></div>
                <div class="sub-data">
                    <div>Name: <b>{{ c.name }}</b></div>
                    <div>Username: <b>{{ c.username }}</b></div>
                </div>
            </div>
            <div>Comapny Email: <b>{{ c.email }}</b> </div>
            <div>Company Industry: <b>{{ c.industry }}</b> </div>
            <div>Company Industry: <b>{{ c.description }}</b> </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const id = route.params.id

const company = ref({})
const errorMsg =ref('')

const fetchCompany = async() => {

    try{
        const res = await fetch(`http://127.0.0.1:5555/viva/${id}`)

        const data = await res.json()
        console.log(data)

        if (!res.ok) {
            throw new Error(data.error || "Something Went Wrong!")
        }

        company.value = data
    }
    
    catch(err){
        console.error(err.message)
        errorMsg.value = err.message
    }
    
}

onMounted(() => {
    console.log(route.params.id) 
    fetchCompany()
    
})
</script>

<style scoped>
.top-profile{
    display: flex;
}

.normal{
    background-color: brown;
}

.logo{
    width: 50px;
    height: auto;
    margin-right: 20px;
    margin-bottom: 10px;
}

.highlighted{
    background-color: lightblue;
}

.errorMsg{
    margin-left: 20px;
    color: red;
}

</style>