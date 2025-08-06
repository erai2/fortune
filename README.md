# FortuneAI 통합 프로젝트

## 📁 구성
- `backend/`: FastAPI + SQLite 규칙 API 서버
- `frontend/`: Vue 3 + Tailwind + Vite 기반 대시보드
- `.env`: 백엔드 URL 설정 (프론트에서 사용)

## ▶ 실행 방법

### 1. 백엔드 실행 (Python 3.8+)
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 5000
```

### 2. 프론트엔드 실행
```bash
cd frontend
npm install
npm run dev
```

### 3. Streamlit 명리 텍스트 구조화 (선택)
```bash
streamlit run app.py
```

### 4. Windows 자동 실행
루트 디렉터리의 `run_dev.bat` 파일을 실행하면 백엔드와 프론트엔드가 각기 다른 콘솔 창에서 동시에 시작됩니다. 최초 실행 시에는 `backend/requirements.txt` 설치와 `frontend` 디렉터리의 `npm install`을 먼저 수행하세요.

접속: http://localhost:5173
