<!-- src/layouts/DefaultLayout.vue -->
<template>
  <!-- 👇 ページ共通のラップ（Navbarは含まない） -->
  <div class="min-h-[calc(100vh-4rem)] bg-gray-200 text-gray-800 px-4 md:px-8 py-6">
    <div class="max-w-5xl mx-auto border border-gray-300 bg-white rounded-lg p-6 shadow">
      <slot />
    </div>
  </div>
</template>

<script setup>
// 特に import は不要。Slot でコンテンツを包むだけ。
</script>
