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
                        <button class="start-btn" @click="handleStart">Start the quiz</button>
                    </div>
                </div>
            </div>
        </div>
    </main>
</template>

<script>
import { useRouter } from 'vue-router';

    export default {
        props: ['quiz'],
        setup(props) {
            const router = useRouter()

            const formatTime = (seconds) => {
                if (!seconds) return
                const mins = Math.floor(seconds / 60)
                const secs = seconds % 60
                return `${mins}m ${secs}s`
            }

            const handleBack = () => {
                router.back()                
            }
            const handleStart = () => {
                router.push({ name: 'TakingQuiz', params: { id: props.quiz.id } })
            }

            return { formatTime, handleBack, handleStart }
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