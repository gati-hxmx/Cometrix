<script setup>
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import DefaultLayout from '@/layouts/DefaultLayout.vue'

const userStore = useUserStore()

onMounted(() => {
  userStore.fetchUser()
})
</script>

<template>
  <DefaultLayout>
    <!-- Hero セクション -->
<section
  class="bg-cover bg-center bg-no-repeat py-32 text-center"
  style="background-image: url('/hero-bg.png');"
>
  <div class="px-6">
    <!-- テキスト背景ボックス -->
    <div class="bg-black/60 backdrop-blur-sm rounded-lg p-8 text-white shadow-md">
      <h1 class="text-4xl font-bold mb-4">
        YouTube/Twitchライブチャットを<br class="sm:hidden" />可視化・分析する
      </h1>
      <p class="text-lg mb-6">
        Cometrixは、配信アーカイブのチャットをグラフとリストで見やすく分析できるツールです。
      </p>
      <RouterLink
        to="/analyze"
        class="inline-block bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded text-lg transition"
      >
        分析をはじめる
      </RouterLink>
    </div>
  </div>
</section>


    <!-- 機能紹介 -->
    <section class="py-16 bg-white">
      <div class="max-w-4xl mx-auto px-4 text-center">
        <h2 class="text-2xl font-semibold mb-8">主な機能</h2>
        <div class="grid sm:grid-cols-3 gap-8">
          <div>
            <p class="text-xl font-bold text-blue-600 mb-2">📊 グラフ可視化</p>
            <p class="text-sm text-gray-600">30秒ごとのチャット数を棒グラフで表示</p>
          </div>
          <div>
            <p class="text-xl font-bold text-blue-600 mb-2">💬 チャット一覧</p>
            <p class="text-sm text-gray-600">ユーザー・コメント・タイムスタンプを時系列に表示</p>
          </div>
          <div>
            <p class="text-xl font-bold text-blue-600 mb-2">🔗 URL貼るだけ</p>
            <p class="text-sm text-gray-600">YouTube動画URLを入力するだけですぐ分析</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 対応サービス紹介 -->
<section class="py-12 bg-white border-t border-gray-100">
  <div class="max-w-4xl mx-auto px-4 text-center">
    <h2 class="text-2xl font-semibold mb-8 text-gray-800">対応サイト</h2>
    <div class="flex justify-center items-center gap-12 flex-wrap">
      <!-- YouTube -->
      <div class="flex items-center gap-3">
        <img
          src="https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg"
          alt="YouTube"
          class="h-8"
        />
      </div>

      <!-- Twitch -->
      <div class="flex items-center gap-3">
<img
  src="/twitch_wordmark_extruded_purple.svg"
  alt="Twitch"
  class="h-8"
/>
      </div>
    </div>
  </div>
</section>


    <!-- プラン紹介 -->
<section class="py-16 bg-gray-50">
  <div class="max-w-6xl mx-auto px-4 text-center">
    <h2 class="text-2xl font-semibold mb-6">プラン比較</h2>
    <div class="grid sm:grid-cols-3 gap-6">
      <!-- Free Plan -->
      <div class="bg-white border rounded-lg p-6 shadow-sm">
        <h3 class="text-xl font-bold mb-2 text-gray-800">Free Plan</h3>
        <p class="text-sm text-gray-500 mb-4">¥0 / 月</p>
        <ul class="text-sm text-gray-600 space-y-1">
          <li>✅ 月3本まで分析可能</li>
          <li>✅ 基本機能のみ</li>
          <li>❌ 高度な分析機能</li>
        </ul>
      </div>

      <!-- Pro Plan (Monthly) -->
      <div class="bg-white border border-blue-500 rounded-lg p-6 shadow-md">
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

      <!-- Pro Plan (Annual) -->
      <div class="bg-white border border-blue-500 rounded-lg p-6 shadow-md">
        <h3 class="text-xl font-bold mb-2 text-blue-600">Pro Plan（年間）</h3>
        <p class="text-sm text-gray-500 mb-4">
          ¥5,900 / 年<br />
          <span class="text-xs text-green-600">※ 月額の2ヶ月分お得</span>
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
