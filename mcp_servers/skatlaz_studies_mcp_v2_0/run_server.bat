@echo off
call venv\Scripts\activate
uvicorn skatlaz_studies_mcp.server:app --host 127.0.0.1 --port 8045 --reload
pause
