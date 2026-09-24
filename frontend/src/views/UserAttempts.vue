<template>
    <main class="container" v-if="userAttempts">
        <div class="page-header">
            <div>
                <h1>My Attempts</h1>
                <p>{{ totalAttempts }} attempts in total</p>
            </div>
            <label class="sort">
                Sort by
                <select>
                    <option value="newestFirst">Newest first</option>
                    <option value="oldestFirst">Oldest first</option>
                    <option value="highestAccuracy">Highest accuracy</option>
                    <option value="lowestAccuracy">Lowest accuracy</option>
                </select>
            </label>
        </div>

        <section class="table-card">
            <div class="row head">
                <span>Quiz</span>
                <span>Date</span>
                <span>Score</span>
                <span>Percentage</span>
                <span>Time taken</span>
                <span></span>
            </div>
            
            <div class="row" v-for="attempt in userAttempts" :key="attempt.id">
                <div>
                    <div class="quiz-name">{{ attempt.quiz_title }}</div>
                    <div class="quiz-meta">{{ attempt.quiz_category }} · {{ attempt.quiz_difficulty }}</div>
                </div>
                <div data-label="Date">{{ formatDate(attempt.started_at) }}</div>
                <div data-label="Score">{{ attempt.score }} / {{ attempt.total_questions }}</div>
                <div data-label="Percentage">
                    <span class="badge" :class="level(attempt.percentage)">{{ Math.round(attempt.percentage * 100) / 100 }}%</span>
                    <div class="bar">
                        <span :class="level(attempt.percentage)" :style="{ width: attempt.percentage + '%' }"></span>
                    </div>
                </div>
                <div data-label="Time taken">{{ formatTime(attempt.time_taken) }}</div>
                <!-- Fix: router-link -->
                <button class="btn" @click="ViewQuizResult(attempt._id)">View result</button>
                <!-- <p>{{ attempt }}</p> -->
            </div>
        </section>

        <div class="pagination">
            <span class="count">Showing {{ userAttempts.length }} of {{ totalAttempts }}</span>
            <div class="pager">
                <span class="page">Page 1</span>
                <button @click="prevPage" :disabled="currentPage <= 1">Previous</button>
                <button @click="nextPage" :disabled="currentPage > totalAttempts % 10">Next</button>
            </div>
        </div>
        <!-- <p>{{ userAttempts }}</p> -->
    </main>
</template>

<script>
import { useAuthStore } from '@/stores/auth';
import { useQuizzesStore } from '@/stores/QuizzesStore';
import { useResultsStore } from '@/stores/Results';
import { useUsersStore } from '@/stores/Users';
import { computed, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

    export default {
        setup() {
            const authStore = useAuthStore()
            const usersStore = useUsersStore()
            const resultsStore = useResultsStore()
            const quizzesStore = useQuizzesStore()
            const userAttempts = ref(null)
            const totalAttempts = ref(0)
            const currentPage = ref(1)
            const router = useRouter()
            const userId = computed(() => {
                return authStore.user.id || null
            })

            const nextPage = () => {
                if (currentPage.value > totalAttempts.value % 10) return
                currentPage.value++
                loadUserAttempts()
            }
            const prevPage = () => {
                if (currentPage.value <= 1) return
                currentPage.value--
                loadUserAttempts()
            }

            const level = (p) => (p >= 80 ? 'good' : p >= 60 ? 'mid' : 'low')

            async function loadUserAttempts() {
                if (userId.value == null) return

                userAttempts.value = await usersStore.getUserAttempts(userId.value, currentPage.value)
                if (userAttempts.value?.message == "this user has no attempts on this page") {
                    userAttempts.value = null
                    return
                }
                totalAttempts.value = userAttempts.value.total_attempts
                userAttempts.value = userAttempts.value.result
            }

            async function ViewQuizResult(resultId) {
                if (!resultId) return
                const response = await resultsStore.getResult(resultId)
                quizzesStore.setResult(response)

                router.replace({ name: "ReviewAnswers" })
            }

            const formatTime = (seconds) => {
                if (seconds == null) return '-'

                const total = Math.round(Number(seconds))
                const h = Math.floor(total / 3600)
                const m = Math.floor((total % 3600) / 60)
                const s = total % 60

                if (h > 0) return `${h}h ${m}m ${s}s`
                if (m > 0) return `${m}m ${String(s).padStart(2, '0')}s`
                return `${s}s`
            }
            const formatDate = (date) => {
              if (!date) return
              const monthMap = {
                "01": "Jan",
                "02": "Feb",
                "03": "Mar",
                "04": "Apr",
                "05": "May",
                "06": "Jun",
                "07": "Jul",
                "08": "Aug",
                "09": "Sep",
                "10": "Oct",
                "11": "Nov",
                "12": "Dec"
              }
              date = date.substring(0, 10)
              const year = date.slice(0, 4) // Year
              const month = date.slice(5, 7) // Month
              const day = date.slice(-2) // Day
              const fullMonth = monthMap[String(month)]
              return `${day} ${fullMonth}, ${year}`
            }

            onMounted(() => {
                loadUserAttempts()
            })

            return {
                ViewQuizResult,
                nextPage,
                prevPage,
                userAttempts,
                currentPage,
                level,
                formatDate,
                totalAttempts,
                formatTime
            }
        }
    }
</script>

<style scoped>
.container {
    --indigo: #4f46e5;
    --indigo-dark: #4338ca;
    --card: #ffffff;
    --text: #111827;
    --muted: #6b7280;
    --line: #e5e7eb;
    --green-bg: #dcfce7;
    --green-text: #166534;
    --green-bar: #22a55a;
    --amber-bg: #fef3c7;
    --amber-text: #92400e;
    --amber-bar: #e39a17;
    --red-bg: #fee2e2;
    --red-text: #991b1b;
    --red-bar: #dc3a3a;
}

.container,
.container * {
    box-sizing: border-box;
}

/* Page */
.container {
    max-width: 1100px;
    margin: 0 auto;
    padding: 40px 24px 60px;
}

.page-header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 16px;
    margin-bottom: 20px;
}

.page-header h1 {
    margin: 0;
    font-size: 32px;
    font-weight: 700;
}

.page-header p {
    margin: 4px 0 0;
    color: var(--muted);
    font-size: 15px;
}

.sort {
    display: flex;
    align-items: center;
    gap: 10px;
    color: var(--muted);
    font-size: 15px;
}

.sort select {
    padding: 9px 14px;
    font-size: 15px;
    border: 1px solid #9ca3af;
    border-radius: 8px;
    background: var(--card);
    color: var(--text);
}

/* Table */
.table-card {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 14px;
    overflow: hidden;
}

.row {
    display: grid;
    grid-template-columns: 2.4fr 1fr 0.8fr 1.5fr 1fr 1.1fr;
    gap: 12px;
    align-items: center;
    padding: 18px 24px;
    border-top: 1px solid var(--line);
}

.row.head {
    border-top: none;
    background: #f9fafb;
    font-size: 13px;
    font-weight: 600;
    color: var(--muted);
    padding-top: 14px;
    padding-bottom: 14px;
}

.quiz-name { font-size: 17px; font-weight: 600; }

.quiz-meta {
    margin-top: 3px;
    font-size: 14px;
    color: var(--muted);
}

.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 600;
}

.badge.good { background: var(--green-bg); color: var(--green-text); }
.badge.mid  { background: var(--amber-bg); color: var(--amber-text); }
.badge.low  { background: var(--red-bg);   color: var(--red-text); }

.bar {
    height: 6px;
    margin-top: 8px;
    background: #eef0f3;
    border-radius: 3px;
    overflow: hidden;
    max-width: 160px;
}

.bar span { display: block; height: 100%; border-radius: 3px; }
.bar .good { background: var(--green-bar); }
.bar .mid  { background: var(--amber-bar); }
.bar .low  { background: var(--red-bar); }

.btn {
    display: inline-block;
    padding: 10px 16px;
    border: none;
    border-radius: 8px;
    background: var(--indigo);
    color: #fff;
    font-size: 14px;
    font-weight: 600;
    text-align: center;
    text-decoration: none;
    cursor: pointer;
}

.btn:hover { background: var(--indigo-dark); }

/* Pagination */
.pagination {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 20px;
}

.pagination .count { color: var(--muted); font-size: 15px; }

.pager { display: flex; align-items: center; gap: 10px; }

.pager .page { color: var(--indigo); font-size: 15px; }

.pager button {
    padding: 9px 16px;
    font-size: 15px;
    background: var(--card);
    border: 1px solid #d1d5db;
    border-radius: 8px;
    color: var(--text);
    cursor: pointer;
}

.pager button:hover:not(:disabled) { background: #f3f4f6; }
.pager button:disabled { color: #9ca3af; cursor: not-allowed; }

/* Mobile: each row becomes a stacked card */
@media (max-width: 800px) {
    .navbar { padding: 12px 16px; }
    .nav-links a { padding: 8px 10px; font-size: 13px; }

    .row.head { display: none; }

    .row {
    grid-template-columns: 1fr 1fr;
    row-gap: 10px;
    }

    .row > :first-child,
    .row > :last-child { grid-column: 1 / -1; }

    .row [data-label]::before {
    content: attr(data-label);
    display: block;
    font-size: 12px;
    color: var(--muted);
    margin-bottom: 2px;
    }
}
</style>