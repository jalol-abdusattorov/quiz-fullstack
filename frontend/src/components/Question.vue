<template>
    <div class="question-card" v-if="question">
        <h2>{{ question.question }}</h2>
        <div v-for="(option, index) in question.options" :key="option">
            <div class="choice">
                <input type="radio" name="answer" :value="index" v-model="selectedAnswer">
                <p>{{ option }}</p>
            </div>
        </div>
        <p>Your answer: {{ selectedAnswer == 0 ? "A" : selectedAnswer == 1 ? "B" : selectedAnswer == 2 ? "C" : selectedAnswer == 3 ? "D" : "..." }}</p>
    </div>
</template>

<script>
import { ref } from 'vue';

    export default {
        props: ['question'],
        setup(props) {
            const selectedAnswer = ref(null)

            return { selectedAnswer }
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