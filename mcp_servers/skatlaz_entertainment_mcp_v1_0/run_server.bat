@echo off
call venv\Scripts\activate
uvicorn skatlaz_entertainment_mcp.server:app --host 127.0.0.1 --port 8092 --reload
