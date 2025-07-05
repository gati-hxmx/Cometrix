<template>

    <div class="text-center">
    <p class="text-gray-500 text-sm">再生位置</p>
    <p class="text-2xl font-bold leading-tight font-mono tracking-wider">{{ formattedTime }}</p>
  </div>
</template>

<script setup>
import { useChatStore } from '@/stores/chat'
import { computed } from 'vue'

const chat = useChatStore()

function formatTime(seconds) {
  const h = String(Math.floor(seconds / 3600)).padStart(2, '0')
  const m = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0')
  const s = String(seconds % 60).padStart(2, '0')
  return `${h}:${m}:${s}`
}

const formattedTime = computed(() => formatTime(chat.currentTime))
</script>
