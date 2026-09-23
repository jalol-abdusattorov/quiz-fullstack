import { defineStore } from "pinia";
import { ref } from "vue";

export const useUsersStore = defineStore('UsersStore', () => {
    const loading = ref(false)
    const error = ref(null)

    async function getUserDetails(userId) {
        loading.value = true
        error.value = null

        try {
            const response = await this.$api.get(`/users/${userId}`);
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

    async function getUserAttempts(userId, page) {
        if (page < 0) { 
            return
        }

        loading.value = true
        error.value = null

        try {
            const params = {
                params: {
                    page: page
                }
            }

            const response = await this.$api.get(`/users/${userId}/attempts`, params);
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
        getUserDetails,
        getUserAttempts
    }
})