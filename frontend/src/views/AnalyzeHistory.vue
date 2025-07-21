<template>
    <DefaultLayout>
  <div class="max-w-5xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-6">分析履歴</h1>

    <div v-if="!logs.length" class="text-gray-600">
      分析履歴がありません。
    </div>

    <div v-else class="space-y-4">
      <div
        v-for="log in logs"
        :key="log.id"
        class="border rounded shadow-sm p-4 hover:bg-gray-50 transition"
      >
        <div class="flex justify-between items-center">
          <div class="text-sm text-gray-500">{{ formatDate(log.analyzed_at) }}</div>
<span
  class="text-xs px-2 py-1 rounded capitalize"
  :class="platformClass(log.platform)"
>
  {{ log.platform }}
</span>

        </div>
        <div class="mt-2">
          <p class="font-semibold text-lg">
  {{ isValidTitle(log.video_title) ? log.video_title : '（タイトルなし）' }}
</p>

          <a
            :href="log.video_url"
            target="_blank"
            class="text-sm text-blue-600 hover:underline"
          >
            {{ log.video_url }}
          </a>
        </div>
        <div class="mt-2 text-sm text-gray-600">
          コメント数: {{ log.comment_count }} ／ 再生時間: {{ formatDuration(log.duration_sec) }}
        </div>
      </div>
    </div>
  </div>
  </DefaultLayout>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useUserStore } from '@/stores/user'
import DefaultLayout from '@/layouts/DefaultLayout.vue'

const logs = ref([])
const userStore = useUserStore()

onMounted(async () => {
  if (!userStore.email) return
  try {
    const res = await fetch(`http://localhost:8000/api/analysis/history?email=${userStore.email}`)
    if (res.ok) {
      const json = await res.json()
      console.log('[debug] logs:', json) // ← ここ追加
      logs.value = json
    } else {
      console.error('Failed to fetch logs')
    }
  } catch (e) {
    console.error(e)
  }
})



function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleString('ja-JP')
}

function formatDuration(sec) {
  const h = Math.floor(sec / 3600)
  const m = Math.floor((sec % 3600) / 60)
  const s = sec % 60
  return `${h}時間${m}分${s}秒`
}

function isValidTitle(title) {
  return !!title && title.trim() !== ''
}

function platformClass(platform) {
  if (platform === 'youtube') {
    return 'bg-red-100 text-red-700'
  } else if (platform === 'twitch') {
    return 'bg-purple-100 text-purple-700'
  } else {
    return 'bg-gray-200 text-gray-800'
  }
}


</script>

<style scoped>
</style>
