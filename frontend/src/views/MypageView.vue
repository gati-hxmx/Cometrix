<template>
  <DefaultLayout>
    <main class="p-6 max-w-3xl mx-auto">
      <h1 class="text-2xl font-bold mb-6">マイページ</h1>

      <!-- ユーザー情報 -->
      <div class="bg-white shadow-md rounded-lg p-5 mb-6 border">
        <div class="flex items-center gap-4">
          <div class="flex-shrink-0 bg-blue-100 text-blue-600 p-3 rounded-full">
            <i class="i-lucide-user w-6 h-6"></i>
          </div>
          <div>
            <p class="text-lg font-semibold">{{ name }}</p>
            <p class="text-sm text-gray-500">{{ email }}</p>
          </div>
        </div>
      </div>

      <!-- サブスク情報 -->
      <div class="bg-white shadow-md rounded-lg p-5 mb-6 border">
        <div class="flex items-center gap-4 mb-4">
          <div
            class="flex-shrink-0 bg-green-100 text-green-600 p-3 rounded-full"
          >
            <i class="i-lucide-credit-card w-6 h-6"></i>
          </div>
          <div>
            <h2 class="text-lg font-semibold">サブスクリプション</h2>
          </div>
        </div>

        <div v-if="subscription">
          <div class="mb-2">
            <p>
              プラン: <span class="font-medium">{{ subscription.plan }}</span>
            </p>
            <p class="text-sm text-gray-500">
              状態:
              <span :class="statusClass(subscription.status)">
                {{ statusLabel(subscription.status) }}
              </span>
            </p>
          </div>

          <!-- ボタン -->
          <div class="mt-4 flex flex-wrap gap-3">
            <button
              v-if="['inactive', 'canceled'].includes(subscription.status)"
              @click="handleUpgrade"
              class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
            >
              アップグレードする
            </button>

            <button
              v-if="['active', 'trialing'].includes(subscription.status)"
              @click="handleCancel"
              class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded"
            >
              解約する
            </button>

            <button
              v-if="subscription.status === 'canceling'"
              @click="handleUncancel"
              class="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded"
            >
              解約をキャンセルする
            </button>
          </div>

          <!-- 解約予定など -->
          <p
            v-if="subscription.status === 'canceling'"
            class="text-sm text-orange-500 mt-4"
          >
            解約予定（{{ formatDate(subscription.end_date) }}まで利用可能）
          </p>
          <p
            v-if="subscription.status === 'canceled'"
            class="text-sm text-red-500 mt-4"
          >
            解約済み（{{ formatDate(subscription.end_date) }}まで利用可能）
          </p>

          <!-- 請求履歴リンク -->
          <router-link
            v-if="['active', 'trialing'].includes(subscription.status)"
            to="/billing/history"
            class="text-sm text-blue-600 hover:underline mt-6 inline-block"
          >
            請求履歴を見る →
          </router-link>
        </div>

        <div v-else class="text-sm text-gray-500">
          サブスクリプション情報を取得中...
        </div>
      </div>

      <!-- 退会 -->
      <div class="text-center mt-8">
        <router-link
          to="/delete-account"
          class="text-sm text-red-600 hover:underline"
        >
          アカウントを退会する
        </router-link>
      </div>
    </main>
  </DefaultLayout>
</template>

<script setup>
import DefaultLayout from "@/layouts/DefaultLayout.vue";
import { useUserStore } from "@/stores/user";
import { computed, watchEffect } from "vue";
import { STRIPE_API_BASE } from "@/config/api";

const userStore = useUserStore();
const name = computed(() => userStore.name);
const email = computed(() => userStore.email);
const subscription = computed(() => userStore.subscription);

watchEffect(async () => {
  if (email.value) {
    await userStore.fetchSubscription();
  }
});

function formatDate(dateStr) {
  const date = new Date(dateStr);
  return date.toLocaleDateString("ja-JP", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

function statusClass(status) {
  return (
    {
      active: "text-green-600 font-semibold",
      trialing: "text-indigo-600 font-semibold",
      canceling: "text-orange-600 font-semibold",
      canceled: "text-red-500 font-semibold",
      inactive: "text-gray-500 font-semibold",
    }[status] || "text-gray-500"
  );
}

function statusLabel(status) {
  return (
    {
      active: "アクティブ",
      trialing: "トライアル中",
      canceling: "解約予定",
      canceled: "解約済み",
      inactive: "未契約",
    }[status] || status
  );
}

async function handleUpgrade() {
  try {
    const res = await fetch(`${STRIPE_API_BASE}/create-checkout-session`, {
      method: "POST",
      credentials: "include",
    });
    const data = await res.json();
    if (data.url) window.location.href = data.url;
    else alert("セッションURLが取得できませんでした");
  } catch (err) {
    console.error("Checkoutエラー:", err);
    alert("通信エラーが発生しました");
  }
}

async function handleCancel() {
  if (!confirm("本当に解約しますか？")) return;
  try {
    const res = await fetch(`${STRIPE_API_BASE}/cancel-subscription`, {
      method: "POST",
      credentials: "include",
    });
    const data = await res.json();
    alert(data.message || "キャンセル完了");
    await userStore.fetchSubscription();
  } catch (err) {
    console.error("キャンセルエラー:", err);
    alert("通信エラーが発生しました");
  }
}

async function handleUncancel() {
  if (!confirm("解約をキャンセルしますか？")) return;
  try {
    const res = await fetch(`${STRIPE_API_BASE}/uncancel-subscription`, {
      method: "POST",
      credentials: "include",
    });
    const data = await res.json();
    alert(data.message || "キャンセル解除完了");
    await userStore.fetchSubscription();
  } catch (err) {
    console.error("解約キャンセルエラー:", err);
    alert("通信エラーが発生しました");
  }
}
</script>
