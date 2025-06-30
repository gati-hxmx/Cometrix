<script setup>
import { useChatStore } from '@/stores/chat'
import { computed } from 'vue'

const chat = useChatStore()

const embedUrl = computed(() => {
  return chat.videoId
    ? `https://www.youtube.com/embed/${chat.videoId}`
    : ''
})
</script>

<template>
  <div class="w-full h-full rounded overflow-hidden shadow bg-black/10">
    <iframe
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

