<template>
  <div>
    <form @submit.prevent="uploadFile">
      <input type="file" ref="fileInput" />
      <button type="submit">AI 규칙 추출</button>
    </form>
    <div v-if="loading">AI 분석중...</div>
    <div v-if="error">{{ error }}</div>
  </div>
</template>
<script setup>
import { ref } from 'vue'
const emit = defineEmits(['rules'])
const fileInput = ref(null)
const loading = ref(false)
const error = ref('')
const backendUrl = import.meta.env.VITE_BACKEND_URL
async function uploadFile() {
  if (!fileInput.value.files[0]) {
    error.value = "파일을 선택해주세요."; return;
  }
  loading.value = true; error.value = ""
  const form = new FormData()
  form.append('file', fileInput.value.files[0])
  const res = await fetch(`${backendUrl}/extract_rules`, { method: 'POST', body: form })
  const data = await res.json()
  if (data.rules) emit('rules', data.rules)
  else error.value = "AI 추출 실패"
  loading.value = false
  }
</script>


