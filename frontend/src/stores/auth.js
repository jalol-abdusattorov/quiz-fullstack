import { jwtDecode } from 'jwt-decode';
import axios from 'axios'
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

function parseJwt(token) {
    try {
        const base64Url = token.split('.')[1]
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
        const jsonPayload = decodeURIComponent(
            atob(base64)
                .split('')
                .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
                .join('')
        )
        return JSON.parse(jsonPayload)
    } catch (e) {
        return null
    }
}

export function isTokenExpired(token) {
  if (!token) return true;

  try {
    const decoded = jwtDecode(token);
    const currentTime = Date.now() / 1000;

    return decoded.exp < currentTime;
  } catch (error) {
    return true;
  }
}

export const useAuthStore = defineStore('auth', () => {
    const user = ref(JSON.parse(localStorage.getItem('user')) || null)
    const token = ref(localStorage.getItem('token') || null)
    const loading = ref(false)
    const error = ref(null)

    const isAuthenticated = computed(() => !!user.value && !!token.value)

    const isAdmin = computed(() => {
        if (!token.value) {
            return false
        }
        // Decode the JWT using paseJWT helper function
        const decoded = parseJwt(token.value)
        return decoded?.admin || user.value?.admin || false
    })

    function setAuthData(userData, tokenValue) {
        user.value = userData
        token.value = tokenValue

        localStorage.setItem('user', JSON.stringify(userData))
        localStorage.setItem('token', tokenValue)
    }

    const register = async (credentials) => {
        loading.value = true
        error.value = null

        try {
            const response = await axios.post('http://localhost:8000/users', credentials)
            const data = response.data

            const tokenValue = data.token

            if (data.id && tokenValue) {
                const userData = { id: data.id, email: credentials.email }
                setAuthData(userData, tokenValue)
            }

            return data
        } catch (exc) {
            error.value =
                err.response?.data?.detail ||
                err.response?.data?.message ||
                'Registration failed'
            throw err
        } finally {
            loading.value = false
        }
    }

    const login = async (credentials) => {
        loading.value = true
        error.value = null

        try {
            const formData = new URLSearchParams()
            formData.append('username', credentials.email)
            formData.append('password', credentials.password)

            const response = await axios.post('http://localhost:8000/api/auth/login', formData, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            })

            const data = response.data

            const tokenValue = data.token.access_token  // || data.access_token
            const userId = data.id

            const userData = { id: userId, email: credentials.email }

            setAuthData(userData, tokenValue)

            return userData
        } catch (err) {
            error.value =
                err.response?.data?.detail ||
                err.response?.data?.message ||
                'Invalid email or password'
            throw err
        } finally {
            loading.value = false
        }
    }

    function logout() {
        user.value = null
        token.value = null
        error.value = null

        localStorage.removeItem('user')
        localStorage.removeItem('token')
    }

    return { user, token, loading, error, isAuthenticated, isAdmin, register, login, logout }
})