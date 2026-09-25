<template>
    <div>
        <!-- ADMIN -->
        <header class="navbar" v-if="isAdmin">
            <router-link :to="{ name: 'Home' }" class="brand">Quiz</router-link>
            <nav class="router-links">
                <router-link class="nav-btn" :to="{ name: 'AdminDashboard' }">Dashboard</router-link>
            </nav>
        </header>
    </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth';
import { storeToRefs } from 'pinia';
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';

    export default {
        name: "AppHeader",
        setup() {
            const authStore = useAuthStore()
            const { isAdmin } = storeToRefs(authStore)
            const router = useRouter()

            const ToProfilePage = () => {
              router.push({ name: 'UserProfile' })
            }
            onMounted(() => {
                if (!authStore.isAdmin) {
                    router.replace({ name: "Login" })
                }
            })

            return { ToProfilePage, isAdmin }
        }
    }
</script>


<style scoped>
.profile-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  vertical-align: middle;
  margin-left: 15px;
  transition: 0.2s ease;
  cursor: pointer;
}
.profile-icon:hover {
  transform: translateY(-1px);
}

.navbar {
  background-color: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 2px rgba(0, 0, 0, 0.137);
}

.brand {
  font-size: 1.25rem;
  font-weight: 700;
  color: #4f46e5;
  text-decoration: none;
  margin-right: auto;
}

.nav-links {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.nav-btn {
  background: none;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #64748b;
  text-decoration: none;
  transition: all 0.2s ease;
  display: inline-block;
}

.nav-btn:hover {
  background-color: #f1f5f9;
  color: #0f172a;
}

/* Styled active state for current page using exact active class */
.nav-btn.router-link-exact-active {
  background-color: #e0e7ff;
  color: #4f46e5;
  font-weight: 600;
}

/* Hover style for Logout link */
.nav-btn.logout:hover {
  background-color: #fef2f2;
  color: #ef4444;
}

/* Optional: custom active style when sitting on the /logout route */
.nav-btn.logout.router-link-exact-active {
  background-color: #fef2f2;
  color: #ef4444;
}
</style>