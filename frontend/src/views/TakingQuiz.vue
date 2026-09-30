<template>
    <main class="quiz-main">
        <ConfirmModal v-if="showModal" @close="toggleModal">
            <div class="modal-content">
                <h1 class="modal-title">Ready to submit?</h1>
                <p class="modal-description">You've answered {{ Object.keys(userAnswers).length }} of {{ questions.length }} questions</p>
                <div class="modal-buttons">
                    <button @click="handleContinue" class="btn btn-secondary">Keep going</button>
                    <button @click="handleSubmitQuiz" :disabled="submitted" class="btn btn-primary">Submit quiz</button>
                </div>
            </div>
        </ConfirmModal>

        <div class="quiz-container" v-if="quiz">
            <!-- Header -->
            <header class="quiz-header">
                <div class="header-content">
                    <h1 class="quiz-title">{{ quiz.title }}</h1>
                    <div class="progress-info">
                        <span class="progress-text">Question {{ currentQuestionNav + 1 }} of {{ quiz.question_ids.length }}</span>
                        <div class="progress-bar">
                            <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
                        </div>
                    </div>
                </div>
                <div class="header-timer">
                    <div class="timer-badge" :class="{ 'timer-warning': isTimerLow, 'timer-critical': isTimerCritical }">
                        <i class="ti ti-clock" aria-hidden="true"></i>
                        <span class="timer-text">{{ formattedTime }}</span>
                    </div>
                </div>
            </header>

            <!-- Main Content -->
            <div class="quiz-content">
                <!-- Question Card -->
                <div class="question-wrapper">
                    <div v-if="currentQuestion" class="question-card">
                        <Question
                            :key="currentQuestion._id"
                            :question="currentQuestion"
                            :saved-answer="getSavedAnswer(currentQuestion._id) ?? null"
                            @select-answer="handleAnswer"
                        />
                    </div>

                    <!-- Actions -->
                    <div class="question-actions">
                        <button 
                            class="btn btn-secondary" 
                            @click="prevQuestion" 
                            :disabled="currentQuestionNav == 0"
                        >
                            <i class="ti ti-arrow-left" aria-hidden="true"></i>
                            Previous
                        </button>
                        <button 
                            class="btn btn-secondary" 
                            @click="nextQuestion" 
                            :disabled="currentQuestionNav >= questions.length - 1"
                        >
                            Next
                            <i class="ti ti-arrow-right" aria-hidden="true"></i>
                        </button>
                        <button
                            class="btn btn-primary submit-btn"
                            @click="handleSubmit"
                        >
                            <i class="ti ti-check" aria-hidden="true"></i>
                            Submit
                        </button>
                    </div>
                </div>

                <!-- Navigation Sidebar -->
                <aside class="question-sidebar">
                    <div class="sidebar-header">
                        <h2 class="sidebar-title">Questions</h2>
                        <span class="sidebar-badge">{{ Object.keys(userAnswers).length }}/{{ questions.length }}</span>
                    </div>
                    <div class="question-nav">
                        <button
                            v-for="(question, index) in questions"
                            :key="question._id"
                            @click="goToQuestion(index)"
                            :class="[
                                'nav-btn',
                                { 'active': currentQuestionNav == index },
                                { 'answered': isQuestionAnswered(question._id) }
                            ]"
                            :title="`Question ${index + 1}${isQuestionAnswered(question._id) ? ' - Answered' : ''}`"
                        >
                            {{ index + 1 }}
                            <i v-if="isQuestionAnswered(question._id)" class="ti ti-check" aria-hidden="true"></i>
                        </button>
                    </div>
                </aside>
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
            const submitted = ref(false)

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
                submitted.value = true
                toggleModal()
                const res = await quizzesStore.submitQuiz(props.id, props.attemptId, userAnswers.value)
                console.log(res);
                router.replace({ name: 'Results' })
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
                // console.log(userAnswers.value);
            }
            async function nextQuestion() {
                if (currentQuestionNav.value + 1 >= questions.value.length) return
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

            const progressPercentage = computed(() => {
                if (!quiz.value) return 0
                return Math.round(((currentQuestionNav.value + 1) / quiz.value.question_ids.length) * 100)
            })

            const isTimerLow = computed(() => {
                return quiz.value && quiz.value.time_limit > 0 && quiz.value.time_limit <= 60
            })

            const isTimerCritical = computed(() => {
                return quiz.value && quiz.value.time_limit > 0 && quiz.value.time_limit <= 10
            })

            onMounted(async () => {
                if (!props.id || !props.attemptId) {
                    router.replace({ name: "Home" })
                }

                quiz.value = await quizzesStore.getQuiz(props.id)
                quizQuestions()
                startTimer()

                for (const questionId of quiz.value.question_ids) {
                    userAnswers.value.push({ 'question_id': questionId, 'selected_answer': null })
                }
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
                submitted,
                isQuestionAnswered,
                handleAnswer,
                toggleModal,
                handleSubmit,
                handleContinue,
                handleSubmitQuiz,
                nextQuestion,
                prevQuestion,
                goToQuestion,
                progressPercentage,
                isTimerLow,
                isTimerCritical,
            };
        }
    }
</script>


<style scoped>
* {
    box-sizing: border-box;
}

.quiz-main {
    min-height: 100vh;
    background: #f5f5f5;
    overflow-x: hidden;
}

/* ============ MODAL ============ */
.modal-content {
    text-align: center;
}

.modal-title {
    font-size: 1.5rem;
    font-weight: 500;
    color: #1a1a1a;
    margin: 0 0 0.5rem 0;
}

.modal-description {
    font-size: 1rem;
    color: #666666;
    margin: 0 0 1.5rem 0;
}

.modal-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}

/* ============ HEADER ============ */
.quiz-header {
    background: #ffffff;
    border-bottom: 1px solid #e0e0e0;
    padding: 1.5rem 2rem;
    position: sticky;
    top: 0;
    z-index: 10;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 2rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.header-content {
    flex: 1;
}

.quiz-title {
    font-size: 1.375rem;
    font-weight: 500;
    color: #1a1a1a;
    margin: 0 0 1rem 0;
}

.progress-info {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.progress-text {
    font-size: 0.875rem;
    color: #666666;
    font-weight: 500;
}

.progress-bar {
    width: 100%;
    height: 4px;
    background: #eeeeee;
    border-radius: 2px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: #5046e5;
    transition: width 0.3s ease;
}

/* ============ TIMER ============ */
.header-timer {
    flex-shrink: 0;
}

.timer-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1rem;
    background: #f5f5f5;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    font-weight: 500;
    color: #1a1a1a;
    transition: all 0.2s ease;
    white-space: nowrap;
}

.timer-badge i {
    font-size: 18px;
}

.timer-text {
    font-family: 'Courier New', monospace;
    font-size: 1.125rem;
    font-weight: 600;
}

.timer-warning {
    background: #fef3c7;
    border-color: #fbbf24;
    color: #92400e;
}

.timer-critical {
    background: #fee2e2;
    border-color: #ef5350;
    color: #991b1b;
    animation: pulse-danger 1s infinite;
}

@keyframes pulse-danger {
    0%, 100% {
        opacity: 1;
    }
    50% {
        opacity: 0.7;
    }
}

/* ============ QUIZ CONTENT ============ */
.quiz-container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

.quiz-content {
    display: grid;
    grid-template-columns: 1fr 280px;
    gap: 2rem;
    padding: 2rem;
    flex: 1;
    max-width: 1400px;
    margin: 0 auto;
    width: 100%;
}

/* ============ QUESTION CARD ============ */
.question-wrapper {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.question-card {
    background: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    padding: 2rem;
    flex: 1;
    animation: fadeIn 0.3s ease-out;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(8px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* ============ QUESTION ACTIONS ============ */
.question-actions {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
}

.btn {
    padding: 0.75rem 1.5rem;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    background: #ffffff;
    color: #374151;
    font-weight: 500;
    font-size: 0.95rem;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.2s ease;
    text-decoration: none;
}

.btn i {
    font-size: 16px;
}

.btn-secondary {
    background: #ffffff;
    border-color: #d1d5db;
    color: #374151;
}

.btn-secondary:hover:not(:disabled) {
    background: #f9fafb;
    border-color: #9ca3af;
}

.btn-primary {
    background: #5046e5;
    border-color: #5046e5;
    color: #ffffff;
}

.btn-primary:hover:not(:disabled) {
    background: #4338ca;
    border-color: #4338ca;
}

.btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.submit-btn {
    margin-left: auto;
    padding: 0.75rem 2rem;
}

/* ============ SIDEBAR ============ */
.question-sidebar {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    height: fit-content;
    position: sticky;
    top: 100px;
}

.sidebar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 0.5rem;
}

.sidebar-title {
    font-size: 0.95rem;
    font-weight: 500;
    color: #1a1a1a;
    margin: 0;
}

.sidebar-badge {
    font-size: 0.875rem;
    background: #dbeafe;
    color: #1e40af;
    padding: 0.25rem 0.75rem;
    border-radius: 8px;
    font-weight: 600;
}

.question-nav {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.5rem;
    background: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    padding: 1rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.nav-btn {
    aspect-ratio: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid #d1d5db;
    background: #ffffff;
    color: #666666;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
    gap: 0;
}

.nav-btn:hover {
    background: #f9fafb;
    border-color: #9ca3af;
}

.nav-btn.answered {
    border-color: #10b981;
    color: #10b981;
}

.nav-btn.answered i {
    position: absolute;
    font-size: 12px;
    bottom: -2px;
    right: -2px;
    background: #10b981;
    color: white;
    border-radius: 50%;
    width: 16px;
    height: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.nav-btn.active {
    background: #5046e5;
    color: #ffffff;
    border-color: #5046e5;
    box-shadow: 0 0 0 2px #ffffff, 0 0 0 4px #5046e5;
}

.nav-btn.active i {
    display: none;
}

/* ============ RESPONSIVE ============ */
@media (max-width: 1024px) {
    .quiz-header {
        flex-direction: column;
        gap: 1rem;
    }

    .header-content {
        width: 100%;
    }

    .quiz-content {
        grid-template-columns: 1fr;
        gap: 1.5rem;
        padding: 1.5rem;
    }

    .question-sidebar {
        position: static;
        top: auto;
    }

    .question-nav {
        grid-template-columns: repeat(6, 1fr);
    }
}

@media (max-width: 768px) {
    .quiz-main {
        font-size: 0.95rem;
    }

    .quiz-header {
        padding: 1rem;
        position: relative;
    }

    .quiz-title {
        font-size: 1.25rem;
    }

    .progress-bar {
        height: 3px;
    }

    .timer-badge {
        padding: 0.5rem 0.75rem;
        font-size: 0.875rem;
    }

    .timer-text {
        font-size: 1rem;
    }

    .quiz-content {
        padding: 1rem;
        gap: 1rem;
    }

    .question-card {
        padding: 1.5rem;
    }

    .question-actions {
        gap: 0.5rem;
    }

    .btn {
        padding: 0.625rem 1rem;
        font-size: 0.875rem;
    }

    .submit-btn {
        margin-left: auto;
    }

    .question-nav {
        grid-template-columns: repeat(4, 1fr);
        padding: 0.75rem;
        gap: 0.375rem;
    }

    .nav-btn {
        font-size: 0.8rem;
    }

    .sidebar-title {
        font-size: 0.875rem;
    }

    .sidebar-badge {
        font-size: 0.75rem;
        padding: 0.2rem 0.5rem;
    }
}

@media (max-width: 480px) {
    .quiz-header {
        padding: 0.75rem;
    }

    .quiz-title {
        font-size: 1.125rem;
        margin-bottom: 0.75rem;
    }

    .progress-text {
        font-size: 0.8rem;
    }

    .timer-text {
        font-size: 0.95rem;
    }

    .quiz-content {
        padding: 0.75rem;
    }

    .question-card {
        padding: 1rem;
    }

    .question-actions {
        flex-direction: column;
    }

    .btn {
        width: 100%;
        justify-content: center;
    }

    .submit-btn {
        margin-left: 0;
    }

    .question-nav {
        grid-template-columns: repeat(3, 1fr);
    }
}
</style>