<template>
  <div class="text-center">
    <p class="text-gray-500 text-sm">再生位置</p>
    <p
      class="text-2xl font-bold font-mono tracking-wider px-2 py-1 inline-block transition-all duration-200 rounded-md cursor-pointer hover:bg-blue-100 "
      @click="copyToClipboard"
    >
      {{ formattedTime }}
    </p>
    <p
  class="text-xs text-green-500 mt-1 h-4 transition-opacity duration-300"
  :class="{ 'opacity-100': copied, 'opacity-0': !copied }"
>
  コピーしました！
</p>
  </div>
</template>

<script setup>
import { useChatStore } from '@/stores/chat'
import { computed, ref } from 'vue'

const chat = useChatStore()
const copied = ref(false)

function formatTime(seconds) {
  const h = String(Math.floor(seconds / 3600)).padStart(2, '0')
  const m = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0')
  const s = String(seconds % 60).padStart(2, '0')
  return `${h}:${m}:${s}`
}

const formattedTime = computed(() => formatTime(chat.currentTime))

function copyToClipboard() {
  navigator.clipboard.writeText(formattedTime.value).then(() => {
    copied.value = true
    setTimeout(() => (copied.value = false), 1500)
  })
}
</script>
