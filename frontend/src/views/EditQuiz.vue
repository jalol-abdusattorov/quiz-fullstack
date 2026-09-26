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
                            <select id="category" v-model="quiz.category">
                                <option value="" disabled>Select category</option>
                                <option value="Programming">Programming</option>
                                <option value="Mathematics">Mathematics</option>
                                <option value="Science">Science</option>
                                <option value="History">History</option>
                                <option value="Geography">Geography</option>
                                <option value="Animals">Animals</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="difficulty">Difficulty</label>
                            <select id="difficulty" v-model="quiz.difficulty">
                                <option value="" disabled>Select difficulty</option>
                                <option value="easy">Easy</option>
                                <option value="medium">Medium</option>
                                <option value="hard">Hard</option>
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
                        <div class="form-group">
                            <label for="question_id">Question IDs</label>

                            <div class="question-id-input">
                                <input
                                    id="question_id"
                                    v-model="questionIdInput"
                                    type="text"
                                    placeholder="Enter question ID"
                                >

                                <button
                                    type="button"
                                    class="add-question-btn"
                                    @click="addQuestionId"
                                >
                                    Add
                                </button>
                            </div>

                            <div v-if="quizQuestionIds.length" class="question-list">
                                <div
                                    v-for="(questionId, index) in quizQuestionIds"
                                    :key="questionId"
                                    class="question-item"
                                >
                                    <span class="question-number">{{ index + 1 }}</span>

                                    <span class="question-id">
                                        {{ questionId }}
                                    </span>

                                    <button
                                        type="button"
                                        class="remove-question-btn"
                                        @click="removeQuestionId(index)"
                                    >
                                        ×
                                    </button>
                                </div>
                            </div>

                            <span v-else class="empty-questions">
                                No questions added yet.
                            </span>
                        </div>
                    </div>

                    <div class="form-actions">
                        <button type="button" class="cancel-btn" @click="handleCancel">
                            Cancel
                        </button>

                        <button type="submit" class="save-btn">
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

    export default {
        components: { AdminAppHeader },
        props: ['quizId'],
        setup(props) {
            const quizzesStore = useQuizzesStore()
            const quiz = ref(null)
            const questionIdInput = ref('')
            const router = useRouter()

            const quizQuestionIds = computed(() => {
                return quiz.value.question_ids || []
            })

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
            }
        }
    }
</script>

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
}

.subtitle {
    margin: 6px 0 28px;
    color: #64748b;
    font-size: 14px;
}


/* Form */

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
    transition: border-color 0.2s, box-shadow 0.2s;
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


/* Category / Difficulty / Time */

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


/* Buttons */

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

.save-btn {
    border: 1px solid #2563eb;
    background: #2563eb;
    color: white;
}

.save-btn:hover {
    background: #1d4ed8;
}

.question-id-input {
    display: flex;
    gap: 10px;
}

.question-id-input input {
    flex: 1;
}

.add-question-btn {
    padding: 0 18px;
    border: 1px solid #2563eb;
    border-radius: 8px;
    background: #2563eb;
    color: white;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: 0.2s;
}

.add-question-btn:hover {
    background: #1d4ed8;
}

.question-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-top: 12px;
}

.question-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 12px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
}

.question-number {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 26px;
    height: 26px;
    border-radius: 6px;
    background: #e0e7ff;
    color: #4338ca;
    font-size: 12px;
    font-weight: 700;
    flex-shrink: 0;
}

.question-id {
    flex: 1;
    color: #334155;
    font-family: monospace;
    font-size: 13px;
    word-break: break-all;
}

.remove-question-btn {
    width: 28px;
    height: 28px;
    border: none;
    border-radius: 6px;
    background: #fee2e2;
    color: #dc2626;
    font-size: 18px;
    line-height: 1;
    cursor: pointer;
    transition: 0.2s;
}

.remove-question-btn:hover {
    background: #fecaca;
}

.empty-questions {
    display: block;
    margin-top: 10px;
    color: #94a3b8;
    font-size: 13px;
}


/* Mobile */

@media (max-width: 650px) {
    .edit-quiz {
        padding: 20px 12px;
    }

    .form-card {
        padding: 22px;
    }

    .form-row {
        grid-template-columns: 1fr;
        gap: 0;
    }

    .form-actions {
        flex-direction: column-reverse;
    }

    .form-actions button {
        width: 100%;
    }
}
</style>