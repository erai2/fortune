-cd frontend
npm install
npm run dev
<template>
  <div class="bg-gray-800 rounded-lg shadow-lg p-6">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-bold text-primary">규칙 관리</h2>
      <button @click="$emit('refresh')" class="bg-primary text-white px-4 py-2 rounded hover:bg-blue-600">
        새로고침
      </button>
    </div>
    
    <div v-if="rules.length === 0" class="text-gray-400 text-center py-8">
      등록된 규칙이 없습니다.
    </div>
    
    <div v-else class="overflow-x-auto">
      <table class="w-full text-left">
        <thead>
          <tr class="border-b border-gray-600">
            <th class="py-3 px-4 text-primary">조건</th>
            <th class="py-3 px-4 text-primary">결과</th>
            <th class="py-3 px-4 text-primary">유형</th>
            <th class="py-3 px-4 text-primary">비고</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(rule, i) in rules" :key="i" class="border-b border-gray-700 hover:bg-gray-700">
            <td class="py-3 px-4">{{ rule.condition }}</td>
            <td class="py-3 px-4">{{ rule.result }}</td>
            <td class="py-3 px-4">{{ rule.rule_type }}</td>
            <td class="py-3 px-4 text-gray-300">{{ rule.note }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
defineProps({
  rules: {
    type: Array,
    default: () => []
  }
})

defineEmits(['refresh'])
</script>
