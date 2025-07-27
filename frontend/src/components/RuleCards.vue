
<template>
  <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
    <div v-for="(rule, i) in rules" :key="i" class="bg-gray-700 p-6 rounded-lg shadow hover:shadow-lg transition-shadow">
      <div class="text-lg font-semibold text-primary mb-2">{{ rule.condition }}</div>
      <div class="mb-2"><span class="text-gray-400">결과:</span> {{ rule.result }}</div>
      <div class="mb-2"><span class="text-gray-400">유형:</span> {{ rule.rule_type }}</div>
      <div class="text-sm text-gray-300"><span class="text-gray-400">비고:</span> {{ rule.note }}</div>
    </div>
  </div>
  
  <div v-if="rules.length === 0" class="text-gray-400 text-center py-8">
    표시할 규칙이 없습니다.
  </div>
</template>

<script setup>
defineProps({
  rules: {
    type: Array,
    default: () => []
  }
})
</script>
