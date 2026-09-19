<template>
    <div>
        <header class="navbar">
            <router-link :to="{ name: 'Home' }" class="brand">Quiz</router-link>
            <nav class="router-links">
                <!-- ADMIN -->
                <template v-if="isAdmin">
                    <router-link class="nav-btn" :to="{ name: 'Home' }">Home</router-link>
                    <router-link class="nav-btn" :to="{ name: 'Quizzes' }">Quizzes</router-link>
                    <router-link class="nav-btn" :to="{ name: 'QuizBrowser' }">Browse Quizzes</router-link>
                    <router-link class="nav-btn" :to="{ name: 'Logout' }">Logout</router-link>
                </template>

                <!-- LOGGED IN -->
                <template v-else-if="isAuthenticated">
                    <router-link class="nav-btn" :to="{ name: 'Home' }">Home</router-link>
                    <router-link class="nav-btn" :to="{ name: 'Quizzes' }">Quizzes</router-link>
                    <router-link class="nav-btn" :to="{ name: 'QuizBrowser' }">Browse Quizzes</router-link>
                    <router-link class="nav-btn" :to="{ name: 'Logout' }">Logout</router-link>
                </template>

                <!-- LOGGED OUT -->
                <template v-else>
                    <router-link class="nav-btn" :to="{ name: 'Login' }">Login</router-link>
                    <router-link class="nav-btn" :to="{ name: 'Register' }">Register</router-link>
                </template>
            </nav>
        </header>
    </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth';
import { storeToRefs } from 'pinia';

    export default {
        name: "AppHeader",
        setup() {
            const authStore = useAuthStore()
            const { isAuthenticated, isAdmin } = storeToRefs(authStore)
            return { isAuthenticated, isAdmin }
        }
    }
</script>


<style scoped>
.navbar {
  background-color: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 2px rgba(0, 0, 0, 0.137);
}

.brand {
  font-size: 1.25rem;
  font-weight: 700;
  color: #4f46e5;
  text-decoration: none;
  margin-right: auto;
}

.nav-links {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.nav-btn {
  background: none;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #64748b;
  text-decoration: none;
  transition: all 0.2s ease;
  display: inline-block;
}

.nav-btn:hover {
  background-color: #f1f5f9;
  color: #0f172a;
}

/* Styled active state for current page using exact active class */
.nav-btn.router-link-exact-active {
  background-color: #e0e7ff;
  color: #4f46e5;
  font-weight: 600;
}

/* Hover style for Logout link */
.nav-btn.logout:hover {
  background-color: #fef2f2;
  color: #ef4444;
}

/* Optional: custom active style when sitting on the /logout route */
.nav-btn.logout.router-link-exact-active {
  background-color: #fef2f2;
  color: #ef4444;
}
</style>