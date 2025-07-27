
<template>
  <div class="bg-gray-800 rounded-lg shadow-lg p-6">
    <div class="flex gap-4 mb-6">
      <button @click="type='table'" :class="tabClass('table')" class="px-4 py-2 rounded">테이블</button>
      <button @click="type='cards'" :class="tabClass('cards')" class="px-4 py-2 rounded">카드</button>
      <button @click="type='mindmap'" :class="tabClass('mindmap')" class="px-4 py-2 rounded">마인드맵</button>
      <button @click="type='network'" :class="tabClass('network')" class="px-4 py-2 rounded">네트워크</button>
    </div>
    
    <RuleTable v-if="type==='table'" :rules="rules"/>
    <RuleCards v-else-if="type==='cards'" :rules="rules"/>
    <MindmapViz v-else-if="type==='mindmap'" :rules="rules"/>
    <NetworkViz v-else-if="type==='network'" :rules="rules"/>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import RuleTable from './RuleTable.vue'
import RuleCards from './RuleCards.vue'
import MindmapViz from './MindmapViz.vue'
import NetworkViz from './NetworkViz.vue'

defineProps({
  rules: {
    type: Array,
    default: () => []
  }
})

const type = ref('table')

function tabClass(t) { 
  return type.value === t ? 'text-primary underline bg-gray-700' : 'hover:bg-gray-700' 
}
</script>
