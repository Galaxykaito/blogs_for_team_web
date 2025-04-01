// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './components/router.js' // 确保导入了router

const app = createApp(App)
app.use(router) // 必须注册路由
app.mount('#app')
