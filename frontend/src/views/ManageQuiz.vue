<template>
    <div v-if="quizDetails" class="manage-page">
        <admin-app-header />

        <ConfirmModal v-if="deleting" class="confirm-modal">
            <h1>Are you sure you want to delete?</h1>

            <p>This quiz will be lost forever.</p>

            <div class="modal-actions">
                <button @click="handleCancel">Cancel</button>
                <button @click="deleteQuiz">Delete</button>
            </div>
        </ConfirmModal>

        <main class="container">
            <!-- Page Header -->
            <div class="page-header">
                <div>
                    <span class="page-label">QUIZ MANAGEMENT</span>
                    <h1>Managing Quiz</h1>
                    <p>View and manage your quiz settings and statistics.</p>
                </div>
            </div>

            <!-- Quiz -->
            <section class="quiz-section">
                <div class="section-header">
                    <div>
                        <h2>Quiz Overview</h2>
                        <p>Information about the selected quiz</p>
                    </div>
                </div>

                <div class="quiz-card">
                    <quizzes-list
                        :quizzes="[quizDetails]"
                        :showManageButton="false"
                    />
                </div>
            </section>

            <!-- Actions -->
            <section class="actions-section">
                <div class="section-header">
                    <div>
                        <h2>Manage Quiz</h2>
                        <p>Choose an action for this quiz</p>
                    </div>
                </div>

                <div class="actions">
                    <router-link
                        :to="{ name: 'QuizStatistics' }"
                        class="action-card statistics-action"
                    >
                        <div class="action-icon">📊</div>

                        <div class="action-info">
                            <h3>Statistics</h3>
                            <p>View quiz performance and results</p>
                        </div>

                        <span class="arrow">→</span>
                    </router-link>

                    <router-link
                        :to="{
                            name: 'EditQuiz',
                            params: { quizId: quizId }
                        }"
                        class="action-card edit-action"
                    >
                        <div class="action-icon">✏️</div>

                        <div class="action-info">
                            <h3>Edit Quiz</h3>
                            <p>Update quiz information and questions</p>
                        </div>

                        <span class="arrow">→</span>
                    </router-link>

                    <button class="action-card delete-action" @click="handleDelete">
                        <div class="action-icon">🗑️</div>

                        <div class="action-info">
                            <h3>Delete Quiz</h3>
                            <p>Permanently remove this quiz</p>
                        </div>

                        <span class="arrow">→</span>
                    </button>
                </div>
            </section>
        </main>

        <!-- Loading -->
        <p v-if="quizzesStore.loading" class="status loading">
            Loading quiz...
        </p>

        <!-- Error -->
        <p v-if="quizzesStore.error" class="status error">
            An error has occurred while loading the quiz.
        </p>
    </div>
</template>

<script>
import AdminAppHeader from '@/components/AdminAppHeader.vue';
import { useQuizzesStore } from '@/stores/QuizzesStore';
import { onMounted, ref } from 'vue';
import QuizzesList from '../components/QuizzesList.vue';
import ConfirmModal from '@/components/ConfirmModal.vue';
import { useRouter } from 'vue-router';

    export default {
        props: ['quizId'],
        components: { AdminAppHeader, QuizzesList, ConfirmModal },
        setup(props) {
            const quizzesStore = useQuizzesStore()
            const quizDetails = ref(null)
            const deleting = ref(false)
            const router = useRouter()

            async function loadQuizDetails() {
                quizDetails.value = await quizzesStore.getQuiz(props.quizId)
            }

            const handleDelete = () => {
                deleting.value = true
            }
            const handleCancel = () => {
                deleting.value = false
            }
            const deleteQuiz = async () => {
                await quizzesStore.deleteQuiz(props.quizId)
                deleting.value = false
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
                quizDetails,
                quizzesStore,
                handleDelete,
                deleting,
                handleCancel,
                deleteQuiz
            }
        }
    }
</script>

<style scoped>
.manage-page {
    min-height: 100vh;
    background: #f8fafc;
    color: #0f172a;
}

/* Main container */
.container {
    width: min(1100px, calc(100% - 40px));
    margin: 0 auto;
    padding: 40px 0 60px;
}

/* Page header */
.page-header {
    margin-bottom: 32px;
}

.page-label {
    display: inline-block;
    margin-bottom: 8px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: #2563eb;
}

.page-header h1 {
    margin: 0;
    font-size: 2rem;
    font-weight: 750;
    letter-spacing: -0.03em;
    color: #0f172a;
}

.page-header p {
    margin: 8px 0 0;
    color: #64748b;
    font-size: 0.95rem;
}

/* Sections */
.quiz-section,
.actions-section {
    margin-bottom: 28px;
}

.section-header {
    margin-bottom: 14px;
}

.section-header h2 {
    margin: 0;
    font-size: 1.15rem;
    font-weight: 700;
    color: #0f172a;
}

.section-header p {
    margin: 4px 0 0;
    color: #64748b;
    font-size: 0.875rem;
}

/* Quiz card */
.quiz-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);
}

.actions {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.action-card {
    display: flex;
    align-items: center;
    width: 100%;
    min-height: 80px;
    box-sizing: border-box;

    padding: 16px 18px;

    border: 1px solid #e2e8f0;
    border-radius: 12px;
    background: #ffffff;

    text-align: left;
    text-decoration: none;
    color: inherit;

    cursor: pointer;

    transition:
        transform 0.18s ease,
        box-shadow 0.18s ease,
        border-color 0.18s ease;
}

.action-card:hover {
    transform: translateY(-1px);
    box-shadow: 0 5px 14px rgba(15, 23, 42, 0.07);
}

/* Icon */
.action-icon {
    display: flex;
    align-items: center;
    justify-content: center;

    width: 42px;
    height: 42px;
    flex-shrink: 0;

    margin-right: 14px;

    border-radius: 10px;
    background: #eff6ff;

    font-size: 1.1rem;
}

/* Text */
.action-info {
    flex: 1;
    min-width: 0;
}

.action-info h3 {
    margin: 0 0 3px;

    font-size: 0.95rem;
    font-weight: 700;
    color: #0f172a;
}

.action-info p {
    margin: 0;

    font-size: 0.8rem;
    line-height: 1.4;
    color: #64748b;
}

/* Arrow */
.arrow {
    flex-shrink: 0;
    margin-left: 16px;

    color: #94a3b8;
    font-size: 1.2rem;

    transition:
        transform 0.18s ease,
        color 0.18s ease;
}

.action-card:hover .arrow {
    transform: translateX(3px);
    color: #2563eb;
}

/* Statistics */
.statistics-action:hover {
    border-color: #93c5fd;
}

.statistics-action .action-icon {
    background: #eff6ff;
}

/* Edit */
.edit-action:hover {
    border-color: #c4b5fd;
}

.edit-action .action-icon {
    background: #f5f3ff;
}

/* Delete */
.delete-action {
    font-family: inherit;
}

.delete-action:hover {
    border-color: #fca5a5;
}

.delete-action .action-icon {
    background: #fef2f2;
}

.delete-action:hover .arrow {
    color: #dc2626;
}

/* Status messages */
.status {
    width: min(1100px, calc(100% - 40px));
    margin: 20px auto;
    padding: 14px 16px;

    border-radius: 10px;

    font-size: 0.9rem;
}

.loading {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    color: #1d4ed8;
}

.error {
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #dc2626;
}

.confirm-modal h1 {
    margin: 0;
    font-size: 1.4rem;
    font-weight: 700;
    color: #0f172a;
    letter-spacing: -0.02em;
}

.confirm-modal p {
    margin: 10px 0 24px;
    font-size: 0.9rem;
    line-height: 1.5;
    color: #64748b;
}

.confirm-modal .modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 8px;
}

.confirm-modal .modal-actions button {
    padding: 9px 18px;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
    font-family: inherit;
    font-size: 0.875rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.18s ease;
}

/* Cancel */
.confirm-modal .modal-actions button:first-child {
    background: #ffffff;
    color: #475569;
}

.confirm-modal .modal-actions button:first-child:hover {
    background: #f8fafc;
    border-color: #cbd5e1;
}

/* Delete */
.confirm-modal .modal-actions button:last-child {
    background: #dc2626;
    border-color: #dc2626;
    color: #ffffff;
}

.confirm-modal .modal-actions button:last-child:hover {
    background: #b91c1c;
    border-color: #b91c1c;
}


/* Responsive */
@media (max-width: 800px) {
    .actions {
        grid-template-columns: 1fr;
    }

    .container {
        width: min(100% - 28px, 1100px);
        padding-top: 28px;
    }

    .page-header h1 {
        font-size: 1.7rem;
    }
}

@media (max-width: 480px) {
    .container {
        width: calc(100% - 20px);
    }

    .quiz-card {
        padding: 12px;
    }

    .action-card {
        min-height: 95px;
        padding: 16px;
    }

    .action-icon {
        width: 40px;
        height: 40px;
    }
}
</style>