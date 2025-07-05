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

<script setup>
import { ref } from 'vue'

const url = ref('')
const errorMessage = ref('')
const isSubmitting = ref(false)

const emit = defineEmits(['submit'])

function extractVideoIdAndPlatform(inputUrl) {
  const trimmed = inputUrl.trim()

  // YouTube
  const ytMatch = trimmed.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})/)
  if (ytMatch) {
    return { platform: 'youtube', videoId: ytMatch[1] }
  }

  // Twitch
  const twitchMatch = trimmed.match(/twitch\.tv\/videos\/(\d+)/)
  if (twitchMatch) {
    return { platform: 'twitch', videoId: twitchMatch[1] }
  }

  return null
}

function handleSubmit() {
  errorMessage.value = ''
  const result = extractVideoIdAndPlatform(url.value)

  if (!result) {
    errorMessage.value = '有効なYouTubeまたはTwitchのURLを入力してください'
    return
  }

  isSubmitting.value = true

  setTimeout(() => {
    emit('submit', result) // { platform, videoId }
    isSubmitting.value = false
  }, 300)
}
</script>
