// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import AboutView from '../views/AboutView.vue'
import AnalyzeView from '../views/AnalyzeView.vue'
import MypageView from '../views/MypageView.vue'
import TestChart from '../views/TestChart.vue'
import Leagal from '../views/Leagal.vue'
import PrivacyPolicy from '@/views/PrivacyPolicy.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/about', name: 'About', component: AboutView },
  { path: '/analyze',name: 'Analyze', component: AnalyzeView},
  { path: '/mypage', name: 'Maypage', component: MypageView },
  { path: '/test', name: 'TestChart', component: TestChart },
  { path: '/leagal', name: 'Leagal', component: Leagal },
  { path: '/privacypolicy', name: 'PrivacyPolicy', component: PrivacyPolicy }
  
  
  // /homeを削除し、/に統一
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
