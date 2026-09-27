<template>
    <div class="dashboard">
        <admin-app-header />

        <p v-if="!quizDashboard" class="empty-dashboard">
            <span class="empty-icon">📊</span>

            <span class="empty-title">No Statistics Yet</span>

            <span class="empty-text">
                This quiz hasn't been attempted yet.
                Statistics will appear here once someone completes the quiz.
            </span>
        </p>

        <main class="dashboard-content" v-if="quizDashboard">
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
                            {{ formatTime(quizDashboard[1].statistics.average_completion) }}
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
                                :style="{
                                    width: ((quizDashboard[1].score_distribution['0-20'] || 0) /
                                        quizDashboard[1].statistics.attempts * 100) + '%'
                                }">
                            </div>
                        </div>
                        <strong>{{ quizDashboard[1].score_distribution["0-20"] || 0 }}</strong>
                    </div>

                    <div class="score-row">
                        <span>21–40%</span>
                        <div class="bar">
                            <div class="bar-fill"
                                :style="{
                                    width: ((quizDashboard[1].score_distribution['21-40'] || 0) /
                                        quizDashboard[1].statistics.attempts * 100) + '%'
                                }">
                            </div>
                        </div>
                        <strong>{{ quizDashboard[1].score_distribution["21-40"] || 0 }}</strong>
                    </div>

                    <div class="score-row">
                        <span>41–60%</span>
                        <div class="bar">
                            <div class="bar-fill"
                                :style="{
                                    width: ((quizDashboard[1].score_distribution['41-60'] || 0) /
                                        quizDashboard[1].statistics.attempts * 100) + '%'
                                }">
                            </div>
                        </div>
                        <strong>{{ quizDashboard[1].score_distribution["41-60"] || 0 }}</strong>
                    </div>

                    <div class="score-row">
                        <span>61–80%</span>
                        <div class="bar">
                            <div class="bar-fill"
                                :style="{
                                    width: ((quizDashboard[1].score_distribution['61-80'] || 0) /
                                        quizDashboard[1].statistics.attempts * 100) + '%'
                                }">
                            </div>
                        </div>
                        <strong>{{ quizDashboard[1].score_distribution["61-80"] || 0 }}</strong>
                    </div>

                    <div class="score-row">
                        <span>81–100%</span>
                        <div class="bar">
                            <div class="bar-fill"
                                :style="{
                                    width: ((quizDashboard[1].score_distribution['81-100'] || 0) /
                                        quizDashboard[1].statistics.attempts * 100) + '%'
                                }">
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
                if (quizDashboard.value?.message == "this quiz haven't been tried yet") {
                    quizDashboard.value = null
                } else {
                    quizDashboard.value = quizDashboard.value.results
                }
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
                quizDashboard,
                quizzesStore
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
    padding: 36px 24px 60px;
}

.section {
    margin-bottom: 42px;
}

.section h1,
.section h2 {
    margin: 0 0 18px;
    color: #0f172a;
}

.section h1 {
    font-size: 24px;
    font-weight: 700;
    letter-spacing: -0.3px;
}

.section h2 {
    font-size: 18px;
    font-weight: 700;
}


/* =========================
   Statistics
========================= */

.empty-dashboard {
    width: min(600px, calc(100% - 40px));
    margin: 80px auto;
    padding: 40px 32px;

    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;

    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;

    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
}

.empty-icon {
    display: flex;
    align-items: center;
    justify-content: center;

    width: 64px;
    height: 64px;
    margin-bottom: 18px;

    border-radius: 16px;
    background: #eff6ff;

    font-size: 28px;
}

.empty-title {
    margin-bottom: 8px;

    font-size: 20px;
    font-weight: 700;
    color: #0f172a;
}

.empty-text {
    max-width: 440px;

    font-size: 14px;
    line-height: 1.6;
    color: #64748b;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
}

.stat-card {
    min-height: 92px;
    padding: 18px 20px;

    display: flex;
    flex-direction: column;
    justify-content: center;

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
    box-shadow: 0 6px 16px rgba(15, 23, 42, 0.07);
}

.stat-label {
    display: block;
    margin-bottom: 8px;

    font-size: 13px;
    font-weight: 500;
    color: #64748b;
}

.stat-value {
    display: block;

    font-size: 23px;
    line-height: 1.2;
    font-weight: 700;
    color: #0f172a;
}


/* =========================
   Score Distribution
========================= */

.distribution {
    padding: 22px;

    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;

    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.03);
}

.score-row {
    display: grid;
    grid-template-columns: 72px minmax(0, 1fr) 32px;
    gap: 14px;
    align-items: center;

    margin-bottom: 17px;
}

.score-row:last-child {
    margin-bottom: 0;
}

.score-row > span {
    font-size: 13px;
    font-weight: 500;
    color: #475569;
}

.score-row strong {
    text-align: right;

    font-size: 13px;
    font-weight: 700;
    color: #334155;
}

.bar {
    height: 9px;

    overflow: hidden;

    background: #e8eef5;
    border-radius: 999px;
}

.bar-fill {
    height: 100%;

    min-width: 4px;

    background: #2563eb;
    border-radius: inherit;

    transition: width 0.4s ease;
}


/* =========================
   Leaderboard
========================= */

.leaderboard {
    overflow: hidden;

    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;

    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);
}

.leaderboard-header,
.leaderboard-row {
    display: grid;
    grid-template-columns: 70px minmax(0, 1fr) 80px;

    align-items: center;

    padding: 14px 20px;
}

.leaderboard-header {
    min-height: 42px;

    background: #f8fafc;
    border-bottom: 1px solid #e2e8f0;

    font-size: 12px;
    font-weight: 600;
    color: #64748b;
}

.leaderboard-header span:last-child {
    text-align: right;
}

.leaderboard-row {
    min-height: 66px;

    border-bottom: 1px solid #f1f5f9;

    transition: background 0.15s ease;
}

.leaderboard-row:hover {
    background: #fafcff;
}

.leaderboard-row:last-child {
    border-bottom: none;
}

.username {
    min-width: 0;

    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;

    font-size: 14px;
    font-weight: 600;
    color: #1e293b;
}

.percentage {
    text-align: right;

    font-size: 14px;
    font-weight: 700;
    color: #2563eb;
}


/* =========================
   Rank
========================= */

.rank {
    display: inline-flex;
    align-items: center;
    justify-content: center;

    width: 34px;
    height: 34px;

    border-radius: 50%;

    font-size: 13px;
    font-weight: 700;

    transition:
        transform 0.15s ease,
        box-shadow 0.15s ease;
}

.rank:hover {
    transform: translateY(-1px) scale(1.04);
}


/* 1st */

.gold {
    background: linear-gradient(135deg, #fff7d6, #fde68a);
    color: #a16207;

    border: 1px solid #f59e0b;

    box-shadow: 0 2px 7px rgba(245, 158, 11, 0.25);
}


/* 2nd */

.silver {
    background: linear-gradient(135deg, #f8fafc, #e2e8f0);
    color: #475569;

    border: 1px solid #94a3b8;

    box-shadow: 0 2px 7px rgba(100, 116, 139, 0.18);
}


/* 3rd */

.bronze {
    background: linear-gradient(135deg, #fff1e6, #fed7aa);
    color: #9a3412;

    border: 1px solid #ea580c;

    box-shadow: 0 2px 7px rgba(234, 88, 12, 0.2);
}


/* Other positions */

.normal {
    background: #f8fafc;
    color: #64748b;

    border: 1px solid #cbd5e1;
}


/* =========================
   Mobile
========================= */

@media (max-width: 800px) {
    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 600px) {
    .dashboard-content {
        padding: 28px 16px 48px;
    }

    .section {
        margin-bottom: 34px;
    }

    .section h1 {
        font-size: 22px;
    }

    .section h2 {
        font-size: 17px;
    }

    .stats-grid {
        grid-template-columns: 1fr 1fr;
        gap: 12px;
    }

    .stat-card {
        min-height: 86px;
        padding: 15px;
    }

    .stat-value {
        font-size: 20px;
    }

    .distribution {
        padding: 18px 16px;
    }

    .score-row {
        grid-template-columns: 65px minmax(0, 1fr) 25px;
        gap: 10px;
    }

    .leaderboard-header,
    .leaderboard-row {
        grid-template-columns: 52px minmax(0, 1fr) 65px;
        padding-left: 14px;
        padding-right: 14px;
    }
}

@media (max-width: 420px) {
    .stats-grid {
        grid-template-columns: 1fr;
    }

    .stat-card {
        min-height: 78px;
    }

    .score-row {
        grid-template-columns: 62px minmax(0, 1fr) 24px;
        gap: 8px;
    }

    .score-row > span,
    .score-row strong {
        font-size: 12px;
    }

    .leaderboard-header,
    .leaderboard-row {
        grid-template-columns: 48px minmax(0, 1fr) 60px;
    }
}
</style>