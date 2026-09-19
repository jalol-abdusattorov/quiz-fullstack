import { defineStore } from "pinia";
import { ref } from "vue";

export const useQuestionsStore = defineStore('questionsStore', () => {
    const questions = ref([])
    const loading = ref(false)
    const error = ref(null)



    return { loading, error, questions }
})