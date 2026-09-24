import { createRouter, createWebHistory } from 'vue-router'
import { isTokenExpired, useAuthStore } from '@/stores/auth'
import { useQuizzesStore } from '@/stores/QuizzesStore'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/register",
      name: "Register",
      // Normal loading:
      // component: Register,
      // Lazy loading:
      component: () => import('@/views/Register.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: "/",
      name: "Home",
      component: () => import('@/views/Home.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: "/login",
      name: "Login",
      component: () => import('@/views/Login.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: "/logout",
      name: "Logout",
      component: () => import('@/views/Logout.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: "/quizzes",
      name: "Quizzes",
      component: () => import('@/views/Quizzes.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: "/quiz/:id",
      name: "QuizDetails",
      component: () => import('@/views/QuizDetails.vue'),
      meta: { requiresAuth: true },
      props: true
    },
    {
      path: "/quizzes/browse",
      name: "QuizBrowser",
      component: () => import('@/views/QuizBrowser.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: "/quizzes/start-quiz/:id/:attemptId",
      name: "TakingQuiz",
      component: () => import('@/views/TakingQuiz.vue'),
      meta: { requiresAuth: true },
      props: true
    },
    {
      path: "/quizzes/submit-quiz/:id",
      name: "Results",
      component: () => import('@/views/Results.vue'),
      beforeEnter: () => {
        const quiz = useQuizzesStore()

        if (!quiz.result) {
          return { name: 'Home', replace: true }
        }
      },
      meta: { requiresAuth: true }
    },
    {
      path: "/quizzes/review-answers",
      name: "ReviewAnswers",
      component: () => import('@/views/ReviewAnswers.vue'),
      beforeEnter: () => {
        const quiz = useQuizzesStore()

        if (!quiz.result) {
          return { name: 'Home', replace: true }
        }
      },
      meta: { requiresAuth: true }
    },
    {
      path: "/profile",
      name: "UserProfile",
      component: () => import('@/views/UserProfile.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: "/attempts/history",
      name: "UserAttempts",
      component: () => import('@/views/UserAttempts.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: "/leaderboard/:quizId",
      name: "Leaderboard",
      component: () => import('@/views/Leaderboard.vue'),
      meta: { requiresAuth: true },
      props: true
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('@/views/NotFound.vue'),
    }
  ],
})

router.beforeEach((to, from) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth) {
    if (!authStore.token || isTokenExpired(authStore.token)) {
      authStore.logout()
      return { name: 'Login' }
    }
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: "Login" }
  }

  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    return { name: "Login" }
  }

  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    return { name: "Home" }
  }

  return true
})

export default router
