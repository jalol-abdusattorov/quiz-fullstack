<template>
    <main>
        <div class="container">
            <div>
                <button class="back-btn" @click="handleBack">← Back to Quizzes</button>
                <div class="quiz-card">
                    <div class="card-content">
                        <h1 class="quiz-title">{{ quiz.title }}</h1>
                        <h3>{{ quiz.description || 'No description provided' }}</h3>
                        <h3 class="quiz-category">Category: {{ quiz.category }}</h3>
                        <h3 class="quiz-difficulty">Difficulty: {{ quiz.difficulty }}</h3>
                        <h3 class="quiz-questions">Questions: {{ quiz.question_ids?.length || 0 }}</h3>
                        <h3 class="quiz-timelimit">Time Limit: {{ formatTime(quiz.time_limit) }}</h3>
                        <button class="start-btn" :disabled="submitted" @click="handleStart">Start the quiz</button>
                        <div class="actions">
                            <button @click="handleLeaderboard">Leaderboard</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>
</template>

<script>
import { useQuizzesStore } from '@/stores/QuizzesStore';
import { onUnmounted, ref } from 'vue';
import { useRouter } from 'vue-router';

    export default {
        props: ['quiz'],
        setup(props) {
            const quizzesStore = useQuizzesStore()
            const router = useRouter()
            const submitted = ref(false)

            const formatTime = (seconds) => {
                if (!seconds) return
                const mins = Math.floor(seconds / 60)
                const secs = seconds % 60
                return `${mins}m ${secs}s`
            }

            const handleBack = () => {
                router.back()                
            }
            const handleStart = async () => {
                submitted.value = true
                const response = await quizzesStore.startQuiz(props.quiz._id)
                router.push({ name: 'TakingQuiz', params: { id: props.quiz._id, attemptId: response.attempt_id } })
            }

            const handleLeaderboard = () => {
                router.push({ name: "Leaderboard", params: { quizId: props.quiz._id } })
            }

            onUnmounted(() => {
                submitted.value = false
            })

            return { submitted, formatTime, handleBack, handleStart, handleLeaderboard }
        }
    }
</script>

<style scoped>
.container {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 100vh;
    margin-top: 20px;
}

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
    margin-top: 10px;
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


/* Quiz Card */
.quiz-card {
    width: 600px;
    background-color: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.5rem;
    display: flex;
    flex-direction: columns;
    justify-content: space-between;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.quiz-card:hover {
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
}

.quiz-description {
    color: #64748b;
    font-size: 0.875rem;
    line-height: 1.5;
    margin: 0;
}

/* Start Button */
.start-btn {
  background-color: #F97316;
  color: #FFFFFF;
  font-weight: 600;
  font-size: 1rem;
  margin-top: 10px;
  padding: 10px 240px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.1s ease;
}

.start-btn:hover {
  background-color: #EA580C;
}

.start-btn:active {
  /* Press effect, shrinks little bit */
  transform: scale(0.98);
}
.start-btn:disabled {
    color: #baaeae;
    background-color: #944a15;
}


/* Back Button */
.back-btn {
  padding: 20px;
  background-color: #E5E7EB;
  color: #374151;
  border: none;
  border-radius: 9px;
}
.back-btn:hover {
  background-color: #D1D5DB;
}

</style>