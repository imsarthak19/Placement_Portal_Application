<template> 
<div class="my-2">
    <div class="mx-5">
        Name: {{ user.name }}
    </div>
    <div class="mx-5">
        Score: {{ user.score }}
</div>

</div>

</template>

<script setup>

defineProps(['user'])

</script>