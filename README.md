# FortuneAI 통합 프로젝트

## 📁 구성
- `backend/`: FastAPI + SQLite 규칙 API 서버
- `frontend/`: Vue 3 + Tailwind + Vite 기반 대시보드
- `.env`: 백엔드 URL 설정 (프론트에서 사용)

## ▶ 실행 방법

### 1. 백엔드 실행 (Python 3.8+)
```bash
cd backend
pip install fastapi uvicorn sqlalchemy pydantic
uvicorn main:app --reload --port 8000
```

### 2. 프론트엔드 실행
```bash
cd frontend
npm install
npm run dev
```

접속: http://localhost:5173

## 🧠 AI 추출 모델 학습
```bash
POST http://localhost:8000/train
```

서버 콘솔에 규칙 목록 출력됨
