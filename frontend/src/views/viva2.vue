<template>
    Hello World
    <div v-if="msg">
        <div> {{ msg.date }}</div>
        <div>{{ msg.message }}</div>
    </div>

    <div>
        <input type="text" v-model="inputValue">
        <button @click="printMsg()">Print</button>
    </div>

    <div v-if="displayValue">
        You Have Entered: {{ displayValue }}
    </div>

    <div class="m-5">SUM
        <div>
            <input type="number" v-model="firstNumber" placeholder="Enter First Number">
            <input class="mx-2" type="number" v-model="secondNumber" placeholder="Enter Second Number">
        </div>
        <div>
            <button class="my-2" @click="fetchSum()">Find Sum</button>
        </div>
        <div v-if="sum">
            <div>
                First No: {{ sum.a }}
            </div>
            <div>
                Second No: {{ sum.b }}
            </div>
            <div>
                 Sum: {{ sum.sum }}
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const msg = ref('')

const inputValue = ref('')
const displayValue = ref('')

const firstNumber = ref('')
const secondNumber = ref('')
const sum = ref('')

const fetchSum = async() =>{
    const res = await fetch(
        `http://127.0.0.1:5555/api/sum?a=${firstNumber.value}&b=${secondNumber.value}`,{
            method:'GET'
        }
    )

    const data = await res.json()
    console.log(data)
    sum.value = data
}


const printMsg = async()=> {
    displayValue.value = inputValue.value
}

const fetchMsg = async() => {
    const res = await fetch(`http://127.0.0.1:5555/viva/msg`,
        {
            method: 'GET'
        }
    )

    const data = await res.json()
    console.log(data)
    msg.value = data
    
}

onMounted(() => {
    fetchMsg()
})
</script>