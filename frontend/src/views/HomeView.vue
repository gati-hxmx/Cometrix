<template>
  <DefaultLayout>
    <!-- Hero セクション -->
    <section class="relative py-32 overflow-hidden bg-white">
      <img
        src="@/components/icons/TOP1.png"
        alt="チャット分析イメージ"
        class="absolute top-0 right-0 w-full max-w-xl object-contain z-0 mt-12 opacity-90 pointer-events-none"
      />
      <div class="relative z-10 max-w-5xl px-6 text-left">
        <h2
          class="text-4xl sm:text-4xl font-extrabold text-gray-900 mb-6 leading-tight tracking-tight"
        >
          アーカイブ動画のチャット分析で<br />
          こんな課題はありませんか？
        </h2>
        <p class="text-lg text-gray-600 mb-8">
          鬱憤アーカイブのチャットを傾向に紐づけ。<br />喋り過ぎの失敗を把握しよう。
        </p>
        <RouterLink
          to="/analyze"
          class="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium py-3 px-6 rounded shadow-md transition duration-200"
        >
          🚀 今すぐ試してみる
        </RouterLink>
      </div>
    </section>

    <!-- 機能紹介 -->
    <section class="bg-gray-50 py-20 px-6">
      <div class="max-w-6xl mx-auto text-center">
        <h2 class="text-3xl font-bold mb-12 text-gray-800">
          Cometrix の主な機能
        </h2>
        <div class="grid sm:grid-cols-3 gap-8">
          <div
            class="bg-white rounded-xl shadow hover:shadow-lg p-6 transition-transform hover:-translate-y-1"
          >
            <BarChart class="mx-auto text-blue-600 w-10 h-10 mb-4" />
            <h3 class="text-lg font-semibold text-gray-800 mb-2">
              グラフ可視化
            </h3>
            <p class="text-sm text-gray-600">
              30秒ごとのチャット数を棒グラフで可視化
            </p>
          </div>
          <div
            class="bg-white rounded-xl shadow hover:shadow-lg p-6 transition-transform hover:-translate-y-1"
          >
            <MessagesSquare class="mx-auto text-blue-600 w-10 h-10 mb-4" />
            <h3 class="text-lg font-semibold text-gray-800 mb-2">
              チャット一覧
            </h3>
            <p class="text-sm text-gray-600">
              コメント・ユーザー・タイムスタンプを時系列で表示
            </p>
          </div>
          <div
            class="bg-white rounded-xl shadow hover:shadow-lg p-6 transition-transform hover:-translate-y-1"
          >
            <Link2 class="mx-auto text-blue-600 w-10 h-10 mb-4" />
            <h3 class="text-lg font-semibold text-gray-800 mb-2">
              URL貼るだけ分析
            </h3>
            <p class="text-sm text-gray-600">
              YouTubeやTwitchのURLを貼るだけですぐ分析
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- 対応サービス -->
    <section class="py-16 bg-white border-t border-gray-100">
      <div class="max-w-4xl mx-auto px-4 text-center">
        <h2 class="text-2xl font-bold mb-8 text-gray-800">対応サイト</h2>
        <div class="flex justify-center items-center gap-12 flex-wrap">
          <img
            src="https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg"
            alt="YouTube"
            class="h-8 opacity-80 hover:opacity-100 transition"
          />
          <img
            src="/twitch_wordmark_extruded_purple.svg"
            alt="Twitch"
            class="h-8 opacity-80 hover:opacity-100 transition"
          />
        </div>
      </div>
    </section>

    <!-- プラン紹介 -->
    <section class="py-24 bg-gray-50">
      <div
        class="max-w-6xl mx-auto px-6 flex flex-col md:flex-row items-center gap-10"
      >
        <!-- 左側画像 -->
        <div class="w-full md:w-1/2">
          <img
            src="@/components/icons/TOP2.png"
            alt="プランイメージ"
            class="w-full max-w-md mx-auto object-contain"
          />
        </div>

        <!-- 右側テキスト -->
        <div class="w-full md:w-1/2 relative z-10">
          <h2
            class="text-3xl font-bold text-gray-900 mb-4 flex items-center gap-3"
          >
            有料プラン
            <span
              class="bg-blue-100 text-blue-600 text-sm font-semibold px-3 py-1 rounded-full"
              >月 ¥780</span
            >
          </h2>
          <ul class="space-y-4 text-gray-700 text-base">
            <li class="flex items-center gap-3">
              <Check class="text-blue-500 w-5 h-5" /> 分析回数無制限
            </li>
            <li class="flex items-center gap-3">
              <BarChart class="text-blue-500 w-5 h-5" /> 高度なチャート分析
            </li>
            <li class="flex items-center gap-3">
              <Bookmark class="text-blue-500 w-5 h-5" /> メモ・保存機能つき
            </li>
            <li class="flex items-center gap-3">
              <LifeBuoy class="text-blue-500 w-5 h-5" /> 優先サポート
            </li>
          </ul>
          <RouterLink
            to="/mypage"
            class="mt-8 inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-3 rounded shadow transition duration-200"
          >
            今すぐアップグレード
          </RouterLink>
        </div>
      </div>
    </section>
  </DefaultLayout>
</template>

<script setup>
import DefaultLayout from "@/layouts/DefaultLayout.vue";
import {
  BarChart,
  MessagesSquare,
  Link2,
  Check,
  Bookmark,
  LifeBuoy,
} from "lucide-vue-next";
</script>
