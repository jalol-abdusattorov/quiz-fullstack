<template>
    <div class="dashboard-layout">
        <main class="container">
            <div class="page-header">
                <div>
                    <h2>Quizzes</h2>
                </div>

                <div class="pagination-controls">
                    <span class="page-indicator">Page {{ currentPage }}</span>
                    <button class="page-btn" :disabled="currentPage <= 1" @click="prevPage">Previous</button>
                    <button class="page-btn" @click="nextPage">Next</button>
                </div>
            </div>

            <QuizzesComponent :quizzes="quizzesStore.quizzes"/>
            <div v-if="quizzesStore.error">An error has occured</div>
            <div v-if="quizzesStore.loading">loading data...</div>
            <div v-if="!quizzesStore.quizzes">Page is empty</div>
        </main>
    </div>
</template>

<script>
import QuizzesComponent from '@/components/QuizzesComponent.vue';
import { useQuizzesStore } from '@/stores/QuizzesStore';
import { onMounted, ref } from 'vue';
import QuizDetails from './QuizDetails.vue';

    export default {
        components: { QuizzesComponent, QuizDetails },
        setup() {
            const quizzesStore = useQuizzesStore()
            const currentPage = ref(1)
            const response = ref('')
            
            onMounted(() => {
                quizzesStore.getQuizzes(currentPage.value)
            })

            async function nextPage() {
                currentPage.value++;
                response.value = await quizzesStore.getQuizzes(currentPage.value)
            }
            async function prevPage() {
                if (currentPage.value !== 1)  {
                    currentPage.value--;
                    response.value = await quizzesStore.getQuizzes(currentPage.value)
                }
            }
            const selectedQuiz = (quizId) => {
                
            }

            return { currentPage, nextPage, prevPage, quizzesStore, response, selectedQuiz }
        }
    }
</script>

<style scoped>
.dashboard-layout {
  min-height: 100vh;
  background-color: #f8fafc;
  color: #1e293b;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.page-header h2 {
  font-size: 1.75rem;
  font-weight: 700;
  margin: 0;
}

.subtitle {
  color: #64748b;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.page-indicator {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
}

.page-btn {
  background-color: #ffffff;
  border: 1px solid #cbd5e1;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.page-btn:hover:not(:disabled) {
  background-color: #f8fafc;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>