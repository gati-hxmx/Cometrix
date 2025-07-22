<template>
  <button
    @click="toggleDarkMode"
    class="p-2 rounded bg-gray-200 dark:bg-gray-700"
  >
    <span v-if="isDark">🌙 ダークモード</span>
    <span v-else>☀️ ライトモード</span>
  </button>
</template>

<script setup>
import { ref, onMounted } from "vue";

const isDark = ref(false);

onMounted(() => {
  // localStorageから状態を取得
  isDark.value = localStorage.getItem("darkMode") === "true";
  updateHtmlClass();
});

const toggleDarkMode = () => {
  isDark.value = !isDark.value;
  localStorage.setItem("darkMode", isDark.value);
  updateHtmlClass();
};

const updateHtmlClass = () => {
  document.documentElement.classList.toggle("dark", isDark.value);
};
</script>
