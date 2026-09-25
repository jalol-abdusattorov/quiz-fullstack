<template>
    <div class="dashboard-layout">
        <main class="container">
            <div class="page-header">
                <div>
                    <h2>Quizzes</h2>
                </div>

                <div class="pagination-controls">
                    <p class="page-indicatior" v-if="isPopularQuizzes">Popular Quizzes</p>
                    <p class="page-indicatior" v-if="!isPopularQuizzes">All Quizzes</p>
                    <button class="page-btn all-quizzes" @click="allQuizzes">All Quizzes</button>
                    <button class="page-btn popular-quizzes" @click="popularQuizzes">Popular Quizzes</button>
                    <span class="page-indicator">Page {{ currentPage }}</span>
                    <button class="page-btn" :disabled="currentPage <= 1" @click="prevPage">Previous</button>
                    <button class="page-btn" @click="nextPage">Next</button>
                </div>
            </div>

            <div class="filters">
              <label for="category-choice">Category: </label>
              <select class="select-box" v-model="category" @change="handleSelect">
                <option value="" disabled selected>Select an option...</option>
                <option value="Programming">Programming</option>
                <option value="Mathematics">Mathematics</option>
                <option value="Science">Science</option>
                <option value="History">History</option>
                <option value="Geography">Geography</option>
                <option value="Animals">Animals/Nature</option>
              </select>
            </div>

            
            <template v-if="isPopularQuizzes">
              <QuizzesComponent :quizzes="quizzesStore.quizzes.result" :is-popular-quizzes="true" v-if="quizzesStore.quizzes?.result"/>

              <div v-if="quizzesStore.quizzes?.result">
                <div v-if="Object.keys(quizzesStore.quizzes?.result).length === 0">This page is empty</div>
              </div>
            </template>

            <template v-else>
              <QuizzesComponent :quizzes="quizzesStore.quizzes" :is-popular-quizzes="false" />
              <div v-if="quizzesStore.quizzes">
                <p v-if="quizzesStore.quizzes.length === 0">This page is empty</p>
              </div>
              <p v-else>This page is empty</p>
            </template>

            <div v-if="quizzesStore.error">An error has occured</div>
            <div v-if="quizzesStore.loading">Loading data...</div>
        </main>
    </div>
</template>

<script>
import QuizzesComponent from '@/components/QuizzesComponent.vue';
import { useQuizzesStore } from '@/stores/QuizzesStore';
import { onMounted, ref } from 'vue';
import QuizDetails from './QuizDetails.vue';

    export default {
        name: "Quizzes",
        components: { QuizzesComponent, QuizDetails },
        setup() {
            const category = ref()
            const isPopularQuizzes = ref(false)
            const quizzesStore = useQuizzesStore()
            const currentPage = ref(1)

            onMounted(() => {
                quizzesStore.getQuizzes(currentPage.value)
            })

            async function nextPage() {
                if (currentPage.value >= 99) return
                currentPage.value++;
                if (!isPopularQuizzes.value) {
                  await quizzesStore.getQuizzes(currentPage.value)
                } else {
                  await quizzesStore.getPopularQuizzes(currentPage.value)
                }
            }
            async function prevPage() {
                if (currentPage.value > 1)  {
                    currentPage.value--;
                    if (!isPopularQuizzes.value) {
                      await quizzesStore.getQuizzes(currentPage.value)
                    } else {
                      await quizzesStore.getPopularQuizzes(currentPage.value)
                    }
                }
            }

            async function allQuizzes() {
              isPopularQuizzes.value = false
              await quizzesStore.getQuizzes(currentPage.value)
            }

            async function popularQuizzes() {
              isPopularQuizzes.value = true
              await quizzesStore.getPopularQuizzes(currentPage.value)
            }

            async function handleSelect() {
              currentPage.value = 1
              if (isPopularQuizzes.value) isPopularQuizzes.value = false
              await quizzesStore.getQuizzesByCategory(category.value, currentPage.value)
            }

            return { currentPage, nextPage, prevPage, quizzesStore, isPopularQuizzes, category, popularQuizzes, allQuizzes, handleSelect }
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

/* .page-btn */
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

.filters {
  background-color:#ddd;
  padding: 15px;
  margin-bottom: 20px;
  border-radius: 7px;
}

.select-box {
  background: #ddd;
  padding: 10px;
  border-radius: 5px;
  border: 0.8px solid #1e293b;
  margin-left: 15px;
}

</style>