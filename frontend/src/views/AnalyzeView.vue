<script setup>
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import VideoUrlInput from '@/components/analyze/VideoUrlInput.vue';
</script>

<template>
  <DefaultLayout>
  <main class="p-8">
    <VideoUrlInput @submit="handleVideoIdSubmit" />

    <div v-if="videoId" class="mt-6">
      <p>取得した動画ID: <strong>{{ videoId }}</strong></p>
      <!-- 次ステップへ進める -->
    </div>
  </main>
  </DefaultLayout>
</template>
