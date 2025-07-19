<script setup>
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

onMounted(() => {
  userStore.logout()
})
</script>

<template>
  <div class="p-8 max-w-xl mx-auto text-center">
    <h1 class="text-2xl font-bold mb-4">退会が完了しました</h1>
    <p class="text-gray-600 mb-6">ご利用ありがとうございました。</p>
    <router-link to="/" class="text-blue-600 hover:underline">ホームに戻る</router-link>
  </div>
</template>
