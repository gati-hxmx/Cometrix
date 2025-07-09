<script setup>
import { ref } from 'vue'
import { useChatStore } from '@/stores/chat'

const chat = useChatStore()

const includeWordsInput = ref('')
const excludeWordsInput = ref('')
const includeUsersInput = ref('')
const excludeUsersInput = ref('')

// 折りたたみ制御用
const showAdvanced = ref(false)

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

<template>
  <div class="p-4 bg-white shadow rounded space-y-3 relative">


    <!-- ✅ 横並びの入力欄＋ボタン -->
    <div class="flex items-end gap-2">
      <div class="flex-1">
        <input
          v-model="includeWordsInput"
          class="w-full border rounded px-2 py-1"
          placeholder="含めたいワード"
        />
      </div>

          <!-- フィルタ適用 -->
      <div class="self-start">
        <button
          @click="applyFilters"
          class="bg-blue-500 text-white px-4 py-1 rounded hover:bg-blue-600"
        >
          フィルタを適用
        </button>
      </div>

      <!-- 詳細表示切替 -->
      <div class="self-start">
        <button
          @click="showAdvanced = !showAdvanced"
          class="text-sm text-blue-600 hover:underline"
        >
          {{ showAdvanced ? '詳細を隠す' : '詳細を表示' }}
        </button>
      </div>


    </div>

    <!-- ✅ 詳細設定：上方向に浮かせて表示 -->
    <div
      v-if="showAdvanced"
      class="absolute top-full left-0 w-full p-4 bg-white border rounded shadow z-10 space-y-3"
    >
      <div>
        <label class="block text-sm font-medium">除外したいワード</label>
        <input
          v-model="excludeWordsInput"
          class="w-full border rounded px-2 py-1"
          placeholder="例: 荒らし, NG"
        />
      </div>

      <div>
        <label class="block text-sm font-medium">含めたいユーザー</label>
        <input
          v-model="includeUsersInput"
          class="w-full border rounded px-2 py-1"
          placeholder="例: user123"
        />
      </div>

      <div>
        <label class="block text-sm font-medium">除外したいユーザー</label>
        <input
          v-model="excludeUsersInput"
          class="w-full border rounded px-2 py-1"
          placeholder="例: 荒らし太郎"
        />
      </div>
    </div>
  </div>
</template>


