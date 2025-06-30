// stores/user.js

import { defineStore } from 'pinia'
import axios from 'axios'

export const useUserStore = defineStore('user', {
  state: () => ({
    name: null,
    email: null,
  }),
  persist: true, // ✅ ←これでlocalStorageに保存
  actions: {
    async fetchUser() {
      try {
        const res = await axios.get('http://localhost:5000/api/user', { withCredentials: true })
        this.name = res.data.name
        this.email = res.data.email
      } catch {
        this.name = null
        this.email = null
      }
    },
    async logout() {
      try {
        await axios.get('http://localhost:5000/logout', {
          withCredentials: true
        })

        this.name = null
        this.email = null

        const router = useRouter()
        router.push('/')  // ← ホーム画面に遷移
      } catch (e) {
        console.error('ログアウトに失敗しました', e)
      }
    }
  }
})
