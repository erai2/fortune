FortuneAI/
├── backend/
│   └── main.py
├── frontend/
│   ├── package.json
│   ├── .env
│   └── src/

pip install fastapi uvicorn

uvicorn main:app --reload --port 8000

cd frontend
npm install

#chk! VITE_BACKEND_URL=http://localhost:(____)
npm run dev
