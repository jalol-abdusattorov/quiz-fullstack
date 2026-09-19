import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

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
      path: "/quizzes/start-quiz/:id",
      name: "TakingQuiz",
      component: () => import('@/views/TakingQuiz.vue'),
      meta: { requiresAuth: true },
      props: true
    },
        {
      path: "/quizzes/submit-quiz/:id",
      name: "Results",
      component: () => import('@/views/Results.vue'),
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
