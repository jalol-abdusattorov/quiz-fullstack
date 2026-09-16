import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/main.css'
import api from './api/axios.js'

const app = createApp(App)
app.use(router)

const pinia = createPinia()
pinia.use(({ store }) => {
    store.$api = api
})

app.use(pinia)
app.config.globalProperties.$api = api

app.mount('#app')