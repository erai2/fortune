<template>
  <div class="min-h-screen bg-dark text-white">
    <nav class="bg-gray-800 flex items-center justify-between px-8 py-4 shadow">
      <div class="text-2xl font-bold text-primary">AI 사주 규칙 대시보드</div>
      <div class="flex gap-4">
        <button @click="tab='rules'" :class="tabClass('rules')" class="px-4 py-2 rounded">규칙관리</button>
        <button @click="tab='viz'" :class="tabClass('viz')" class="px-4 py-2 rounded">시각화</button>
        <button @click="tab='ai'" :class="tabClass('ai')" class="px-4 py-2 rounded">AI 추출</button>
      </div>
    </nav>
    <main class="p-8">
      <RuleTable v-if="tab==='rules'" :rules="rules" @refresh="fetchRules"/>
      <VizTabs v-else-if="tab==='viz'" :rules="rules"/>
      <AiExtractor v-else-if="tab==='ai'" @rules="setRules"/>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import RuleTable from './components/RuleTable.vue'
import VizTabs from './components/VizTabs.vue'
import AiExtractor from './components/AiExtractor.vue'

const tab = ref('rules')
const rules = ref([])

function tabClass(t) { 
  return tab.value === t ? 'text-primary underline bg-gray-700' : 'hover:bg-gray-700' 
}

function setRules(newRules) { 
  rules.value = newRules 
}

async function fetchRules() {
  try {
    const res = await fetch('/rules')
    const data = await res.json()
    rules.value = data.rules || []
  } catch (error) {
    console.error('규칙 조회 실패:', error)
    rules.value = []
  }
}

onMounted(fetchRules)
</script>