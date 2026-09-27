```vue
<template>
    <main class="dashboard">

        <!-- No Statistics -->
        <EmptyStats v-if="!userStats" />

        <template v-if="userStats">

            <!-- Statistics -->
            <div class="stats-container">
                <div class="stats-header">
                    <div>
                        <span class="section-label">YOUR PERFORMANCE</span>
                        <h2 class="title">Your Statistics</h2>
                        <p class="subtitle">
                            An overview of your quiz performance.
                        </p>
                    </div>
                </div>

                <div class="cards-grid">

                    <!-- Average Score -->
                    <div class="stat-card blue">
                        <div class="card-header">
                            <span class="card-icon">📈</span>
                            <span>Average Score</span>
                        </div>

                        <div class="card-body">
                            <span class="stat-number">
                                {{ Math.round(userStats.average_score * 100) / 100 }}
                            </span>
                            <span class="stat-suffix">%</span>
                        </div>
                    </div>

                    <!-- Quizzes Completed -->
                    <div class="stat-card green">
                        <div class="card-header">
                            <span class="card-icon">✓</span>
                            <span>Quizzes Completed</span>
                        </div>

                        <div class="card-body">
                            <span class="stat-number">
                                {{ userStats.quizzes_taken }}
                            </span>
                        </div>
                    </div>

                    <!-- Best Score -->
                    <div class="stat-card orange">
                        <div class="card-header">
                            <span class="card-icon">🏆</span>
                            <span>Best Score</span>
                        </div>

                        <div class="card-body">
                            <span class="stat-number">
                                {{ userStats.best_score }}
                            </span>
                            <span class="stat-suffix">%</span>
                        </div>
                    </div>

                </div>
            </div>

            <!-- Divider -->
            <div class="section-divider"></div>

            <!-- Recent Attempts -->
            <section class="recent-attempts">

                <div class="recent-header">
                    <div>
                        <span class="section-label">HISTORY</span>
                        <h1>Recent Attempts</h1>
                        <p>
                            Your latest completed quizzes.
                        </p>
                    </div>
                </div>

                <!-- Attempts exist -->
                <div
                    v-if="userRecentAttempts"
                    class="quizzes"
                >
                    <QuizzesComponent
                        :quizzes="userRecentAttempts"
                    />
                </div>

                <!-- No attempts -->
                <div
                    v-else
                    class="no-recent-attempts"
                >
                    <div class="recent-empty-icon">
                        📝
                    </div>

                    <h2>No Recent Attempts</h2>

                    <p>
                        You haven't completed any quizzes recently.
                        Your completed quizzes will appear here.
                    </p>

                    <router-link
                        class="recent-quizzes-link"
                        :to="{ name: 'Quizzes' }"
                    >
                        Find a Quiz
                        <span>→</span>
                    </router-link>
                </div>

            </section>

        </template>

    </main>
</template>

<script>
import { useAuthStore } from '@/stores/auth';
import { useQuizzesStore } from '@/stores/QuizzesStore';
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import QuizzesComponent from '@/components/QuizzesComponent.vue';
import EmptyStats from '@/components/EmptyStats.vue';

    export default {
        components: { QuizzesComponent, EmptyStats },
        name: "Home",
        setup() {
            const authStore = useAuthStore()
            const quizzesStore = useQuizzesStore()
            const router = useRouter()
            const userStats = ref(null)
            const userRecentAttempts = ref([])

            async function userStatistics() {
                userStats.value = await quizzesStore.getUserStatistics(authStore.user.id)
                if (userStats.value?.message === "this user has no statistics") {
                    userStats.value = null
                } else {
                    userStats.value = userStats.value.result[0]
                }
            }

            async function userRecentAttemptsFunc() {
                userRecentAttempts.value = await quizzesStore.getUserRecentAttepmts(authStore.user.id)
                if (userRecentAttempts.value?.message === "this user has no recent attemtps") {
                  userRecentAttempts.value = null
                } else {
                  userRecentAttempts.value = userRecentAttempts.value.result
                }
            }

            onMounted(() => {
              if (!authStore.isAuthenticated) {
                router.push({ name: "Login" })
              }
              userStatistics()
              userRecentAttemptsFunc()
            })

            return { authStore, userStats, userRecentAttempts }
        }
    }
</script>


<style scoped>
/* =========================================================
   Main
========================================================= */

.dashboard {
    min-height: 100vh;
    padding: 40px 24px 70px;
    background: #f8fafc;
    color: #0f172a;
    box-sizing: border-box;
}


/* =========================================================
   Statistics Container
========================================================= */

.stats-container {
    width: min(1000px, 100%);
    margin: 0 auto;

    padding: 28px;

    background: #ffffff;

    border: 1px solid #e2e8f0;
    border-radius: 16px;

    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04);

    box-sizing: border-box;
}

.stats-header {
    margin-bottom: 24px;
}

.section-label {
    display: block;

    margin-bottom: 6px;

    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.09em;

    color: #2563eb;
}

.title {
    margin: 0;

    font-family: 'Poppins', 'Inter', sans-serif;
    font-size: 1.55rem;
    font-weight: 700;

    color: #0f172a;
}

.subtitle {
    margin: 5px 0 0;

    font-family: 'Inter', sans-serif;
    font-size: 0.875rem;

    color: #64748b;
}


/* =========================================================
   Statistics Cards
========================================================= */

/* =========================================================
   Statistics Cards
========================================================= */

.cards-grid {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: stretch;
    gap: 20px;
}

.stat-card {
    flex: 1;
    min-width: 180px;
    overflow: hidden;
    background: #ffffff;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    transition:
        transform 0.18s ease,
        box-shadow 0.18s ease;
}

.stat-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

/* Card Header */

.card-header {
    color: #ffffff;
    font-family: 'Inter', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    padding: 12px 16px;
}

/* Remove the icon styling visually */
.card-icon {
    display: none;
}

/* Card Body */

.card-body {
    min-height: 95px;
    padding: 24px 16px;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #ffffff;
}

/* Number */

.stat-number {
    font-family: 'Poppins', 'Inter', sans-serif;
    font-size: 2.75rem;
    font-weight: 700;
    line-height: 1;
    margin: 0;
}

.stat-suffix {
    margin-left: 4px;
    font-family: 'Poppins', 'Inter', sans-serif;
    font-size: 1rem;
    font-weight: 600;
}

/* =========================================================
   Blue Card
========================================================= */

.stat-card.blue {
    border: 2px solid #2b6cb0;
}

.stat-card.blue .card-header {
    background-color: #2b6cb0;
}

.stat-card.blue .stat-number,
.stat-card.blue .stat-suffix {
    color: #1a365d;
}

/* =========================================================
   Green Card
========================================================= */

.stat-card.green {
    border: 2px solid #38a169;
}

.stat-card.green .card-header {
    background-color: #38a169;
}

.stat-card.green .stat-number {
    color: #2f855a;
}

/* =========================================================
   Orange Card
========================================================= */

.stat-card.orange {
    border: 2px solid #dd6b20;
}

.stat-card.orange .card-header {
    background-color: #dd6b20;
}

.stat-card.orange .stat-number,
.stat-card.orange .stat-suffix {
    color: #dd6b20;
}


/* =========================================================
   Divider
========================================================= */

.section-divider {
    width: min(1000px, 100%);
    height: 1px;

    margin: 42px auto;

    background: #e2e8f0;
}


/* =========================================================
   Recent Attempts
========================================================= */

.recent-attempts {
    width: min(1000px, 100%);
    margin: 0 auto;
}

.recent-header {
    margin-bottom: 20px;
}

.recent-header h1 {
    margin: 0;

    font-family: 'Poppins', 'Inter', sans-serif;
    font-size: 1.45rem;
    font-weight: 700;

    color: #0f172a;
}

.recent-header p {
    margin: 5px 0 0;

    font-family: 'Inter', sans-serif;
    font-size: 0.875rem;

    color: #64748b;
}


/* Quiz List */

.quizzes {
    display: flex;
    flex-direction: column;
    gap: 14px;
}


/* =========================================================
   No Recent Attempts
========================================================= */

.no-recent-attempts {
    display: flex;
    flex-direction: column;
    align-items: center;

    padding: 44px 30px;

    text-align: center;

    background: #ffffff;

    border: 1px dashed #cbd5e1;
    border-radius: 14px;
}

.recent-empty-icon {
    width: 58px;
    height: 58px;

    display: flex;
    align-items: center;
    justify-content: center;

    margin-bottom: 16px;

    border-radius: 14px;

    background: #f8fafc;
    border: 1px solid #e2e8f0;

    font-size: 25px;
}

.no-recent-attempts h2 {
    margin: 0 0 8px;

    font-family: 'Poppins', 'Inter', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;

    color: #0f172a;
}

.no-recent-attempts p {
    max-width: 420px;

    margin: 0 0 20px;

    font-family: 'Inter', sans-serif;
    font-size: 0.875rem;
    line-height: 1.6;

    color: #64748b;
}


/* Recent Quiz Link */

.recent-quizzes-link {
    display: inline-flex;
    align-items: center;
    gap: 7px;

    padding: 9px 15px;

    border: 1px solid #dbeafe;
    border-radius: 8px;

    background: #eff6ff;
    color: #1d4ed8;

    font-family: 'Inter', sans-serif;
    font-size: 0.825rem;
    font-weight: 600;

    text-decoration: none;

    transition:
        background 0.18s ease,
        border-color 0.18s ease;
}

.recent-quizzes-link span {
    transition: transform 0.18s ease;
}

.recent-quizzes-link:hover {
    background: #dbeafe;
    border-color: #bfdbfe;
}

.recent-quizzes-link:hover span {
    transform: translateX(3px);
}


/* =========================================================
   Responsive
========================================================= */

@media (max-width: 800px) {
    .dashboard {
        padding: 28px 16px 50px;
    }

    .stats-container {
        padding: 22px;
    }

    .cards-grid {
        flex-direction: column;
    }

    .stat-card {
        width: 100%;
    }
}

@media (max-width: 520px) {
    .dashboard {
        padding: 20px 12px 40px;
    }

    .stats-container {
        padding: 18px;
        border-radius: 13px;
    }

    .title {
        font-size: 1.35rem;
    }

    .stat-number {
        font-size: 2.4rem;
    }

    .card-body {
        min-height: 80px;
        padding: 22px 16px;
    }

    .section-divider {
        margin: 30px auto;
    }

    .recent-header h1 {
        font-size: 1.3rem;
    }

    .no-recent-attempts {
        padding: 34px 20px;
    }
}
</style>