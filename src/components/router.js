import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/home.vue'
import Member from '@/views/Member.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/member/:id',
    name: 'Member',
    component: Member,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router