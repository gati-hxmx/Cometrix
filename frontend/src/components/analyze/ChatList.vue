<script setup>
import { useChatStore } from '@/stores/chat'
const chat = useChatStore()
</script>

<template>
  <div class="w-full h-full">

    <div class="h-full border rounded shadow bg-white overflow-y-auto flex flex-col">
      <template v-if="chat.comments.length > 0">
        <ul class="divide-y text-sm leading-relaxed">
          <li
            v-for="(c, i) in chat.comments"
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
          チャットデータがありません
        </div>
      </template>
    </div>
  </div>
</template>
