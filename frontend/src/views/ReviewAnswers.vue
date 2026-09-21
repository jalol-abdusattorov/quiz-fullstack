<template>
    <div>
        <h1>Reviews page</h1>
        <div>
            <QuestionAnswer :question-and-answer="quizStore.result.answers[currentQuestionAndAnswerNav]"/>
        </div>
    </div>
</template>

<script>
import QuestionAnswer from '@/components/QuestionAnswer.vue';
import { useQuizzesStore } from '@/stores/QuizzesStore';
import { onMounted, ref } from 'vue';

    export default {
        components: { QuestionAnswer },
        setup() {
            const quizStore = useQuizzesStore()
            const currentQuestionAndAnswerNav = ref(1)

            onMounted(() => {
                fillQuizQuestions()
            })

            return { quizStore, currentQuestionAndAnswerNav }
        }
    }
</script>

<style scoped>

</style>