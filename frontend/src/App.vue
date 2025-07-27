<template>
  <div class="min-h-screen bg-dark text-white">
    <nav class="bg-gray flex items-center justify-between px-8 py-4 shadow">
      <div class="text-2xl font-bold text-primary">AI 사주 규칙 대시보드</div>
      <div class="flex gap-4">
        <button @click="tab='rules'" :class="tabClass('rules')">규칙관리</button>
        <button @click="tab='viz'" :class="tabClass('viz')">시각화</button>
        <button @click="tab='ai'" :class="tabClass('ai')">AI 추출</button>
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
function tabClass(t){ return tab.value===t ? 'text-primary underline' : '' }
function setRules(newRules){ rules.value = newRules }
async function fetchRules(){
  const res = await fetch('/rules'); rules.value = (await res.json()).rules
}
onMounted(fetchRules)
</script>
<style>
body, html { background: #191D24; color: #fff; }
</style>
