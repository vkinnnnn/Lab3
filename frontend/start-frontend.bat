@echo off
echo ========================================
echo  Loan Intelligence Frontend
echo  Starting development server...
echo ========================================
echo.

cd /d "%~dp0"
npm run dev -- -p 3002

pause
