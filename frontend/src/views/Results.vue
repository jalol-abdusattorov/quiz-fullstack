<template>
    <div v-if="quizStore.result" class="results-page">
        <h1>Quiz completed</h1>
        <h2 v-if="quiz">{{ quiz.title }}</h2>

        <div class="stat-result">
            <h3>{{ quizStore.result.score }} / {{ quizStore.result.total_questions }}</h3>
            <h3>{{ Math.round(quizStore.result.percentage * 100) / 100 }}%</h3>
        </div>
        <div class="result">
            <h3>Total questions: {{ quizStore.result.total_questions }}</h3>
            <h3>Correct: {{ quizStore.result.score }}</h3>
            <h3>Incorrect: {{ quizStore.result.total_questions - quizStore.result.score }}</h3>
            <h3>Time: {{ formatTime(quizStore.result.time_taken) }}</h3>
        </div>
        <div class="actions">
            <button @click="handleReviewAnswers">Review Answers</button>
            <button @click="handleLeaderboard">Leaderboard</button>
            <button @click="hanldeTryAgain">Try Again</button>
        </div>
    </div>
</template>

<script>
import { useQuizzesStore } from '@/stores/QuizzesStore';
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
    setup() {
        const quizStore = useQuizzesStore()
        const quiz = ref(null)
        const router = useRouter()

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

        const getQuizDetails = async () => {
            quiz.value = await quizStore.getQuiz(quizStore.result.quiz_id)
        }

        const hanldeTryAgain = () => {
            router.replace({ name: "QuizDetails", params: { id: quizStore.result.quiz_id } })
        }
        const handleReviewAnswers = () => {
            router.replace({ name: 'ReviewAnswers' })
        }

        const handleLeaderboard = () => {
            router.push({ name: 'Leaderboard', params: { quizId: quiz.value._id } })
        }

        onMounted(() => {
            if (!quizStore.result) {
                router.replace({ name: 'Home' })
                return
            }
            getQuizDetails()
        })

        return { handleLeaderboard, formatTime, handleReviewAnswers, hanldeTryAgain, quizStore, quiz }
    }
}
</script>

<style scoped>
.results-page {
    font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
    max-width: 480px;
    margin: 2rem auto;
    padding: 2rem 1.5rem;
    background: #ffffff;
    border-radius: 16px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
    text-align: center;
    color: #1f2937;
}

.results-page h1 {
    margin: 0 0 0.25rem;
    font-size: 1.75rem;
    font-weight: 700;
}

.results-page h2 {
    margin: 0 0 1.5rem;
    font-size: 1.05rem;
    font-weight: 500;
    color: #6b7280;
}

/* Score + percentage */
.stat-result {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.stat-result h3 {
    flex: 1;
    margin: 0;
    padding: 1.25rem 0.5rem;
    font-size: 1.75rem;
    font-weight: 700;
    color: #4f46e5;
    background: #eef2ff;
    border-radius: 12px;
}

/* Breakdown list */
.result {
    margin-bottom: 1.75rem;
    text-align: left;
}

.result h3 {
    margin: 0;
    padding: 0.75rem 0.25rem;
    font-size: 1rem;
    font-weight: 500;
    border-bottom: 1px solid #e5e7eb;
}

.result h3:last-child {
    border-bottom: none;
}

/* Buttons */
.actions {
    font-family: inherit;
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    justify-content: center;
}

.actions button {
    flex: 1 1 130px;
    padding: 0.75rem 1rem;
    font-size: 0.95rem;
    font-weight: 600;
    color: #374151;
    background: #ffffff;
    border: 1px solid #d1d5db;
    border-radius: 10px;
    cursor: pointer;
    transition: background 0.15s, border-color 0.15s, transform 0.05s;
}

.actions button:hover {
    background: #f3f4f6;
    border-color: #9ca3af;
}

.actions button:active {
    transform: translateY(1px);
}

/* "Try Again" is the primary action */
.actions button:last-child {
    color: #ffffff;
    background: #4f46e5;
    border-color: #4f46e5;
}

.actions button:last-child:hover {
    background: #4338ca;
    border-color: #4338ca;
}

@media (max-width: 480px) {
    .results-page {
        margin: 1rem;
        padding: 1.5rem 1rem;
    }

    .stat-result h3 {
        font-size: 1.4rem;
    }
}
</style>