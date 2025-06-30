<template>
  <div class="p-4">
    🏠 Home View<br />
    ようこそ、{{ userStore.name || 'ゲスト' }} さん
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

    return { userStore }
  }
}
</script>
