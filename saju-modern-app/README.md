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
