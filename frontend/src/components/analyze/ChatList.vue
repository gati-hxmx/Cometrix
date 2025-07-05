<script setup>
import { computed, ref } from 'vue'
import { useChatStore } from '@/stores/chat'

const chat = useChatStore()
const copiedIndex = ref(null) // どのチャットがコピーされたか

const RANGE = 20
const visibleComments = computed(() => {
  const now = chat.currentTime
  return chat.comments
    .filter(c => {
      const ts = Math.floor(c.timestamp)
      return ts >= now - RANGE && ts <= now
    })
    .sort((a, b) => b.timestamp - a.timestamp)
})

// 📋 コピー処理
async function copyText(text, index) {
  try {
    await navigator.clipboard.writeText(text)
    copiedIndex.value = index

    // 1.5秒後にメッセージを非表示
    setTimeout(() => {
      if (copiedIndex.value === index) copiedIndex.value = null
    }, 1500)
  } catch (err) {
    console.error('コピーに失敗:', err)
  }
}
</script>

<template>
  <div class="w-full h-full">
    <div class="h-full border rounded shadow bg-white overflow-y-auto flex flex-col">
      <template v-if="visibleComments.length > 0">
        <ul class="divide-y text-sm leading-relaxed">
          <li
            v-for="(c, i) in visibleComments"
            :key="i"
            class="px-4 py-2 hover:bg-blue-50 transition rounded cursor-pointer"
            @click="copyText(`${c.text}`, i)"
          >
            <div class="text-xs text-gray-500">{{ c.time_str }} | {{ c.author }}</div>
            <div class="text-gray-800">{{ c.text }}</div>
            <div v-if="copiedIndex === i" class="text-xs text-green-500 mt-1 h-4 transition-opacity opacity-100">
              コピーしました！
            </div>
            <div v-else class="h-4 opacity-0"></div> <!-- レイアウト固定用 -->
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
