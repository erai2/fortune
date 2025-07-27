<template>
  <div class="max-w-xl mx-auto bg-gray-800 p-6 rounded shadow mt-6">
    <form @submit.prevent="uploadFile">
      <div class="mb-2">
        <input type="file" ref="fileInput" class="bg-gray border p-2 rounded w-full text-white"/>
      </div>
      <button type="submit" class="bg-primary px-4 py-2 rounded text-white">AI 규칙 추출</button>
    </form>
    <div v-if="loading" class="mt-4 text-sky-400">AI 분석중...</div>
    <div v-if="error" class="mt-2 text-red-400">{{ error }}</div>
  </div>
</template>
<script setup>
import { ref } from 'vue'
const emit = defineEmits(['rules'])
const fileInput = ref(null)
const loading = ref(false)
const error = ref('')
async function uploadFile() {
  if (!fileInput.value.files[0]) { error.value = "파일을 선택해주세요."; return; }
  loading.value = true; error.value = ""
  const form = new FormData()
  form.append('file', fileInput.value.files[0])
  const res = await fetch('/extract_rules', { method: 'POST', body: form })
  const data = await res.json()
  if (data.rules) emit('rules', data.rules)
  else error.value = "AI 추출 실패"; loading.value = false
  loading.value = false
}
</script>
