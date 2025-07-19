<script setup>
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import { useUserStore } from '@/stores/user'
import { computed, watchEffect } from 'vue'

const userStore = useUserStore()

const name = computed(() => userStore.name)
const email = computed(() => userStore.email)
const subscription = computed(() => userStore.subscription)

watchEffect(async () => {
  if (email.value) {
    await userStore.fetchSubscription()
  }
})

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('ja-JP', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

async function handleUpgrade() {
  try {
    const res = await fetch("http://localhost:5001/create-checkout-session", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email: email.value })
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

async function handleCancel() {
  if (!confirm("本当に解約しますか？")) return

  try {
    const res = await fetch("http://localhost:5001/cancel-subscription", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email: email.value })
    })
    const data = await res.json()
    alert(data.message || "キャンセル処理を完了しました")

    await userStore.fetchSubscription()
  } catch (error) {
    console.error("キャンセルエラー:", error)
    alert("通信エラーが発生しました")
  }
}

async function handleUncancel() {
  if (!confirm("解約をキャンセルしますか？")) return

  try {
    const res = await fetch("http://localhost:5001/uncancel-subscription", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email: email.value })
    })
    const data = await res.json()
    alert(data.message || "解約キャンセル処理を完了しました")

    await userStore.fetchSubscription()
  } catch (error) {
    console.error("解約キャンセルエラー:", error)
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
          <div>
            <p class="font-medium">{{ name }}</p>
            <p class="text-sm text-gray-500">{{ email }}</p>
          </div>
        </div>

        <div v-else class="text-gray-400 text-sm">ユーザー情報が取得できませんでした</div>
      </div>

      <div class="bg-white border rounded p-4 shadow-sm">
        <h2 class="font-semibold text-gray-700 mb-2">サブスクリプション</h2>

        <div v-if="subscription">
          <p class="mb-1">プラン: <strong>{{ subscription.plan }}</strong></p>
          <p class="text-sm text-gray-500 mb-4">状態: {{ subscription.status }}</p>

          <button
            v-if="subscription.status !== 'active' && subscription.status !== 'canceling'"
            @click="handleUpgrade"
            class="bg-blue-600 hover:bg-blue-700 text-white text-sm px-4 py-2 rounded mr-2"
          >
            アップグレードする
          </button>

          <button
            v-if="subscription.status === 'active' || subscription.status === 'trialing'"
            @click="handleCancel"
            class="bg-gray-600 hover:bg-gray-700 text-white text-sm px-4 py-2 rounded"
          >
            解約する
          </button>

          <p v-if="subscription.status === 'canceling'" class="text-sm text-orange-500">
            解約予定（{{ formatDate(subscription.end_date) }}まで利用可能）
          </p>

          <button
            v-if="subscription.status === 'canceling'"
            @click="handleUncancel"
            class="bg-gray-600 hover:bg-gray-700 text-white text-sm px-4 py-2 rounded"
          >
            解約をキャンセルする
          </button>




          <p v-if="subscription.status === 'canceled'" class="text-sm text-red-500">
            解約済み（{{ formatDate(subscription.end_date) }}まで利用可能）
          </p>
        </div>

        <div v-else class="text-sm text-gray-500">サブスクリプション情報を取得中...</div>
      </div>

      <div class="mt-8 text-center">
  <router-link to="/delete-account" class="text-sm text-red-600 hover:underline">
    アカウントを退会する
  </router-link>
</div>
    </main>
  </DefaultLayout>
</template>
