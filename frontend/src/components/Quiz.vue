<template>
    <div class="quiz-card">
        <div class="card-content">
            <h3 class="quiz-title">{{ quiz.title }}</h3>
            <p class="quiz-description">{{ quiz.description || 'No description provided' }}</p>
            <p class="quiz-category">Category: {{ quiz.category }}</p>
            <p class="quiz-difficulty">{{ quiz.difficulty }} difficulty</p>
            <p class="quiz-questions">{{ quiz.question_ids?.length || 0 }} Questions</p>
            <p class="quiz-timelimit">{{ formatTime(quiz.time_limit) }}</p>
        </div>
        <router-link :to="{ name: 'QuizDetails', params: { id: quiz._id } }" class="view-btn">View quiz</router-link>
    </div>
</template>

<script>
    export default {
        props: ['quiz'],
        setup() {
            const formatTime = (seconds) => {
                if (!seconds) return
                const mins = Math.floor(seconds / 60)
                const secs = seconds % 60
                return `${mins}m ${secs}s`
            }

            return { formatTime }
        }
    }
</script>

<style scoped>
.quiz-card {
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.quiz-card a {
    width: 200px;
    text-align: center;
    text-decoration: none;
}

.quiz-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
}

.quiz-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
  color: #0f172a;
}

.quiz-description {
  color: #64748b;
  font-size: 0.875rem;
  line-height: 1.5;
  margin: 0;
}

.quiz-category {
  color: #444;
  line-height: 1.5;
  margin: 0;
  margin-top: 10px;
}

.quiz-difficulty {
  color: #444;
  line-height: 1;
  margin: 0;
}

.quiz-questions {
  color: #444;
  line-height: 1;
  margin: 0;
}

.view-btn {
  margin-top: 1.5rem;
  width: 100%;
  padding: 0.625rem;
  background-color: #4f46e5;
  color: #ffffff;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.view-btn:hover {
  background-color: #4338ca;
}
</style>