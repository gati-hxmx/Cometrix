<template>
  <div>
    <!-- ナビゲーションバー -->
    <nav
      class="fixed top-0 left-0 right-0 bg-white border-b border-gray-200 shadow-sm z-50 h-16"
    >
      <div
        class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between h-full items-center"
      >
        <!-- 左: ハンバーガー + ロゴ -->
        <div class="flex items-center space-x-4">
          <!-- ハンバーガーメニュー -->
          <button
            v-if="isLoggedIn"
            @click.stop="toggleMenu"
            class="text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded p-1"
          >
            <Menu class="w-6 h-6" />
          </button>

          <RouterLink
            to="/"
            class="text-blue-600 text-2xl font-semibold hover:text-blue-800 flex items-center"
          >
            <img
              src="/brand_logo(favicon).png"
              alt="Cometrix Logo"
              class="h-10 mr-2"
            />
            Cometrix
          </RouterLink>
        </div>

        <!-- 中央: 検索フォーム -->
        <div class="flex-1 px-8">
          <form
            @submit.prevent="goToAnalysis"
            class="max-w-xl mx-auto flex items-center bg-white border border-gray-300 rounded-full shadow-sm overflow-hidden"
          >
            <input
              v-model="videoUrl"
              type="text"
              placeholder="YouTubeまたはTwitchのURLを入力"
              class="flex-1 px-4 py-2 text-sm focus:outline-none border-none"
            />
            <button
              type="submit"
              class="bg-gray-100 hover:bg-gray-200 px-4 py-2"
            >
              <Search class="w-5 h-5 text-gray-600" />
            </button>
          </form>
        </div>

        <!-- 右: 通常リンク -->
        <div class="flex items-center space-x-6 text-gray-700">
          <template v-if="isLoggedIn">
            <RouterLink
              to="/mypage"
              class="text-sm font-medium text-blue-600 hover:underline"
            >
              {{ name }}
            </RouterLink>
            <button
              @click="logout"
              class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded"
            >
              ログアウト
            </button>
          </template>

          <RouterLink
            v-else
            to="/login"
            class="text-blue-500 px-4 py-2 flex items-center gap-2"
          >
            <LogIn class="w-4 h-4" />
            ログイン
          </RouterLink>
        </div>
      </div>
    </nav>

    <!-- サイドメニュー -->
    <transition name="slide">
      <aside
        v-if="menuOpen && isLoggedIn"
        ref="sidebarRef"
        class="fixed top-16 left-0 h-full w-55 bg-white shadow-md z-40 border-r border-gray-200 px-4 py-4 space-y-4"
      >
        <div class="space-y-2">
          <RouterLink
            to="/"
            class="flex items-center space-x-3 px-3 py-2 rounded hover:bg-gray-100"
            :class="{ 'bg-gray-100': $route.path === '/' }"
          >
            <Home class="w-5 h-5" />
            <span>ホーム</span>
          </RouterLink>

          <RouterLink
            to="/analyze"
            class="flex items-center space-x-3 px-3 py-2 rounded hover:bg-gray-100"
            :class="{ 'bg-gray-100': $route.path === '/analyze' }"
          >
            <BarChart class="w-5 h-5" />
            <span>アーカイブ分析</span>
          </RouterLink>

          <RouterLink
            to="/live-analyze"
            class="flex items-center space-x-3 px-3 py-2 rounded hover:bg-gray-100"
            :class="{ 'bg-gray-100': $route.path === '/live-analyze' }"
          >
            <Zap class="w-5 h-5" />
            <span>LIVE分析</span>
          </RouterLink>

          <RouterLink
            to="/subscriptions"
            class="flex items-center space-x-3 px-3 py-2 rounded hover:bg-gray-100"
            :class="{ 'bg-gray-100': $route.path === '/subscriptions' }"
          >
            <Tv class="w-5 h-5" />
            <span>登録チャンネル</span>
          </RouterLink>

          <RouterLink
            to="/history"
            class="flex items-center space-x-3 px-3 py-2 rounded hover:bg-gray-100"
            :class="{ 'bg-gray-100': $route.path === '/history' }"
          >
            <Clock class="w-5 h-5" />
            <span>履歴</span>
          </RouterLink>

          <RouterLink
            to="/mypage"
            class="flex items-center space-x-3 px-3 py-2 rounded hover:bg-gray-100"
            :class="{ 'bg-gray-100': $route.path === '/mypage' }"
          >
            <User class="w-5 h-5" />
            <span>マイページ</span>
          </RouterLink>
        </div>
      </aside>
    </transition>

    <!-- 下のコンテンツ -->
    <main class="pt-16">
      <slot />
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter, useRoute, RouterLink } from "vue-router";
import { useUserStore } from "@/stores/user";
import {
  LogIn,
  Menu,
  Home,
  Tv,
  User,
  Clock,
  BarChart,
  Zap,
} from "lucide-vue-next";

const router = useRouter();
const route = useRoute();
const userStore = useUserStore();

const isLoggedIn = computed(() => userStore.name !== null);
const name = computed(() => userStore.name);
const menuOpen = ref(false);

function toggleMenu() {
  menuOpen.value = !menuOpen.value;
}

function logout() {
  userStore.logout();
  router.push("/");
}

import { onMounted, onBeforeUnmount } from "vue";

const sidebarRef = ref(null);

function handleClickOutside(event) {
  if (
    menuOpen.value &&
    sidebarRef.value &&
    !sidebarRef.value.contains(event.target)
  ) {
    menuOpen.value = false;
  }
}

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
});

onBeforeUnmount(() => {
  document.removeEventListener("click", handleClickOutside);
});

import { Search } from "lucide-vue-next";

const videoUrl = ref("");

function goToAnalysis() {
  if (videoUrl.value.trim()) {
    router.push({ path: "/analyze", query: { video: videoUrl.value.trim() } });
    videoUrl.value = "";
  }
}
</script>

<style scoped>
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}
.slide-enter-from {
  transform: translateX(-100%);
}
.slide-enter-to {
  transform: translateX(0%);
}
.slide-leave-from {
  transform: translateX(0%);
}
.slide-leave-to {
  transform: translateX(-100%);
}
</style>
