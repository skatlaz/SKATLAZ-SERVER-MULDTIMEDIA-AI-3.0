@echo off
python -m venv venv
call venv\Scripts\activate
python -m pip install --upgrade pip wheel setuptools
pip install -r requirements.txt
echo.
echo Instalacao concluida.
pause
