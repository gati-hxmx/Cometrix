<template>
  <div class="w-full max-w-5xl h-[300px] mx-auto mt-6 rounded border shadow bg-white flex items-center justify-center">
    <template v-if="displayVolumeData.length > 0">
      <canvas ref="canvasRef" class="w-full h-full" />
    </template>
    <template v-else>
      <div class="text-gray-400 text-sm">チャートデータがありません</div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onBeforeUnmount } from 'vue'
import { Chart, registerables } from 'chart.js'
import zoomPlugin from 'chartjs-plugin-zoom'
import annotationPlugin from 'chartjs-plugin-annotation'
import { useChatStore } from '@/stores/chat'

Chart.register(...registerables, zoomPlugin, annotationPlugin)

const chat = useChatStore()
const canvasRef = ref(null)
let chartInstance = null
const clickedIndex = ref(null)

// ✅ 表示用データ（フィルターON時は filteredVolumePer30s をベースに反映）
const displayVolumeData = computed(() => {
  if (!chat.isFilterActive) return chat.volumePer30s

  const filteredMap = new Map(
    chat.filteredVolumePer30s.map(v => [v.start_str, v.count])
  )

  return chat.volumePer30s.map(v => ({
    ...v,
    count: filteredMap.get(v.start_str) ?? 0
  }))
})



// ✅ グラフ描画
const drawChart = () => {
  if (!canvasRef.value) return
  const ctx = canvasRef.value.getContext('2d')
  if (!ctx) return
  if (chartInstance) chartInstance.destroy()

  const labels = displayVolumeData.value.map(v =>
    v.start_str ?? formatTime(v.timestamp)
  )
  const dataValues = displayVolumeData.value.map(v => v.count)

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

          const selected = displayVolumeData.value[index]
          const ts = selected?.start_str ?? formatTime(selected?.timestamp)
          if (ts) chat.setSelectedTimestamp(ts)

          drawChart()
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
          pan: { enabled: true, mode: 'x', speed: 0.1 },
          zoom: {
            wheel: { enabled: true, speed: 0.05, modifierKey: 'ctrl' },
            pinch: { enabled: true },
            mode: 'x'
          },
          limits: { x: { minRange: 100 } }
        }
      }
    }
  })
}

watch(displayVolumeData, async () => {
  await nextTick()
  drawChart()
}, { deep: true })


// ✅ グラフ再描画トリガー：volumePer30s / filteredVolumePer30s / isFilterActive の変化に反応
watch(
  [() => chat.volumePer30s, () => chat.filteredVolumePer30s, () => chat.isFilterActive],
  async () => {
    await nextTick()
    drawChart()
  },
  { deep: true }
)

watch(displayVolumeData, async (val) => {
  console.log('📊 displayVolumeData:', val)  // ← 追加
  console.log('📊 非ゼロの count 数:', displayVolumeData.value.filter(v => v.count > 0).length)
console.log('📊 全データの一部:', displayVolumeData.value.slice(0, 10))

  if (val.length > 0) {
    await nextTick()
    drawChart()
  }
}, { deep: true })


// 🧹 クリーンアップ
onBeforeUnmount(() => {
  if (chartInstance) chartInstance.destroy()
})

// ✅ 秒 → hh:mm:ss に変換
function formatTime(seconds) {
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  const s = Math.floor(seconds % 60)
  return [h, m, s].map(n => String(n).padStart(2, '0')).join(':')
}
</script>
