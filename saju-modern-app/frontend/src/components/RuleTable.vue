<template>
  <div>
    <div class="mb-4 flex gap-2">
      <button class="bg-primary text-white px-4 py-2 rounded" @click="exportRules('json')">JSON</button>
      <button class="bg-primary text-white px-4 py-2 rounded" @click="exportRules('excel')">Excel</button>
      <button class="bg-primary text-white px-4 py-2 rounded" @click="exportRules('pdf')">PDF</button>
    </div>
    <table class="w-full bg-gray-900 text-white rounded shadow">
      <thead><tr class="bg-gray"><th>조건</th><th>결과</th><th>유형</th><th>비고</th></tr></thead>
      <tbody>
        <tr v-for="(rule,i) in rules" :key="i">
          <td>{{rule.condition}}</td>
          <td>{{rule.result}}</td>
          <td>{{rule.rule_type}}</td>
          <td>{{rule.note}}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
<script setup>
import * as XLSX from "xlsx"
import jsPDF from "jspdf"
const props = defineProps({ rules: Array })
function exportRules(type) {
  if(type==="json"){
    const blob=new Blob([JSON.stringify(props.rules,null,2)],{type:"application/json"});
    const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download="rules.json";a.click();
  } else if(type==="excel"){
    const ws=XLSX.utils.json_to_sheet(props.rules);const wb=XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb,ws,"Rules");XLSX.writeFile(wb,"rules.xlsx");
  } else if(type==="pdf"){
    const doc=new jsPDF();props.rules.forEach((r,i)=>doc.text(`${i+1}. ${r.condition} → ${r.result}`,10,10+i*10));
    doc.save("rules.pdf");
  }
}
</script>
