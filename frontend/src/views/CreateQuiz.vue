<template>
    <div class="page">
        <confirm-modal v-if="quizCreatedSuccessfuly">
            <div class="confirm-modal">
                <h1>Quiz is now public</h1>
                <p>Your quiz has been published and is now available to everyone.</p>

                <button @click="changeRoutes">Continue</button>
            </div>
        </confirm-modal>

        <div class="create-quiz">

            <div class="header">
                <div>
                    <p class="eyebrow">QUIZ MANAGEMENT</p>
                    <h1>Create Quiz</h1>
                    <p class="subtitle">
                        Create a new quiz and configure its basic settings.
                    </p>
                </div>
            </div>

            <form @submit.prevent="handleSubmit">

                <div class="form-section">
                    <h2>Quiz Information</h2>
                    <p class="section-description">
                        Add the basic information about your quiz.
                    </p>

                    <div class="form-group">
                        <label>Title</label>
                        <input
                            type="text"
                            v-model="title"
                            placeholder="e.g. JavaScript Fundamentals"
                        >
                    </div>

                    <div class="form-group">
                        <label>Description</label>
                        <textarea
                            v-model="description"
                            placeholder="Describe what this quiz is about..."
                            rows="4"
                        ></textarea>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label>Category</label>
                            <select v-model="category">
                                <option value="" disabled>Select a category</option>
                                <option value="Technology">Technology</option>
                                <option value="Programming">Programming</option>
                                <option value="Mathematics">Mathematics</option>
                                <option value="Science">Science</option>
                                <option value="History">History</option>
                                <option value="Geography">Geography</option>
                                <option value="Animals">Animals</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Difficulty</label>
                            <select v-model="difficulty">
                                <option value="" disabled>Select difficulty</option>
                                <option value="easy">Easy</option>
                                <option value="medium">Medium</option>
                                <option value="hard">Hard</option>
                            </select>
                        </div>
                    </div>
                </div>

                <div class="form-section">
                    <h2>Quiz Settings</h2>
                    <p class="section-description">
                        Configure how the quiz will work.
                    </p>

                    <div class="form-group time-input">
                        <label>Time Limit</label>

                        <div class="input-with-unit">
                            <input
                                type="number"
                                v-model="timeLimit"
                                min="1"
                            >
                            <span>seconds</span>
                        </div>

                        <small>
                            Set how much time users have to complete the quiz.
                        </small>
                    </div>

                    <div class="form-section questions-section">

                        <div class="questions-header">
                            <div>
                                <h2>Questions</h2>
                                <p class="section-description">
                                    Create the questions and choose the correct answer.
                                </p>
                            </div>

                            <div class="question-count">
                                <span>{{ questions.length }}</span>
                                Questions
                            </div>
                        </div>


                        <div
                            v-for="(question, index) in questions"
                            :key="index"
                            class="question-card"
                        >
                            <div class="question-card-header">
                                <div class="question-title">
                                    <span class="question-number">{{ index + 1 }}</span>

                                    <div>
                                        <h3>Question {{ index + 1 }}</h3>
                                        <p>Enter the question and its possible answers.</p>
                                    </div>
                                </div>
                            </div>

                            <div class="question-content">

                                <!-- Question -->
                                <div class="form-group">
                                    <label>Question</label>

                                    <textarea
                                        v-model="question.question"
                                        placeholder="e.g. What is the capital of France?"
                                        rows="3"
                                    ></textarea>
                                </div>

                                <!-- Options -->
                                <div class="options-section">
                                    <label class="options-label">Answer Options</label>

                                    <div class="options-grid">

                                        <div class="option-group">
                                            <span class="option-label">A</span>
                                            <input
                                                v-model="question.options[0]"
                                                type="text"
                                                placeholder="Option A"
                                            >
                                        </div>

                                        <div class="option-group">
                                            <span class="option-label">B</span>
                                            <input
                                                v-model="question.options[1]"
                                                type="text"
                                                placeholder="Option B"
                                            >
                                        </div>

                                        <div class="option-group">
                                            <span class="option-label">C</span>
                                            <input
                                                v-model="question.options[2]"
                                                type="text"
                                                placeholder="Option C"
                                            >
                                        </div>

                                        <div class="option-group">
                                            <span class="option-label">D</span>
                                            <input
                                                v-model="question.options[3]"
                                                type="text"
                                                placeholder="Option D"
                                            >
                                        </div>

                                    </div>
                                </div>

                                <!-- Correct answer -->
                                <div class="question-bottom">
                                    <div class="form-group correct-answer-group">
                                        <label>Correct Answer</label>

                                        <select v-model="question.correct_answer">
                                            <option :value="null" disabled>
                                                Select the correct answer
                                            </option>

                                            <option :value="0">Option A</option>
                                            <option :value="1">Option B</option>
                                            <option :value="2">Option C</option>
                                            <option :value="3">Option D</option>
                                        </select>
                                    </div>

                                    <button
                                        type="button"
                                        class="delete-question-btn"
                                        @click="deleteQuestion(index)"
                                    >
                                        Delete Question
                                    </button>
                                </div>

                            </div>
                        </div>

                        <button
                            type="button"
                            class="add-question-btn"
                            @click="addQuestion"
                        >
                            <span class="plus-icon">+</span>

                            <span>
                                <strong>Add Question</strong>
                                <small>Add another question to this quiz</small>
                            </span>
                        </button>

                    </div>

                </div>

                <div class="form-actions">
                    <p class="error">{{ error }}</p>

                    <button type="button" class="cancel-btn" @click="handleCancel">
                        Cancel
                    </button>

                    <button type="submit" class="submit-btn" :disabled="!isValidQuiz">
                        Create Quiz
                    </button>
                </div>

            </form>
        </div>
    </div>
</template>

<script>
import { useQuestionsStore } from '@/stores/QuestionsStore';
import { useQuizzesStore } from '@/stores/QuizzesStore';
import { computed, onUnmounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import ConfirmModal from '../components/ConfirmModal.vue';

    export default {
        components: { ConfirmModal },
        setup() {
            const quizzesStore = useQuizzesStore()
            const questionsStore = useQuestionsStore()

            const title = ref('')
            const description = ref('')
            const category = ref('')
            const difficulty = ref('')
            const timeLimit = ref(300)
            const error = ref(null)
            const router = useRouter()

            const questions = ref([])
            const quizCreatedSuccessfuly = ref(false)

            const isValidQuiz = computed(() => {
                const validCategories = ['Technology', 'Programming', 'Mathematics', 'Science', 'History', 'Geography', 'Animals']
                const validDifficulties = ['easy', 'medium', 'hard']

                const validTitle = title.value.trim().length > 0
                const validCategory = validCategories.includes(category.value)
                const validDifficulty = validDifficulties.includes(difficulty.value)
                const validTime_limit = timeLimit.value > 30
                const validQuestions = questions.value.length > 0
                const validQuestion = ref(false)

                for (const question of questions.value) {
                    const hasDuplicates = new Set([question.options[0].trim(), question.options[1].trim(), question.options[2].trim(), question.options[3].trim()])

                    if (hasDuplicates.size < 4) {
                        error.value = 'Cannot have duplicate'
                        return false
                    }

                    if (question.question.trim().length == 0) {
                        error.value = "Question shouldn't be empty"
                        return false
                    }
                    if (question.options[0].trim().length == 0 || question.options[1].trim().length == 0 || question.options[2].trim().length == 0 || question.options[3].trim().length == 0) {
                        error.value = "Answers shouldn't be empty"
                        return false
                    }
                    if (question.correct_answer == null) {
                        error.value = "Correct answer shouldn't be empty"
                        return false
                    }
                }
                validQuestion.value = true

                if (!validTitle) {
                    error.value = 'Enter a value to Title'
                    return false
                }
                if (!validCategory) {
                    error.value = 'Select a value to Category'
                    return false
                }
                if (!validDifficulty) {
                    error.value = 'Select a value to Difficulty'
                    return false
                }
                if (!validTime_limit) {
                    error.value = "Time limit shouldn't be less than 30 seconds"
                    return false 
                }
                if (!validQuestions) {
                    error.value = 'Atleast 1 question'
                    return false
                }

                if (validTitle && validCategory && validDifficulty && validTime_limit && validQuestions) {
                    error.value = null
                    return true
                }
            })

            const addQuestion = () => {
                questions.value.push({
                    question: '',
                    options: ['', '', '', ''],
                    correct_answer: null,
                    category: category.value,
                    difficulty: difficulty.value,
                })
            }
            const deleteQuestion = (index) => {
                questions.value.splice(index, 1)
            }

            const handleSubmit = async () => {
                if (!category || !difficulty) return

                const questionIds = ref([])
                for (let i in questions.value) {
                    const response = await questionsStore.createQuestion(questions.value[i])
                    if (response) {
                        questionIds.value.push(response.question_id)
                    }
                }

                const quizDetails = {
                    title: title.value,
                    description: description.value,
                    category: category.value,
                    difficulty: difficulty.value,
                    question_ids: questionIds.value,
                    time_limit: timeLimit.value
                }

                const response = await quizzesStore.createQuiz(quizDetails)

                if (response?.quiz_id) {
                    quizCreatedSuccessfuly.value = true
                } else {
                    quizCreatedSuccessfuly.value = false
                    console.error(quizzesStore.error);
                    alert("Something went wrong")
                }
            }

            const changeRoutes = () => {
                try {
                    router.back()
                } catch (exc) {
                    router.push({ name: 'AdminDashboard' })
                }
            }

            const handleCancel = () => {
                changeRoutes()
            }

            onUnmounted(() => {
                quizCreatedSuccessfuly.value = false
            })

            return {
                title,
                description,
                category,
                difficulty,
                timeLimit,
                isValidQuiz,
                error,
                questions,
                quizCreatedSuccessfuly,
                changeRoutes,
                addQuestion,
                deleteQuestion,
                handleSubmit,
                handleCancel,
            }
        }
    }
</script>


<style scoped>

.page {
    min-height: 100vh;
    padding-top: 50px;
    padding-bottom: 50px;
    background: #f8fafc;
}

.create-quiz {
    max-width: 800px;
    margin: 0 auto;
}

/* =============================================
   ======= Quiz Creation Success Modal =========
   ============================================= */

.confirm-modal {
    text-align: center;
}

/* Success Title */
.confirm-modal h1 {
    margin: 0;
    color: #172033;
    font-size: 24px;
    font-weight: 700;
    line-height: 1.3;
    letter-spacing: -0.3px;
}

/* Description */
.confirm-modal p {
    margin: 10px 0 26px;
    color: #64748b;
    font-size: 14px;
    line-height: 1.5;
}

/* Continue Button */
.confirm-modal button {
    width: 100%;
    height: 44px;
    padding: 0 20px;

    border: none;
    border-radius: 10px;

    background: #4f46e5;
    color: #ffffff;

    font-family: inherit;
    font-size: 14px;
    font-weight: 600;

    cursor: pointer;
    box-shadow: 0 4px 10px rgba(79, 70, 229, 0.18);

    transition:
        background 0.2s ease,
        transform 0.2s ease,
        box-shadow 0.2s ease;
}

.confirm-modal button:hover {
    background: #4338ca;
    transform: translateY(-1px);
    box-shadow: 0 6px 14px rgba(79, 70, 229, 0.22);
}

.confirm-modal button:active {
    transform: translateY(0);
    box-shadow: 0 3px 7px rgba(79, 70, 229, 0.16);
}



/* Header */

.header {
    margin-bottom: 32px;
}

.eyebrow {
    margin: 0 0 8px;
    color: #6366f1;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
}

.header h1 {
    margin: 0;
    color: #111827;
    font-size: 32px;
}

.subtitle {
    margin-top: 8px;
    color: #64748b;
    font-size: 15px;
}


/* Form Sections */

.form-section {
    margin-bottom: 20px;
    padding: 28px;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
}

.form-section h2 {
    margin: 0;
    color: #1e293b;
    font-size: 18px;
}

.section-description {
    margin: 6px 0 24px;
    color: #94a3b8;
    font-size: 14px;
}


/* Form */

.form-group {
    margin-bottom: 20px;
}

.form-group:last-child {
    margin-bottom: 0;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    color: #334155;
    font-size: 14px;
    font-weight: 600;
}

input,
textarea,
select {
    width: 100%;
    box-sizing: border-box;
    border: 1px solid #cbd5e1;
    border-radius: 9px;
    outline: none;
    background: #ffffff;
    color: #1e293b;
    font-family: inherit;
    font-size: 14px;
    transition: 0.2s;
}

input,
select {
    height: 44px;
}

input,
textarea {
    padding: 11px 13px;
}

select {
    padding: 0 13px;
    cursor: pointer;
}

textarea {
    min-height: 100px;
    resize: vertical;
}

input::placeholder,
textarea::placeholder {
    color: #94a3b8;
}

input:focus,
textarea:focus,
select:focus {
    border-color: #6366f1;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}


/* Two-column fields */

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
}


/* Time Limit */

.input-with-unit {
    position: relative;
    display: flex;
    align-items: center;
}

.input-with-unit input {
    padding-right: 80px;
}

.input-with-unit span {
    position: absolute;
    right: 14px;
    color: #64748b;
    font-size: 13px;
}

small {
    display: block;
    margin-top: 7px;
    color: #94a3b8;
    font-size: 12px;
}


/* Questions */

.questions-section {
    padding-bottom: 24px;
}

.questions-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 24px;
}

.questions-header .section-description {
    margin-bottom: 0;
}

.question-count {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 6px 10px;
    border-radius: 8px;
    background: #eef2ff;
    color: #4f46e5;
    font-size: 12px;
    font-weight: 600;
}

.question-count span {
    font-weight: 700;
}


/* Question Card */

.question-card {
    overflow: hidden;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    background: #ffffff;
    margin-bottom: 10px;
}

.question-card-header {
    padding: 18px 20px;
    border-bottom: 1px solid #e2e8f0;
    background: #f8fafc;
}

.question-title {
    display: flex;
    align-items: center;
    gap: 12px;
}

.question-number {
    width: 34px;
    height: 34px;
    flex-shrink: 0;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 9px;
    background: #4f46e5;
    color: #ffffff;

    font-size: 13px;
    font-weight: 700;
}

.question-title h3 {
    margin: 0;
    color: #1e293b;
    font-size: 15px;
}

.question-title p {
    margin: 3px 0 0;
    color: #94a3b8;
    font-size: 12px;
}

.question-content {
    padding: 22px 20px;
}


/* Answer Options */

.options-section {
    margin-bottom: 22px;
}

.options-label {
    display: block;
    margin-bottom: 10px;
    color: #334155;
    font-size: 14px;
    font-weight: 600;
}

.options-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
}

.option-group {
    display: flex;
    align-items: center;
    gap: 8px;
}

.option-label {
    width: 32px;
    height: 32px;
    flex-shrink: 0;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 7px;
    background: #f1f5f9;
    color: #475569;

    font-size: 12px;
    font-weight: 700;
}

.option-group input {
    flex: 1;
}


/* Correct Answer */

.correct-answer-group {
    max-width: 350px;
    margin-bottom: 0;
}

.question-bottom {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 20px;
}

.delete-question-btn {
    height: 44px;
    padding: 0 16px;
    border: 1px solid #fecaca;
    border-radius: 9px;
    background: #fff;
    color: #dc2626;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: 0.2s;
}

.delete-question-btn:hover {
    background: #fef2f2;
    border-color: #fca5a5;
}

/* Add Question */

.add-question-btn {
    width: 100%;
    min-height: 62px;

    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;

    margin-top: 14px;
    padding: 10px;

    border: 1px dashed #a5b4fc;
    border-radius: 11px;

    background: #f8faff;
    color: #4f46e5;

    cursor: pointer;
    transition: 0.2s;
}

.add-question-btn:hover {
    border-color: #6366f1;
    background: #eef2ff;
}

.plus-icon {
    width: 30px;
    height: 30px;
    flex-shrink: 0;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 50%;
    background: #e0e7ff;

    font-size: 20px;
}

.add-question-btn span:last-child {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.add-question-btn strong {
    font-size: 13px;
}

.add-question-btn small {
    margin-top: 2px;
    color: #818cf8;
    font-size: 11px;
}


/* Bottom Actions */

.form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    margin-top: 24px;
}

button {
    height: 44px;
    padding: 0 22px;

    border-radius: 9px;

    font-family: inherit;
    font-size: 14px;
    font-weight: 600;

    cursor: pointer;
    transition: 0.2s;
}

.cancel-btn {
    border: 1px solid #cbd5e1;
    background: #ffffff;
    color: #475569;
}

.cancel-btn:hover {
    background: #f8fafc;
}

.submit-btn {
    border: none;
    background: #4f46e5;
    color: #ffffff;
    box-shadow: 0 3px 8px rgba(79, 70, 229, 0.25);
}

.submit-btn:hover {
    background: #4338ca;
    transform: translateY(-1px);
}


/* Disabled Create Button */

.submit-btn:disabled {
    background: #cbd5e1;
    color: #f8fafc;
    box-shadow: none;
    cursor: not-allowed;
    transform: none;
}

.submit-btn:disabled:hover {
    background: #cbd5e1;
    transform: none;
}


/* Error */

.error {
    margin: 0 auto 0 0;
    color: #ef4444;
    font-size: 13px;
    font-weight: 600;
}


/* Responsive */

@media (max-width: 600px) {

    .page {
        padding: 30px 15px;
    }

    .header h1 {
        font-size: 27px;
    }

    .form-section {
        padding: 20px;
    }

    .form-row,
    .options-grid {
        grid-template-columns: 1fr;
        gap: 0;
    }

    .options-grid {
        gap: 10px;
    }

    .questions-header {
        flex-direction: column;
        gap: 12px;
    }

    .correct-answer-group {
        max-width: none;
    }

    .form-actions {
        flex-direction: column-reverse;
    }

    .form-actions button {
        width: 100%;
    }

    .error {
        margin: 0;
    }
}

</style>