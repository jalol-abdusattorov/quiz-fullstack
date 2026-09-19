<template>
    <main>
        <div class="container">
            <div v-if="quiz" class="quiz-info">
                <h1>{{ quiz.title }}</h1>
                <h2>Question  {{ currentQuestionNav + 1 }} / {{ quiz.question_ids.length }}</h2>
                <h2>Time  {{ formattedTime }}s</h2>
            </div>
            <div>
                <div v-if="currentQuestion" class="question-card">
                    <Question :question="currentQuestion"/>
                    <div class="actions">
                        <button class="page-btn" @click="prevQuestion" :disabled="currentQuestionNav == 0">Previous</button>
                        <button class="page-btn" @click="nextQuestion" :disabled="currentQuestionNav + 1 == questions.length">Next</button>
                        <button class="submit-btn">Submit</button>
                    </div>
                </div>
            </div>
        </div>
    </main>
</template>

<script>
import Question from '@/components/Question.vue';
import { useQuizzesStore } from '@/stores/QuizzesStore';
import { computed, onMounted, onUnmounted, ref } from 'vue';

    export default {
        props: ['id'],
        components: { Question },
        setup(props) {
            const quizzesStore = useQuizzesStore()
            const quiz = ref(null)
            const currentQuestionNav = ref(0)
            const questions = ref([])
            let timerInterval = null
            // store user answer to object; question_id : answers
            const userAnswers = ref({})

            // Format raw seconds into MM:SS (e.g., 01:00, 00:59, 00:00)
            const formattedTime = computed(() => {
                if (!quiz.value) return "00:00"
                const minutes = Math.floor(quiz.value.time_limit / 60)
                const seconds = quiz.value.time_limit % 60
                return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
            })

            const currentQuestion = computed(() => {
                return questions.value[currentQuestionNav.value] || null
            })
            async function nextQuestion() {
                if (currentQuestionNav.value + 1 >= questions.length) return
                currentQuestionNav.value++
            }
            async function prevQuestion() {
                if (currentQuestionNav.value <= 0) return
                currentQuestionNav.value--
            }
            async function quizQuestions() {
                questions.value = await quizzesStore.getQuizQuestions(props.id)
            }

            const startTimer = () => {
                if (timerInterval || quiz.value.time_limit <= 0) return

                timerInterval = setInterval(() => {
                    if (quiz.value.time_limit > 0) {
                        quiz.value.time_limit -= 1
                    } else {
                        alert("Time is up! your answers will be auto submitted!")
                        stopTimer()
                    }
                }, 1000);
            }

            const stopTimer = () => {
                clearInterval(timerInterval)
                timerInterval = null
            }

            onMounted(async () => {
                quiz.value = await quizzesStore.getQuiz(props.id)
                quizQuestions()
                startTimer()
            })
            onUnmounted(() => {
                stopTimer()
            })

            return { startTimer, formattedTime, quiz, quizzesStore, currentQuestionNav, questions, currentQuestion, nextQuestion, prevQuestion }
        }
    }
</script>

<style scoped>
/* Container */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

h1 {
    margin: 10px;
}
h2 {
    margin: 10px;
}


/* Quiz title & Question indicator */
.quiz-info {
    display: flex;
    flex-direction: column;
    align-items: center;
}

/* Question card */
.question-card {
    padding: 25px;
    background-color: #ffffff;
    margin: 8px;
    border-radius: 8px;
}

/* Pagination */
.actions {
  display: flex;
  justify-content: left;
  align-items: center;
  gap: 0.75rem;
}
.page-indicator {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
}

/* Page buttons */
.page-btn {
  background-color: #ffffff;
  border: 1px solid #cbd5e1;
  padding: 10px;
  padding-left: 25px;
  padding-right: 25px;
  border-radius: 6px;
  font-size: 0.875rem;
  cursor: pointer;
  margin-left: 25px;
  transition: background-color 0.15s ease;
}
.page-btn:hover:not(:disabled) {
  background-color: #f8fafc;
}
.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Submit Button */
.submit-btn {
    background-color: #F97316;
    color: white;
    font-weight: 600;
    padding: 10px 30px;
    border: none;
    border-radius: 6px;
    margin-left: 770px;
}

.submit-btn:hover {
  background-color: #EA580C;
}

.submit-btn:active {
  /* Press effect, shrinks little bit */
  transform: scale(0.98);
}
</style>