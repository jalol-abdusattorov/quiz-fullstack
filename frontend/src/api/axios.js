import { useAuthStore } from "@/stores/auth";
import axios from "axios";

const api = axios.create({
    baseURL: 'http://localhost:8000'
    // baseURL: 'http://192.168.100.103:5173'
})

api.interceptors.request.use(
    (config) => {
        const authStore = useAuthStore()
        // console.log(authStore);
        if (authStore.token) {
            config.headers.Authorization = `Bearer ${authStore.token}`
        }

        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

export default api