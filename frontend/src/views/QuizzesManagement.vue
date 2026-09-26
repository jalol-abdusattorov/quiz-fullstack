<template>
    <div class="dashboard-layout">
        <admin-app-header />
        <main class="container">
            <div class="search-quiz">
                <input class="search-bar" type="text" @input="onTyping" v-model="searching" placeholder="Search quizzes...">
                <select class="select-box search-filter-box" v-model="searchingBy">
                    <option value="title" selected>By Title</option>
                    <option value="description">By Description</option>
                    <option value="category">By Category</option>
                    <option value="difficulty">By Difficulty</option>
                </select>
            </div>
            <div class="filters">
                <div>
                    <label>Category: </label>
                    <select class="select-box" v-model="category" @change="getFilteredQuizzes">
                        <option value="all" selected>All</option>
                        <option value="Programming">Programming</option>
                        <option value="Mathematics">Mathematics</option>
                        <option value="Science">Science</option>
                        <option value="History">History</option>
                        <option value="Geography">Geography</option>
                        <option value="Animals">Animals</option>
                    </select>
                </div>
                <div>
                    <label>difficulty: </label>
                    <select class="select-box" v-model="difficulty" @change="getFilteredQuizzes">
                        <option value="all" selected>All</option>
                        <option value="easy">Easy</option>
                        <option value="medium">Medium</option>
                        <option value="hard">Hard</option>
                    </select>
                </div>
                <div>
                    <label>Sorting: </label>
                    <select class="select-box" v-model="sortingBy" @change="getFilteredQuizzes">
                        <option value="created_at" selected>Date</option>
                        <option value="time_limit">Time limit</option>
                        <option value="question_ids">Questions count</option>
                    </select>
                    <select class="select-box" v-model="sortOrder" @change="getFilteredQuizzes">
                        <option value="ascending">Ascending</option>
                        <option value="descending">Descending</option>
                    </select>
                </div>
            </div>
            <div class="pagination-controls">
                <span class="page-indicator">Page {{ currentPage }}</span>
                <button class="page-btn" :disabled="currentPage <= 1" @click="prevPage">Previous</button>
                <button class="page-btn" @click="nextPage">Next</button>
            </div>
            <div v-if="quizzesStore.quizzes.length">
                <QuizzesList :quizzes="quizzesStore.quizzes" :showManageButton="true" />
            </div>
            <div v-if="quizzesStore.loading">Loading data...</div>
            <div v-if="quizzesStore.error">An error has occured</div>
            <p v-if="!quizzesStore.quizzes?.length">This page is empty</p>
        </main>
    </div>
</template>

<script>
import { useQuizzesStore } from '@/stores/QuizzesStore';
import AdminAppHeader from '../components/AdminAppHeader.vue';
import { onMounted, ref } from 'vue';
import QuizzesList from '@/components/QuizzesList.vue';

    export default {
        components: { AdminAppHeader, QuizzesList },
        setup() {
            const quizzesStore = useQuizzesStore()
            const currentPage = ref(1)
            const category = ref('all')
            const difficulty = ref('all')
            const sortingBy = ref('created_at')
            const sortOrder = ref('ascending')

            const searchingBy = ref('title')
            const searching = ref('')
            const isSearchingQuizzes = ref(false)

            const performSearch = () => {
                searchQuizzesWithFilter()
            }

            let debounceTimer = null
            const onTyping = () => {
                clearTimeout(debounceTimer);

                debounceTimer = setTimeout(() => {
                    performSearch()
                }, 200)
            }

            async function prevPage() {
                if (currentPage.value <= 1) return
                currentPage.value--
                if (!isSearchingQuizzes.value) {
                    getFilteredQuizzes()
                } else {
                    searchQuizzesWithFilter()
                }
            }
            async function nextPage() {
                if (currentPage.value >= 99) return
                currentPage.value++
                if (!isSearchingQuizzes.value) {
                    getFilteredQuizzes()
                } else {
                    searchQuizzesWithFilter()
                }
            }
            async function getFilteredQuizzes() {
                await quizzesStore.filterQuizzes(
                    category.value,
                    difficulty.value,
                    sortingBy.value,
                    sortOrder.value,
                    currentPage.value
                )
                isSearchingQuizzes.value = false
            }
            async function searchQuizzesWithFilter() {
                await quizzesStore.searchQuiz(
                    searchingBy.value,
                    searching.value,
                    currentPage.value
                )
                isSearchingQuizzes.value = true
            }

            onMounted(() => {
                getFilteredQuizzes()
            })

            return {
                onTyping,
                category,
                difficulty,
                sortingBy,
                sortOrder,
                searchingBy,
                searching,
                isSearchingQuizzes,
                currentPage,
                prevPage,
                nextPage,
                quizzesStore,
                getFilteredQuizzes
            }
        }
    }
</script>

<style scoped>
/* Main container and Layout */
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

/* Page controls */
.pagination-controls {
  display: flex;
  justify-content: right;
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

/* Search bar */
.search-quiz {
    display: flex;
    justify-content: center;
    margin: 15px;
}

.search-bar {
    color: #ffffff;
    border-radius: 10px;
    border: 1px solid #ddd;
    color: black;
    width: 700px;
    height: 35px;
    padding-left: 10px;
    padding-right: 10px;
    margin-left: 10px;
    margin-right: 10px;
}

/* Category bar */
.filters {
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  background-color:#ddd;
  padding: 15px;
  margin-bottom: 20px;
  border-radius: 7px;
}

.filters div {
    margin-left: 15px;
    margin-right: 15px;
}

.select-box {
  background: #ddd;
  padding: 10px;
  border-radius: 5px;
  border: 0.8px solid #1e293b;
  margin-left: 5px;
  margin-right: 5px;
  text-align: center;
}

.search-filter-box {
    background-color: #50c878;
}
</style>