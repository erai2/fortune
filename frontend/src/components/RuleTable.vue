<template>
  <div>
    <h2 class="text-xl font-bold mb-4">규칙 목록</h2>

    <div class="mb-4 flex gap-2 flex-wrap">
      <input v-model="newRule.condition" placeholder="조건" class="border px-3 py-2 rounded text-black" />
      <input v-model="newRule.result" placeholder="결과" class="border px-3 py-2 rounded text-black" />
      <input v-model="newRule.rule_type" placeholder="규칙 유형" class="border px-3 py-2 rounded text-black" />
      <input v-model="newRule.note" placeholder="메모" class="border px-3 py-2 rounded text-black" />
      <button @click="addRule" class="bg-green-500 px-4 py-2 rounded text-white hover:bg-green-600">추가</button>
    </div>

    <table class="w-full text-left border-collapse">
      <thead>
        <tr>
          <th class="border p-2">조건</th>
          <th class="border p-2">결과</th>
          <th class="border p-2">유형</th>
          <th class="border p-2">메모</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(rule, index) in rules" :key="index">
          <td class="border p-2">{{ rule.condition }}</td>
          <td class="border p-2">{{ rule.result }}</td>
          <td class="border p-2">{{ rule.rule_type }}</td>
          <td class="border p-2">{{ rule.note }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { reactive } from 'vue'

const props = defineProps({
  rules: Array
})

const emit = defineEmits(['refresh'])
const backendUrl = import.meta.env.VITE_BACKEND_URL
const newRule = reactive({ condition: '', result: '', rule_type: '', note: '' })

async function addRule() {
  if (!newRule.condition || !newRule.result || !newRule.rule_type) return
  try {
    await fetch(`${backendUrl}/rules`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newRule)
    })
    newRule.condition = ''
    newRule.result = ''
    newRule.rule_type = ''
    newRule.note = ''
    emit('refresh')
  } catch (error) {
    console.error('규칙 추가 실패:', error)
  }
}
</script>

