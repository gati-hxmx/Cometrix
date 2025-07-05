<script setup>
import { useChatStore } from '@/stores/chat'
import { computed, watch, ref, onMounted, nextTick } from 'vue'

const chat = useChatStore()
const embedUrl = ref('')
const currentTime = ref(0)

let player = null

function timeStrToSeconds(timeStr) {
  const [h, m, s] = timeStr.split(':').map(Number)
  return h * 3600 + m * 60 + s
}

// ▶️ URL設定：videoId または selectedTimestamp に応じて更新
watch(
  () => chat.videoId,
  (newId) => {
    if (newId) {
      embedUrl.value = `https://www.youtube.com/embed/${newId}?enablejsapi=1`
    }
  },
  { immediate: true }
)

watch(
  () => chat.selectedTimestamp,
  (newTime) => {
    if (chat.videoId && newTime) {
      const seconds = timeStrToSeconds(newTime)
      embedUrl.value = `https://www.youtube.com/embed/${chat.videoId}?start=${seconds}&autoplay=1&enablejsapi=1`
    }
  }
)



onMounted(async () => {
  await nextTick()

  const createPlayer = () => {
    player = new YT.Player('youtube-player', {
      events: {
        onReady: () => {
          console.log('✅ Player ready')
          setInterval(() => {
            if (player?.getCurrentTime) {
              currentTime.value = Math.floor(player.getCurrentTime())
              chat.setCurrentTime(currentTime.value)  // ← Pinia に反映！
            }
          }, 1000)
        },

      }
    })
  }

if (window.YT && typeof window.YT.Player === 'function') {
  createPlayer()
} else if (!document.getElementById('youtube-api')) {
  const tag = document.createElement('script')
  tag.src = 'https://www.youtube.com/iframe_api'
  tag.id = 'youtube-api'
  document.head.appendChild(tag)
  window.onYouTubeIframeAPIReady = createPlayer
}

})

function formatTime(seconds) {
  const h = Math.floor(seconds / 3600).toString().padStart(2, '0')
  const m = Math.floor((seconds % 3600) / 60).toString().padStart(2, '0')
  const s = Math.floor(seconds % 60).toString().padStart(2, '0')
  return `${h}:${m}:${s}`
}

const currentTimeStr = computed(() => formatTime(currentTime.value))
</script>

<template>
  <div class="w-full h-full rounded overflow-hidden shadow bg-black/10">
    <iframe
      id="youtube-player"
      v-if="chat.videoId"
      :src="embedUrl"
      frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
      allowfullscreen
      class="w-full h-full"
    ></iframe>

    <div v-else class="flex items-center justify-center w-full h-full text-gray-500 text-sm">
      ここにYouTube動画が表示されます
    </div>
  </div>

</template>
