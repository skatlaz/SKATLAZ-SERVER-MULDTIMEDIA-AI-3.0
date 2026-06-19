@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
title Skatlaz Server AI 3.0 + MCP Servers

echo ======================================================
echo  SKATLAZ SERVER AI 3.0 - START ALL MCP SERVERS
echo ======================================================
echo.

if not exist venv (
  echo [1/4] Criando ambiente virtual principal...
  py -m venv venv
)
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
if exist requirements.txt pip install -r requirements.txt
if exist requirements_ai_mcp.txt pip install -r requirements_ai_mcp.txt

echo.
echo [2/4] Preparando banco de dados Django...
python manage.py migrate

echo.
echo [3/4] Iniciando MCP Servers em janelas separadas...

call :start_mcp "Entertainment MCP" "mcp_servers\skatlaz_entertainment_mcp_v1_0" "uvicorn skatlaz_entertainment_mcp.server:app --host 127.0.0.1 --port 8092 --reload"
call :start_mcp "GexProg DeepSeek Code MCP" "mcp_servers\skatlaz_gexprog_mcp_v1_0" "uvicorn server:app --host 127.0.0.1 --port 8077 --reload"
call :start_mcp "InfoToday MCP" "mcp_servers\skatlaz_infotoday_mcp" "python -m uvicorn server:app --host 127.0.0.1 --port 8093 --reload"
call :start_mcp "Music Producer 1.1 MCP" "mcp_servers\skatlaz_mcp_music_producer_v1_1" "uvicorn mcp_server:app --host 127.0.0.1 --port 8787 --reload"
call :start_mcp "Music Producer 2.0 MCP" "mcp_servers\skatlaz_mcp_music_producer_v2_0" "uvicorn mcp_server:app --host 127.0.0.1 --port 8788 --reload"
call :start_mcp "Office AI Worker MCP" "mcp_servers\skatlaz_mcp_office_ai_worker_v2_1" "python main.py server"
call :start_mcp "Money MCP" "mcp_servers\skatlaz_money_mcp_v2_0" "uvicorn skatlaz_money_mcp.server:app --host 127.0.0.1 --port 8020 --reload"
call :start_mcp "OpenStudio MCP" "mcp_servers\skatlaz_openstudio_mcp_v2_0" "uvicorn skatlaz_openstudio.api.server:app --host 127.0.0.1 --port 8088 --reload"
call :start_mcp "Studies MCP" "mcp_servers\skatlaz_studies_mcp_v2_0" "uvicorn skatlaz_studies_mcp.server:app --host 127.0.0.1 --port 8045 --reload"
call :start_mcp "SurfTask MCP" "mcp_servers\skatlaz_surftask_mcp_v1_0" "uvicorn skatlaz_surftask_mcp.server:app --host 127.0.0.1 --port 8790 --reload"
call :start_mcp "WorldSports MCP" "mcp_servers\skatlaz_worldsports_mcp_v1_0" "python main.py server"

echo.
echo [4/4] Iniciando Skatlaz Server AI 3.0 em http://localhost:8000/
echo Abra o navegador em: http://localhost:8000/
echo.
python manage.py runserver 127.0.0.1:8000
pause
exit /b

:start_mcp
set "MCP_TITLE=%~1"
set "MCP_DIR=%~2"
set "MCP_CMD=%~3"
if exist "%MCP_DIR%" (
  echo Starting %MCP_TITLE%...
  start "%MCP_TITLE%" cmd /k "cd /d %%~dp0%MCP_DIR% && if not exist venv py -m venv venv && call venv\Scripts\activate.bat && if exist requirements.txt pip install -r requirements.txt && %MCP_CMD%"
) else (
  echo [WARN] Pasta nao encontrada: %MCP_DIR%
)
exit /b
