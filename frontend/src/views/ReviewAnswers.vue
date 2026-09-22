<!-- <template>
    <div class="container" v-if="quiz">
        <h1>Reviews page - {{ quiz.title }}</h1>
        <div>
            <QuestionAnswer :question-and-answer="quizStore.result.answers[currentQuestionAndAnswerNav - 1]"/>
        </div>
        <div class="actions">
            <p class="page-indicator">Answer {{ currentQuestionAndAnswerNav }}</p>
            <button class="page-btn" @click="nextQAndA" :disabled="currentQuestionAndAnswerNav >= quizStore.result.answers.length">Next</button>
            <button class="page-btn" @click="prevQAndA" :disabled="currentQuestionAndAnswerNav <= 1">Previous</button>
        </div>
        <div class="question-nav">
            <div v-for="(answer, index) in quizStore.result.answers" :key="answer.question_id">
                <button @click="handleNav(index)" class="nav-btn">{{ index + 1 }}</button>
            </div>
        </div>
    </div>
</template> -->

<template>
  <div class="review-page-container" v-if="quiz">
    <h1 class="page-title">Reviews Page - {{ quiz.title }}</h1>

    <div class="card-section">
      <QuestionAnswer 
        :question-and-answer="quizStore.result.answers[currentQuestionAndAnswerNav - 1]"
      />
    </div>

    <div class="navigation-bar">
        <button 
        v-for="(answer, index) in quizStore.result.answers" 
        :key="answer.question_id"
        @click="handleNav(index + 1)" 
        class="nav-num-btn"
        :class="{ active: currentQuestionAndAnswerNav === index + 1 }"
        >
        {{ index + 1 }}
        </button>
    </div>

    <div class="actions-wrapper">
      <button 
        class="action-btn btn-secondary" 
        @click="prevQAndA" 
        :disabled="currentQuestionAndAnswerNav <= 1"
      >
        Previous
      </button>

      <button 
        class="action-btn btn-primary" 
        @click="nextQAndA" 
        :disabled="currentQuestionAndAnswerNav >= quizStore.result.answers.length"
      >
        Next
      </button>
    </div>
    <div class="link">
        <router-link :to="{ name: 'Home' }">Back to home</router-link>
    </div>
  </div>
</template>


<script>
import QuestionAnswer from '@/components/QuestionAnswer.vue';
import { useQuizzesStore } from '@/stores/QuizzesStore';
import { computed, onMounted, ref } from 'vue';

    export default {
        components: { QuestionAnswer },
        setup() {
            const quizStore = useQuizzesStore()
            const currentQuestionAndAnswerNav = ref(1)
            const quiz = ref(null)
            const quizQuestionsIds = computed(() => {
                if (!quiz.value) return null
                return quiz?.value.question_ids || null
            })

            const nextQAndA = () => {
                if (currentQuestionAndAnswerNav.value >= quizQuestionsIds.value.length) {
                    return
                }
                currentQuestionAndAnswerNav.value++
            }
            const prevQAndA = () => {
                if (currentQuestionAndAnswerNav.value <= 1) return
                currentQuestionAndAnswerNav.value--
            }

            function handleNav(index) {
                currentQuestionAndAnswerNav.value = index
            }

            onMounted(async () => {  
                const quizId = quizStore.result?.quiz_id
                if (quizId) {
                    quiz.value = await quizStore.getQuiz(quizId)
                }
            })

            return {
                handleNav,
                quizQuestionsIds,
                quiz,
                quizStore,
                currentQuestionAndAnswerNav,
                nextQAndA,
                prevQAndA
            }
        }
    }
</script>

<style scoped>
.link {
    margin-top: 10px;
}

.review-page-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 2.5rem 1.5rem;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Page Header Title */
.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #111827;
  text-align: center;
  margin-bottom: 2rem;
}

/* Center Card Container */
.card-section {
  width: 100%;
  margin-bottom: 2rem;
}

/* Question Number Selector Bar */
.navigation-bar {
  background-color: #0d131f;
  border-radius: 10px;
  padding: 10px 16px;
  display: flex;
  gap: 12px;
  justify-content: center;
  align-items: center;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.nav-num-btn {
  background-color: transparent;
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  width: 38px;
  height: 38px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-num-btn:hover {
  border-color: #ffffff;
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-num-btn.active {
  background-color: #e65100;
  border-color: #e65100;
  color: #ffffff;
  font-weight: 700;
}

/* Action Buttons Container (Next / Previous) */
.actions-wrapper {
  display: flex;
  gap: 16px;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.action-btn {
  padding: 10px 28px;
  font-size: 0.95rem;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.btn-secondary {
  background-color: #ffffff;
  color: #374151;
  border: 1px solid #d1d5db;
}

.btn-secondary:hover:not(:disabled) {
  background-color: #f9fafb;
  border-color: #9ca3af;
}

.btn-primary {
  background-color: #5046e5;
  color: #ffffff;
}

.btn-primary:hover:not(:disabled) {
  background-color: #4338ca;
}

.action-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>