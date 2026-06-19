@echo off
call venv\Scripts\activate
uvicorn skatlaz_surftask_mcp.server:app --host 127.0.0.1 --port 8787 --reload
pause
