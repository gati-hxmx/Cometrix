<script setup>
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import { useUserStore } from '@/stores/user'
import { computed } from 'vue'

const userStore = useUserStore()

// userStore.user が null でない場合のみ name, email にアクセス
const name = computed(() => userStore.name)
const email = computed(() => userStore.email)

const subscription = {
  plan: 'Free Plan',
  status: '未加入'
}
</script>

<template>
  <DefaultLayout>
    <main class="p-8 max-w-xl mx-auto">
      <h1 class="text-xl font-bold mb-6">マイページ</h1>

      <div class="bg-white border rounded p-4 shadow-sm mb-6">
        <h2 class="font-semibold text-gray-700 mb-2">ユーザー情報</h2>

        <div v-if="name" class="flex items-center gap-4">
          <!-- <img :src="userStore.picture" class="w-12 h-12 rounded-full" alt="User Icon" /> -->
          <div>
            <p class="font-medium">{{ name }}</p>
            <p class="text-sm text-gray-500">{{ email }}</p>
          </div>
        </div>

        <div v-else class="text-gray-400 text-sm">ユーザー情報が取得できませんでした</div>

      </div>

      <div class="bg-white border rounded p-4 shadow-sm">
        <h2 class="font-semibold text-gray-700 mb-2">サブスクリプション</h2>
        <p class="mb-1">プラン: <strong>{{ subscription.plan }}</strong></p>
        <p class="text-sm text-gray-500">状態: {{ subscription.status }}</p>
      </div>
    </main>
  </DefaultLayout>
</template>
