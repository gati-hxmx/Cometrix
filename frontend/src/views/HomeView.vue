<template>
  <div class="p-4">
    🏠 Home View<br />
    ようこそ、{{ user?.name || 'ゲスト' }} さん
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'HomeView',
  setup() {
    const user = ref(null)

    onMounted(async () => {
      try {
        const res = await axios.get('http://localhost:5000/api/userinfo', {
          withCredentials: true
        })
        user.value = res.data
      } catch (e) {
        console.warn("未認証")
      }
    })

    return { user }
  }
}
</script>
