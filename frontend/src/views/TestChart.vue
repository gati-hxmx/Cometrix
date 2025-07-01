<template>
  <div class="w-full max-w-5xl h-[300px] mx-auto mt-6 rounded border shadow bg-white flex items-center justify-center">
    <template v-if="chat.volumePer30s.length > 0">
      <canvas ref="canvasRef" class="w-full h-full" />
    </template>
    <template v-else>
      <div class="text-gray-400 text-sm">チャートデータがありません</div>
    </template>
  </div>
</template>

<script setup>
import { ref, watch, nextTick, onBeforeUnmount } from 'vue'
import { Chart, registerables } from 'chart.js'
import zoomPlugin from 'chartjs-plugin-zoom'
import { useChatStore } from '@/stores/chat'

Chart.register(...registerables, zoomPlugin)

const chat = useChatStore()
const canvasRef = ref(null)
let chartInstance = null
const clickedIndex = ref(null)  // 🔸 クリックされたバーのインデックスを保持

const drawChart = () => {
  if (!canvasRef.value) return

  const ctx = canvasRef.value.getContext('2d')
  if (!ctx) return

  if (chartInstance) {
    chartInstance.destroy()
  }

  const labels = chat.volumePer30s.map(v => v.start_str)
  const dataValues = chat.volumePer30s.map(v => v.count)

  // 🔸 バーの色設定：クリックしたバーだけピンク
  const backgroundColors = dataValues.map((_, idx) =>
    idx === clickedIndex.value ? 'rgba(255, 99, 132, 1)' : 'rgba(59, 130, 246, 0.3)'
  )
  const hoverBackgroundColors = dataValues.map((_, idx) =>
    idx === clickedIndex.value ? 'rgba(255, 99, 132, 1)' : 'rgba(59, 130, 246, 1)'
  )

  chartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: 'チャット数（30秒ごと）',
          data: dataValues,
          backgroundColor: backgroundColors,
          hoverBackgroundColor: hoverBackgroundColors
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: false,
      onClick: (e, elements) => {
          if (elements.length > 0) {
            const index = elements[0].index
            clickedIndex.value = index

            // ✅ 該当のバーのタイムスタンプを Pinia に保存
            const selectedTimestamp = chat.volumePer30s[index]?.start_str
            if (selectedTimestamp) {
              chat.setSelectedTimestamp(selectedTimestamp)
            }

            drawChart()  // 🔄 ピンクで再描画
          }
        },

      scales: {
        x: {
          title: { display: true, text: '時間（配信内）' },
          ticks: { autoSkip: true, maxTicksLimit: 10 }
        },
        y: {
          beginAtZero: true,
          title: { display: true, text: 'チャット数' }
        }
      },
      plugins: {
        legend: { display: false },
        zoom: {
          pan: {
            enabled: true,
            mode: 'x',
            speed: 0.1
          },
          zoom: {
            wheel: {
              enabled: true,
              speed: 0.05,
              modifierKey: 'ctrl'
            },
            pinch: { enabled: true },
            mode: 'x'
          },
          limits: {
            x: { minRange: 100 }
          }
        }
      }
    }
  })
}

// 🔁 volumePer30s が更新されたらチャート再描画
watch(
  () => chat.volumePer30s,
  async (val) => {
    if (val.length > 0) {
      await nextTick()
      drawChart()
    }
  },
  { deep: true }
)

// 🧹 コンポーネント破棄時にチャート破棄
onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.destroy()
  }
})
</script>
