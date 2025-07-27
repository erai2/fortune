from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
import json

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
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
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    rules = json.loads(response['choices'][0]['message']['content'])
    return {"rules": rules}

@app.get("/rules")
def get_rules():
    try:
        with open("rules.json", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error: {e}")
        return {"rules": []}

@app.post("/rules")
async def add_rule(rule: dict):
    try:
        with open("rules.json", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"rules": []}
    data['rules'].append(rule)
    with open("rules.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return {"message": "Rule added successfully."}