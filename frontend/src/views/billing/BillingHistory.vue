<template>
  <default-layout>
    <div class="p-6">
      <h2 class="text-xl font-bold mb-4">請求履歴</h2>
      <div v-if="loading">読み込み中...</div>
      <div v-else-if="history.length === 0">履歴がありません。</div>
      <div v-else>
        <table class="w-full border">
          <thead>
            <tr class="bg-gray-100">
              <th class="p-2 border">支払い日</th>
              <th class="p-2 border">金額</th>
              <th class="p-2 border">通貨</th>
              <th class="p-2 border">ステータス</th>
              <th class="p-2 border">請求ID</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in history" :key="item.invoice_id">
              <td class="p-2 border">{{ formatDate(item.paid_at) }}</td>
              <td class="p-2 border">{{ item.amount }}</td>
              <td class="p-2 border">{{ item.currency }}</td>
              <td class="p-2 border">{{ item.status }}</td>
              <td class="p-2 border">{{ item.invoice_id }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </default-layout>
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
</script>
