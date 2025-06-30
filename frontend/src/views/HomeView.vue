<template>
  <div class="p-4">
    🏠 Home View


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
