<template>
    <div>
        <ViewQuiz :quiz="quiz" />
    </div>
</template>

<script>
import ViewQuiz from '@/components/ViewQuiz.vue';
import { useQuizzesStore } from '@/stores/QuizzesStore';
import { onMounted, ref } from 'vue';

    export default {
        props: ['id'],
        components: { ViewQuiz },
        setup(props) {
            const quizStore = useQuizzesStore()   
            const quiz = ref({})
            onMounted(async() => {
                quiz.value = await quizStore.getQuiz(props.id)
                // console.log(quiz.value);
            })

            return { quiz }
        }
    }
</script>

<style scoped>

</style>