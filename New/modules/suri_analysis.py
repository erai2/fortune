import json, os
from langchain_openai import ChatOpenAI

DB_PATH = './data/suam_analysis.json'

def load_analysis():
    if os.path.exists(DB_PATH):
        with open(DB_PATH, encoding='utf-8') as f:
            return json.load(f)
    return []

def save_analysis(data):
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def build_prompt(tiangan, dizhi, topic):
    # ... (위 예시와 동일) ...
    return prompt

def llm_auto_analysis(api_key, tiangan, dizhi, topic):
    prompt = build_prompt(tiangan, dizhi, topic)
    llm = ChatOpenAI(openai_api_key=api_key, temperature=0.2)
    response = llm.invoke(prompt)
    # (분리 파싱, 예시 참고)
    return parsed_result

# 기타 CRUD 함수(추가, 검색, 수정, 삭제 등)