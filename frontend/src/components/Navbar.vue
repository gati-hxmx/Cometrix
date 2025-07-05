<template>
  <nav class="w-full bg-white border-b border-gray-200 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16 items-center">
        <!-- 左: ロゴ -->
        <div class="flex-shrink-0 text-blue-600 text-2xl font-semibold">
          <RouterLink to="/" class="hover:text-blue-800">
            <img src="/brand_logo(favicon).png" alt="Cometrix Logo" class="inline-block h-10 mr-2">
            Cometrix
          </RouterLink>
        </div>

        <!-- 右: ナビゲーションリンク -->
        <div class="flex items-center space-x-6 text-gray-700">
          <RouterLink to="/about" class="hover:text-blue-600">Cometrixについて</RouterLink>
          <RouterLink to="/analyze" class="hover:text-blue-600">分析画面</RouterLink>
          <RouterLink
            v-if="!isLoggedIn"
            to="/login"
            class="text-blue-500 px-4 py-2  text-m transition duration-200 flex items-center gap-2"
          >
            <LogIn class="w-4 h-4" />
            ログイン
          </RouterLink>




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

        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { LogIn } from 'lucide-vue-next'

const router = useRouter()
const userStore = useUserStore()

const isLoggedIn = computed(() => userStore.name !== null)
const name = computed(() => userStore.name)

function logout() {
  userStore.logout()
  router.push('/')
}
</script>
