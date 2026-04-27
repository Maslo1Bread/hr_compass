@echo off
chcp 65001 > nul
cd /d %~dp0
if not exist .venv (
  python -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install -r requirements.txt
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
pause
