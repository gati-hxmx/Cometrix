import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
import AboutView from "../views/AboutView.vue";
import AnalyzeView from "../views/AnalyzeView.vue";
import MypageView from "../views/MypageView.vue";
import Leagal from "../views/Leagal.vue";
import PrivacyPolicy from "../views/PrivacyPolicy.vue";
import BillingSuccess from "@/views/billing/BillingSuccess.vue";
import BillingCancel from "@/views/billing/BillingCancel.vue";
import DeleteAccount from "@/views/account/DeleteAccount.vue";
import GoodbyeComplete from "@/views/account/GoodbyeComplete.vue";
import LiveAnalyze from "@/views/LiveAnalyze.vue";
import Subscriptions from "@/views/Subscriptions.vue";
import AnalyzeHistory from "@/views/AnalyzeHistory.vue";
import BillingHistory from "@/views/billing/BillingHistory.vue";
import NotFound from "@/views/NotFound.vue";

const routes = [
  { path: "/", name: "Home", component: HomeView },
  { path: "/login", name: "Login", component: LoginView },
  { path: "/about", name: "About", component: AboutView },
  { path: "/analyze", name: "Analyze", component: AnalyzeView },
  { path: "/mypage", name: "Mypage", component: MypageView },
  { path: "/leagal", name: "Leagal", component: Leagal },
  { path: "/privacypolicy", name: "PrivacyPolicy", component: PrivacyPolicy },
  {
    path: "/billingsuccess",
    name: "BillingSuccess",
    component: BillingSuccess,
  },
  { path: "/billingcancel", name: "BillingCancel", component: BillingCancel },
  { path: "/delete-account", name: "DeleteAccount", component: DeleteAccount },
  {
    path: "/goodbye-complete",
    name: "GoodbyeComplete",
    component: GoodbyeComplete,
  },
  { path: "/live-analyze", name: "LiveAnalyze", component: LiveAnalyze },
  { path: "/subscriptions", name: "Subscriptions", component: Subscriptions },
  { path: "/history", name: "AnalyzeHistory", component: AnalyzeHistory },
  {
    path: "/billing/history",
    name: "BillingHistory",
    component: BillingHistory,
  },
  { path: "/:pathMatch(.*)*", name: "NotFound", component: NotFound },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

const protectedRoutes = ["/analyze", "/mypage"];

router.beforeEach(async (to, from, next) => {
  // ✨ Pinia store を setup 内で初期化する
  const { useUserStore } = await import("@/stores/user");
  const userStore = useUserStore();

  if (protectedRoutes.includes(to.path)) {
    if (!userStore.email) {
      await userStore.fetchUser();
    }

    if (!userStore.subscription) {
      await userStore.fetchSubscription();
    }

    if (userStore.subscription === null) {
      return next("/login");
    }
  }

  return next();
});

export default router;
