<template>
  <div class="p-4">
    🏠 Home View

    <div v-if="userStore.name" class="mt-4">
      <button @click="logout" class="bg-red-500 text-white px-4 py-2 rounded">
        ログアウト
      </button>
    </div>
  </div>
</template>

<script>
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

export default {
  name: 'HomeView',
  setup() {
    const userStore = useUserStore()

    onMounted(() => {
      userStore.fetchUser()
    })

    const logout = () => {
      userStore.logout()
    }

    return { userStore, logout }
  }
}
</script>
