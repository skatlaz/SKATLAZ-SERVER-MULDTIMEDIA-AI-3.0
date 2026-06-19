@echo off
call venv\Scripts\activate
python -m uvicorn server:app --host 127.0.0.1 --port 8092 --reload
pause
