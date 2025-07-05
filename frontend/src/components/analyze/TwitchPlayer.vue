<!-- components/analyze/TwitchPlayer.vue -->
<template>
  <iframe
    :src="embedUrl"
    frameborder="0"
    allowfullscreen
    width="100%"
    height="100%"
  ></iframe>
</template>


<script setup>
import { useChatStore } from '@/stores/chat'
import { computed, watch, ref } from 'vue'

const chat = useChatStore()
const videoId = chat.videoId

const embedUrl = ref(`https://player.twitch.tv/?video=${videoId}&parent=localhost`)

// 🔁 selectedTimestamp に応じて URL 更新
watch(
  () => chat.selectedTimestamp,
  (newTime) => {
    if (chat.platform === 'twitch' && chat.videoId && newTime) {
      const seconds = timeStrToSeconds(newTime)
      const twitchTimeStr = secondsToTwitchTime(seconds)

      embedUrl.value = `https://player.twitch.tv/?video=${chat.videoId}&time=${twitchTimeStr}&parent=localhost&autoplay=true`
    }
  },
  { immediate: true }
)

// ⏱ 秒→ Twitchフォーマット（例: "1h2m3s"）
function secondsToTwitchTime(sec) {
  const h = Math.floor(sec / 3600)
  const m = Math.floor((sec % 3600) / 60)
  const s = sec % 60
  return `${h}h${m}m${s}s`
}

// 🧮 "00:01:23" → 83秒 形式変換
function timeStrToSeconds(timeStr) {
  const [h, m, s] = timeStr.split(':').map(Number)
  return h * 3600 + m * 60 + s
}
</script>

