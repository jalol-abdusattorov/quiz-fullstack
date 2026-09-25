import { defineStore } from "pinia";
import { ref } from "vue";

export const useAdminStore = defineStore('AdminStore', () => {
    const loading = ref(false)
    const error = ref(null)

    async function getAdminDashboard() {
        loading.value = true
        error.value = null

        try {
            const response = await this.$api.get("/admin/get-dashboard");
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
        getAdminDashboard
    }
})