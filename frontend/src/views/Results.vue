<template>
    <div>
        <h1>Results page</h1>
        <p>{{ id }} | {{ answers }}</p>
    </div>
</template>

<script>
export default {
    props: ['id'],
    computed: {
        answers() {
            try {
                return JSON.parse(this.$route.query.answers || '[]');
            } catch (exception) {
                return [];
            }
        }
    }
}
</script>

<style scoped>

</style>