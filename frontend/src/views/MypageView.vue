<script setup>
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import { useUserStore } from '@/stores/user'
import { computed, ref, onMounted } from 'vue'

const userStore = useUserStore()
const name = computed(() => userStore.name)
const email = computed(() => userStore.email)

// ← ココを ref にする（リアルタイム更新用）
const subscription = ref({
  plan: 'Free Plan',
  status: '読み込み中...'
})

// ✅ onMountedでサブスク情報をサーバーから取得
onMounted(async () => {
  try {
    const res = await fetch('http://localhost:5001/api/subscription', {
      credentials: 'include'
    })
    const data = await res.json()
    subscription.value = {
      plan: data.plan,
      status: data.status
    }
  } catch (err) {
    console.error('取得エラー', err)
    subscription.value = {
      plan: 'Free Plan',
      status: '取得失敗'
    }
  }
})

async function handleUpgrade() {
  try {
    const res = await fetch("http://localhost:5001/create-checkout-session", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email: email.value })  // ← メール送信！
    })
    const data = await res.json()
    if (data.url) {
      window.location.href = data.url
    } else {
      alert("セッションURLが取得できませんでした")
    }
  } catch (error) {
    console.error("Checkoutエラー:", error)
    alert("通信エラーが発生しました")
  }
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
        <p class="text-sm text-gray-500 mb-4">状態: {{ subscription.status }}</p>

        <button
          @click="handleUpgrade"
          class="bg-blue-600 hover:bg-blue-700 text-white text-sm px-4 py-2 rounded"
        >
          アップグレードする
        </button>
      </div>

    </main>
  </DefaultLayout>
</template>
