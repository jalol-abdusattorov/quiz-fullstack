<template>
    <div>
        <form @submit.prevent="handleSubmit">
            <label>Email</label>
            <input v-model="email" type="email" required>

            <label>Password</label>
            <div class="password-input">
                <input 
                    v-model="password" 
                    :type="showPassword ? 'text' : 'password'" 
                    required
                >
                <button 
                    type="button" 
                    class="password-toggle" 
                    @click="togglePassword"
                    :aria-label="showPassword ? 'Hide password' : 'Show password'"
                >
                    {{ showPassword ? 'Hide' : 'Show' }}
                </button>
            </div>

            <div class="form-actions">
                <button type="submit" class="login-btn">Login</button>
                <router-link class="register-link" :to="{ name: 'Register' }">Don't have an account?</router-link>
            </div>
            <p class="error">{{ authStore.error }}</p>
        </form>
    </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth';
import { onUnmounted, ref } from 'vue';
import { useRouter } from 'vue-router'

    export default {
        name: "Login",
        setup() {
            const authStore = useAuthStore()
            const router = useRouter()

            const email = ref('')
            const password = ref('')
            const showPassword = ref(false)

            const togglePassword = () => {
                showPassword.value = !showPassword.value
            }

            const handleSubmit = async () => {
                try {
                    await authStore.login({ email: email.value, password: password.value })
                    router.push({ name: "Home" })
                } catch (exc) {
                    
                }
            }
            onUnmounted(() => {
                authStore.error = null
            })

            return { email, password, showPassword, togglePassword, authStore, handleSubmit }
        }
    }
</script>

<style scoped>
a {
    text-decoration: none;
    color: rgb(77, 86, 165);
    transition: 0.2s ease;
}

a:hover {
    text-decoration: underline;
}
form {
    max-width: 420px;
    margin: 30px auto;
    background: white;
    text-align: left;
    padding: 40px;
    border-radius: 10px;
}
label {
    color: #2c3e50;
    display: inline-block;
    margin: 25px 0 15px;
    font-size: 0.6em;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: bold;
}
input {
    display: block;
    padding: 10px 6px;
    width: 100%;
    box-sizing: border-box;
    border: none;
    border-bottom: 1px solid #ddd;
    color: #555;
}

/* Password Input Wrapper & Toggle Styling */
.password-input {
    position: relative;
    width: 100%;
    display: flex;
    align-items: center;
}

.password-input input {
    padding-right: 70px;
}

.password-toggle {
    position: absolute;
    right: 0;
    
    /* Clear general button margins and positioning shifts */
    margin: 0;
    padding: 4px 10px;

    /* Primary Indigo Theme */
    background: #e0e7ff;
    color: #4f46e5;

    border: 1px solid #c7d2fe;
    border-radius: 6px;

    font-size: 11px;
    font-weight: 600;

    cursor: pointer;
    box-sizing: border-box;

    transition: color 0.2s ease, background-color 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
}

.password-toggle:hover {
    color: #ffffff;
    background-color: #4f46e5;
    border-color: #4f46e5;
    box-shadow: 0 2px 8px rgba(79, 70, 229, 0.25);
}

.password-toggle:active {
    color: #ffffff;
    background-color: #4338ca;
    border-color: #4338ca;
    box-shadow: none;
}

.pill {
    display: inline-block;
    margin: 20px 10px 0 0;
    padding: 6px 12px;
    background: #eee;
    border-radius: 20px;
    font-size: 12px;
    letter-spacing: 1px;
    font-weight: bold;
    color: #777;
    cursor: pointer;
}

button.login-btn {
    background-color: #0b6dff;
    border: 0;
    padding: 10px 20px;
    margin-top: 20px;
    color: white;
    border-radius: 15px;
    transition: 0.2s ease;
}
button.login-btn:hover {
    cursor: pointer;
    background-color: #0b6dffc5;
}
button.login-btn:active {
    color: rgba(255, 255, 255, 0.673);
    background-color: #1c5a83;
}
button.login-btn[disabled] {
    color: rgba(255, 255, 255, 0.673);
    background-color: #1c5a83;
}

.error {
    color: #ff0062;
    margin-top: 10px;
    font-size: 0.8em;
    font-weight: bold;
}
.form-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 15px;
}
</style>