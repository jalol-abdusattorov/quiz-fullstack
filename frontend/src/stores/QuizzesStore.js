import { defineStore } from "pinia";
import { ref } from "vue";

export const useQuizzesStore = defineStore('quizzesStore', () => {
    const quizzes = ref([])
    const loading = ref(false)
    const error = ref(null)
    const result = ref(null)

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
            console.error(exception);
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
        } catch (exception) {
            error.value = exception.message || exception
            console.error(exception);
        } finally {
            loading.value = false
        }
    }

    async function getQuizzesByCategory(category, page) {
        loading.value = true
        error.value = null

        try {
            const response = await this.$api.get(`/quizzes/category/${category}/${page}`)
            const data = response.data
            // console.log(data.result);
            quizzes.value = data.result

            return data
        } catch (exception) {
            error.value = exception.message || exception
            console.error(exception);
        } finally {
            loading.value = false
        }
    }

    async function getUserStatistics(userId) {
        loading.value = true
        error.value = null

        try {
            const response = await this.$api.get(`/users/${userId}/statistics`)
            const data = response.data
            // console.log(data.result);

            return data
        } catch (exception) {
            error.value = exception.message || exc
        } finally {
            loading.value = false
        }
    }

    async function getUserRecentAttepmts(userId) {
        loading.value = true
        error.value = null

        try {
            const response = await this.$api.get(`/users/${userId}/recent-attempts`)
            const data = response.data
            // console.log(data.result);

            return data
        } catch (exception) {
            error.value = exception.message || exception
            console.error(exception);
        } finally {
            loading.value = false
        }
    }
    
    async function filterQuizzes(category, difficulty, sortingBy, sortingOrder, page) {
        loading.value = true
        error.value = null

        try {
            const params = {
                params: {
                    category: category,
                    difficulty: difficulty,
                    sorting_by: sortingBy,
                    sorting_order: sortingOrder,
                    page: page
                }
            }

            const response = await this.$api.get(`/quizzes`, params)
            const data = response.data
            // console.log(data);
            quizzes.value = data.result

            return data
        } catch (exception) {
            error.value = exception.message || exception
            console.error(exception);
        } finally {
            loading.value = false
        }
    }

    async function searchQuiz(searchBy, search, page) {
        search = search.trim()
        loading.value = true
        error.value = null

        try {
            const params = {
                params: {
                    search_by: searchBy,
                    search: search
                }
            }

            const response = await this.$api.get(`/quizzes/search/${page}`, params)
            const data = response.data
            quizzes.value = data

            return data
        } catch (exception) {
            error.value = exception.message || exception
            console.error(exception);
        } finally {
            loading.value = false
        }
    }

    async function getQuizQuestions(quizId) {
        loading.value = true
        error.value = null

        try {
            const response = await this.$api.get(`/quizzes/${quizId}/questions`)
            const data = response.data
            // console.log(data);

            return data
        } catch (exception) {
            error.value = exception.message || exception
        } finally {
            loading.value = false
        }
    }

    async function startQuiz(quizId) {
        if (!quizId) return
        loading.value = true
        error.value = null

        try {
            const response = await this.$api.post(`/quizzes/${quizId}/start`)
            const data = response.data
            // console.log(data)

            return data
        } catch (exception) {
            error.value = exception.message || exception
        } finally {
            loading.value = false
        }
    }

    async function submitQuiz(quizId, attemptId, userAnswers) {
        loading.value = true
        error.value = null

        try {
            const params = {
                attempt_id: attemptId,
                answers: userAnswers
            }

            const response = await this.$api.post(`/quizzes/${quizId}/submit`, params)
            const data = response.data
            setResult(data)
            // console.log(result.value);

            return data
        } catch (exception) {
            error.value = exception.message || exception
        } finally {
            loading.value = false
        }
    }

    function setResult(newResult) {
        result.value = newResult
    }

    function clearResult() {
        result.value = null
    }

    return {
        result,
        clearResult,
        setResult,
        submitQuiz,
        startQuiz,
        getQuizQuestions,
        quizzes,
        loading,
        error,
        getQuizzes,
        getQuiz,
        getPopularQuizzes,
        getQuizzesByCategory,
        getUserStatistics,
        getUserRecentAttepmts,
        filterQuizzes,
        searchQuiz
    }
})