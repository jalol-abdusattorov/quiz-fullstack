<template>
    <div class="quiz-grid">
        <Quiz v-for="quiz in quizzes" :key="quiz._id" :quiz="quiz" />
    </div>
</template>

<script>
import Quiz from './Quiz.vue';

    export default {
        props: ['quizzes'],
        components: { Quiz }
    }
</script>

<style scoped>
.quiz-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}
</style>