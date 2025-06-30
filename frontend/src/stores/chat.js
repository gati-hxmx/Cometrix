// stores/chat.js
import { defineStore } from 'pinia'

export const useChatStore = defineStore('chat', {
  state: () => ({
    videoId: '',
    comments: [],
    volumePer30s: [],
    loading: false,
    error: null
  }),
  actions: {
    async fetchChatData(videoId) {
      this.videoId = videoId
      this.loading = true
      this.error = null

      try {
        const res = await fetch(`http://localhost:8000/api/chat-data?videoId=${videoId}`)
        if (!res.ok) throw new Error('チャットデータの取得に失敗しました')
        const data = await res.json()
        this.comments = data.comments
        this.volumePer30s = data.volume_per_30s
      } catch (err) {
        this.error = err.message
      } finally {
        this.loading = false
      }
    }
  }
})
