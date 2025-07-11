<template>
  <DefaultLayout>
    <!-- Hero セクション -->
    <section class="bg-cover bg-center bg-no-repeat py-32 text-center" style="background-image: linear-gradient(to bottom, rgba(0,0,0,0.5), rgba(0,0,0,0.8)), url('/hero-bg.png');">
      <div class="px-6">
        <div class="bg-black/50 backdrop-blur-sm rounded-lg p-8 text-white shadow-lg animate-fade-in">
          <h1 class="text-4xl font-bold mb-4 leading-tight">
            YouTube / Twitch ライブチャットを<br class="sm:hidden" /><br>
            <span class="text-blue-400">可視化・分析</span> する
          </h1>
          <p class="text-lg mb-6 text-gray-200">
            Cometrixは、配信アーカイブのチャットをグラフとリストで見やすく分析できるツールです。
          </p>
          <RouterLink
            to="/analyze"
            class="inline-flex items-center bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded text-lg transition shadow-md"
          >
            <span class="mr-2">🚀</span> 分析をはじめる
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- 機能紹介 -->
    <section class="py-16 bg-white">
      <div class="max-w-4xl mx-auto px-4 text-center">
        <h2 class="text-2xl font-semibold mb-8">主な機能</h2>
        <div class="grid sm:grid-cols-3 gap-8">
          <div class="hover:shadow-md hover:-translate-y-1 transition rounded p-4">
            <div class="bg-blue-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3">
              <BarChart class="w-6 h-6 text-blue-600" />
            </div>
            <p class="text-xl font-bold text-blue-600 mb-1">グラフ可視化</p>
            <p class="text-sm text-gray-600">30秒ごとのチャット数を棒グラフで表示</p>
          </div>
          <div class="hover:shadow-md hover:-translate-y-1 transition rounded p-4">
            <div class="bg-blue-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3">
              <MessagesSquare class="w-6 h-6 text-blue-600" />
            </div>
            <p class="text-xl font-bold text-blue-600 mb-1">チャット一覧</p>
            <p class="text-sm text-gray-600">ユーザー・コメント・タイムスタンプを時系列に表示</p>
          </div>
          <div class="hover:shadow-md hover:-translate-y-1 transition rounded p-4">
            <div class="bg-blue-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3">
              <Link2 class="w-6 h-6 text-blue-600" />
            </div>
            <p class="text-xl font-bold text-blue-600 mb-1">URL貼るだけ</p>
            <p class="text-sm text-gray-600">YouTube動画URLを入力するだけですぐ分析</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 対応サービス -->
    <section class="py-12 bg-white border-t border-gray-100">
      <div class="max-w-4xl mx-auto px-4 text-center">
        <h2 class="text-2xl font-semibold mb-8 text-gray-800">対応サイト</h2>
        <div class="flex justify-center items-center gap-12 flex-wrap">
          <img src="https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg" alt="YouTube" class="h-8 opacity-80 hover:opacity-100 transition" />
          <img src="/twitch_wordmark_extruded_purple.svg" alt="Twitch" class="h-8 opacity-80 hover:opacity-100 transition" />
        </div>
      </div>
    </section>

    <!-- プラン紹介 -->
    <section class="py-16 bg-gray-50">
      <div class="max-w-6xl mx-auto px-4 text-center">
        <h2 class="text-2xl font-semibold mb-6">プラン比較</h2>
        <div class="grid sm:grid-cols-3 gap-6">
          <div class="bg-white border rounded-lg p-6 shadow-sm">
            <h3 class="text-xl font-bold mb-2 text-gray-800">Free Plan</h3>
            <p class="text-sm text-gray-500 mb-4">¥0 / 月</p>
            <ul class="text-sm text-gray-600 space-y-1">
              <li>✅ 月3本まで分析可能</li>
              <li>✅ 基本機能のみ</li>
              <li>❌ 高度な分析機能</li>
            </ul>
          </div>
          <div class="relative bg-white border border-blue-500 rounded-lg p-6 shadow-md">
            <span class="absolute top-4 right-4 text-xs bg-blue-600 text-white px-2 py-1 rounded-full">おすすめ</span>
            <h3 class="text-xl font-bold mb-2 text-blue-600">Pro Plan（月額）</h3>
            <p class="text-sm text-gray-500 mb-4">¥600 / 月</p>
            <ul class="text-sm text-gray-600 space-y-1 mb-4">
              <li>✅ 無制限に分析可能</li>
              <li>✅ 全機能利用可</li>
              <li>✅ 優先サポート</li>
            </ul>
            <RouterLink
              to="/mypage"
              class="inline-block bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded text-sm"
            >
              月額でアップグレード
            </RouterLink>
          </div>
          <div class="relative bg-white border border-blue-500 rounded-lg p-6 shadow-md">
            <h3 class="text-xl font-bold mb-2 text-blue-600">Pro Plan（年間）</h3>
            <p class="text-sm text-gray-500 mb-4">
              ¥5,900 / 年<br />
              <span class="inline-block text-green-700 font-semibold bg-green-100 px-2 py-0.5 rounded text-xs">2ヶ月分お得！</span>
            </p>
            <ul class="text-sm text-gray-600 space-y-1 mb-4">
              <li>✅ 無制限に分析可能</li>
              <li>✅ 全機能利用可</li>
              <li>✅ 優先サポート</li>
            </ul>
            <RouterLink
              to="/mypage"
              class="inline-block bg-blue-600 hover:bg-green-700 text-white px-4 py-2 rounded text-sm"
            >
              年間でアップグレード
            </RouterLink>
          </div>
        </div>
      </div>
    </section>
  </DefaultLayout>
</template>

<script setup>
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import { BarChart, MessagesSquare, Link2 } from 'lucide-vue-next'
</script>

<style scoped>
@keyframes fade-in {
  0% { opacity: 0; transform: translateY(10px); }
  100% { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
  animation: fade-in 0.8s ease-out;
}
</style>
