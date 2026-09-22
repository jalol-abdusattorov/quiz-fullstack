import { defineStore } from "pinia";
import { ref } from "vue";

export const useQuestionsStore = defineStore('questionsStore', () => {
    const loading = ref(false)
    const error = ref(null)

    async function getQuestionDetails(questionId) {
        loading.value = true
        error.value = null

        try {
            const response = await this.$api.get(`/questions/${questionId}`);
            const data = response.data;
            // console.log(data);
            
            return data
        } catch (exception) {
            error.value = exception.message || exception
            console.error(exception);
        } finally {
            loading.value = false
        }
    }

    return {
        loading,
        error,
        getQuestionDetails
    }
})