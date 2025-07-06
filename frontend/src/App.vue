<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useUserStore } from '@/stores/user'
import Navbar from '@/components/Navbar.vue'
import { onMounted } from 'vue'


const userStore = useUserStore()

function logout() {
  userStore.clearUser()
}
onMounted(() => {
  userStore.fetchUser()  // ✅ ログイン済みならここで状態が復元される
})

</script>

<template>
  <Navbar />
  <RouterView />
</template>

