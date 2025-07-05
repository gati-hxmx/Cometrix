<template>
    <DefaultLayout>
    <div class="p-6 max-w-3xl mx-auto space-y-12">
    <section>
      <h1 class="text-3xl font-bold mb-4">プライバシーポリシー</h1>
      <div class="space-y-4 text-sm leading-relaxed">
        <p>Cometrix（以下、「本サービス」といいます。）は、利用者のプライバシーを尊重し、以下のとおり個人情報を適切に取り扱います。</p>

        <h2 class="text-xl font-semibold mt-6">1. 取得する情報</h2>
        <ul class="list-disc list-inside">
          <li>Googleアカウントによるログイン時のメールアドレス、表示名</li>
          <li>チャット分析用に入力された動画URL</li>
          <li>ユーザーが作成したメモ、分析結果</li>
          <li>利用ログ（アクセス日時、IPアドレス、ブラウザ情報など）</li>
        </ul>
        <p>なお、決済情報（クレジットカード番号など）は Stripe により安全に処理され、当方では保持・管理いたしません。</p>

        <h2 class="text-xl font-semibold mt-6">2. 情報の利用目的</h2>
        <p>取得した情報は以下の目的で利用します：</p>
        <ul class="list-disc list-inside">
          <li>サービスの提供および改善</li>
          <li>ユーザー認証とアカウント管理</li>
          <li>不正利用の防止・対応</li>
          <li>ユーザーからの問い合わせ対応</li>
        </ul>

        <h2 class="text-xl font-semibold mt-6">3. 情報の保存</h2>
        <p>収集したデータは、<strong>日本国内（さくらのクラウド）</strong>のサーバーに保管されます。第三者によるアクセスができないよう適切に管理します。</p>

        <h2 class="text-xl font-semibold mt-6">4. 第三者提供</h2>
        <p>取得した個人情報は、法令に基づく場合を除き、第三者に提供することはありません。</p>

        <h2 class="text-xl font-semibold mt-6">5. Cookieおよびトラッキング</h2>
        <p>本サービスでは、ログインセッション管理のためにCookieを使用する場合がありますが、個人を特定する目的でのトラッキングには使用しません。</p>

        <h2 class="text-xl font-semibold mt-6">6. ポリシーの変更</h2>
        <p>本ポリシーの内容は、必要に応じて変更することがあります。重要な変更がある場合は、Webサイト上で通知します。</p>

        <p class="text-right text-xs text-gray-500 mt-8">最終改定日：2025年7月</p>
      </div>
    </section>
  </div>
    </DefaultLayout>
</template>

<script setup>
import DefaultLayout from '@/layouts/DefaultLayout.vue'
</script>