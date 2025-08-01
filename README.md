# FortuneAI 통합 프로젝트

## 📁 구성
- `backend/`: FastAPI 규칙 API 서버
- `frontend/`: Vue 3 + Tailwind + Vite 대시보드
- 각 폴더의 `.env` 파일에서 필요한 환경 변수를 설정합니다.

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

### 3. 루트에서 동시 실행
루트 디렉터리의 Node 스크립트를 이용하면 백엔드와 프론트를 동시에 실행할 수 있습니다.
```bash
npm install
npm run dev
```

### 4. Windows 자동 실행
루트 디렉터리의 `run_dev.bat` 파일을 실행하면 백엔드와 프론트엔드가 각기 다른 콘솔 창에서 동시에 시작됩니다. 최초 실행 시에는 `backend/requirements.txt` 설치와 `frontend` 디렉터리의 `npm install`을 먼저 수행하세요.

### 5. Docker Compose 실행
Docker가 설치되어 있다면 다음 명령으로 두 서비스를 함께 시작할 수 있습니다.
```bash
docker compose up --build
```
이후 [http://localhost:5173](http://localhost:5173) 로 접속하면 됩니다.
컨테이너 간 통신을 위해 프론트엔드에는 `VITE_BACKEND_URL=http://backend:8000` 환경 변수가 자동으로 지정됩니다.

접속: http://localhost:5173

### 무료 백엔드 호스팅 추천
FastAPI로 작성된 백엔드는 Docker 이미지를 이용해 무료 호스팅 서비스에 배포할 수 있습니다.
다음과 같은 플랫폼을 이용하면 개인 프로젝트 용도로 부담 없이 사용할 수 있습니다.

- [Railway](https://railway.app/) – 간단한 Docker 배포와 환경 변수 설정을 지원합니다.
- [Render](https://render.com/) – 무료 웹 서비스 플랜으로 소규모 API를 운용할 수 있습니다.

각 플랫폼의 가이드를 참고하여 `docker compose` 명령 대신 Docker 이미지를 빌드해 업로드하면 됩니다.

## 🧠 AI 추출 모델 학습
```bash
POST http://localhost:8000/train
```

서버 콘솔에 규칙 목록 출력됨
