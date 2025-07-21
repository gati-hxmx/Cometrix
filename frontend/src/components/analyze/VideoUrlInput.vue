<!-- components/VideoUrlInput.vue -->
<template>
  <div class="w-full max-w-xl mx-auto">
    <form @submit.prevent="handleSubmit" class="flex gap-2">
            <!-- YouTube -->
      <div class="flex items-center gap-3">
        <img
          src="/Users/uedahayato/Develp/Cometrix/commetrix/frontend/src/assets/yt_logo_rgb_light.png"
          alt="YouTube"
          class="h-4"
        />
      </div>

      <!-- Twitch -->
      <div class="flex items-center gap-3">
        <img
          src="/Users/uedahayato/Develp/Cometrix/commetrix/frontend/src/assets/glitch_flat_purple.svg"
          alt="Twitch"
          class="h-6"
        />
      </div>

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
import { useUserStore } from '@/stores/user'

const url = ref('')
const errorMessage = ref('')
const isSubmitting = ref(false)
const emit = defineEmits(['submit'])

const userStore = useUserStore()

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

async function handleSubmit() {
  errorMessage.value = ''
  const result = extractVideoIdAndPlatform(url.value)

  if (!result) {
    errorMessage.value = '有効なYouTubeまたはTwitchのURLを入力してください'
    return
  }

  isSubmitting.value = true

  // 🔽 YouTubeの場合だけジョブ送信
  if (result.platform === 'youtube') {
    try {
      const res = await fetch("http://localhost:8000/api/analyze/youtube/async", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          url: url.value.trim(),
          user_id: userStore.userId,
        }),
      })
      const data = await res.json()
      console.log('分析ジョブ送信成功:', data.task_id)
      // task_id は必要であれば emit で渡すことも可能
    } catch (err) {
      console.error('ジョブ送信失敗', err)
      errorMessage.value = 'ジョブ送信に失敗しました'
    }
  }

  if (result.platform === 'twitch') {
  try {
    const res = await fetch("http://localhost:8000/api/analyze/twitch/async", {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        json_path: `/Users/uedahayato/Develp/Cometrix/commetrix/chat_data/twitch_${result.videoId}.json`,
        video_id: result.videoId,
        user_id: userStore.userId,
      }),
    })
    const data = await res.json()
    console.log('Twitch分析ジョブ送信成功:', data.task_id)
  } catch (err) {
    console.error('Twitchジョブ送信失敗', err)
    errorMessage.value = 'ジョブ送信に失敗しました'
  }
}


  // 既存機能：emitで親に渡す
  emit('submit', result)

  isSubmitting.value = false
}
</script>

