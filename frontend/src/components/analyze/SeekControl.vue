<template>
  <div class="flex items-center justify-center space-x-4 ">
    <!-- -秒ボタン -->
    <button
      @click="seek(-seekSeconds)"
      class="flex items-center bg-gray-200 hover:bg-gray-300 px-3 py-1 rounded text-sm"
    >
      <Rewind class="w-4 h-4 mr-1" />

    </button>

    <!-- 秒数入力 -->
    <input
      v-model.number="seekSeconds"
      type="number"
      min="1"
      class="w-16 text-center border rounded px-1 py-1 text-sm"
    />
    <span class="text-sm text-gray-600">秒</span>

    <!-- +秒ボタン -->
    <button
      @click="seek(seekSeconds)"
      class="flex items-center bg-gray-200 hover:bg-gray-300 px-3 py-1 rounded text-sm"
    >
      
      <FastForward class="w-4 h-4 ml-1" />
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useChatStore } from '@/stores/chat'
import { Rewind, FastForward } from 'lucide-vue-next'

const chat = useChatStore()

// ユーザーが入力する秒数
const seekSeconds = ref(10)

// ✅ hh:mm:ss 変換
function formatTime(seconds) {
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  const s = Math.floor(seconds % 60)
  return [h, m, s].map(n => String(n).padStart(2, '0')).join(':')
}

// ✅ シーク処理
function seek(offset) {
  const newSec = Math.max(chat.currentTime + offset, 0)
  chat.setSelectedTimestamp(formatTime(newSec))
}
</script>
