<template>
  <div class="not-found">
    <h1>404 - Page Not Found</h1>
    <p>The page you are looking for does not exist.</p>
    <router-link :to="{ name: 'Home' }" v-if="authStore.isAuthenticated">Go back to Home</router-link>
    <template v-else>
        <router-link :to="{ name: 'Login' }">Login</router-link> |
        <router-link :to="{ name: 'Register' }">Register</router-link>
    </template>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth';

    export default {
        name: "NotFound",
        setup() {
            const authStore = useAuthStore()

            return { authStore }
        }
    }
</script>

<style scoped>
    .not-found {
        text-align: center;
        margin-top: 50px;
    }
    a {
        text-decoration: none;
        color: rgb(77, 86, 165);
        transition: 0.2s ease;
    }

    a:hover {
        text-decoration: underline;
    }
</style>