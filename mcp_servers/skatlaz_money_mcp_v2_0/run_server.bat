@echo off
call venv\Scripts\activate
uvicorn skatlaz_money_mcp.server:app --host 127.0.0.1 --port 8020 --reload
pause
