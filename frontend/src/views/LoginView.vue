<template>
<div class="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-white">
  <div class="transform -translate-y-32 text-center max-w-md w-full p-6 bg-white border rounded-xl shadow-md">
      <!-- ロゴと見出し -->
      <div class="mb-6">
        <img
          src="/brand_logo(favicon).png"
          alt="Cometrix"
          class="mx-auto mb-4"
          style="height: 64px"
        />
        <h1 class="text-xl font-bold text-gray-800">ログイン / 新規登録</h1>
      </div>

      <!-- Googleログインボタン -->
      <div class="mb-4">
        <a
          href="http://localhost:5000/login/google"
          class="inline-flex items-center justify-center bg-white border px-4 py-2 rounded shadow hover:shadow-md transition"
        >
          <img
            src="https://developers.google.com/identity/images/g-logo.png"
            alt="Google"
            class="w-5 h-5 mr-2"
          />
          <span class="text-sm text-gray-700 font-medium">Googleでログイン</span>
        </a>
      </div>

      <!-- 補足テキスト -->
      <p class="text-xs text-gray-400 mt-6">アカウントをお持ちでない方は、ログイン時に自動登録されます。</p>
    </div>
  </div>
</template>
