<template>
    <div>
        <h1>Leaderboard page</h1>
        <p>{{ currentPage }}</p>
        <p>{{ leaderboard }}</p>
    </div>
</template>

<script>
import { useQuizzesStore } from '@/stores/QuizzesStore';
import { onMounted, ref } from 'vue';

    export default {
        props: ['quizId'],
        setup(props) {
            const quizzesStore = useQuizzesStore()
            const leaderboard = ref([])
            const currentPage = ref(1)

            const nextPage = () => {
                currentPage.value++
            }
            const prevPage = () => {
                if (currentPage.value <= 1) return
                currentPage.value--
            }

            async function loadLeaderboard() {
                leaderboard.value = await quizzesStore.getQuizLeaderboardRankings(props.quizId, currentPage.value)
            }

            onMounted(() => {
                loadLeaderboard()
            })

            return { quizzesStore, leaderboard, currentPage, nextPage, prevPage }
        }
    }
</script>

<style scoped>

</style>