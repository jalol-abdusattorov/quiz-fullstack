<template>
    <main>
        <ConfirmModal v-if="showModal" @close="toggleModal">
            <h1 class="modal-h1">You have answered {{ Object.keys(userAnswers).length }} of {{ questions.length }} questions.</h1>
            <h2 class="modal-h2">Are you sure you want to submit?</h2>
            <button @click="handleContinue" class="continue-btn">Continue Quiz</button>
            <button @click="handleSubmitQuiz" class="submit-quiz-btn">Submit Quiz</button>
        </ConfirmModal>
        <div class="container">
            <div v-if="quiz" class="quiz-info">
                <h1>{{ quiz.title }}</h1>
                <h2>Question  {{ currentQuestionNav + 1 }} / {{ quiz.question_ids.length }}</h2>
                <h2>Time  {{ formattedTime }}s</h2>
            </div>
            <div>
                <div v-if="currentQuestion" class="question-card">
                    <Question
                    :key="currentQuestion._id"
                    :question="currentQuestion"
                    :saved-answer="getSavedAnswer(currentQuestion._id) ?? null"
                    @select-answer="handleAnswer"
                    />
                    <div class="actions">
                        <button class="page-btn" @click="prevQuestion" :disabled="currentQuestionNav == 0">Previous</button>
                        <button class="page-btn" @click="nextQuestion" :disabled="currentQuestionNav >= questions.length - 1">Next</button>
                        <button
                            class="submit-btn"
                            @click="handleSubmit"
                            >
                            Submit
                        </button>
                    </div>
                </div>
                <div class="question-nav">
                    <div v-for="(question, index) in questions" :key="question._id">
                        <button
                            @click="goToQuestion(index)"
                            :class="['nav-btn', { 'active': currentQuestionNav == index, 'answered': isQuestionAnswered(question._id) }]"
                        >
                            {{ index + 1 }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </main>
</template>

<script>
import ConfirmModal from '@/components/ConfirmModal.vue';
import Question from '@/components/Question.vue';
import { useQuizzesStore } from '@/stores/QuizzesStore';
import { computed, onMounted, onUnmounted, ref } from 'vue';
import { useRouter } from 'vue-router';

    export default {
        props: ['id', 'attemptId'],
        components: { Question, ConfirmModal },
        setup(props) {
            const quizzesStore = useQuizzesStore()
            const quiz = ref(null)
            const currentQuestionNav = ref(0)
            const questions = ref([])
            let timerInterval = null
            const showModal = ref(false)
            const router = useRouter()

            // [{ "question_id": "...", "selected_answer": "..." }]
            const userAnswers = ref([])

            const currentQuestion = computed(() => {
                return questions.value[currentQuestionNav.value] || null
            })
            const formattedTime = computed(() => {
                // Format raw seconds into MM:SS (e.g., 01:00, 00:59, 00:00)
                if (!quiz.value) return "00:00"
                const minutes = Math.floor(quiz.value.time_limit / 60)
                const seconds = quiz.value.time_limit % 60
                return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
            })

            const toggleModal = () => {
                showModal.value = !showModal.value
                if (showModal.value) {
                    stopTimer()
                } else if (!showModal.value) {
                    startTimer()
                }
            }

            const handleSubmit = () => {
                toggleModal()
            }

            const handleContinue = () => {
                toggleModal()
            }

            const handleSubmitQuiz = async () => {
                toggleModal()
                try {
                    await quizzesStore.submitQuiz(props.id, props.attemptId, userAnswers.value)
                    
                    router.replace({ name: 'Results' })
                } catch (exception) {
                    router.replace({ name: "Home" })
                }
            }

            const getSavedAnswer = (questionId) => {
                const entry = userAnswers.value.find(item => item.question_id === questionId)
                return entry !== undefined ? entry.selected_answer : null
            }

            const isQuestionAnswered = (questionId) => {
                return userAnswers.value.some(item => item.question_id === questionId && item.selected_answer !== null);
            }

            const handleAnswer = (answer) => {
                if (!currentQuestion.value) return

                const existingIndex = userAnswers.value.findIndex(
                    item => item.question_id === currentQuestion.value._id
                )

                if (existingIndex !== -1) {
                    userAnswers.value[existingIndex].selected_answer = answer
                } else {
                    userAnswers.value.push({
                        question_id: currentQuestion.value._id,
                        selected_answer: answer
                    })
                }
            }
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

            const goToQuestion = (index) => {
                currentQuestionNav.value = index
            }

            const startTimer = () => {
                if (timerInterval || quiz.value.time_limit <= 0) return

                timerInterval = setInterval(() => {
                    if (quiz.value.time_limit > 0) {
                        quiz.value.time_limit -= 1
                    } else {
                        alert("Time is up! Quiz will be auto submitted")
                        stopTimer()
                        handleSubmitQuiz()
                    }
                }, 1000);
            }

            const stopTimer = () => {
                clearInterval(timerInterval)
                timerInterval = null
            }

            onMounted(async () => {
                if (!props.id || !props.attemptId) {
                    router.replace({ name: "Home" })
                }

                quiz.value = await quizzesStore.getQuiz(props.id)
                quizQuestions()
                startTimer()
            })
            onUnmounted(() => {
                stopTimer()
            })

            return {
                quiz,
                questions,
                currentQuestionNav,
                currentQuestion,
                userAnswers,
                showModal,
                formattedTime,
                getSavedAnswer,
                isQuestionAnswered,
                handleAnswer,
                toggleModal,
                handleSubmit,
                handleContinue,
                handleSubmitQuiz,
                nextQuestion,
                prevQuestion,
                goToQuestion
            };
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

.modal-h1 {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 8px;
}
.modal-h2 {
  font-size: 16px;
  font-weight: 400;
  color: #4a4a4a;
  margin-bottom: 20px;
}

/* Continue quiz button & Submit quiz button final */
.continue-btn {
    background: #768eaf;
    color: #ffffff;
    padding: 10px;
    margin: 5px;
    border: none;
    border-radius: 9px;
    cursor: pointer;
}
.continue-btn:hover {
    background: #7287a4;
}
.submit-quiz-btn {
    background-color: #F97316;
    box-shadow: 0 0 10px rgba(249, 115, 22, 0.6);
    color: #ffffff;
    padding: 10px;
    margin: 5px;
    border: none;
    cursor: pointer;
    border-radius: 9px;
    transition: background-color 0.2s ease;
}
.submit-quiz-btn:hover {
    background-color: #dd6b19;
    box-shadow: 0 0 10px rgba(230, 111, 26, 0.6);
}


/* Questions navigator */
.question-nav {
    display: flex;
    gap: 12px;
    background-color: #121820;
    padding: 16px;
    border-radius: 12px;
}
.nav-btn {
    width: 40px;
    height: 40px;
    border-radius: 6px;
    border: 2px solid transparent;
    background-color: #ffffff;
    color: #121820;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}
.nav-btn:hover {
    background-color: #e2e8f0;
}
.nav-btn.answered {
    background-color: #0d9488; /* Soft teal indicator for completed */
    color: #ffffff;
}
.nav-btn.active {
    background-color: #f97316;
    color: #ffffff;
    border-color: #ffffff;
    box-shadow: 0 0 10px rgba(249, 115, 22, 0.6);
    transform: scale(1.08);
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
    margin-left: auto;
    text-decoration: underline 2px transparent;
    transition: text-decoration 0.3s ease;
}

.submit-btn:hover {
  background-color: #EA580C;
  text-decoration-color: #ffffff;
}

.submit-btn:active {
  /* Press effect, shrinks little bit */
  transform: scale(0.98);
}
</style>