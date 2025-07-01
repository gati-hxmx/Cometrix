<template>
  <div class="w-full max-w-5xl h-[300px] mx-auto mt-6 rounded border shadow bg-white flex items-center justify-center">
    <!-- チャートあり -->
    <template v-if="chat.volumePer30s.length > 0">
      <canvas ref="canvasRef" class="w-full h-full" />
    </template>

    <!-- チャートなし -->
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

const drawChart = () => {
  if (!canvasRef.value) {
    console.warn('Canvas not ready')
    return
  }

  const ctx = canvasRef.value.getContext('2d')
  if (!ctx) return

  if (chartInstance) {
    chartInstance.destroy()
  }

  chartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: chat.volumePer30s.map(v => v.start_str),
      datasets: [
        {
          label: 'チャット数（30秒ごと）',
          backgroundColor: 'rgba(59, 130, 246, 0.3)',
          hoverBackgroundColor: 'rgba(59, 130, 246, 1)',
          data: chat.volumePer30s.map(v => v.count)
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
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

// 📌 Piniaの volumePer30s を監視して、更新時に再描画
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

// ✅ コンポーネント破棄時にチャートも破棄
onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.destroy()
  }
})
</script>
