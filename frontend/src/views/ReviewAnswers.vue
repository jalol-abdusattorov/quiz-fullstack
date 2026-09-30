<template>

  <div class="review-page-container" v-if="quiz">

    <!-- Header -->
    <header class="review-header">
      <div class="header-content">
        <div class="eyebrow">
          <span class="eyebrow-dot"></span>
          Quiz Review
        </div>

        <h1 class="page-title">{{ quiz.title }}</h1>

        <p class="page-subtitle">
          Review your answers and see how you performed on each question.
        </p>
      </div>

      <div class="question-counter">
        <span class="counter-current">{{ currentQuestionAndAnswerNav }}</span>
        <span class="counter-divider">/</span>
        <span>{{ quizStore.result.answers.length }}</span>
        <small>Questions</small>
      </div>
    </header>


    <!-- Question / Answer -->
    <main class="card-section">

      <div class="question-label">
        <span>Question</span>
        <span class="question-number">
          {{ currentQuestionAndAnswerNav }}
        </span>
      </div>

      <div class="answer-card">
        <QuestionAnswer
          :question-and-answer="
            quizStore.result.answers[currentQuestionAndAnswerNav - 1]
          "
        />
      </div>

    </main>


    <!-- Question Navigation -->
    <section class="navigation-section">

      <div class="navigation-header">
        <div>
          <h2>Questions</h2>
          <p>Select a question to review</p>
        </div>

        <span class="navigation-count">
          {{ currentQuestionAndAnswerNav }} of
          {{ quizStore.result.answers.length }}
        </span>
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

    </section>


    <!-- Previous / Next -->
    <div class="actions-wrapper">

      <button
        class="action-btn btn-secondary"
        @click="prevQAndA"
        :disabled="currentQuestionAndAnswerNav <= 1"
      >
        <span class="arrow">←</span>
        Previous
      </button>

      <button
        class="action-btn btn-primary"
        @click="nextQAndA"
        :disabled="
          currentQuestionAndAnswerNav >= quizStore.result.answers.length
        "
      >
        Next
        <span class="arrow">→</span>
      </button>

    </div>


    <!-- Back Home -->
    <router-link
      :to="{ name: 'Home' }"
      class="back-home"
    >
      <span>←</span>
      Back to home
    </router-link>

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
.review-page-container {
  min-height: 100vh;
  box-sizing: border-box;

  max-width: 950px;
  margin: 0 auto;

  padding: 48px 24px 60px;

  font-family:
    system-ui,
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    Roboto,
    sans-serif;

  color: #172033;
}


/* =========================
   HEADER
========================= */

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;

  gap: 30px;

  margin-bottom: 32px;
}

.header-content {
  min-width: 0;
}

.eyebrow {
  display: flex;
  align-items: center;
  gap: 8px;

  margin-bottom: 10px;

  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;

  color: #6366f1;
}

.eyebrow-dot {
  width: 7px;
  height: 7px;

  border-radius: 50%;

  background: #6366f1;
}

.page-title {
  margin: 0;

  font-size: clamp(1.8rem, 4vw, 2.45rem);
  line-height: 1.15;
  font-weight: 750;

  color: #111827;
}

.page-subtitle {
  margin: 10px 0 0;

  max-width: 600px;

  font-size: 0.95rem;
  line-height: 1.6;

  color: #6b7280;
}


/* Question counter */

.question-counter {
  flex-shrink: 0;

  display: grid;
  grid-template-columns: auto auto auto;
  align-items: baseline;
  column-gap: 4px;

  min-width: 100px;
  padding: 13px 17px;

  border: 1px solid #e5e7eb;
  border-radius: 12px;

  background: #ffffff;

  box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);

  font-size: 0.9rem;
  font-weight: 600;

  color: #9ca3af;
}

.counter-current {
  font-size: 1.4rem;
  font-weight: 750;
  color: #4f46e5;
}

.counter-divider {
  color: #d1d5db;
}

.question-counter small {
  grid-column: 1 / -1;

  margin-top: 3px;

  font-size: 0.7rem;
  font-weight: 600;

  color: #9ca3af;
}


/* =========================
   QUESTION CARD
========================= */

.card-section {
  width: 100%;
  margin-bottom: 28px;
}

.question-label {
  display: flex;
  align-items: center;
  justify-content: space-between;

  margin-bottom: 10px;
  padding: 0 4px;

  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;

  color: #9ca3af;
}

.question-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;

  width: 27px;
  height: 27px;

  border-radius: 8px;

  background: #eef2ff;

  color: #4f46e5;

  font-size: 0.78rem;
}

.answer-card {
  width: 100%;
  box-sizing: border-box;

  padding: 24px;

  border: 1px solid #e5e7eb;
  border-radius: 18px;

  background: #ffffff;

  box-shadow:
    0 10px 30px rgba(15, 23, 42, 0.06),
    0 2px 6px rgba(15, 23, 42, 0.03);
}


/* =========================
   NAVIGATION SECTION
========================= */

.navigation-section {
  width: 100%;
  box-sizing: border-box;

  margin-bottom: 24px;
  padding: 20px;

  border: 1px solid #e5e7eb;
  border-radius: 16px;

  background: #f9fafb;
}

.navigation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  gap: 20px;

  margin-bottom: 16px;
}

.navigation-header h2 {
  margin: 0 0 3px;

  font-size: 0.95rem;
  font-weight: 700;

  color: #1f2937;
}

.navigation-header p {
  margin: 0;

  font-size: 0.78rem;

  color: #9ca3af;
}

.navigation-count {
  padding: 6px 10px;

  border-radius: 7px;

  background: #ffffff;
  border: 1px solid #e5e7eb;

  font-size: 0.75rem;
  font-weight: 600;

  color: #6b7280;
}


/* Question buttons */

.navigation-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.nav-num-btn {
  width: 40px;
  height: 40px;

  display: flex;
  align-items: center;
  justify-content: center;

  border: 1px solid #dfe3ea;
  border-radius: 9px;

  background: #ffffff;

  color: #4b5563;

  font-size: 0.85rem;
  font-weight: 650;

  cursor: pointer;

  transition:
    background 0.18s ease,
    color 0.18s ease,
    border-color 0.18s ease,
    transform 0.18s ease,
    box-shadow 0.18s ease;
}

.nav-num-btn:hover {
  border-color: #a5b4fc;

  background: #eef2ff;

  color: #4f46e5;

  transform: translateY(-1px);
}

.nav-num-btn.active {
  border-color: #4f46e5;

  background: #4f46e5;

  color: #ffffff;

  box-shadow: 0 4px 10px rgba(79, 70, 229, 0.22);

  transform: translateY(-1px);
}


/* =========================
   ACTION BUTTONS
========================= */

.actions-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;

  width: 100%;

  gap: 14px;

  margin-bottom: 28px;
}

.action-btn {
  min-width: 130px;

  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;

  padding: 11px 20px;

  border-radius: 10px;

  font-size: 0.88rem;
  font-weight: 650;

  cursor: pointer;

  transition:
    background 0.18s ease,
    border-color 0.18s ease,
    transform 0.18s ease,
    box-shadow 0.18s ease;

  box-sizing: border-box;
}

.arrow {
  font-size: 1rem;
  line-height: 1;
}

.btn-secondary {
  border: 1px solid #d9dde5;

  background: #ffffff;

  color: #374151;
}

.btn-secondary:hover:not(:disabled) {
  background: #f9fafb;

  border-color: #b9bec8;

  transform: translateY(-1px);
}

.btn-primary {
  border: 1px solid #4f46e5;

  background: #4f46e5;

  color: #ffffff;

  box-shadow: 0 4px 10px rgba(79, 70, 229, 0.15);
}

.btn-primary:hover:not(:disabled) {
  background: #4338ca;

  border-color: #4338ca;

  transform: translateY(-1px);

  box-shadow: 0 6px 14px rgba(79, 70, 229, 0.2);
}

.action-btn:disabled {
  opacity: 0.4;

  cursor: not-allowed;

  box-shadow: none;
}


/* =========================
   BACK HOME
========================= */

.back-home {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 6px;

  width: fit-content;

  margin: 0 auto;

  color: #6b7280;

  font-size: 0.85rem;
  font-weight: 600;

  text-decoration: none;

  transition:
    color 0.18s ease,
    gap 0.18s ease;
}

.back-home:hover {
  color: #4f46e5;
  gap: 9px;
}


/* =========================
   RESPONSIVE
========================= */

@media (max-width: 650px) {

  .review-page-container {
    padding: 30px 16px 45px;
  }

  .review-header {
    align-items: flex-start;
    flex-direction: column;
    gap: 18px;
  }

  .question-counter {
    width: fit-content;
  }

  .answer-card {
    padding: 16px;
  }

  .navigation-section {
    padding: 16px;
  }

  .navigation-header {
    align-items: flex-start;
    flex-direction: column;
    gap: 10px;
  }

  .nav-num-btn {
    width: 37px;
    height: 37px;
  }

  .actions-wrapper {
    gap: 10px;
  }

  .action-btn {
    flex: 1;
    min-width: 0;
  }

}
</style>