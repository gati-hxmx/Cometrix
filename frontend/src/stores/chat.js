// stores/chat.js
import { defineStore } from 'pinia'

export const useChatStore = defineStore('chat', {
  state: () => ({
    platform: '',
    videoId: '',
    comments: [],
    volumePer30s: [],
    loading: false,
    error: null,
    highlightedIndex: null,
    selectedTimestamp: null,
    currentTime: 0,
  }),
  actions: {
    // ✅ platform も受け取る
    async fetchChatData(platform, videoId) {
      this.platform = platform
      this.videoId = videoId
      this.loading = true
      this.error = null

      try {
        let url
        if (platform === 'youtube') {
          url = `http://localhost:8000/api/chat-data?videoId=${videoId}`
        } else if (platform === 'twitch') {
          url = `http://localhost:8000/api/analyze/twitch/${videoId}`
        } else {
          throw new Error('未対応のプラットフォームです')
        }

        const res = await fetch(url)
        if (!res.ok) throw new Error('チャットデータの取得に失敗しました')

        const data = await res.json()
        this.comments = data.comments
        this.volumePer30s = data.volume_per_30s
      } catch (err) {
        this.error = err.message
      } finally {
        this.loading = false
      }
    },

    setHighlightedIndex(index) {
      this.highlightedIndex = index
    },
    clearHighlightedIndex() {
      this.highlightedIndex = null
    },
    setSelectedTimestamp(ts) {
      this.selectedTimestamp = ts
    },
    setCurrentTime(time) {
      this.currentTime = time
    }
  }
})
