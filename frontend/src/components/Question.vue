<template>
    <div class="question-card" v-if="question">
        <h2>{{ question.question }}</h2>
        <div v-for="(option, index) in question.options" :key="option">
            <div class="choice">
                <input
                    type="radio"
                    :name="'question_' + question._id"
                    :value="index"
                    v-model="selectedAnswer"
                    @change="sendAnswer"
                >

                <p>{{ option }}</p>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, watch } from 'vue';

    export default {
        props: ['question', 'savedAnswer'],
        emits: ['select-answer'],
        setup(props, { emit }) {
            const selectedAnswer = ref(props.savedAnswer)

            watch(() => props.savedAnswer, (newVal) => {
                selectedAnswer.value = newVal;
            });

            const sendAnswer = () => {
                emit('select-answer', selectedAnswer.value)
            }

            return { selectedAnswer, sendAnswer }
        }
    }
</script>

<style scoped>
/* Radio */
input[type="radio"] {
    margin-right: 10px;
    cursor: pointer;
}

/* Choice */
.choice {
    display: flex;
    justify-content: start;
}
</style>