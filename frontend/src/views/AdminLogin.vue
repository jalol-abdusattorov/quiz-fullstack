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
                    class="toggle-password"
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

.toggle-password {
    position: absolute;
    right: 10px;
    top: 8px;

    border: none;
    background: none;
    color: #2563eb;
    cursor: pointer;
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