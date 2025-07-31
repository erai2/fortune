from fastapi import UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
import json
import logging
from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "AI 규칙 대시보드 API"}

# Secure CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 보안상 실제 배포 시에는 도메인을 지정하는 것이 좋습니다.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client securely
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configure logging
logging.basicConfig(level=logging.INFO)


@app.post("/extract_rules")
async def extract_rules(file: UploadFile = File(...)):
    # Validate file type and size
    if not file.content_type or not file.content_type.startswith('text/'):
        raise HTTPException(status_code=400,
                            detail="Only text files are allowed")

    MAX_FILE_SIZE = 10 * 1024 * 1024
    file_content = await file.read()
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    try:
        text = file_content.decode('utf-8')
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Invalid text encoding")

    # Limit text length for security
    if len(text) > 50000:
        text = text[:50000]

    prompt = f"""
아래는 명리학 사례 데이터입니다. 이 텍스트에서 'condition', 'result', 'rule_type', 'note' 형태의 규칙 JSON을 5개만 추출해줘:
{text[:5000]}
예시:
[
  {{"condition":"일간=갑, 월지=오", "result":"목화 조화 구조", "rule_type":"격국", "note":"화생토 가능성"}},
  ...
]
"""

    try:
        response = openai_client.chat.completions.create(model="gpt-4",
                                                         messages=[{
                                                             "role":
                                                             "user",
                                                             "content":
                                                             prompt
                                                         }],
                                                         temperature=0.3,
                                                         max_tokens=2000)
        rules_text = response.choices[0].message.content

        if rules_text is None:
            logging.warning("OpenAI response was empty.")
            return {"rules": []}

        try:
            rules = json.loads(rules_text)
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON received from OpenAI: {e}")
            raise HTTPException(status_code=500,
                                detail="Invalid JSON from OpenAI")

        return {"rules": rules}
    except Exception as e:
        logging.error(f"OpenAI API error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process text")


@app.get("/rules")
def get_rules():
    try:
        with open("rules.json", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"rules": []}
    except Exception as e:
        logging.error(f"Error reading rules: {e}")
        raise HTTPException(status_code=500, detail="Failed to read rules")


@app.post("/rules")
async def add_rule(rule: dict):
    # Validate rule structure
    required_fields = ["condition", "result", "rule_type", "note"]
    if not all(field in rule for field in required_fields):
        raise HTTPException(status_code=400, detail="Missing required fields")

    # Validate field lengths
    for field, value in rule.items():
        if not isinstance(value, str) or len(value) > 1000:
            raise HTTPException(status_code=400, detail=f"Invalid {field}")

    try:
        try:
            with open("rules.json", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {"rules": []}

        # Limit total rules (prevent DoS)
        if len(data.get("rules", [])) >= 10000:
            raise HTTPException(status_code=400,
                                detail="Maximum rules limit reached")

        data['rules'].append(rule)
        with open("rules.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return {"message": "Rule added successfully."}
    except Exception as e:
        logging.error(f"Error adding rule: {e}")
        raise HTTPException(status_code=500, detail="Failed to add rule")
