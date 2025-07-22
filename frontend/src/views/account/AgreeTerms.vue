<template>
  <div
    class="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-white"
  >
    <div
      class="transform -translate-y-20 text-left max-w-3xl w-full p-6 bg-white border rounded-xl shadow-md"
    >
      <h1 class="text-2xl font-bold text-gray-800 mb-6">利用規約への同意</h1>

      <div
        class="h-64 overflow-y-scroll border p-4 rounded text-sm text-gray-700 bg-gray-50"
      >
        <TermsOfServiceContent />
      </div>

      <div class="mt-4 flex items-start gap-2">
        <input type="checkbox" id="agree" v-model="agreed" class="mt-1" />
        <label for="agree" class="text-sm text-gray-700">
          利用規約に同意します
        </label>
      </div>

      <div class="mt-6">
        <button
          :disabled="!agreed"
          @click="handleAgree"
          class="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 disabled:opacity-50 transition"
        >
          同意して Google で登録
        </button>
      </div>

      <div class="mt-4 text-xs text-gray-400 text-center">
        すでにアカウントをお持ちの場合は、<router-link
          to="/login"
          class="underline"
          >こちら</router-link
        >
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import TermsOfServiceContent from "@/components/common/TermsOfServiceContent.vue";

const agreed = ref(false);

const handleAgree = () => {
  // Google OAuth にリダイレクト（Flask側で登録処理も兼ねる）
  window.location.href = "http://localhost:5000/login/google?new_user=1";
};
</script>
