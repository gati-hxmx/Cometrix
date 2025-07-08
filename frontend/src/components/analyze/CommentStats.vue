<template>
  <div class="flex gap-6 text-center text-gray-600 text-sm">

      <div class="text-center">
    <p class="text-gray-500 text-sm">累計コメント</p>
    <p class="text-2xl font-bold leading-tight">{{ totalComments }}</p>
  </div>

    <div class="border-l h-full"></div>

      <div class="text-center">
    <p class="text-gray-500 text-sm">平均コメント</p>
    <p class="text-2xl font-bold leading-tight">{{ averagePer30s }}</p>
  </div>

  <div class="border-l h-full"></div>
  </div>
</template>

<script setup>
import { useChatStore } from '@/stores/chat'
import { computed } from 'vue'

const chat = useChatStore()

const totalComments = computed(() => chat.comments.length)

const averagePer30s = computed(() => {
  const total = chat.volumePer30s.reduce((sum, bucket) => sum + bucket.count, 0)
  const count = chat.volumePer30s.length
  return count > 0 ? Math.round(total / count) : 0
})
</script>
