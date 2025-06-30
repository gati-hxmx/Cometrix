<!-- components/VideoUrlInput.vue -->
<template>
  <div class="w-full max-w-xl mx-auto">
    <form @submit.prevent="handleSubmit" class="flex gap-2">
      <input
        v-model="url"
        type="text"
        placeholder="URLを入力"
        class="flex-1 p-2 border rounded"
      />
      <button
        type="submit"
        class="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
        :disabled="isSubmitting"
      >
        分析
      </button>
    </form>
    <p v-if="errorMessage" class="text-red-500 text-sm mt-2">{{ errorMessage }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';

const url = ref('');
const errorMessage = ref('');
const isSubmitting = ref(false);

// イベントを親にemit
const emit = defineEmits<{
  (e: 'submit', videoId: string): void;
}>();

function extractVideoId(inputUrl: string): string | null {
  const regExp = /(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})/;
  const match = inputUrl.match(regExp);
  return match ? match[1] : null;
}

function handleSubmit() {
  errorMessage.value = '';
  const id = extractVideoId(url.value.trim());

  if (!id) {
    errorMessage.value = '有効なYouTubeのURLを入力してください';
    return;
  }

  isSubmitting.value = true;

  // 少し遅延させてUX感を出す（後で削除してOK）
  setTimeout(() => {
    emit('submit', id);
    isSubmitting.value = false;
  }, 300);
}
</script>
