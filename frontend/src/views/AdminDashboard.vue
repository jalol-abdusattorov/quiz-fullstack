<template>
    <main>
        <admin-app-header />
        <div class="container">
            <div v-if="adminDashboardData && popularQuizzes">
                <h1>Admin Dashboard</h1>
                <p>Total Users: {{ adminDashboardData.total_users }}</p>
                <p>Total Quizzes: {{ adminDashboardData.total_quizzes }}</p>
                <p>Total Questions: {{ adminDashboardData.total_questions }}</p>
                <p>Total Attempts: {{ adminDashboardData.total_attempts }}</p>
                <hr>
                <h1>Trending/Popular Quizzes</h1>
                <QuizzesList :quizzes="popularQuizzes" :is-popular-quizzes="true" :showManageButton="true" />
            </div>
        </div>
    </main>
</template>

<script>
import { useAdminStore } from '@/stores/AdminStore.js';
import AdminAppHeader from '../components/AdminAppHeader.vue';
import { onMounted, ref } from 'vue';
import { useAuthStore } from '@/stores/auth.js';
import { useRouter } from 'vue-router';
import { useQuizzesStore } from '@/stores/QuizzesStore.js';
import QuizzesList from '@/components/QuizzesList.vue';

    export default {
        components: { AdminAppHeader, QuizzesList },
        setup() {
            const adminStore = useAdminStore()
            const quizzesStore = useQuizzesStore()
            const adminDashboardData = ref(null)
            const popularQuizzes = ref(null)

            async function loadAdminDashboardData() {
                adminDashboardData.value = await adminStore.getAdminDashboard()
            }
            async function loadPopularQuizzes() {
                popularQuizzes.value = await quizzesStore.getPopularQuizzes(1)
                popularQuizzes.value = popularQuizzes.value.result
            }

            onMounted(() => {
                if (!useAuthStore().isAdmin) useRouter().push({ name: "Login" })
                loadAdminDashboardData()
                loadPopularQuizzes()
            })

            return { adminDashboardData, popularQuizzes }
        }
    }
</script>

<style scoped>
.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}
</style>