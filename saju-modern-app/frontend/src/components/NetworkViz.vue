<template>
  <div class="p-4 text-center">
    <div v-if="rules.length === 0" class="text-gray-400">네트워크 데이터 없음</div>
    <div v-else>
      <pre class="bg-gray-800 text-sky-400 p-4 rounded shadow text-left">
        {{ JSON.stringify(rules, null, 2) }}
      </pre>
      <!-- 실제 network 라이브러리 연결은 확장 구현 가능! -->
    </div>
  </div>
</template>
<script setup>
const props = defineProps({ rules: Array })
</script>
