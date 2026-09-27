<template>
    <div v-if="quiz">
        <div class="edit-quiz">
            <div class="form-card">
                <h1>Edit Quiz</h1>
                <p class="subtitle">Update your quiz information</p>

                <form @submit.prevent="handleSubmit">

                    <div class="form-group">
                        <label for="title">Title</label>
                        <input
                            id="title"
                            v-model="quiz.title"
                            type="text"
                            placeholder="Enter quiz title"
                        >
                    </div>

                    <div class="form-group">
                        <label for="description">Description</label>
                        <textarea
                            id="description"
                            v-model="quiz.description"
                            placeholder="Enter quiz description"
                            rows="4"
                        ></textarea>
                    </div>

                    <div class="form-row">

                        <div class="form-group">
                            <label for="category">Category</label>

                            <select
                                id="category"
                                v-model="quiz.category"
                            >
                                <option value="" disabled>
                                    Select category
                                </option>

                                <option value="Programming">
                                    Programming
                                </option>

                                <option value="Mathematics">
                                    Mathematics
                                </option>

                                <option value="Science">
                                    Science
                                </option>

                                <option value="History">
                                    History
                                </option>

                                <option value="Geography">
                                    Geography
                                </option>

                                <option value="Animals">
                                    Animals
                                </option>
                            </select>
                        </div>


                        <div class="form-group">
                            <label for="difficulty">Difficulty</label>

                            <select
                                id="difficulty"
                                v-model="quiz.difficulty"
                            >
                                <option value="" disabled>
                                    Select difficulty
                                </option>

                                <option value="easy">
                                    Easy
                                </option>

                                <option value="medium">
                                    Medium
                                </option>

                                <option value="hard">
                                    Hard
                                </option>
                            </select>
                        </div>


                        <div class="form-group">
                            <label for="time_limit">Time Limit</label>

                            <div class="time-input">
                                <input
                                    id="time_limit"
                                    v-model="quiz.time_limit"
                                    type="number"
                                    min="1"
                                    placeholder="1800"
                                >

                                <span>seconds</span>
                            </div>
                        </div>


                        <div class="form-group question-group">
                            <label for="question_id">
                                Question IDs
                            </label>

                            <div class="question-id-input">
                                <input
                                    id="question_id"
                                    v-model="questionIdInput"
                                    type="text"
                                    placeholder="Enter a 24-character question ID"
                                    autocomplete="off"
                                    @input="onTyping"
                                >

                                <button
                                    type="button"
                                    class="add-question-btn"
                                    :disabled="!validQuestionId"
                                    @click="addQuestionId"
                                >
                                    <span class="add-icon">+</span>
                                    Add
                                </button>
                            </div>

                            <span class="question-hint">
                                Add question IDs to include them in this quiz.
                            </span>
                            <span class="invalid-question-id" v-if="!validQuestionId">
                                Invalid Question ID
                            </span>

                            <div
                                v-if="quizQuestionIds.length"
                                class="question-list"
                            >
                                <div
                                    v-for="(questionId, index) in quizQuestionIds"
                                    :key="questionId"
                                    class="question-item"
                                >
                                    <div class="question-number">
                                        {{ index + 1 }}
                                    </div>

                                    <div class="question-content">
                                        <span class="question-label">
                                            Question {{ index + 1 }}
                                        </span>

                                        <span class="question-id">
                                            {{ questionId }}
                                        </span>
                                    </div>

                                    <button
                                        type="button"
                                        class="remove-question-btn"
                                        @click="removeQuestionId(index)"
                                        aria-label="Remove question"
                                    >
                                        ×
                                    </button>
                                </div>
                            </div>


                            <div
                                v-else
                                class="empty-questions"
                            >
                                <span class="empty-icon">＋</span>
                                <span>No questions added yet</span>
                            </div>
                        </div>

                    </div>


                    <div class="form-actions">
                        <button
                            type="button"
                            class="cancel-btn"
                            @click="handleCancel"
                        >
                            Cancel
                        </button>

                        <button
                            type="submit"
                            class="save-btn"
                        >
                            Save Changes
                        </button>
                    </div>

                </form>
            </div>
        </div>
    </div>
</template>

<script>
import { useQuizzesStore } from '@/stores/QuizzesStore';
import { computed, onMounted, ref } from 'vue';
import AdminAppHeader from '../components/AdminAppHeader.vue';
import { useRouter } from 'vue-router';
import { useQuestionsStore } from '@/stores/QuestionsStore.js';

    export default {
        components: { AdminAppHeader },
        props: ['quizId'],
        setup(props) {
            const quizzesStore = useQuizzesStore()
            const questionsStore = useQuestionsStore()
            const quiz = ref(null)
            const questionIdInput = ref('')
            const router = useRouter()
            const validQuestionId = ref(false)

            const quizQuestionIds = computed(() => {
                return quiz.value.question_ids || []
            })

            let debounceTimer = null
            const onTyping = () => {
                clearTimeout(debounceTimer);

                debounceTimer = setTimeout(() => {
                    if (questionIdInput.value.length == 24) {
                        isValidQuestionId()
                    } else {
                        validQuestionId.value = false
                    }
                }, 100)
            }

            async function isValidQuestionId() {
                questionIdInput.value = questionIdInput.value.trim()

                const response = await questionsStore.validQuestionId(questionIdInput.value)
                console.log(response);
                if (response?.message == 'question does not exist') {
                    validQuestionId.value = false
                    return
                }

                validQuestionId.value = true
            }

            async function loadQuizDetails() {
                quiz.value = await quizzesStore.getQuiz(props.quizId)
            }

            const addQuestionId = () => {
                quizQuestionIds.value.push(questionIdInput.value)
                questionIdInput.value = ''
            }
            const removeQuestionId = (index) => {
                quizQuestionIds.value.splice(index, 1)
            }

            const handleSubmit = async () => {
                const EditingValues = {
                    title: quiz.value.title ?? null,
                    description: quiz.value.description ?? null,
                    category: quiz.value.category ?? null,
                    difficulty: quiz.value.difficulty ?? null,
                    question_ids: quizQuestionIds.value ?? null,
                    time_limit: quiz.value.time_limit ?? null
                }

                const response = await quizzesStore.editQuiz(props.quizId, EditingValues)                
                alert(response.message)
                try {
                    router.back()
                } catch (exc) {
                    router.push({ name: 'AdminDashboard' })
                }
            }
            const handleCancel = async () => {
                try {
                    router.back()
                } catch (exc) {
                    router.push({ name: 'AdminDashboard' })
                }
            }

            onMounted(async () => {
                await loadQuizDetails()
            })

            return {
                quiz,
                quizQuestionIds,
                questionIdInput,
                addQuestionId,
                removeQuestionId,
                handleSubmit,
                handleCancel,
                validQuestionId,
                onTyping,
            }
        }
    }
</script>

```css
<style scoped>
.edit-quiz {
    min-height: 100vh;
    padding: 40px 20px;
    background: #f8fafc;
}

.form-card {
    max-width: 800px;
    margin: 0 auto;
    padding: 32px;

    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;

    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.form-card h1 {
    margin: 0;
    color: #0f172a;
    font-size: 26px;
    font-weight: 700;
}

.subtitle {
    margin: 6px 0 28px;
    color: #64748b;
    font-size: 14px;
}


/* =========================
   Form
========================= */

.form-group {
    display: flex;
    flex-direction: column;
    gap: 7px;
    margin-bottom: 20px;
}

.form-group label {
    font-size: 14px;
    font-weight: 600;
    color: #334155;
}

.form-group input,
.form-group textarea,
.form-group select {
    width: 100%;
    box-sizing: border-box;

    padding: 11px 13px;

    border: 1px solid #cbd5e1;
    border-radius: 8px;

    background: #ffffff;
    color: #1e293b;

    font-size: 14px;
    font-family: inherit;

    outline: none;

    transition:
        border-color 0.2s ease,
        box-shadow 0.2s ease,
        background 0.2s ease;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
    border-color: #2563eb;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.form-group textarea {
    resize: vertical;
    min-height: 100px;
}

.form-group input::placeholder,
.form-group textarea::placeholder {
    color: #94a3b8;
}


/* =========================
   Category / Difficulty / Time
========================= */

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 16px;
}

.time-input {
    display: flex;
    align-items: center;

    border: 1px solid #cbd5e1;
    border-radius: 8px;

    overflow: hidden;

    background: #ffffff;

    transition:
        border-color 0.2s ease,
        box-shadow 0.2s ease;
}

.time-input:focus-within {
    border-color: #2563eb;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.time-input input {
    border: none;
    border-radius: 0;
    box-shadow: none !important;
}

.time-input span {
    padding-right: 12px;

    color: #64748b;
    font-size: 13px;

    white-space: nowrap;
}


/* =========================
   Buttons
========================= */

.form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;

    margin-top: 30px;
    padding-top: 20px;

    border-top: 1px solid #e2e8f0;
}

.form-actions button {
    padding: 10px 18px;

    border-radius: 8px;

    font-size: 14px;
    font-weight: 600;

    cursor: pointer;

    transition:
        background 0.2s ease,
        border-color 0.2s ease,
        transform 0.15s ease,
        box-shadow 0.2s ease;
}

.cancel-btn {
    border: 1px solid #cbd5e1;
    background: #ffffff;
    color: #475569;
}

.cancel-btn:hover {
    background: #f8fafc;
}

.save-btn {
    border: 1px solid #2563eb;
    background: #2563eb;
    color: #ffffff;
}

.save-btn:hover {
    background: #1d4ed8;
    border-color: #1d4ed8;
    transform: translateY(-1px);
    box-shadow: 0 3px 8px rgba(37, 99, 235, 0.2);
}


/* =========================
   Question IDs
========================= */

.question-group {
    margin-top: 4px;
}

.question-id-input {
    display: flex;
    gap: 10px;
}

.question-id-input input {
    flex: 1;
    min-width: 0;
}


/* Add button */

.add-question-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;

    min-width: 82px;
    padding: 0 16px;

    border: 1px solid #2563eb;
    border-radius: 8px;

    background: #2563eb;
    color: #ffffff;

    font-size: 14px;
    font-weight: 600;

    cursor: pointer;

    transition:
        background 0.2s ease,
        border-color 0.2s ease,
        transform 0.15s ease,
        box-shadow 0.2s ease;
}

.add-icon {
    font-size: 18px;
    font-weight: 400;
    line-height: 1;
}

.add-question-btn:hover:not(:disabled) {
    background: #1d4ed8;
    border-color: #1d4ed8;

    transform: translateY(-1px);

    box-shadow: 0 3px 8px rgba(37, 99, 235, 0.2);
}

.add-question-btn:active:not(:disabled) {
    transform: translateY(0);
}


/* Disabled Add button */

.add-question-btn:disabled {
    background: #e2e8f0;
    border-color: #e2e8f0;

    color: #94a3b8;

    cursor: not-allowed;

    box-shadow: none;
    transform: none;
}


/* Hint */

.question-hint {
    display: block;

    margin-top: 7px;

    color: #94a3b8;
    font-size: 12px;
}

/* Invalid Question ID */
.invalid-question-id {
    color: #ff0062;
    margin: 0;
    margin-top: 7px;
    font-size: 0.8em;
    font-weight: bold;
}

/* =========================
   Question List
========================= */

.question-list {
    display: flex;
    flex-direction: column;
    gap: 8px;

    margin-top: 14px;
}


/* Individual question */

.question-item {
    display: flex;
    align-items: center;
    gap: 12px;

    padding: 10px 12px;

    background: #f8fafc;

    border: 1px solid #e2e8f0;
    border-radius: 9px;

    transition:
        background 0.15s ease,
        border-color 0.15s ease,
        box-shadow 0.15s ease;
}

.question-item:hover {
    background: #f1f5f9;
    border-color: #cbd5e1;

    box-shadow: 0 2px 5px rgba(15, 23, 42, 0.04);
}


/* Question number */

.question-number {
    display: flex;
    align-items: center;
    justify-content: center;

    width: 30px;
    height: 30px;

    flex-shrink: 0;

    border-radius: 7px;

    background: #dbeafe;
    color: #1d4ed8;

    font-size: 12px;
    font-weight: 700;
}


/* Question information */

.question-content {
    display: flex;
    flex-direction: column;
    gap: 3px;

    min-width: 0;
    flex: 1;
}

.question-label {
    font-size: 12px;
    font-weight: 600;
    color: #64748b;
}

.question-id {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;

    color: #334155;

    font-family:
        "SFMono-Regular",
        Consolas,
        "Liberation Mono",
        monospace;

    font-size: 13px;
}


/* Remove button */

.remove-question-btn {
    display: flex;
    align-items: center;
    justify-content: center;

    width: 30px;
    height: 30px;

    flex-shrink: 0;

    border: 1px solid #fecaca;
    border-radius: 7px;

    background: #fff1f2;
    color: #dc2626;

    font-size: 19px;
    line-height: 1;

    cursor: pointer;

    transition:
        background 0.15s ease,
        border-color 0.15s ease,
        transform 0.15s ease;
}

.remove-question-btn:hover {
    background: #fee2e2;
    border-color: #fca5a5;

    transform: scale(1.04);
}

.remove-question-btn:active {
    transform: scale(0.96);
}


/* =========================
   Empty Questions
========================= */

.empty-questions {
    display: flex;
    align-items: center;
    gap: 8px;

    margin-top: 12px;
    padding: 13px 14px;

    border: 1px dashed #cbd5e1;
    border-radius: 8px;

    background: #f8fafc;

    color: #94a3b8;
    font-size: 13px;
}

.empty-icon {
    font-size: 16px;
    color: #94a3b8;
}


/* =========================
   Mobile
========================= */

@media (max-width: 650px) {
    .edit-quiz {
        padding: 20px 12px;
    }

    .form-card {
        padding: 22px;
        border-radius: 12px;
    }

    .form-card h1 {
        font-size: 23px;
    }

    .form-row {
        grid-template-columns: 1fr;
        gap: 0;
    }

    .question-id-input {
        flex-direction: column;
    }

    .add-question-btn {
        min-height: 42px;
    }

    .form-actions {
        flex-direction: column-reverse;
    }

    .form-actions button {
        width: 100%;
    }
}

@media (max-width: 400px) {
    .form-card {
        padding: 18px;
    }

    .question-item {
        gap: 8px;
        padding: 9px;
    }

    .question-id {
        font-size: 11px;
    }
}
</style>