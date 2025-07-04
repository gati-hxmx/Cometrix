// stores/user.js

import { defineStore } from 'pinia'
import axios from 'axios'

export const useUserStore = defineStore('user', {
  state: () => ({
    name: null,
    email: null,
    subscription: null,  // ← 追加！
  }),
  persist: true,
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
    async fetchSubscription() {
      try {
        const res = await axios.get('http://localhost:5000/api/subscription', {
          withCredentials: true
        })
        this.subscription = res.data  // 例: { plan: 'free', status: 'active' }
      } catch (e) {
        console.error('サブスクリプション情報の取得に失敗しました', e)
        this.subscription = null
      }
    },
    async logout() {
      try {
        await axios.get('http://localhost:5000/logout', {
          withCredentials: true
        })

        this.name = null
        this.email = null
        this.subscription = null  // ← 忘れず初期化！

        const router = useRouter()
        router.push('/')
      } catch (e) {
        console.error('ログアウトに失敗しました', e)
      }
    }
  }
})
