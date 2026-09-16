import { defineStore } from "pinia";
import { ref } from "vue";

export const useQuizzesStore = defineStore('quizzesStore', () => {
    const quizzes = ref([])
    const loading = ref(false)
    const error = ref(null)

    async function getQuizzes(page) {
        loading.value = true
        error.value = null

        try {
            // http://localhost:8000
            const response = await this.$api.get(`/quizzes/get-all-quizzes/${page}`)
            const data = response.data
            quizzes.value = data.quizzes

            return data
        } catch (exception) {
            error.value = exception.message || exception
            console.error(exception);
        } finally {
            loading.value = false
        }
    }

    async function getQuiz(quizId) {
        loading.value = true
        error.value = null
        try {
            const response = await this.$api.get(`/quizzes/${quizId}`)
            const data = response.data
            // console.log(data);

            return data
        } catch (exception) {
            error.value = exception.message || exception
        } finally {
            loading.value = false
        }
    }

    async function getPopularQuizzes(page) {
        loading.value = true
        error.value = null
        try {
            const response = await this.$api.get(`/quizzes/popular/${page}`)
            const data = response.data
            quizzes.value = data

            return data
        } catch (exc) {
            error.value = exc.message || exc``
        } finally {
            loading.value = false
        }
    }

    return { quizzes, loading, error, getQuizzes, getQuiz, getPopularQuizzes }
})