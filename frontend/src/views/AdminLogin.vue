<template>
    <div class="login-container">
        <form @submit.prevent="handleSubmit" class="login-form">
            <h2>Admin Login</h2>

            <label>Email</label>
            <input
                v-model="email"
                type="email"
                placeholder="Email"
                required
            >

            <label>Password</label>
            <div class="password-input">
                <input
                    v-model="password"
                    :type="showPassword ? 'text' : 'password'"
                    placeholder="Password"
                    required
                >

                <button
                    type="button"
                    class="password-toggle"
                    @click="showPassword = !showPassword"
                >
                    {{ showPassword ? 'Hide' : 'Show' }}
                </button>
            </div>

            <button type="submit">Login</button>

            <p v-if="authStore.error" class="error">
                {{ authStore.error }}
            </p>
        </form>
    </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

    export default {
        setup() {
            const authStore = useAuthStore()
            const email = ref('')
            const password = ref('')
            const showPassword = ref(false)
            const router = useRouter()

            const handleSubmit = async () => {
                if (email.value.trim().length == 0 || password.value.trim().length == 0) {
                    return
                }

                await authStore.login({ email: email.value, password: password.value })
                if (!authStore.isAdmin) {
                    authStore.error = "Incorrect email or password"
                    return
                }
                router.push({ name: "AdminDashboard" })
            }


            return { email, password, showPassword, handleSubmit, authStore }
        }
    }
</script>

<style scoped>
.login-container {
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #f5f5f5;
}

.login-form {
    width: 350px;
    padding: 30px;
    background: white;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.login-form h2 {
    text-align: center;
    margin-bottom: 25px;
}

.login-form label {
    display: block;
    margin-bottom: 5px;
}

.login-form input {
    width: 100%;
    box-sizing: border-box;
    padding: 10px;
    margin-bottom: 15px;
    border: 1px solid #ccc;
    border-radius: 5px;
}

.password-input {
    position: relative;
}

.password-input input {
    padding-right: 60px;
}

.password-toggle {
    position: absolute;
    top: 8px;
    right: 8px;

    /* Remove top/transform positioning entirely to avoid layout shifts */
    bottom: auto;
    transform: none;

    margin: 0;
    padding: 4px 10px;

    /* Primary theme colors */
    background: #e0e7ff;
    color: #4f46e5;

    border: 1px solid #c7d2fe;
    border-radius: 6px;

    font-size: 11px;
    font-weight: 600;

    cursor: pointer;

    /* Fix dimensions so size changes never trigger mouse leave/enter loops */
    box-sizing: border-box;

    transition: color 0.2s ease, background-color 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
}

.password-toggle:hover {
    color: #ffffff;
    background: #4f46e5;
    border-color: #4f46e5;
    box-shadow: 0 2px 8px rgba(79, 70, 229, 0.25);
}

.password-toggle:active {
    background: #4338ca;
    box-shadow: none;
}

.login-form > button {
    width: 100%;
    padding: 10px;
    border: none;
    border-radius: 5px;
    background: #2563eb;
    color: white;
    cursor: pointer;
}

.login-form > button:hover {
    background: #1d4ed8;
}

.error {
    color: red;
    text-align: center;
}
</style>