<template>
    <main>
        <p v-if="authStore.loading">Loading...</p>
        <form @submit.prevent="handleSubmit">
            <label>Username: </label>
            <input v-model="username" type="username" required>

            <label>Email: </label>
            <input v-model="email" type="email" required>

            <label>Password: </label>
            <input v-model="password" type="password" required>

            <label>Password Confirmation: </label>
            <input v-model="passwordConfirmation" type="password" required>

            <div class="terms">
                <input type="checkbox" v-model="termsAccepted" required>
                <label class="terms-conditions">Accept terms and conditions</label>
            </div>

            <div class="form-actions">
                <button type="submit" :disabled="!termsAccepted">register</button>
                <router-link :to="{ name: 'Login' }" class="login-link">Already have an account?</router-link>
            </div>
            <p class="error">{{ authStore.error }}</p>
        </form>
    </main>
</template>

<script>
    import { useRouter } from 'vue-router';
    import { useAuthStore } from '@/stores/auth';
    import { onUnmounted, ref } from 'vue';

    export default {
        name: "Register",
        setup() {
            const authStore = useAuthStore()

            const router = useRouter()

            const termsAccepted = ref(false)
            const username = ref('')
            const email = ref('')
            const password = ref('')
            const passwordConfirmation = ref('')

            const handleSubmit = async () => {
                if (password.value !== passwordConfirmation.value) {
                    authStore.error = "Password doesn't match confirmation password"
                    passwordConfirmation.value = ''
                    return
                }
                try {
                    const response = await authStore.register({
                        username: username.value,
                        email: email.value,
                        password: password.value
                    })

                    if (response === "error") {
                        return
                    }

                    await authStore.login({
                        email: email.value,
                        password: password.value
                    })

                    router.push({ name: "Home" })
                } catch (err) {
                    console.error(err)
                }
            }

            onUnmounted(() => {
                authStore.error = null
            })

            return { handleSubmit, username, email, password, passwordConfirmation, termsAccepted, authStore }
        }
    }
</script>

<style scoped>
    .form-actions {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .form-actions a {
        text-decoration: none;
        color: rgb(77, 86, 165);
        transition: 0.2s ease;
    }

    .form-actions a:hover {
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
    input[type="checkbox"] {
        display: inline-block;
        width: 16px;
        margin: 0 10px 0 0;
        position: relative;
        top: 2px;
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
    button {
        background-color: #0b6dff;
        border: 0;
        padding: 10px 20px;
        margin-top: 20px;
        color: white;
        border-radius: 15px;
        transition: 0.2 ease;
    }
    button:hover {
        cursor: pointer;
        background-color: #0b6dffc5;
    }
    button:active {
        color: rgba(255, 255, 255, 0.673);
        background-color: #1c5a83;
    }
    button[disabled] {
        color: rgba(255, 255, 255, 0.673);
        background-color: #1c5a83;
    }
    .error {
        color: #ff0062;
        margin-top: 10px;
        font-size: 0.8em;
        font-weight: bold;
    }
</style>