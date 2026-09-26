<template>
    <div v-if="quizDashboard" class="dashboard">
        <admin-app-header />

        <main class="dashboard-content">

            <!-- Statistics -->
            <section class="section">
                <h1>Quiz Statistics</h1>

                <div class="stats-grid">
                    <div class="stat-card">
                        <span class="stat-label">Total Attempts</span>
                        <span class="stat-value">
                            {{ quizDashboard[1].statistics.attempts }}
                        </span>
                    </div>

                    <div class="stat-card">
                        <span class="stat-label">Average Percentage</span>
                        <span class="stat-value">
                            {{ Math.round(quizDashboard[1].statistics.average_percentage * 100) / 100 }}%
                        </span>
                    </div>

                    <div class="stat-card">
                        <span class="stat-label">Highest Percentage</span>
                        <span class="stat-value">
                            {{ Math.round(quizDashboard[1].statistics.highest_percentage * 100) / 100 }}%
                        </span>
                    </div>

                    <div class="stat-card">
                        <span class="stat-label">Average Completion</span>
                        <span class="stat-value">
                            {{ formatTime(Math.round(quizDashboard[1].statistics.average_completion * 100) / 100) }}
                            /
                            mm:ss
                        </span>
                    </div>
                </div>
            </section>


            <!-- Score Distribution -->
            <section class="section">
                <h2>Score Distribution</h2>

                <div class="distribution">
                    <div class="score-row">
                        <span>0–20%</span>
                        <div class="bar">
                            <div class="bar-fill"
                                :style="{ width: (quizDashboard[1].score_distribution['0-20'] || 0) + '%' }">
                            </div>
                        </div>
                        <strong>{{ quizDashboard[1].score_distribution["0-20"] || 0 }}</strong>
                    </div>

                    <div class="score-row">
                        <span>21–40%</span>
                        <div class="bar">
                            <div class="bar-fill"
                                :style="{ width: (quizDashboard[1].score_distribution['21-40'] || 0) + '%' }">
                            </div>
                        </div>
                        <strong>{{ quizDashboard[1].score_distribution["21-40"] || 0 }}</strong>
                    </div>

                    <div class="score-row">
                        <span>41–60%</span>
                        <div class="bar">
                            <div class="bar-fill"
                                :style="{ width: (quizDashboard[1].score_distribution['41-60'] || 0) + '%' }">
                            </div>
                        </div>
                        <strong>{{ quizDashboard[1].score_distribution["41-60"] || 0 }}</strong>
                    </div>

                    <div class="score-row">
                        <span>61–80%</span>
                        <div class="bar">
                            <div class="bar-fill"
                                :style="{ width: (quizDashboard[1].score_distribution['61-80'] || 0) + '%' }">
                            </div>
                        </div>
                        <strong>{{ quizDashboard[1].score_distribution["61-80"] || 0 }}</strong>
                    </div>

                    <div class="score-row">
                        <span>81–100%</span>
                        <div class="bar">
                            <div class="bar-fill"
                                :style="{ width: (quizDashboard[1].score_distribution['81-100'] || 0) + '%' }">
                            </div>
                        </div>
                        <strong>{{ quizDashboard[1].score_distribution["81-100"] || 0 }}</strong>
                    </div>
                </div>
            </section>


            <!-- Leaderboard -->
            <section class="section">
                <h2>Leaderboard</h2>

                <div class="leaderboard">

                    <div class="leaderboard-header">
                        <span>Rank</span>
                        <span>User</span>
                        <span>Score</span>
                    </div>

                    <div
                        v-for="user in quizDashboard[1].top_users"
                        :key="user._id"
                        class="leaderboard-row"
                    >
                        <span
                            class="rank"
                            :class="{
                                gold: user.percentage_rank == 1,
                                silver: user.percentage_rank == 2,
                                bronze: user.percentage_rank == 3,
                                normal: user.percentage_rank > 3
                            }"
                        >
                            {{ user.percentage_rank }}
                        </span>

                        <span class="username">
                            {{ user.username || user._id }}
                        </span>

                        <span class="percentage">
                            {{ Math.round(user.percentage * 100) / 100 }}%
                        </span>
                    </div>

                </div>
            </section>

        </main>
    </div>
</template>

<script>
import { useQuizzesStore } from '@/stores/QuizzesStore';
import { onMounted, ref } from 'vue';
import AdminAppHeader from '../components/AdminAppHeader.vue';

    export default {
        components: { AdminAppHeader },
        props: ['quizId'],
        setup(props) {
            const quizzesStore = useQuizzesStore()
            const quizDashboard = ref(null)

            async function loadQuizDashboard() {
                quizDashboard.value = await quizzesStore.getQuizDashboard(props.quizId)
                quizDashboard.value = quizDashboard.value.results
            }   

            function formatTime(seconds) {
                const hours = Math.floor(seconds / 3600);
                const minutes = Math.floor((seconds % 3600) / 60);
                const secs = Math.floor(seconds % 60);

                if (hours > 0) {
                    return `${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
                }

                return `${String(minutes).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
            }

            onMounted(async () => {
                await loadQuizDashboard()
            })

            return {
                formatTime,
                quizDashboard
            }
        }
    }
</script>

<style scoped>
.dashboard {
    min-height: 100vh;
    background: #f8fafc;
    color: #1e293b;
}

.dashboard-content {
    max-width: 1000px;
    margin: 0 auto;
    padding: 40px 24px;
}

.section {
    margin-bottom: 40px;
}

.section h1,
.section h2 {
    margin: 0 0 20px;
    color: #0f172a;
}

.section h1 {
    font-size: 24px;
}

.section h2 {
    font-size: 20px;
}


/* Statistics */

.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
}

.stat-card {
    padding: 20px;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.04);
}

.stat-label {
    display: block;
    margin-bottom: 10px;
    font-size: 14px;
    color: #64748b;
}

.stat-value {
    font-size: 24px;
    font-weight: 700;
    color: #0f172a;
}


/* Score Distribution */

.distribution {
    padding: 20px;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
}

.score-row {
    display: grid;
    grid-template-columns: 70px 1fr 40px;
    gap: 12px;
    align-items: center;
    margin-bottom: 16px;
}

.score-row:last-child {
    margin-bottom: 0;
}

.score-row > span {
    font-size: 14px;
    color: #475569;
}

.score-row strong {
    text-align: right;
    color: #334155;
}

.bar {
    height: 10px;
    overflow: hidden;
    background: #e2e8f0;
    border-radius: 999px;
}

.bar-fill {
    height: 100%;
    background: #2563eb;
    border-radius: inherit;
    transition: width 0.3s ease;
}


/* Leaderboard */

.leaderboard {
    overflow: hidden;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.04);
}

.leaderboard-header,
.leaderboard-row {
    display: grid;
    grid-template-columns: 80px 1fr 40px;
    align-items: center;
    padding: 14px 20px;
}

.leaderboard-header {
    background: #f8fafc;
    border-bottom: 1px solid #e2e8f0;

    font-size: 13px;
    font-weight: 600;
    color: #64748b;
}

.leaderboard-row {
    min-height: 60px;
    border-bottom: 1px solid #f1f5f9;
}

.leaderboard-row:last-child {
    border-bottom: none;
}

.username {
    font-weight: 600;
    color: #1e293b;
}

.percentage {
    text-align: right;
    font-weight: 700;
    color: #2563eb;
}


/* Rank */

.rank {
    width: 34px;
    height: 34px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 50%;
    font-weight: 800;
}

.gold {
    background: #fef3c7;
    color: #d97706;
    border: 2px solid #f59e0b;
}

.silver {
    background: #f1f5f9;
    color: #64748b;
    border: 2px solid #94a3b8;
}

.bronze {
    background: #ffedd5;
    color: #c2410c;
    border: 2px solid #ea580c;
}

.normal {
    color: #64748b;
}


/* Mobile */

@media (max-width: 700px) {
    .dashboard-content {
        padding: 24px 16px;
    }

    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .leaderboard-header,
    .leaderboard-row {
        grid-template-columns: 55px 1fr 70px;
        padding: 12px 14px;
    }
}

@media (max-width: 450px) {
    .stats-grid {
        grid-template-columns: 1fr;
    }
}
</style>