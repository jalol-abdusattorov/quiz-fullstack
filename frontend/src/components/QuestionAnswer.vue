<!-- <template>
    <div class="container">
        <div class="question-card" v-if="question">
            <h2>{{ questionAndAnswer }}</h2>
            <h2>{{ question.question }}</h2>
            <h2>Your answer: {{ questionAndAnswer.selected_answer }}</h2>
            <h2>Correct answer: {{ question.correct_answer }}</h2>
            <h2>{{ questionAndAnswer.selected_answer === question.correct_answer ? "Correct" : "Incorrect" }}</h2>
        </div>
    </div>
</template> -->

<template>
  <div class="review-card-wrapper" v-if="question">
    <div 
      class="status-badge" 
      :class="isCorrect ? 'badge-correct' : 'badge-incorrect'"
    >
      <span class="status-icon">
        <template v-if="isCorrect">
          <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
          </svg>
        </template>
        <template v-else>
          <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor">
            <path d="M12 2C6.47 2 2 6.47 2 12s4.47 10 10 10 10-4.47 10-10S17.53 2 12 2zm5 13.59L15.59 17 12 13.41 8.41 17 7 15.59 10.59 12 7 8.41 8.41 7 12 10.59 15.59 7 17 8.41 13.41 12 17 15.59z"/>
          </svg>
        </template>
      </span>
      <span class="status-text">{{ isCorrect ? 'CORRECT' : 'INCORRECT' }}</span>
    </div>

    <h3 class="question-text">{{ question.question }}</h3>

    <div class="details-container">
      <div class="detail-row">
        <span class="label">Result:</span>
        <span class="value" :class="isCorrect ? 'text-correct' : 'text-incorrect'">
          {{ isCorrect ? 'Correct' : 'Incorrect' }}
        </span>
      </div>

      <div class="detail-row">
        <span class="label">Your Selected Answer:</span>
        <span class="highlight-chip" :class="isCorrect ? 'chip-correct' : 'chip-incorrect'">
          {{ userAnswerText }}
        </span>
      </div>

      <div class="detail-row" v-if="question.correct_answer !== undefined && question.correct_answer !== null">
        <span class="label">Correct Answer:</span>
        <span class="value bold-value">{{ correctAnswerText }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { useQuestionsStore } from '@/stores/QuestionsStore';
import { computed, onMounted, ref, watch } from 'vue';

    export default {
        props: ['questionAndAnswer'],
        setup(props) {
            const questionStore = useQuestionsStore()
            const question = ref()

            const isCorrect = computed(() => {
                if (!props.questionAndAnswer || !question.value) return false
                return props.questionAndAnswer.selected_answer === question.value.correct_answer
            })

            const correctAnswerText = computed(() => {
                if (!question.value || question.value.correct_answer == null) return null
                return question.value.options?.[question.value.correct_answer] ?? question.value.correct_answer
            })
            const userAnswerText = computed(() => {
                if (!question.value || !props.questionAndAnswer || props.questionAndAnswer.selected_answer == null) return null
                return question.value.options?.[props.questionAndAnswer.selected_answer] ?? props.questionAndAnswer.selected_answer
            })

            watch(
                () => props.questionAndAnswer,
                async () => {
                    await loadQuestion()
                },
                { deep: true }
            )

            async function loadQuestion() {
                if (props.questionAndAnswer?.question_id) {
                        question.value = null
                        question.value = await questionStore.getQuestionDetails(props.questionAndAnswer.question_id)
                    }
            }

            onMounted(() => {
                loadQuestion()
            })

            return {
                isCorrect,
                questionStore,
                question,
                correctAnswerText,
                userAnswerText
            }
        },
    }
</script>


<style scoped>
.review-card-wrapper {
  background: #ffffff;
  border-radius: 16px;
  padding: 40px 32px;
  max-width: 680px;
  margin: 0 auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  text-align: center;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Status Badge */
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
  font-size: 1.1rem;
  letter-spacing: 0.5px;
  margin-bottom: 24px;
}

.badge-correct {
  color: #2e7d32;
}

.badge-incorrect {
  color: #d32f2f;
}

.status-icon {
  display: flex;
  align-items: center;
}

/* Question Styling */
.question-text {
  font-size: 1.35rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 24px 0;
  line-height: 1.4;
}

/* Details Section */
.details-container {
  display: flex;
  flex-direction: column;
  gap: 14px;
  align-items: center;
}

.detail-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.05rem;
  color: #333333;
}

.label {
  font-weight: 600;
  color: #222222;
}

.value {
  font-weight: 500;
}

.bold-value {
  font-weight: 700;
  color: #111111;
}

.text-correct {
  color: #2e7d32;
  font-weight: 600;
}

.text-incorrect {
  color: #d32f2f;
  font-weight: 600;
}

/* Highlighted answer badge */
.highlight-chip {
  padding: 3px 12px;
  border-radius: 6px;
  font-weight: 700;
}

.chip-correct {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.chip-incorrect {
  background-color: #ffebee;
  color: #c62828;
}
</style>