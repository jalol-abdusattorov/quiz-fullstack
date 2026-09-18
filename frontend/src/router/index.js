import { createRouter, createWebHistory } from 'vue-router'
import Register from '@/views/Register.vue'
import Home from '@/views/Home.vue'
import Login from '@/views/Login.vue'
import Logout from '@/views/Logout.vue'
import Quizzes from '@/views/Quizzes.vue'
import { useAuthStore } from '@/stores/auth'
import NotFound from '@/views/NotFound.vue'
import QuizDetails from '@/views/QuizDetails.vue'
import QuizBrowser from '@/views/QuizBrowser.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/register",
      name: "Register",
      component: Register,
      meta: { requiresGuest: true }
    },
    {
      path: "/",
      name: "Home",
      component: Home,
      meta: { requiresAuth: true }
    },
    {
      path: "/login",
      name: "Login",
      component: Login,
      meta: { requiresGuest: true }
    },
    {
      path: "/logout",
      name: "Logout",
      component: Logout,
      meta: { requiresAuth: true }
    },
    {
      path: "/quizzes",
      name: "Quizzes",
      component: Quizzes,
      meta: { requiresAuth: true }
    },
    {
      path: "/quiz/:id",
      name: "QuizDetails",
      component: QuizDetails,
      meta: { requiresAuth: true },
      props: true
    },
    {
      path: "/quizzes/browse",
      name: "QuizBrowser",
      component: QuizBrowser,
      meta: { requiresAuth: true }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: NotFound
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
