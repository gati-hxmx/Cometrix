// stores/chat.js
import { defineStore } from 'pinia'
import { useUserStore } from '@/stores/user'  // 👈 追加：ユーザー情報を取得

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
    
        filters: {
      includeWords: [],
      excludeWords: [],
      includeUsers: [],
      excludeUsers: [],
    }
  }),

  getters: {
    // ✅ フィルタが有効かどうか
    isFilterActive(state) {
      const f = state.filters
      return (
        f.includeWords.length > 0 ||
        f.excludeWords.length > 0 ||
        f.includeUsers.length > 0 ||
        f.excludeUsers.length > 0
      )
    },

    // ✅ フィルタ適用後のチャット一覧
    filteredComments(state) {
      return state.comments.filter(c => {
        const { text, author } = c
        const f = state.filters

        if (f.includeWords.length > 0 &&
            !f.includeWords.some(word => text.includes(word))) {
          return false
        }
        if (f.excludeWords.some(word => text.includes(word))) {
          return false
        }
        if (f.includeUsers.length > 0 &&
            !f.includeUsers.includes(author)) {
          return false
        }
        if (f.excludeUsers.includes(author)) {
          return false
        }

        return true
      })
    },

    // ✅ フィルタ適用後の30秒ごとのチャット数
// chat.js の getters 内 filteredVolumePer30s
filteredVolumePer30s(state) {
  const bins = {}

  state.filteredComments.forEach(c => {
    const sec = Math.floor(c.timestamp)
    const bin = Math.floor(sec / 30) * 30
    bins[bin] = (bins[bin] || 0) + 1
  })

  return Object.entries(bins)
    .sort((a, b) => a[0] - b[0])
    .map(([timestamp, count]) => ({
      timestamp: Number(timestamp),
      count,
      start_str: formatTime(Number(timestamp))  // ✅ 追加ここ
    }))
}



  },

  actions: {
    // ✅ platform も受け取る
    async fetchChatData(platform, videoId) {
      this.platform = platform
      this.videoId = videoId
      this.loading = true
      this.error = null

      const userStore = useUserStore()
      const email = userStore.email

      try {
        let url, res, data

        // --- ✅ Twitch は従来どおり同期取得 ---
        if (platform === 'twitch') {
          url = `http://localhost:8000/api/chat-data/twitch`
          res = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ videoId, email })
          })
          if (!res.ok) throw new Error('Twitchチャットの取得に失敗しました')
          data = await res.json()
          this.comments = data.comments
          this.volumePer30s = data.volume_per_30s
          return
        }

        // --- ✅ YouTube は非同期ジョブとして投げる ---
        // chat.js で fetch のURLを明示的にFastAPIサーバに向ける
const jobRes = await fetch(`http://localhost:8000/api/analyze/youtube/async`, {

          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ videoId, email })
        })
        if (!jobRes.ok) throw new Error('ジョブ登録に失敗しました')
        const { task_id } = await jobRes.json()

        // --- ✅ ステータス監視（ポーリング） ---
        let attempts = 0
        let result = null
        while (attempts < 60) {
          const statusRes = await fetch(`http://localhost:8000/api/analyze/task-status/${task_id}`)
          const statusJson = await statusRes.json()

          if (statusJson.status === 'SUCCESS' && statusJson.result) {
            result = statusJson.result
            break
          }
          if (statusJson.status === 'FAILURE') {
            throw new Error('分析に失敗しました')
          }

          await new Promise(r => setTimeout(r, 500))
          attempts++
        }

        if (!result) throw new Error('タイムアウトしました')

        this.comments = result.comments
        this.volumePer30s = result.volume_per_30s

      } catch (err) {
        this.error = err.message
      } finally {
        this.loading = false
      }
    }
,

        // ✅ フィルタ条件の更新
    setFilters(newFilters) {
      this.filters = {
        includeWords: newFilters.includeWords || [],
        excludeWords: newFilters.excludeWords || [],
        includeUsers: newFilters.includeUsers || [],
        excludeUsers: newFilters.excludeUsers || [],
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

function formatTime(seconds) {
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  const s = Math.floor(seconds % 60)
  return [h, m, s].map(n => String(n).padStart(2, '0')).join(':')
}

