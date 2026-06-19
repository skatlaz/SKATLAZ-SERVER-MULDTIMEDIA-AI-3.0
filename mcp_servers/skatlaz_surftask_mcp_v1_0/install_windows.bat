@echo off
py -3.11 -m venv venv
call venv\Scripts\activate
python -m pip install --upgrade pip wheel setuptools
pip install -r requirements.txt
python -m playwright install chromium
echo.
echo Instalacao concluida.
echo Para OCR, instale tambem o Tesseract OCR no Windows se desejar usar leitura de imagens.
pause
