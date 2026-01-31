@echo off
REM Simple starter script for Windows
python -m uvicorn main:app --host 0.0.0.0 --port 8000
pause

