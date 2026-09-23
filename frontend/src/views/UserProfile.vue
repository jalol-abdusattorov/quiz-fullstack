<template>
    <div class="container">
        <h1 v-if="user">Your Profile, {{ user.username }} </h1>

        <div class="empty-user-stats" v-if="!userStats">
            <h1>You currently have no statistics</h1>
            <h2>Play more quizzes to get more statistics</h2>
            <router-link class="router-link-to-quizzes" :to="{ name: 'Quizzes' }">Quizzes</router-link>
        </div>

    <template v-if="userStats">
        <div class="stats-container">
            <h2 class="title">Your Statistics</h2>

            <div class="cards-grid">
            <!-- Average Score Card -->
                <div class="stat-card blue">
                    <div class="card-header">Average Score</div>
                    <div class="card-body">
                        <span class="stat-number">{{ Math.round(userStats.average_score * 100) / 100 }}</span>
                </div>
            </div>

            <!-- Quizzes Completed Card -->
            <div class="stat-card green">
                <div class="card-header">Quizzes Completed</div>
                <div class="card-body">
                    <span class="stat-number">{{ userStats.quizzes_taken }}</span>
                </div>
            </div>

            <!-- Best Score Card -->
            <div class="stat-card orange">
                    <div class="card-header">Best Score</div>
                    <div class="card-body">
                        <span class="stat-number">{{ userStats.best_score }}</span>
                    </div>
                </div>
            </div>

            <!-- Quizzes Completed Card -->
            <div class="stat-card red">
                <div class="card-header">Accuracy</div>
                <div class="card-body">
                    <span class="stat-number">{{ userStats.accuracy }}%</span>
                </div>
            </div>
        </div>
    </template>


        <div class="recent-attempts" v-if="userRecentAttempts">
            <hr>
            <h1>Recent attempts</h1>
            <div class="quizzes">
                <QuizzesComponent :quizzes="userRecentAttempts" />
            </div>
        </div>
    </div>
</template>

<script>
import QuizzesComponent from '@/components/QuizzesComponent.vue';
import { useAuthStore } from '@/stores/auth';
import { useQuizzesStore } from '@/stores/QuizzesStore';
import { useUsersStore } from '@/stores/Users';
import { onMounted, ref } from 'vue';

    export default {
        components: { QuizzesComponent },
        setup() {
            const authStore = useAuthStore()
            const quizzesStore = useQuizzesStore()
            const usersStore = useUsersStore()
            const userId = authStore.user.id
            const userStats = ref(null)
            const userRecentAttempts = ref([])
            const user = ref(null)

            async function loadUserStatistics() {
                userStats.value = await quizzesStore.getUserStatistics(userId)
                if (userStats.value?.message == "this user has no statistics") {
                    userStats.value = null
                } else {
                    userStats.value = userStats.value.result[0]
                }
            }
            async function loadUserRecentAttempts() {
                userRecentAttempts.value = await quizzesStore.getUserRecentAttepmts(userId)
                if (userRecentAttempts.value?.message === "this user has no recent attemtps") {
                  userRecentAttempts.value = null
                } else {
                  userRecentAttempts.value = userRecentAttempts.value.result
                }
            }
            async function loadUserDetails() {
                if (!userId) return
                user.value = await usersStore.getUserDetails(userId)
            }

            onMounted(() => {
                loadUserStatistics()
                loadUserRecentAttempts()
                loadUserDetails()
            })

            return { user, userRecentAttempts, authStore, userStats }
        }
    }
</script>

<style scoped>
.container {
  max-width: 1400px;
  margin: 0 auto;
}

.empty-user-stats {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.router-link-to-quizzes {
  text-decoration: underline 2px transparent;
  text-underline-offset: 4px;
  transition: text-decoration 0.3s ease;
}
.router-link-to-quizzes:hover {
  text-decoration-color: #000;
}

hr {
  color: #e7e4e4;
}

/* Recent Attempts */
.recent-attempts .quizzes {
  display: flex;
  flex-direction: column;
  margin-left: 15px;
}
.recent-attempts h1 {
  font-family: 'Poppins', 'Inter', sans-serif;
  margin-left: 43%;
}

/* Main Outer Container */
.stats-container {
  background-color: #ffffff;
  border-radius: 16px;
  padding: 32px;
  padding-left: 350px;
  padding-right: 350px;
  max-width: 800px;
  margin: 0 auto;
  margin-top: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  text-align: center;
}

.title {
  font-family: 'Poppins', 'Inter', sans-serif;
  font-size: 1.75rem;
  font-weight: 700;
  color: #1a202c;
  margin-bottom: 24px;
}

/* Flexbox layout to place cards side-by-side */
.cards-grid {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: 20px;
}

/* General Stat Card Style */
.stat-card {
  flex: 1;
  min-width: 180px;
  border-radius: 12px;
  overflow: hidden; /* Clips background colors inside rounded borders */
  background-color: #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
}

/* Card Header */
.card-header {
  color: #ffffff;
  font-family: 'Inter', sans-serif;
  font-size: 0.95rem;
  font-weight: 600;
  padding: 12px 16px;
}

/* Card Body (fixes clipping issues) */
.card-body {
  padding: 24px 16px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #ffffff;
}

/* Stat Number */
.stat-number {
  font-family: 'Poppins', sans-serif;
  font-size: 2.75rem;
  font-weight: 700;
  line-height: 1;
  margin: 0; /* Ensures no default heading margin overflows */
}

/* Blue Card Theme */
.stat-card.blue {
  border: 2px solid #2b6cb0;
}
.stat-card.blue .card-header {
  background-color: #2b6cb0;
}
.stat-card.blue .stat-number {
  color: #1a365d;
}

/* Green Card Theme */
.stat-card.green {
  border: 2px solid #38a169;
}
.stat-card.green .card-header {
  background-color: #38a169;
}
.stat-card.green .stat-number {
  color: #2f855a;
}

/* Orange Card Theme */
.stat-card.orange {
  border: 2px solid #dd6b20;
}
.stat-card.orange .card-header {
  background-color: #dd6b20;
}
.stat-card.orange .stat-number {
  color: #dd6b20;
}

/* Red Card Theme */
.stat-card.red {
  border: 2px solid #dd3620;
}
.stat-card.red .card-header {
  background-color: #dd3620;
}
.stat-card.red .stat-number {
  color: #b52e1c;
}

/* Responsive breakpoint for small mobile screens */
@media (max-width: 640px) {
  .cards-grid {
    flex-direction: column;
  }
}
</style>