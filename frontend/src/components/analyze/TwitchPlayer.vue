<script setup>
import { useChatStore } from '@/stores/chat'
import { ref, watch, onMounted, onUnmounted, nextTick } from 'vue'

const chat = useChatStore()
const player = ref(null)
const timer = ref(null)
const isPlaying = ref(false)

function timeStrToSeconds(timeStr) {
  const [h, m, s] = timeStr.split(':').map(Number)
  return h * 3600 + m * 60 + s
}

function secondsToTwitchTime(sec) {
  const h = Math.floor(sec / 3600)
  const m = Math.floor((sec % 3600) / 60)
  const s = sec % 60
  return `${h}h${m}m${s}s`
}

function loadTwitchScript() {
  return new Promise((resolve, reject) => {
    if (window.Twitch && window.Twitch.Player) {
      resolve()
    } else {
      const script = document.createElement('script')
      script.src = 'https://player.twitch.tv/js/embed/v1.js'
      script.onload = resolve
      script.onerror = reject
      document.body.appendChild(script)
    }
  })
}

function startTimer() {
  clearInterval(timer.value)
  timer.value = setInterval(async () => {
    if (player.value && isPlaying.value) {
      const current = await player.value.getCurrentTime()
      chat.setCurrentTime(Math.floor(current))
    }
  }, 1000)
}

function stopTimer() {
  clearInterval(timer.value)
}

// 🎯 初期表示でもプレイヤーを生成
onMounted(async () => {
  if (chat.platform === 'twitch' && chat.videoId) {
    await loadTwitchScript()
    await nextTick()

    if (!player.value) {
      const embed = new window.Twitch.Player("twitch-player", {
        video: chat.videoId,
        time: '0h0m0s',
        autoplay: false,
        parent: ["localhost"],
        width: "100%",
        height: "100%",
      })

      embed.addEventListener(window.Twitch.Player.READY, () => {
        embed.setQuality('720p60')
        embed.play()
        startTimer()
      })

      embed.addEventListener(window.Twitch.Player.PLAY, () => {
        isPlaying.value = true
      })
      embed.addEventListener(window.Twitch.Player.PAUSE, () => {
        isPlaying.value = false
      })

      player.value = embed
    }
  }
})

// 🔁 selectedTimestamp が変化したときに seek
watch(
  () => chat.selectedTimestamp,
  async (newTime) => {
    if (player.value && newTime) {
      const sec = timeStrToSeconds(newTime)
      player.value.seek(sec)
    }
  }
)

onUnmounted(() => {
  stopTimer()
})
</script>

<template>
  <div class="aspect-video w-full h-full">
    <div id="twitch-player" class="w-full h-full rounded shadow" />
  </div>
</template>
