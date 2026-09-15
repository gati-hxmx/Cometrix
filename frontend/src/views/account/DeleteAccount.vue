<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import { ANALYZE_API_BASE } from '@/config/api'


const router = useRouter()
const userStore = useUserStore()

async function handleDelete() {
  const confirmed = confirm("本当にアカウントを削除してもよろしいですか？この操作は取り消せません。")
  if (!confirmed) return

  try {
    const res = await fetch(`${ANALYZE_API_BASE}/api/delete-account`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email: userStore.email })
    })

    if (!res.ok) {
      const error = await res.json()
      alert(error.detail || "削除に失敗しました")
      return
    }

    alert("アカウントを削除しました。ご利用ありがとうございました。")
    router.push("/goodbye-complete") // → 次ステップで実装予定
  } catch (e) {
    console.error("削除リクエスト失敗:", e)
    alert("通信エラーが発生しました")
  }
}
</script>

<template>
<DefaultLayout>
  
  <div class="max-w-lg mx-auto p-8">
    <h1 class="text-xl font-bold mb-6 text-red-600">アカウント退会の確認</h1>

    <p class="mb-4 text-gray-700">
      退会すると、すべての保存データが完全に削除され、復元はできません。Stripeの契約も同時に解約されます。
    </p>

    <p class="mb-6 text-gray-600 text-sm">
      以下のボタンを押すと、アカウント削除が即時に実行されます。
    </p>

    <button
      @click="handleDelete"
      class="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
    >
      アカウントを削除する
    </button>
  </div>
</DefaultLayout>
</template>
