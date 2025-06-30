<!-- src/views/HomeView.vue -->
<script setup>
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import DefaultLayout from '@/layouts/DefaultLayout.vue'

const userStore = useUserStore()

onMounted(() => {
  userStore.fetchUser()
})

const logout = () => {
  userStore.logout()
}
</script>

<template>
  <DefaultLayout>
    <div class="p-4">
      <h1 class="text-xl font-bold">🏠 Home View</h1>
      <p class="text-gray-600">
        このエリアは白いカード内に表示されているはずです
      </p>

    </div>
  </DefaultLayout>
</template>
