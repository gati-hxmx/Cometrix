import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import AboutView from '../views/AboutView.vue'
import AnalyzeView from '../views/AnalyzeView.vue'
import MypageView from '../views/MypageView.vue'
import TestChart from '../views/TestChart.vue'
import Leagal from '../views/Leagal.vue'
import PrivacyPolicy from '@/views/PrivacyPolicy.vue'
import BillingSuccess from '@/views/billing/BillingSuccess.vue'
import BillingCancel from '@/views/billing/BillingCancel.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/about', name: 'About', component: AboutView },
  { path: '/analyze', name: 'Analyze', component: AnalyzeView },
  { path: '/mypage', name: 'Mypage', component: MypageView },
  { path: '/test', name: 'TestChart', component: TestChart },
  { path: '/leagal', name: 'Leagal', component: Leagal },
  { path: '/privacypolicy', name: 'PrivacyPolicy', component: PrivacyPolicy },
  { path: '/billingsuccess', name: 'BillingSuccess', component: BillingSuccess },
  { path: '/billingcancel', name: 'BillingCancel', component: BillingCancel }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

const protectedRoutes = ['/analyze', '/mypage']

router.beforeEach(async (to, from, next) => {
  // ✨ Pinia store を setup 内で初期化する
  const { useUserStore } = await import('@/stores/user')
  const userStore = useUserStore()

  if (protectedRoutes.includes(to.path)) {
    if (!userStore.email) {
      await userStore.fetchUser()
    }

    if (!userStore.subscription) {
      await userStore.fetchSubscription()
    }

    if (userStore.subscription === null) {
      return next('/login')
    }
  }

  return next()
})

export default router
