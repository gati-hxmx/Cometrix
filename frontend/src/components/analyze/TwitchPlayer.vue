<script setup>
import { useChatStore } from '@/stores/chat'
import { watch, ref, onUnmounted } from 'vue'

const chat = useChatStore()
const embedUrl = ref('')
const baseTimestamp = ref(0)
const timer = ref(null)

// 秒→Twitchの time=1h2m3s形式
function secondsToTwitchTime(sec) {
  const h = Math.floor(sec / 3600)
  const m = Math.floor((sec % 3600) / 60)
  const s = sec % 60
  return `${h}h${m}m${s}s`
}

// "00:01:23" → 83秒
function timeStrToSeconds(timeStr) {
  const [h, m, s] = timeStr.split(':').map(Number)
  return h * 3600 + m * 60 + s
}

// 🎯 タイマー開始
function startTimer(startSec) {
  baseTimestamp.value = startSec
  chat.setCurrentTime(startSec)

  clearInterval(timer.value)
  timer.value = setInterval(() => {
    baseTimestamp.value += 1
    chat.setCurrentTime(baseTimestamp.value)
  }, 1000)
}

// 🔁 selectedTimestamp に応じて再生とタイマー
watch(
  () => chat.selectedTimestamp,
  (newTime) => {
    if (chat.platform === 'twitch' && chat.videoId && newTime) {
      const seconds = timeStrToSeconds(newTime)
      const twitchTimeStr = secondsToTwitchTime(seconds)

      embedUrl.value = `https://player.twitch.tv/?video=${chat.videoId}&time=${twitchTimeStr}&parent=localhost&autoplay=true`
      startTimer(seconds)
    }
  },
  { immediate: true }
)

// ⛔️ コンポーネント破棄時にタイマー停止
onUnmounted(() => {
  clearInterval(timer.value)
})
</script>

<template>
  <iframe
    :src="embedUrl"
    frameborder="0"
    allowfullscreen
    width="100%"
    height="100%"
  ></iframe>
</template>
