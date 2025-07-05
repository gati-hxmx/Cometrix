<script setup>
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import VideoUrlInput from '@/components/analyze/VideoUrlInput.vue';

import { useChatStore } from '@/stores/chat'
import YoutubePlayer from '@/components/analyze/YoutubePlayer.vue'
import ChatList from '@/components/analyze/ChatList.vue'
import ChatVolumeChart from '@/components/analyze/ChatVolumeChart.vue'
import LoadingOverlay from '@/components/analyze/common/LoadingOverlay.vue';
// AnalyzeView.vue の <script setup> の冒頭に以下を追加
import { ref } from 'vue'
import TestChart from './TestChart.vue';
import TwitchPlayer from '@/components/analyze/TwitchPlayer.vue'


const chat = useChatStore()

const handleVideoIdSubmit = ({ platform, videoId }) => {
  chat.fetchChatData(platform, videoId)
}


const isLoading = ref(false)

function startAnalysis() {
  isLoading.value = true

  // 仮に2秒待って完了する処理（あとでAPIに置き換える）
  setTimeout(() => {
    isLoading.value = false
  }, 2000)
}
</script>

<template>
  <DefaultLayout>
  <main class="p-8">
    <VideoUrlInput @submit="handleVideoIdSubmit" />
<!-- 横並び -->
<div class="mt-6 flex gap-4 items-start">
  <!-- 左：動画 -->
  <div class="w-3/4">
    <div class="aspect-video">
      <YoutubePlayer v-if="chat.platform === 'youtube'" />
      <TwitchPlayer v-else-if="chat.platform === 'twitch'" />
      <div v-else class="text-gray-500">対応していない動画です</div>
    </div>
  </div>

  <!-- 右：チャット（動画の高さ: 16:9 → 約56.25%） -->
<div
  class="w-1/4 overflow-y-auto"
  style="height: calc((100vw * 0.6) * 0.5625); max-height: 380px;"
>
  <ChatList />
</div>

</div>
<!-- <ChatVolumeChart /> -->
  <TestChart />

    <div v-if="videoId" class="mt-6">
      <p>取得した動画ID: <strong>{{ videoId }}</strong></p>
      <!-- 次ステップへ進める -->
    </div>
  </main>
  <LoadingOverlay v-if="isLoading" />
 
 
  </DefaultLayout>
</template>
