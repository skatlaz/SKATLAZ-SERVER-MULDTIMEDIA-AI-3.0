@echo off
call venv\Scripts\activate
uvicorn skatlaz_openstudio.api.server:app --host 127.0.0.1 --port 8088 --reload
pause
