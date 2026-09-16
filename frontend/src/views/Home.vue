<template>
    <div>
        <h1>This is Home page</h1>
        <h2 v-if="authStore.isAdmin">Welcome back, admin123</h2>
        <p>user statistikasi bolish kerak shu yerda, hammasidan oxirida qilinish kerak</p>
    </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

    export default {
        setup() {
            const authStore = useAuthStore()
            const router = useRouter()

            if (!authStore.isAuthenticated) {
                router.push({ name: "Login" })
            }
            return { authStore }
        }
    }
</script>