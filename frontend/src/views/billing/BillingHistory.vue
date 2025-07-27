<template>
  <DefaultLayout>
    <div class="p-6 max-w-5xl mx-auto">
      <h2 class="text-2xl font-bold mb-6">請求履歴</h2>

      <div v-if="loading" class="text-center py-10 text-gray-500">
        <span class="animate-pulse">読み込み中...</span>
      </div>

      <div v-else-if="history.length === 0" class="text-center text-gray-500">
        表示できる請求履歴はありません。
      </div>

      <div v-else class="overflow-x-auto rounded-lg border shadow-sm bg-white">
        <table class="min-w-full text-sm text-left">
          <thead class="bg-gray-50 border-b">
            <tr>
              <th class="p-3">支払い日</th>
              <th class="p-3">金額</th>
              <th class="p-3">通貨</th>
              <th class="p-3">ステータス</th>
              <th class="p-3">請求ID</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="item in history"
              :key="item.invoice_id"
              class="hover:bg-gray-50 border-b"
            >
              <td class="p-3">{{ formatDate(item.paid_at) }}</td>
              <td class="p-3">{{ formatAmount(item.amount) }}</td>
              <td class="p-3">{{ item.currency.toUpperCase() }}</td>
              <td class="p-3">
                <span :class="statusBadgeClass(item.status)">
                  {{ statusLabel(item.status) }}
                </span>
              </td>
              <td class="p-3 break-all text-gray-500">{{ item.invoice_id }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useUserStore } from "@/stores/user";
import DefaultLayout from "@/layouts/DefaultLayout.vue";

const userStore = useUserStore();
const history = ref([]);
const loading = ref(true);

onMounted(async () => {
  try {
    const { data } = await axios.get(
      `${import.meta.env.VITE_API_URL}/api/billing/history?email=${
        userStore.email
      }`
    );
    history.value = data;
  } catch (err) {
    console.error("請求履歴取得に失敗:", err);
  } finally {
    loading.value = false;
  }
});

const formatDate = (iso) => {
  return new Date(iso).toLocaleDateString("ja-JP", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

const formatAmount = (value) => {
  return new Intl.NumberFormat("ja-JP", {
    style: "currency",
    currency: "JPY",
  }).format(value / 100);
};

const statusLabel = (status) => {
  return (
    {
      paid: "支払い済み",
      open: "未払い",
      failed: "失敗",
    }[status] || status
  );
};

const statusBadgeClass = (status) => {
  return (
    {
      paid: "inline-block px-2 py-1 text-xs font-semibold text-green-700 bg-green-100 rounded",
      open: "inline-block px-2 py-1 text-xs font-semibold text-yellow-800 bg-yellow-100 rounded",
      failed:
        "inline-block px-2 py-1 text-xs font-semibold text-red-700 bg-red-100 rounded",
    }[status] ||
    "inline-block px-2 py-1 text-xs text-gray-700 bg-gray-100 rounded"
  );
};
</script>
