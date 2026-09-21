<template>  
    <div class="quiz-card" v-if="quiz">
      <div class="card-content">
          <h3 class="quiz-title">{{ quiz.title }}</h3>
          <p class="quiz-description">{{ substring(quiz.description) || 'No description provided' }}</p>
          <p class="quiz-category-difficulty">{{ quiz.category }} · {{ quiz.difficulty }}</p>
          <p class="quiz-questions">{{ quiz.question_ids?.length || 0 }} Questions · {{ formatTime(quiz.time_limit) }}</p>
          <p class="quiz-date">Created at:<br>{{ formatDate(quiz.created_at) }}</p>
          <p class="quiz-recent-attempt" v-if="quiz.completed_at">Recent attempt:<br>{{ formatDate(quiz.completed_at) }}</p>
      </div>
      <router-link v-if="quiz?._id"  :to="{ name: 'QuizDetails', params: { id: quiz._id } }" class="view-btn">View quiz</router-link>
    </div>
</template>

<script>
    export default {
        props: ['quiz'],
        setup(props) {
            const formatTime = (seconds) => {
                if (!seconds) return
                const mins = Math.floor(seconds / 60)
                const secs = seconds % 60
                return `${mins}m ${secs}s`
            }
            const formatDate = (date) => {
              const monthMap = {
                "01": "January",
                "02": "February",
                "03": "March",
                "04": "April",
                "05": "May",
                "06": "June",
                "07": "July",
                "08": "August",
                "09": "September",
                "10": "October",
                "11": "November",
                "12": "December"
              }

              date = date.substring(0, 10)
              const year = date.slice(0, 4) // Year
              const month = date.slice(5, 7) // Month
              const day = date.slice(-2) // Day
              const fullMonth = monthMap[String(month)]
              return `Year ${year}, ${day} of ${fullMonth}`
            }

            const substring = (sentence) => {
              if (!sentence) return

              if (sentence.length > 50) {
                sentence = sentence.substring(0, 50) + "..."
              }
              return sentence
            }

            return { formatTime, formatDate, substring }
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
.quiz-date {
  color: #64748b;
  font-size: 0.875rem;
  line-height: 1;
  margin: 0;
  margin-top: 10px;
}
.quiz-recent-attempt {
  color: #64748b;
  font-size: 0.875rem;
  line-height: 1.2;
  margin: 0;
  margin-top: 10px;
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
  line-height: 0;
  margin-top: 10px;
  margin-bottom: 25px;
}
.quiz-category-difficulty {
  color: #444;
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