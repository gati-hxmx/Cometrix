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
import CommentStats from '@/components/analyze/CommentStats.vue'
import PlaybackTime from '@/components/analyze/PlaybackTime.vue'
import MemoEditor from '@/components/analyze/MemoEditor.vue'
import ChatFilter from '@/components/analyze/ChatFilter.vue'
// import ChatChart from '@/components/ChatChart.vue'



const tabs = ['チャット', '字幕', 'メモ']
const activeTab = ref('チャット')

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

          <div v-else class="flex items-center justify-center w-full h-full text-gray-500 text-sm">
      ここに動画が表示されます
    </div>
    </div>
  </div>

<!-- 右：チャットエリアをタブ付きにする -->
<div
  class="w-1/4 overflow-hidden border rounded shadow bg-white"
  style="height: calc((100vw * 0.6) * 0.6); max-height: 380px;"
>
  <!-- タブヘッダー -->
  <div class="flex border-b text-sm font-medium">
    <button
      v-for="tab in tabs"
      :key="tab"
      @click="activeTab = tab"
      :class="[
        'flex-1 py-2 text-center hover:bg-gray-100',
        activeTab === tab ? 'bg-blue-100 font-bold' : 'bg-white'
      ]"
    >
      {{ tab }}
    </button>
  </div>

  <!-- タブの内容 -->
  <div class="overflow-y-auto h-full">
    <ChatList v-if="activeTab === 'チャット'" />
    <div v-else-if="activeTab === '字幕'" class="p-4 text-sm text-gray-600">字幕はまだ未実装です</div>
    <div v-else-if="activeTab === 'メモ'" class="p-4 text-sm text-gray-600"><MemoEditor /></div>
  </div>
</div>



</div>
<div class="flex gap-8 mt-6">
  <CommentStats />
  <PlaybackTime />
    <div class="space-y-4">
    <ChatFilter />
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
