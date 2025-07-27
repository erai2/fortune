<template>
  <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
    <div v-for="(rule, i) in rules" :key="i" class="bg-gray p-4 rounded shadow">
      <div class="text-lg font-semibold text-primary">{{ rule.condition }}</div>
      <div class="mt-1">결과: {{ rule.result }}</div>
      <div class="mt-1">유형: {{ rule.rule_type }}</div>
      <div class="mt-1 text-sm text-gray-300">비고: {{ rule.note }}</div>
    </div>
  </div>
</template>
<script setup>
const props = defineProps({ rules: Array })
</script>
