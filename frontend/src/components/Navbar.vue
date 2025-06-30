<template>
  <nav class="w-full bg-white border-b border-gray-200 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16 items-center">
        <!-- 左: ロゴ -->
        <div class="flex-shrink-0 text-blue-600 text-2xl font-semibold">
          <RouterLink to="/" class="hover:text-blue-800">
            Cometrix
          </RouterLink>
        </div>

        <!-- 右: ナビゲーションリンク -->
        <div class="flex items-center space-x-6 text-gray-700">
          <RouterLink to="/" class="hover:text-blue-600">Home</RouterLink>
          <RouterLink to="/about" class="hover:text-blue-600">About</RouterLink>
          <RouterLink
            v-if="!isLoggedIn"
            to="/login"
            class="hover:text-blue-600"
          >
            Login
          </RouterLink>

          <template v-if="isLoggedIn">
            <span class="text-sm font-medium text-gray-600">
              {{ name }}
            </span>
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

const router = useRouter()
const userStore = useUserStore()

const isLoggedIn = computed(() => userStore.name !== null)
const name = computed(() => userStore.name)

function logout() {
  userStore.logout()
  router.push('/')
}
</script>
