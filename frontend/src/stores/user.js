// stores/user.js

import { defineStore } from 'pinia'
import axios from 'axios'
import { AUTH_API_BASE } from '@/config/api'
import router from '@/router'

export const useUserStore = defineStore('user', {
  state: () => ({
    name: null,
    email: null,
    subscription: null,  // ← 追加！
  }),
    persist: {
    paths: ['name', 'email']  // 👈 subscriptionは保持しない
  },
  actions: {
    async fetchUser() {
      try {
        const res = await axios.get(`${AUTH_API_BASE}/api/user`, { withCredentials: true })
        this.name = res.data.name
        this.email = res.data.email
      } catch {
        this.name = null
        this.email = null
      }
    },
    async fetchSubscription() {
      try {
        const res = await axios.get(`${AUTH_API_BASE}/api/subscription`, {
          withCredentials: true
        })
        console.log('📦 subscription fetched:', res.data)  // ← 追加
        this.subscription = res.data
      } catch (e) {
        console.error('サブスクリプション情報の取得に失敗しました', e)
        this.subscription = null
      }
    }
,
    async logout() {
      try {
        await axios.get(`${AUTH_API_BASE}/logout`, {
          withCredentials: true
        })

        this.name = null
        this.email = null
        this.subscription = null  // ← 忘れず初期化！

        router.push('/')
      } catch (e) {
        console.error('ログアウトに失敗しました', e)
      }
    }
  }
})
