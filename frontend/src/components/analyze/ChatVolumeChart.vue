<script setup>
import { useChatStore } from '@/stores/chat'
import { computed } from 'vue'
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

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const chat = useChatStore()

const chartData = computed(() => ({
  labels: chat.volumePer30s.map(v => v.start_str),
  datasets: [
    {
      label: 'チャット数（30秒ごと）',
      backgroundColor: '#3B82F6',
      data: chat.volumePer30s.map(v => v.count)
    }
  ]
}))

const chartOptions = {
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
  plugins: { legend: { display: false } }
}
</script>


<template>
  <div class="w-full max-w-5xl h-[300px] mx-auto mt-6 rounded border shadow bg-white flex items-center justify-center">
    <template v-if="chat.volumePer30s.length > 0">
      <Bar :data="chartData" :options="chartOptions" />
    </template>
    <template v-else>
      <div class="text-gray-400 text-sm">チャートデータがありません</div>
    </template>
  </div>
</template>
