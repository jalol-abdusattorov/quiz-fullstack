<template>
    <main>
        <div class="container">
            <div class="quiz-card">
                <div class="card-content">
                    <h3 class="quiz-title">{{ quiz.title }}</h3>
                    <p class="quiz-description">{{ quiz.description || 'No description provided' }}</p>
                    <p class="quiz-category">Category: {{ quiz.category }}</p>
                    <p class="quiz-difficulty">{{ quiz.difficulty }} difficulty</p>
                    <p class="quiz-questions">{{ quiz.question_ids?.length || 0 }} Questions</p>
                    <p class="quiz-timelimit">Time Limit - {{ formatTime(quiz.time_limit) }}</p>
                </div>
            </div>
            <div>
                <button class="back-btn" @click="handleBack">Back</button>
                <button class="start-btn" @click="console.log('Start');">Start the quiz</button>
            </div>
        </div>
    </main>
</template>

<script>
import { useRouter } from 'vue-router';

    export default {
        props: ['quiz'],
        setup() {
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

            return { formatTime, handleBack }
        }
    }
</script>

<style scoped>
    /* main {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
    } */
    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        /* justify-content: center; */
        min-height: 100vh;
    }

    .quiz-card {
        width: 600px;
        /* height: 400px; */
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

    .quiz-description {
        color: #64748b;
        font-size: 0.875rem;
        line-height: 1.5;
        margin: 0;
    }

    .quiz-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
    }

    .start-btn {
        padding: 20px;
        background-color: rgb(117, 231, 92);
        border: none;
        border-radius: 10px;
        transition: 0.2s ease;
    }

    .start-btn:hover {
        background-color: rgba(117, 231, 92, 0.618);
    }

    .start-btn:active {
        background-color: rgba(117, 231, 92, 0.322);
    }

    /* ------------ */

    .back-btn {
        padding: 20px;
        background-color: rgb(255, 69, 56);
        border: none;
        border-radius: 10px;
        transition: 0.2s ease;
    }

    .back-btn:hover {
        background-color: rgba(255, 69, 56, 0.647);
    }

    .back-btn:active {
        background-color: rgba(255, 69, 56, 0.29);
    }

</style>