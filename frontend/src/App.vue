<script setup>
import { RouterLink, RouterView } from "vue-router";
import { useUserStore } from "@/stores/user";
import Navbar from "@/components/Navbar.vue";
import { onMounted } from "vue";

const userStore = useUserStore();

function logout() {
  userStore.clearUser();
}
onMounted(async () => {
  await userStore.fetchUser(); // ① ログイン状態の復元
  if (userStore.email) {
    await userStore.fetchSubscription(); // ② サブスク状態の復元
  }
});
</script>

<template>
  <Navbar />
  <RouterView />
</template>
