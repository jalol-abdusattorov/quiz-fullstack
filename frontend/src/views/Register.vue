<template>
    <main>
        <p v-if="authStore.loading">Loading...</p>

        <form @submit.prevent="handleSubmit">
            <label>Username:</label>
            <input v-model="username" type="username" required>

            <label>Email:</label>
            <input v-model="email" type="email" required>

            <label>Password:</label>

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

            <!-- Password strength -->
            <div v-if="password" class="password-strength">
                <div class="strength-header">
                    <span>Password strength</span>
                    <strong>{{ strengthLabel }}</strong>
                </div>

                <div class="strength-bar">
                    <span
                        v-for="segment in 5"
                        :key="segment"
                        class="strength-segment"
                        :class="{
                            active: segment <= zxcvbnResult.score + 1,
                            weak: zxcvbnResult.score <= 1 && segment <= zxcvbnResult.score + 1,
                            medium: zxcvbnResult.score === 2 && segment <= zxcvbnResult.score + 1,
                            strong: zxcvbnResult.score === 3 && segment <= zxcvbnResult.score + 1,
                            veryStrong: zxcvbnResult.score === 4 && segment <= zxcvbnResult.score + 1
                        }"
                    ></span>
                </div>

                <p class="strength-hint">
                    <span v-if="zxcvbnResult.score === 0">
                        Try adding more characters and variety.
                    </span>
                    <span v-else-if="zxcvbnResult.score === 1">
                        Your password could be easier to guess.
                    </span>
                    <span v-else-if="zxcvbnResult.score === 2">
                        Good start, but it can be stronger.
                    </span>
                    <span v-else-if="zxcvbnResult.score === 3">
                        Nice! Your password is strong.
                    </span>
                    <span v-else>
                        Excellent! This is a very strong password.
                    </span>
                </p>
            </div>

            <label>Password Confirmation:</label>

            <div class="password-input">
                <input
                    v-model="passwordConfirmation"
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

            <div class="terms">
                <input type="checkbox" v-model="termsAccepted" required>
                <label class="terms-conditions">
                    Accept terms and conditions
                </label>
            </div>

            <div class="form-actions">
                <button type="submit" :disabled="!termsAccepted || !validPassword">
                    Register
                </button>
                
                <router-link
                    :to="{ name: 'Login' }"
                    class="login-link"
                    >
                    Already have an account?
                </router-link>
            </div>

            <p class="error" v-if="!validPassword" >{{ error }}</p>
            <p class="error">{{ authStore.error }}</p>
        </form>
    </main>
</template>

<script>
    import { useRouter } from 'vue-router';
    import { useAuthStore } from '@/stores/auth';
    import { computed, onUnmounted, ref } from 'vue';
    import { checkPassword } from '@/utils/passwordChecker';

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
            const showPassword = ref(false)
            const error = ref('')

            const togglePassword = () => {
                showPassword.value = !showPassword.value
            }

            const zxcvbnResult = computed(() => checkPassword(password.value))
            const strengthLabel = computed(() => {
                if (!password.value) return ''

                  const labels = {
                    0: 'Too Weak 🔴',
                    1: 'Weak 🔴',
                    2: 'Medium 🟡',
                    3: 'Strong 🟢',
                    4: 'Very Strong ✨'
                }

                return labels[zxcvbnResult.value.score]
            })

            const validPassword = computed(() => {
                if (username.value.trim().length <= 4) {
                    error.value = "Username is too short"
                    return false
                }

                if (!password.value) {
                    error.value = "Enter password"
                    return false
                }

                if (zxcvbnResult.value.score < 3) {
                    error.value = "Password isn't strong enough"
                    return false
                }
                if (password.value !== passwordConfirmation.value) {
                    error.value = "Password is not same as confirmation password"
                    return false
                }

                error.value = null
                return true
            })

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
                error.value = null
            })

            return {
                username,
                email,
                password,
                passwordConfirmation,
                showPassword,
                togglePassword,
                termsAccepted,
                strengthLabel,
                zxcvbnResult,
                error,
                validPassword,
                authStore,
                handleSubmit,
            }
        }
    }
</script>

<style scoped>
.form-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
}

.form-actions a {
    text-decoration: none;
    color: #4d56a5;
    transition: 0.2s ease;
}

.form-actions a:hover {
    text-decoration: underline;
}

form {
    max-width: 420px;
    margin: 30px auto;
    background: #ffffff;
    text-align: left;
    padding: 40px;
    border-radius: 14px;
    box-shadow: 0 8px 30px rgba(15, 23, 42, 0.08);
}

label {
    color: #2c3e50;
    display: inline-block;
    margin: 25px 0 10px;
    font-size: 0.6em;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: bold;
}

input {
    display: block;
    padding: 11px 6px;
    width: 100%;
    box-sizing: border-box;
    border: none;
    border-bottom: 1px solid #ddd;
    color: #555;
    outline: none;
    transition: 0.2s ease;
}

input:focus {
    border-bottom-color: #4f46e5;
}

.password-input {
    position: relative;
    width: 100%;
    display: flex;
    align-items: center; /* Flex alignment handles vertical centering cleanly */
}

.password-input input {
    padding-right: 70px;
}

.password-toggle {
    position: absolute;
    right: 8px;
    
    /* Remove top/transform positioning entirely to avoid layout shifts */
    top: auto;
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

/* =========================
   PASSWORD STRENGTH
   ========================= */

.password-strength {
    margin-top: 14px;
    padding: 14px 15px;
    border-radius: 10px;
    background: #f8fafc;
    border: 1px solid #e8edf3;
}

.strength-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
}

.strength-header span {
    font-size: 11px;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.7px;
}

.strength-header strong {
    font-size: 12px;
    color: #475569;
}

/* Five little segments */

.strength-bar {
    display: flex;
    gap: 5px;
    width: 100%;
}

.strength-segment {
    height: 6px;
    flex: 1;
    border-radius: 10px;
    background: #e2e8f0;
    transition:
        background-color 0.25s ease,
        transform 0.25s ease;
}

.strength-segment.active {
    transform: scaleY(1.15);
}

/* Weak */

.strength-segment.weak {
    background: #ef4444;
}

/* Medium */

.strength-segment.medium {
    background: #eab308;
}

/* Strong */

.strength-segment.strong {
    background: #22c55e;
}

/* Very strong */

.strength-segment.veryStrong {
    background: #10b981;
}

/* Small explanation underneath */

.strength-hint {
    margin: 9px 0 0;
    color: #94a3b8;
    font-size: 11px;
    line-height: 1.4;
}

/* =========================
   TERMS
   ========================= */

.terms {
    display: flex;
    align-items: center;
    margin-top: 25px;
}

.terms input[type="checkbox"] {
    display: inline-block;
    width: 16px;
    height: 16px;
    margin: 0 9px 0 0;
    position: relative;
    top: 0;
}

.terms .terms-conditions {
    margin: 0;
    font-size: 11px;
    text-transform: none;
    letter-spacing: 0;
    font-weight: 500;
    color: #64748b;
}

/* =========================
   BUTTON
   ========================= */

button {
    background-color: #4f46e5;
    border: 0;
    padding: 11px 22px;
    margin-top: 20px;
    color: white;
    border-radius: 9px;
    font-size: 13px;
    font-weight: 600;
    transition:
        background-color 0.2s ease,
        transform 0.2s ease,
        box-shadow 0.2s ease;
}

button:hover:not(:disabled) {
    cursor: pointer;
    background-color: #4338ca;
    transform: translateY(-1px);
    box-shadow: 0 5px 12px rgba(79, 70, 229, 0.2);
}

button:active:not(:disabled) {
    transform: translateY(0);
}

button[disabled] {
    cursor: not-allowed;
    background-color: #cbd5e1;
    color: #f8fafc;
}

/* =========================
   ERROR
   ========================= */

.error {
    color: #e11d48;
    margin-top: 12px;
    font-size: 0.8em;
    font-weight: 600;
}
</style>