
<template>
  <div class="p-4 text-center">
    <div v-if="rules.length === 0" class="text-gray-400 py-8">
      네트워크 데이터가 없습니다.
    </div>
    <div v-else class="bg-gray-700 p-6 rounded-lg">
      <h3 class="text-xl font-bold text-primary mb-4">규칙 네트워크</h3>
      <div class="bg-gray-800 text-sky-400 p-4 rounded shadow text-left overflow-auto max-h-96">
        <pre>{{ JSON.stringify(rules, null, 2) }}</pre>
      </div>
      <div class="text-sm text-gray-400 mt-4">
        * 실제 네트워크 라이브러리 연결은 확장 구현 가능
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
