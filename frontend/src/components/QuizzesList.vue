<template>
    <div class="quiz-grid">
        <template v-if="!isPopularQuizzes">
            <SingleQuiz v-for="quiz in quizzes" :key="quiz._id" :showManageButton="showManageButton" :quiz="quiz" />
        </template>
        <template v-if="isPopularQuizzes">
            <SingleQuiz v-for="quiz in quizzes" :key="quiz._id" :quiz="quiz.quiz_details" :showManageButton="showManageButton" />
        </template>
    </div>
</template>

<script>
import SingleQuiz from './SingleQuiz.vue';

    export default {
        props: ['quizzes', 'isPopularQuizzes', 'showManageButton'],
        components: { SingleQuiz }
    }
</script>

<style scoped>
.quiz-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}
</style>