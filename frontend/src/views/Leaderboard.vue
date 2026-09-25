<template>
  <div class="container">
    <div class="leaderboard">
      <h1 class="title">Leaderboard page</h1>
 
      <!-- "My rank" banner: shown once we know where the current user stands -->
      <div class="my-rank" v-if="myEntry">
        <div class="my-rank-info">
          <span class="rank-badge me">{{ myEntry.leaderboard_rank }}</span>
          <div>
            <div class="my-rank-title">Your position</div>
            <div class="my-rank-sub">{{ myEntry.percentage }}% in {{ myEntry.time_taken }}</div>
          </div>
        </div>
        <button class="btn" v-if="!isOnCurrentPage" @click="goToPage(myPage)">
          Show me on the list
        </button>
        <span class="you-here" v-else>You are on this page</span>
      </div>
 
      <!-- Shown before the user's rank is known / searched for -->
      <div class="my-rank" v-else>
        <div class="my-rank-title">Where do you rank?</div>
        <button class="btn" :disabled="searching" @click="findMyRank">
          {{ searching ? 'Searching…' : 'Find my rank' }}
        </button>
      </div>
 
      <p class="state" v-if="!leaderboard">This quiz has no results yet.</p>
 
      <LeaderboardComponent
        v-else
        :leaderboard="leaderboard"
        :current-username="currentUsername"
      />
 
      <div class="pagination">
        <button class="btn ghost" @click="prevPage" :disabled="currentPage <= 1">
          Previous
        </button>
        <span class="page-label">Page {{ currentPage }}</span>
        <button class="btn ghost" @click="nextPage" :disabled="atEnd">
          Next
        </button>
      </div>
    </div>
  </div>
</template>


<script>
import LeaderboardComponent from '@/components/LeaderboardComponent.vue';
import { useAuthStore } from '@/stores/auth';
import { useQuizzesStore } from '@/stores/QuizzesStore';
import { useUsersStore } from '@/stores/Users';
import { computed, onMounted, ref } from 'vue';

    export default {
        props: ['quizId'],
        components: { LeaderboardComponent },
        setup(props) {
            const authStore = useAuthStore()
            const quizzesStore = useQuizzesStore()
            const usersStore = useUsersStore()
            const leaderboard = ref([])
            const currentPage = ref(1)
            const userId = authStore.user?.id
            const currentUsername = ref(null)
            const myEntry = ref(null)
            const myPage = ref(null)
            const searching = ref(null)
            const atEnd = ref(false)


            const isOnCurrentPage = computed(() => {
                if (!leaderboard.value) return

                for (const idx in leaderboard.value) {
                    if (leaderboard.value[idx].user_id === userId) {
                        return true
                    }
                }
                return false
            })

            const nextPage = async () => {
                currentPage.value++
                await loadLeaderboard()
                if (leaderboard.value === null) {
                    atEnd.value = true
                    currentPage.value--
                    await loadLeaderboard()
                }
            }

            const prevPage = async () => {
                if (currentPage.value <= 1) return
                currentPage.value--
                await loadLeaderboard()
            }
            const goToPage = async (page) => {
                currentPage.value = page
                atEnd.value = false
                await loadLeaderboard()
            }

            async function loadLeaderboard() {
                leaderboard.value = await quizzesStore.getQuizLeaderboardRankings(props.quizId, currentPage.value)
                if (leaderboard.value?.message == "this quiz haven't been tried yet") {
                    leaderboard.value = null
                } else if (leaderboard.value?.message == "this quiz has no statistics on this page") {
                    leaderboard.value = null
                } else {
                    leaderboard.value = leaderboard.value.result

                    // for (const idx in leaderboard.value) {
                    //     if (leaderboard.value[idx].user_id == userId) {
                    //         myEntry.value = leaderboard.value[idx]

                    //         myPage.value = Math.ceil(idx / 10)
                    //         console.log(myPage.value);

                    //         return
                    //     }
                    // }
                }
            }
            async function getCorrectUsername() {
                if (!userId) return

                const response = await usersStore.getUserDetails(userId)
                currentUsername.value = response.username
            }

            async function findMyRank() {
                searching.value = true

                try {
                    myEntry.value = await quizzesStore.getUserLeaderboardRank(props.quizId, userId)
                    myPage.value = Math.ceil(myEntry.value.leaderboard_rank / 10)
                } finally {
                    searching.value = false
                }
            }

            onMounted(() => {
                loadLeaderboard()
                getCorrectUsername()
            })

            return {
                atEnd,
                goToPage,
                searching,
                findMyRank,
                currentUsername,
                myEntry,
                myPage,
                isOnCurrentPage,
                quizzesStore,
                leaderboard,
                currentPage,
                nextPage,
                prevPage
            }
        }
    }
</script>


<style scoped>
.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 16px;
}
 
.leaderboard {
  background: #ffffff;
  border-radius: 16px;
  padding: 32px;
  max-width: 800px;
  margin: 16px auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  font-family: 'Inter', sans-serif;
}
 
.title {
  font-family: 'Poppins', 'Inter', sans-serif;
  font-size: 1.75rem;
  font-weight: 700;
  color: #1a202c;
  text-align: center;
  margin: 0 0 24px;
}
 
/* "My rank" banner */
.my-rank {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
  background: #ebf4ff;
  border: 2px solid #2b6cb0;
  border-radius: 12px;
  padding: 12px 16px;
  margin-bottom: 20px;
}
.my-rank-info {
  display: flex;
  align-items: center;
  gap: 12px;
}
.my-rank-title {
  font-weight: 600;
  color: #1a365d;
}
.my-rank-sub {
  font-size: 0.85rem;
  color: #4a5568;
}
.you-here {
  font-size: 0.85rem;
  font-weight: 600;
  color: #2b6cb0;
}
 
/* Rank badge (shared look with UserLeaderboard.vue) */
.rank-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 34px;
  height: 34px;
  border-radius: 50%;
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 0.95rem;
  color: #4a5568;
  background: #edf2f7;
}
.rank-badge.me {
  box-shadow: 0 0 0 2px #2b6cb0;
}
 
/* Buttons */
.btn {
  border: none;
  border-radius: 8px;
  background: #2b6cb0;
  color: #ffffff;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 0.9rem;
  padding: 8px 16px;
  cursor: pointer;
}
.btn:hover:not(:disabled) { background: #1a365d; }
.btn:focus-visible { outline: 2px solid #1a365d; outline-offset: 2px; }
.btn:disabled { opacity: 0.5; cursor: not-allowed; }
.btn.ghost {
  background: #ffffff;
  color: #2b6cb0;
  border: 2px solid #2b6cb0;
}
.btn.ghost:hover:not(:disabled) { background: #ebf4ff; }
 
/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 24px;
}
.page-label {
  font-weight: 600;
  color: #4a5568;
}
 
.state {
  text-align: center;
  color: #718096;
  padding: 24px 0;
}
 
@media (max-width: 640px) {
  .leaderboard { padding: 20px 12px; }
}
</style>
