<script setup>
import { useUserStore } from '@/stores/user'
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

onMounted(async () => {
  const res = await fetch('/api/userinfo')
  const data = await res.json()
  userStore.setUser({ email: data.email, name: data.name })
  router.push('/') // トップページへ遷移など
})
</script>
