<template>
  <div>
    <h2 class="text-xl font-bold mb-4">규칙 목록</h2>
    
    <div class="mb-4 flex gap-2">
      <input v-model="newRule" placeholder="새 규칙 입력" class="border px-3 py-2 rounded text-black" />
      <button @click="addRule" class="bg-green-500 px-4 py-2 rounded text-white hover:bg-green-600">추가</button>
    </div>

    <ul class="space-y-2">
      <li v-for="rule in rules" :key="rule.id" class="flex justify-between items-center bg-gray-700 p-3 rounded">
        <span>{{ rule.content }}</span>
        <button @click="deleteRule(rule.id)" class="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600">삭제</button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  rules: Array
})

const emit = defineEmits(['refresh'])
const backendUrl = import.meta.env.VITE_BACKEND_URL
const newRule = ref('')

async function addRule() {
  if (!newRule.value.trim()) return
  try {
    await fetch(`${backendUrl}/rules`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: newRule.value })
    })
    newRule.value = ''
    emit('refresh')
  } catch (error) {
    console.error('규칙 추가 실패:', error)
  }
}

async function deleteRule(id) {
  try {
    await fetch(`${backendUrl}/rules/${id}`, { method: 'DELETE' })
    emit('refresh')
  } catch (error) {
    console.error('규칙 삭제 실패:', error)
  }
}
</script>