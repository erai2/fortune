<template>
  <div>
    <div class="flex gap-2 mb-2">
      <button @click="type='table'" :class="tabClass('table')">표</button>
      <button @click="type='cards'" :class="tabClass('cards')">카드</button>
      <button @click="type='mindmap'" :class="tabClass('mindmap')">MindMap</button>
      <button @click="type='network'" :class="tabClass('network')">네트워크</button>
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
const props = defineProps({ rules: Array })
const type = ref('table')
function tabClass(t){ return type.value===t ? 'text-primary underline' : '' }
</script>
