
<script setup>
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import VideoUrlInput from '@/components/analyze/VideoUrlInput.vue';

import { useChatStore } from '@/stores/chat'
import YoutubePlayer from '@/components/analyze/YoutubePlayer.vue'
import ChatList from '@/components/analyze/ChatList.vue'
import ChatVolumeChart from '@/components/analyze/ChatVolumeChart.vue'
import LoadingOverlay from '@/components/analyze/common/LoadingOverlay.vue';
// AnalyzeView.vue の <script setup> の冒頭に以下を追加
import TestChart from './TestChart.vue';
import TwitchPlayer from '@/components/analyze/TwitchPlayer.vue'
import CommentStats from '@/components/analyze/CommentStats.vue'
import PlaybackTime from '@/components/analyze/PlaybackTime.vue'
import MemoEditor from '@/components/analyze/MemoEditor.vue'
import ChatFilter from '@/components/analyze/ChatFilter.vue'
import { useUserStore } from '@/stores/user'
import { computed, ref, onMounted } from 'vue'
import SeekControl from '@/components/analyze/SeekControl.vue'
// import ChatChart from '@/components/ChatChart.vue'



const tabs = ['チャット', '字幕', 'メモ']
const activeTab = ref('チャット')

const chat = useChatStore()

// サブスク状態チェック用
const userStore = useUserStore()
const subscription = computed(() => userStore.subscription)

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
  <main class="px-8">

          <!-- ✅ ガード：未契約状態なら警告だけ表示 -->
      <div v-if="!subscription || ['inactive', 'canceled'].includes(subscription.status)" class="text-center text-gray-600">
        <p class="text-xl font-semibold mb-2">ご利用にはサブスクリプション契約が必要です</p>
        <router-link to="/mypage" class="text-blue-600 hover:underline">マイページから契約してください</router-link>
      </div>

            <!-- ✅ 契約中ユーザー向けの分析画面 -->
      <div v-else>
        <!-- 🎥 動画URL入力と分析UI -->
        <VideoUrlInput @submit="handleVideoIdSubmit" />
        <!-- ... 以下すべて既存の分析UIを内包する -->
        <!-- 既存の動画プレイヤー / チャットタブ / グラフ / 統計など -->
        <!-- ※ここは既存の分析UIをそのまま入れてOK -->

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
  
<div class="flex gap-3 mt-2">
  <CommentStats />
  <PlaybackTime />
  <SeekControl />

  <div class="ml-auto">
    <ChatFilter />
  </div>
</div>




<!-- <ChatVolumeChart /> -->
  <TestChart />

<div v-if="chat.videoId" class="mt-6">
  <p>取得した動画ID: <strong>{{ chat.videoId }}</strong></p>
</div>


  </div>
  </main>
  <LoadingOverlay v-if="isLoading" />
 
 
  </DefaultLayout>
</template>
