import { defineStore } from "pinia";
import { ref } from "vue";

export const useResultsStore = defineStore('ResultsStore', () => {
    const loading = ref(false)
    const error = ref(null)

    async function getResult(resultId) {
        loading.value = true
        error.value = null

        try {
            const response = await this.$api.get(`/results/${resultId}`);
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
        getResult
    }
})