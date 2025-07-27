
<template>
  <div class="max-w-2xl mx-auto bg-gray-800 p-6 rounded-lg shadow-lg">
    <h2 class="text-xl font-bold text-primary mb-4">AI 규칙 추출</h2>
    
    <form @submit.prevent="uploadFile" class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-300 mb-2">
          파일 선택 (텍스트 파일)
        </label>
        <input 
          type="file" 
          ref="fileInput" 
          accept=".txt,.doc,.docx"
          class="w-full bg-gray-700 border border-gray-600 p-3 rounded text-white file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:bg-primary file:text-white hover:file:bg-blue-600"
        />
      </div>
      
      <button 
        type="submit" 
        :disabled="loading"
        class="w-full bg-primary text-white px-6 py-3 rounded hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {{ loading ? 'AI 분석중...' : 'AI 규칙 추출' }}
      </button>
    </form>
    
    <div v-if="loading" class="mt-4 p-4 bg-blue-900 text-blue-200 rounded">
      <div class="flex items-center">
        <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-200 mr-2"></div>
        AI가 텍스트를 분석하고 있습니다...
      </div>
    </div>
    
    <div v-if="error" class="mt-4 p-4 bg-red-900 text-red-200 rounded">
      {{ error }}
    </div>
    
    <div v-if="extractedRules.length > 0" class="mt-6">
      <h3 class="text-lg font-semibold text-primary mb-3">추출된 규칙 ({{ extractedRules.length }}개)</h3>
      <div class="space-y-2 max-h-64 overflow-y-auto">
        <div v-for="(rule, i) in extractedRules" :key="i" class="p-3 bg-gray-700 rounded text-sm">
          <div class="font-medium text-primary">{{ rule.condition }}</div>
          <div class="text-gray-300">{{ rule.result }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['rules'])

const fileInput = ref(null)
const loading = ref(false)
const error = ref('')
const extractedRules = ref([])

async function uploadFile() {
  if (!fileInput.value?.files[0]) {
    error.value = "파일을 선택해주세요."
    return
  }
  
  loading.value = true
  error.value = ""
  extractedRules.value = []
  
  try {
    const formData = new FormData()
    formData.append('file', fileInput.value.files[0])
    
    const response = await fetch('/extract_rules', {
      method: 'POST',
      body: formData
    })
    
    if (!response.ok) {
      throw new Error('서버 오류가 발생했습니다.')
    }
    
    const data = await response.json()
    
    if (data.rules && data.rules.length > 0) {
      extractedRules.value = data.rules
      emit('rules', data.rules)
    } else {
      error.value = "규칙을 추출할 수 없었습니다."
    }
  } catch (err) {
    error.value = `AI 추출 실패: ${err.message}`
  } finally {
    loading.value = false
  }
}
</script>
