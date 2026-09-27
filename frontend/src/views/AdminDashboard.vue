<template>
    <main class="dashboard">
        <admin-app-header />

        <div class="container" v-if="adminDashboardData && popularQuizzes">

            <!-- Header -->
            <div class="page-header">
                <div>
                    <h1>Admin Dashboard</h1>
                    <p>Overview of your quiz platform</p>
                </div>
            </div>


            <!-- Statistics -->
            <section class="section">

                <div class="stats-grid">

                    <div class="stat-card">
                        <div class="stat-icon users-icon">
                            👥
                        </div>

                        <div class="stat-info">
                            <span class="stat-label">Total Users</span>
                            <strong class="stat-value">
                                {{ adminDashboardData.total_users }}
                            </strong>
                        </div>
                    </div>


                    <div class="stat-card">
                        <div class="stat-icon quizzes-icon">
                            📝
                        </div>

                        <div class="stat-info">
                            <span class="stat-label">Total Quizzes</span>
                            <strong class="stat-value">
                                {{ adminDashboardData.total_quizzes }}
                            </strong>
                        </div>
                    </div>


                    <div class="stat-card">
                        <div class="stat-icon questions-icon">
                            ❓
                        </div>

                        <div class="stat-info">
                            <span class="stat-label">Total Questions</span>
                            <strong class="stat-value">
                                {{ adminDashboardData.total_questions }}
                            </strong>
                        </div>
                    </div>


                    <div class="stat-card">
                        <div class="stat-icon attempts-icon">
                            📊
                        </div>

                        <div class="stat-info">
                            <span class="stat-label">Total Attempts</span>
                            <strong class="stat-value">
                                {{ adminDashboardData.total_attempts }}
                            </strong>
                        </div>
                    </div>

                </div>

            </section>


            <!-- Popular Quizzes -->
            <section class="section popular-section">

                <div class="section-header">
                    <div>
                        <h2>Trending & Popular Quizzes</h2>
                        <p>Quizzes getting the most attention from users</p>
                    </div>
                </div>


                <div class="quiz-panel">
                    <QuizzesList
                        :quizzes="popularQuizzes"
                        :is-popular-quizzes="true"
                        :showManageButton="true"
                    />
                </div>

            </section>

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
/* =========================
   Dashboard
========================= */

.dashboard {
    min-height: 100vh;
    background: #f8fafc;
    color: #1e293b;
}

.container {
    max-width: 1100px;
    margin: 0 auto;
    padding: 36px 24px 60px;
}


/* =========================
   Page Header
========================= */

.page-header {
    margin-bottom: 30px;
}

.page-header h1 {
    margin: 0 0 6px;

    font-size: 26px;
    font-weight: 700;
    letter-spacing: -0.4px;

    color: #0f172a;
}

.page-header p {
    margin: 0;

    font-size: 14px;
    color: #64748b;
}


/* =========================
   Sections
========================= */

.section {
    margin-bottom: 42px;
}


/* =========================
   Statistics
========================= */

.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
}

.stat-card {
    display: flex;
    align-items: center;

    min-height: 100px;
    padding: 18px;

    background: #ffffff;

    border: 1px solid #e2e8f0;
    border-radius: 12px;

    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);

    transition:
        transform 0.15s ease,
        box-shadow 0.15s ease,
        border-color 0.15s ease;
}

.stat-card:hover {
    transform: translateY(-2px);

    border-color: #dbe3ee;

    box-shadow:
        0 6px 16px rgba(15, 23, 42, 0.07);
}


/* Icon */

.stat-icon {
    display: flex;
    align-items: center;
    justify-content: center;

    width: 46px;
    height: 46px;

    flex-shrink: 0;

    border-radius: 10px;

    font-size: 21px;
}


/* Different subtle backgrounds */

.users-icon {
    background: #eff6ff;
}

.quizzes-icon {
    background: #f5f3ff;
}

.questions-icon {
    background: #fefce8;
}

.attempts-icon {
    background: #ecfdf5;
}


/* Text */

.stat-info {
    min-width: 0;
    margin-left: 14px;
}

.stat-label {
    display: block;

    margin-bottom: 5px;

    font-size: 13px;
    font-weight: 500;

    color: #64748b;
}

.stat-value {
    display: block;

    font-size: 24px;
    line-height: 1.2;

    color: #0f172a;
}


/* =========================
   Popular Quizzes
========================= */

.section-header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;

    margin-bottom: 16px;
}

.section-header h2 {
    margin: 0 0 5px;

    font-size: 19px;
    font-weight: 700;

    color: #0f172a;
}

.section-header p {
    margin: 0;

    font-size: 13px;
    color: #64748b;
}


/* Quiz container */

.quiz-panel {
    padding: 20px;

    background: #ffffff;

    border: 1px solid #e2e8f0;
    border-radius: 12px;

    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);
}


/* =========================
   Responsive
========================= */

@media (max-width: 900px) {
    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 600px) {
    .container {
        padding: 28px 16px 48px;
    }

    .page-header h1 {
        font-size: 23px;
    }

    .stats-grid {
        grid-template-columns: 1fr;
        gap: 12px;
    }

    .stat-card {
        min-height: 86px;
    }

    .quiz-panel {
        padding: 14px;
    }
}
</style>