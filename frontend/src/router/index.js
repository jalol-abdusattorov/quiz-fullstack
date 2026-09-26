import { createRouter, createWebHistory } from 'vue-router'
import { isTokenExpired, useAuthStore } from '@/stores/auth'
import { useQuizzesStore } from '@/stores/QuizzesStore'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "Home",
      component: () => import('@/views/Home.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: "/register",
      name: "Register",
      component: () => import('@/views/Register.vue'),
      meta: { requiresGuest: true }
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
      path: "/api/admin-login",
      name: "AdminLogin",
      component: () => import('@/views/AdminLogin.vue'),
      meta: { showGlobalComponent: false }
    },
    {
      path: "/admin/dashboard",
      name: "AdminDashboard",
      component: () => import('@/views/AdminDashboard.vue'),
      meta: { requiresAuth: true, requiresAdmin: true, showGlobalComponent: false }
    },
    {
      path: "/quiz-management",
      name: "QuizManagement",
      component: () => import('@/views/QuizzesManagement.vue'),
      meta: { requiresAuth: true, requiresAdmin: true, showGlobalComponent: false }
    },
    {
      path: "/quiz-management/manage/:quizId",
      name: "ManageQuiz",
      component: () => import('@/views/ManageQuiz.vue'),
      meta: { requiresAuth: true, requiresAdmin: true, showGlobalComponent: false },
      props: true
    },
    {
      path: "/quizzes/:quizId/statistics",
      name: "QuizStatistics",
      component: () => import('@/views/QuizStatistics.vue'),
      meta: { requiresAuth: true, requiresAdmin: true, showGlobalComponent: false },
      props: true
    },
    {
      path: "/quizzes/edit-quiz/:quizId",
      name: "EditQuiz",
      component: () => import('@/views/EditQuiz.vue'),
      meta: { requiresAuth: true, requiresAdmin: true, showGlobalComponent: false },
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
