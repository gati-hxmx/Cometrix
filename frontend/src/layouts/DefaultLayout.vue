<!-- src/layouts/DefaultLayout.vue -->
<template>
  <!-- 👇 ページ共通のラップ（Navbarは含まない） -->
  <div
    class="min-h-[calc(100vh-4rem)] bg-blue-50 text-gray-800 px-4 md:px-8 py-6"
  >
    <div
      class="max-w-5xl mx-auto border border-gray-300 bg-white rounded-lg p-6 shadow"
    >
      <slot />
    </div>
  </div>
  <!-- フッター -->
  <footer class="bg-white border-t text-center text-sm text-gray-500 py-4">
    © Cometrix 2025. All rights reserved. |
    <RouterLink to="/leagal" class="mx-2 hover:underline">利用規約</RouterLink>
    <RouterLink to="/privacypolicy" class="mx-2 hover:underline"
      >プライバシーポリシー</RouterLink
    >
  </footer>
</template>

<script setup>
// 特に import は不要。Slot でコンテンツを包むだけ。
</script>
