#!/bin/bash
set -e
mkdir -p saju-modern-app/backend
mkdir -p saju-modern-app/frontend/src/components

# ---------- backend/main.py ----------
cat > saju-modern-app/backend/main.py << 'EOF'
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import openai, os, json

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/extract_rules")
async def extract_rules(file: UploadFile = File(...)):
    text = (await file.read()).decode()
    prompt = f"""
아래는 명리학 사례 데이터입니다. 이 텍스트에서 'condition', 'result', 'rule_type', 'note' 형태의 규칙 JSON을 5개만 추출해줘:
{text}
예시:
[
  {{"condition":"일간=갑, 월지=오", "result":"목화 조화 구조", "rule_type":"격국", "note":"화생토 가능성"}},
  ...
]
"""
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role":"user","content":prompt}],
        temperature=0.3
    )
    rules = json.loads(response['choices'][0]['message']['content'])
    return {"rules": rules}

@app.get("/rules")
def get_rules():
    try:
        with open("rules.json", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"rules": []}

@app.post("/rules")
async def add_rule(rule: dict):
    try:
        with open("rules.json", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = {"rules": []}
    data['rules'].append(rule)
    with open("rules.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return {"ok": True}
EOF

# ---------- backend/rules.json ----------
cat > saju-modern-app/backend/rules.json << 'EOF'
{
  "rules": [
    {
      "condition": "일간=무, 월지=술",
      "result": "토기운이 강한 구조",
      "rule_type": "격국판별",
      "note": "토생금 가능성 있음"
    },
    {
      "condition": "일간=정, 월지=자",
      "result": "수생화의 조화 구조",
      "rule_type": "오행판별",
      "note": "정화가 수기운을 활용함"
    }
  ]
}
EOF

# ---------- backend/requirements.txt ----------
cat > saju-modern-app/backend/requirements.txt << 'EOF'
fastapi
uvicorn
openai
EOF

# ---------- frontend/package.json ----------
cat > saju-modern-app/frontend/package.json << 'EOF'
{
  "name": "saju-modern-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.4.0",
    "xlsx": "^0.18.5",
    "jspdf": "^2.5.1"
  },
  "devDependencies": {
    "vite": "^4.0.0",
    "tailwindcss": "^3.4.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "@vitejs/plugin-vue": "^4.0.0"
  }
}
EOF

# ---------- frontend/vite.config.js ----------
cat > saju-modern-app/frontend/vite.config.js << 'EOF'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/extract_rules': 'http://localhost:8000',
      '/rules': 'http://localhost:8000'
    }
  }
})
EOF

# ---------- frontend/tailwind.config.js ----------
cat > saju-modern-app/frontend/tailwind.config.js << 'EOF'
module.exports = {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
        dark: '#191D24',
        gray: '#374151',
      },
    },
  },
  darkMode: 'class',
  plugins: [],
}
EOF

# ---------- frontend/index.html ----------
cat > saju-modern-app/frontend/index.html << 'EOF'
<!DOCTYPE html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <title>AI 사주 규칙 대시보드</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
  </head>
  <body class="bg-dark text-white">
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
EOF

# ---------- frontend/src/main.js ----------
cat > saju-modern-app/frontend/src/main.js << 'EOF'
import { createApp } from "vue"
import App from "./App.vue"
import "./index.css"
createApp(App).mount("#app")
EOF

# ---------- frontend/src/index.css ----------
cat > saju-modern-app/frontend/src/index.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;
EOF

# ---------- frontend/src/App.vue ----------
cat > saju-modern-app/frontend/src/App.vue << 'EOF'
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
EOF

# ---------- frontend/src/components/RuleTable.vue ----------
cat > saju-modern-app/frontend/src/components/RuleTable.vue << 'EOF'
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
EOF

# ---------- frontend/src/components/VizTabs.vue ----------
cat > saju-modern-app/frontend/src/components/VizTabs.vue << 'EOF'
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
EOF

# ---------- frontend/src/components/RuleCards.vue ----------
cat > saju-modern-app/frontend/src/components/RuleCards.vue << 'EOF'
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
EOF

# ---------- frontend/src/components/MindmapViz.vue ----------
cat > saju-modern-app/frontend/src/components/MindmapViz.vue << 'EOF'
<template>
  <div class="p-4 text-center">
    <div v-if="rules.length === 0" class="text-gray-400">MindMap 데이터 없음</div>
    <div v-else>
      <pre class="bg-gray-800 text-primary p-4 rounded shadow text-left">
        {{ JSON.stringify(rules, null, 2) }}
      </pre>
      <!-- 실제 mindmap 라이브러리 연결은 확장 구현 가능! -->
    </div>
  </div>
</template>
<script setup>
const props = defineProps({ rules: Array })
</script>
EOF

# ---------- frontend/src/components/NetworkViz.vue ----------
cat > saju-modern-app/frontend/src/components/NetworkViz.vue << 'EOF'
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
EOF

# ---------- frontend/src/components/AiExtractor.vue ----------
cat > saju-modern-app/frontend/src/components/AiExtractor.vue << 'EOF'
<template>
  <div class="max-w-xl mx-auto bg-gray-800 p-6 rounded shadow mt-6">
    <form @submit.prevent="uploadFile">
      <div class="mb-2">
        <input type="file" ref="fileInput" class="bg-gray border p-2 rounded w-full text-white"/>
      </div>
      <button type="submit" class="bg-primary px-4 py-2 rounded text-white">AI 규칙 추출</button>
    </form>
    <div v-if="loading" class="mt-4 text-sky-400">AI 분석중...</div>
    <div v-if="error" class="mt-2 text-red-400">{{ error }}</div>
  </div>
</template>
<script setup>
import { ref } from 'vue'
const emit = defineEmits(['rules'])
const fileInput = ref(null)
const loading = ref(false)
const error = ref('')
async function uploadFile() {
  if (!fileInput.value.files[0]) { error.value = "파일을 선택해주세요."; return; }
  loading.value = true; error.value = ""
  const form = new FormData()
  form.append('file', fileInput.value.files[0])
  const res = await fetch('/extract_rules', { method: 'POST', body: form })
  const data = await res.json()
  if (data.rules) emit('rules', data.rules)
  else error.value = "AI 추출 실패"; loading.value = false
  loading.value = false
}
</script>
EOF

# ---------- frontend/README.md ----------
cat > saju-modern-app/README.md << 'EOF'
# AI 사주 규칙 대시보드 (OpenAI 연동, 시각화/카드/엑셀/PDF)

## 1. 백엔드 준비
cd backend
pip install -r requirements.txt

(필수) OpenAI API KEY를 환경변수로 등록
export OPENAI_API_KEY=sk-xxx  # 리눅스/맥
# set OPENAI_API_KEY=sk-xxx   # 윈도우

## 2. 프론트엔드 준비
cd ../frontend
npm install

## 3. 실행
cd ../backend
uvicorn main:app --reload
cd ../frontend
npm run dev

## 4. 접속
브라우저에서 http://localhost:5173

### 주요 기능
- 규칙 관리(표, 카드, Mindmap, 네트워크)
- AI 자동 규칙 추출(OpenAI)
- PDF/엑셀/JSON 내보내기, 반응형
EOF

echo "모든 파일/폴더가 saju-modern-app/ 아래 자동 생성되었습니다!"
echo "README.md 안내대로 OpenAI 키 설정, 백엔드/프론트 설치 후 실행하세요."