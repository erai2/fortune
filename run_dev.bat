@echo off
REM Start backend and frontend servers in separate windows

REM Ensure dependencies are installed first
REM   pip install -r backend\requirements.txt
REM   (cd frontend && npm install)

start "backend" cmd /k "cd backend && uvicorn main:app --reload --port 5000"
start "frontend" cmd /k "cd frontend && npm run dev"
