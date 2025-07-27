
<template>
  <div class="p-4 text-center">
    <div v-if="rules.length === 0" class="text-gray-400 py-8">
      마인드맵 데이터가 없습니다.
    </div>
    <div v-else class="bg-gray-700 p-6 rounded-lg">
      <h3 class="text-xl font-bold text-primary mb-4">규칙 마인드맵</h3>
      <div class="text-left">
        <div v-for="(rule, i) in rules" :key="i" class="mb-4 p-4 bg-gray-600 rounded border-l-4 border-primary">
          <div class="font-semibold">{{ rule.condition }}</div>
          <div class="text-sm text-gray-300 mt-1">→ {{ rule.result }}</div>
        </div>
      </div>
      <div class="text-sm text-gray-400 mt-4">
        * 실제 마인드맵 라이브러리 연결은 확장 구현 가능
      </div>
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
</script>
