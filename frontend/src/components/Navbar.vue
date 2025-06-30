<!-- frontend/src/components/Navbar.vue -->
<template>
  <nav class="bg-gray-800 text-white p-4 flex justify-between items-center">
    <div class="text-xl font-bold">Cometrix</div>
    <div class="space-x-4">
      <RouterLink to="/" class="hover:underline">Home</RouterLink>
      <RouterLink to="/about" class="hover:underline">About</RouterLink>
      <RouterLink v-if="!isLoggedIn" to="/login" class="hover:underline">Login</RouterLink>

      <template v-if="isLoggedIn">
        <span class="ml-2">{{ name }} </span>
        <button
          @click="logout"
          class="ml-4 bg-red-500 hover:bg-red-600 px-3 py-1 rounded"
        >
          ログアウト
        </button>
      </template>
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
