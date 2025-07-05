<!-- components/analyze/MemoEditor.vue -->
<template>
  <div class="flex flex-col h-full">


    <div
      ref="memoArea"
      contenteditable="true"
      class="flex-grow w-full h-full p-2 border rounded bg-gray-50 text-sm text-gray-800 overflow-y-auto focus:outline-none"
      placeholder="ここにメモを記入できます"
    >
      <!-- 初期は空 -->
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const memoArea = ref(null)

// 今後：Piniaに保存 or 再生位置を追加するAPIなどを追加予定
</script>

<style scoped>
/* プレースホルダー風スタイル */
[contenteditable="true"]:empty:before {
  content: attr(placeholder);
  color: #aaa;
}
</style>
