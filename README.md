# FortuneAI

This repository contains a small demo consisting of a FastAPI backend and a simple Vue/Vite frontend. The backend extracts fortune telling rules from text using OpenAI, while the frontend visualises and manages these rules.

## Requirements

- Python 3.12+
- Node.js 20+

## Setup

1. **Install Python dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

2. **Install Node dependencies**
   ```bash
   npm install
   ```
   The project uses `express`, `cors` and `dotenv` in addition to `openai`.

3. **Environment variables**
   - `OPENAI_API_KEY` should be set in a `.env` file or your shell environment.
   - Optionally set `PORT` to change the port for the Node server.

## Running the project

Start the FastAPI server:
```bash
python backend/main.py
# or with uvicorn
uvicorn backend.main:app --reload
```

In another terminal, start the Node proxy:
```bash
npm start
```

The Vue application can then be served with Vite:
```bash
cd frontend
npm install
npm run dev
```

The API will be available on `http://localhost:8000` by default and the frontend on `http://localhost:5173` when using `npm run dev`.
