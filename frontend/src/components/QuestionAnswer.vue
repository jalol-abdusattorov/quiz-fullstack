<template>
    <div class="question-card">
        <h2>{{ questionAndAnswer }}</h2>
        <p>Question</p>
    </div>
</template>

<script>
    export default {
        props: ['questionAndAnswer']
    }
</script>

<style scoped>

</style>