<template>
    <div v-if="quizDetails">
        <admin-app-header />
        <h1>Managing Quiz</h1>

        <div class="managing">
            <quizzes-list :quizzes="[quizDetails]" :showManageButton="false" />
            <div class="actions">
                <router-link :to="{ name: 'QuizStatistics' }" class="btn statistics-btn">statistics</router-link>
                <router-link :to="{ name: 'EditQuiz', params: { quizId: quizId } }" class="btn edit-btn">edit</router-link>
                <button class="btn delete-btn">Delete</button>
            </div>
        </div>

        <p v-if="quizzesStore.loading">Loading...</p>
        <p v-if="quizzesStore.error">An error has occured</p>
    </div>
</template>

<script>
import AdminAppHeader from '@/components/AdminAppHeader.vue';
import { useQuizzesStore } from '@/stores/QuizzesStore';
import { onMounted, ref } from 'vue';
import QuizzesList from '../components/QuizzesList.vue';

    export default {
        props: ['quizId'],
        components: { AdminAppHeader, QuizzesList },
        setup(props) {
            const quizzesStore = useQuizzesStore()
            const quizDetails = ref(null)

            async function loadQuizDetails() {
                quizDetails.value = await quizzesStore.getQuiz(props.quizId)
            }


            onMounted(async () => {
                await loadQuizDetails()
            })

            return {
                quizDetails,
                quizzesStore,
            }
        }
    }
</script>

<style scoped>

</style>