<template>
  <div class="logout-page">
    <div class="logout-card">
      <!-- Warning / Exit Icon -->
      <div class="icon-wrapper">
        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor"
        stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
          <polyline points="16 17 21 12 16 7" />
          <line x1="21" y1="12" x2="9" y2="12" />
        </svg>
      </div>

      <h2 class="logout-title">Log out of your account?</h2>
      <p class="logout-subtitle">
        You will need to enter your credentials again to log back into your dashboard.
      </p>

      <div class="logout-actions">
        <button class="btn btn-confirm" @click="handleLogout">
          Yes, Log me out
        </button>
        <button class="btn btn-cancel" @click="handleCancel">
          Stay logged in
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const handleCancel = () => {
  router.back()
}
</script>

<style scoped>
/* Page container - positions card slightly higher than vertical center */
.logout-page {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding-top: 14vh;
  min-height: calc(100vh - 80px); /* Adjust based on navbar height */
  box-sizing: border-box;
}

/* Central Card */
.logout-card {
  background-color: #ffffff;
  border: 1px solid #e5e7eb;
  padding: 36px 32px;
  border-radius: 16px;
  box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.05);
  max-width: 420px;
  width: 100%;
  text-align: center;
}

/* Soft red icon circle */
.icon-wrapper {
  width: 64px;
  height: 64px;
  background-color: #fef2f2;
  color: #ef4444;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px auto;
}

.logout-title {
  margin: 0 0 8px 0;
  font-family: system-ui, -apple-system, sans-serif;
  font-size: 1.35rem;
  font-weight: 600;
  color: #111827;
}

.logout-subtitle {
  margin: 0 0 28px 0;
  font-size: 0.95rem;
  color: #6b7280;
  line-height: 1.5;
}

/* Stacked action buttons on separate lines for clean hierarchy */
.logout-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.btn {
  width: 100%;
  padding: 12px;
  border-radius: 10px;
  font-size: 0.95rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn:active {
  transform: scale(0.99);
}

/* Primary Destructive Action */
.btn-confirm {
  background-color: #ef4444;
  color: #ffffff;
}
.btn-confirm:hover {
  background-color: #dc2626;
}

/* Secondary Cancel Action */
.btn-cancel {
  background-color: #f3f4f6;
  color: #374151;
}
.btn-cancel:hover {
  background-color: #e5e7eb;
}
</style>