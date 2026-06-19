@echo off
py -3.11 -m venv venv
call venv\Scripts\activate
python -m pip install --upgrade pip wheel setuptools
pip install -r requirements.txt
echo.
echo Instale tambem FFmpeg e adicione ao PATH: C:\ffmpeg\bin
echo Para OCR, instale Tesseract OCR se for usar pytesseract.
pause
