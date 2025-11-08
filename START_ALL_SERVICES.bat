@echo off
echo ========================================
echo Starting LoanIQ Full Stack Application
echo ========================================
echo.

echo [1/2] Starting FastAPI Backend on port 8000...
start "LoanIQ Backend" cmd /k "cd /d C:\Lab3\Lab3 && python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak >nul

echo [2/2] Starting Next.js Frontend on port 3000...
start "LoanIQ Frontend" cmd /k "cd /d C:\Lab3\Lab3\frontend && npm run dev"

timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo All Services Started!
echo ========================================
echo.
echo Backend API:  http://localhost:8000
echo API Docs:     http://localhost:8000/docs
echo Frontend App: http://localhost:3000
echo.
echo Press Ctrl+C in each window to stop services
echo ========================================
