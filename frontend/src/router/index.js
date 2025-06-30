// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import AboutView from '../views/AboutView.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/about', name: 'About', component: AboutView },
  // /homeを削除し、/に統一
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
