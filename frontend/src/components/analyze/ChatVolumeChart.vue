<script setup>
import { useChatStore } from '@/stores/chat'
import { computed, watch, ref } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'
import zoomPlugin from 'chartjs-plugin-zoom'
import annotationPlugin from 'chartjs-plugin-annotation'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, zoomPlugin, annotationPlugin)

const chat = useChatStore()
const chartRef = ref(null)

const chartData = computed(() => ({
  labels: chat.volumePer30s.map(v => v.start_str),
  datasets: [
    {
      label: 'チャット数（30秒ごと）',
      backgroundColor: 'rgba(59, 130, 246, 0.3)',
      hoverBackgroundColor: 'rgba(59, 130, 246, 1)',
      data: chat.volumePer30s.map(v => v.count)
    }
  ]
}))

const chartOptions = computed(() => ({
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
      pan: { enabled: true, mode: 'x', speed: 0.1 },
      zoom: {
        wheel: { enabled: true, speed: 0.05, modifierKey: 'ctrl' },
        pinch: { enabled: true },
        mode: 'x'
      },
      limits: {
        x: { minRange: 100 }
      }
    },
    annotation: {
      annotations: {
        indicator: {
          type: 'line',
          borderColor: 'rgba(255, 0, 0, 0.8)',
          borderWidth: 2,
          scaleID: 'x',
          value: currentXLabel.value,
          label: {
            display: true,
            content: '再生位置',
            backgroundColor: 'rgba(255, 0, 0, 0.1)',
            color: 'red',
            position: 'start',
            font: {
              weight: 'bold'
            }
          }
        }
      }
    }
  }
}))

// ✅ 現在の再生位置から該当ラベル（例: 00:05:00）を算出
const currentXLabel = computed(() => {
  const sec = Math.floor(chat.currentTime)
  const bucket = Math.floor(sec / 30) * 30
  const match = chat.volumePer30s.find(v => v.start === bucket)
  return match?.start_str || ''
})

// ✅ 再生位置が変化するたびにチャート更新
watch(currentXLabel, (newVal) => {
  if (chartRef.value?.chart) {
    chartRef.value.chart.options.plugins.annotation.annotations.indicator.value = newVal
    chartRef.value.chart.update('none')
  }
})
</script>

<template>
  <div class="w-full max-w-5xl h-[300px] mx-auto mt-6 rounded border shadow bg-white flex items-center justify-center">
    <template v-if="chat.volumePer30s.length > 0">
      <Bar ref="chartRef" :data="chartData" :options="chartOptions" />
    </template>
    <template v-else>
      <div class="text-gray-400 text-sm">チャートデータがありません</div>
    </template>
  </div>
</template>
