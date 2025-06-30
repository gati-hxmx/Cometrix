<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useUserStore } from '@/stores/user'
import Navbar from '@/components/Navbar.vue'

const userStore = useUserStore()

function logout() {
  userStore.clearUser()
}
</script>

<template>
  <Navbar />
  <RouterView />
</template>

