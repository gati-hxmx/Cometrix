<template>
  <div class="p-3 bg-white shadow rounded relative text-sm">
    <!-- ✅ メイン行 -->
    <div class="flex items-center gap-2">
      <div class="flex-1 relative">
        <input
          v-model="includeWordsInput"
          class="w-full border rounded pl-8 pr-2 py-1 text-sm"
          placeholder="ワードを含める"
        />
        <Search class="w-4 h-4 absolute left-2 inset-y-0 my-auto text-gray-400" />
      </div>

      <button
        @click="applyFilters"
        class="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded flex items-center gap-1"
        title="フィルターを適用"
      >
        <Filter class="w-4 h-4" />
      </button>

      <button
        @click="showAdvanced = !showAdvanced"
        class="text-gray-600 hover:text-blue-600"
        title="詳細フィルター"
      >
        <component :is="showAdvanced ? ChevronUp : ChevronDown" class="w-5 h-5" />
      </button>
    </div>

    <!-- ✅ 詳細：上に浮かせて表示 -->
    <transition name="fade">
      <div
        v-if="showAdvanced"
        class="absolute bottom-full mb-3 w-full p-4 bg-white border rounded shadow-lg z-10 space-y-3"
      >
        <div class="relative">
          <input
            v-model="excludeWordsInput"
            class="w-full border rounded pl-8 pr-2 py-1"
            placeholder="除外ワード"
          />
          <X class="w-4 h-4 absolute left-2 inset-y-0 my-auto text-gray-400" />
        </div>

        <div class="relative">
          <input
            v-model="includeUsersInput"
            class="w-full border rounded pl-8 pr-2 py-1"
            placeholder="ユーザーを含める"
          />
          <User class="w-4 h-4 absolute left-2 inset-y-0 my-auto text-gray-400" />
        </div>

        <div class="relative">
          <input
            v-model="excludeUsersInput"
            class="w-full border rounded pl-8 pr-2 py-1"
            placeholder="除外ユーザー"
          />
          <UserX class="w-4 h-4 absolute left-2 inset-y-0 my-auto text-gray-400" />
        </div>
      </div>
    </transition>
  </div>
</template>


<script setup>
import { ref, watch } from 'vue'
import { useChatStore } from '@/stores/chat'
import {
  Filter, ChevronDown, ChevronUp, X, User, UserX, Search
} from 'lucide-vue-next'

const chat = useChatStore()
const includeWordsInput = ref('')
const excludeWordsInput = ref('')
const includeUsersInput = ref('')
const excludeUsersInput = ref('')
const showAdvanced = ref(false)

// 新しい分析結果が読み込まれたら、入力欄の表示も一緒にクリアする
watch(() => chat.videoId, () => {
  includeWordsInput.value = ''
  excludeWordsInput.value = ''
  includeUsersInput.value = ''
  excludeUsersInput.value = ''
})

function applyFilters() {
  chat.setFilters({
    includeWords: splitInput(includeWordsInput.value),
    excludeWords: splitInput(excludeWordsInput.value),
    includeUsers: splitInput(includeUsersInput.value),
    excludeUsers: splitInput(excludeUsersInput.value),
  })
}

function splitInput(text) {
  return text.split(',').map(s => s.trim()).filter(Boolean)
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
