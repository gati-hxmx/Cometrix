<script setup>
import { computed } from 'vue'
import { useChatStore } from '@/stores/chat'

const chat = useChatStore()

// ✅ 表示範囲（±15秒）
const RANGE = 20

// ✅ フィルタされたチャット一覧
const visibleComments = computed(() => {
  const now = chat.currentTime
  return chat.comments
    .filter(c => {
      const ts = Math.floor(c.timestamp)
      return ts >= now - RANGE && ts <= now
    })
    .sort((a, b) => b.timestamp - a.timestamp) // 🔁 降順
})
</script>

<template>
  <div class="w-full h-full">
    <div class="h-full border rounded shadow bg-white overflow-y-auto flex flex-col">
      <template v-if="visibleComments.length > 0">
        <ul class="divide-y text-sm leading-relaxed">
          <li
            v-for="(c, i) in visibleComments"
            :key="i"
            class="px-4 py-2"
          >
            <div class="text-xs text-gray-500">{{ c.time_str }} | {{ c.author }}</div>
            <div class="text-gray-800">{{ c.text }}</div>
          </li>
        </ul>
      </template>

      <template v-else>
        <div class="flex-1 flex items-center justify-center text-gray-400 text-sm p-4">
          現在の再生位置に一致するチャットはありません
        </div>
      </template>
    </div>
  </div>
</template>
