@echo off
python -c "import pandas,docx,pypdf,openpyxl,pptx,fastapi,cryptography,qrcode; print('Dependencias principais OK')"
python -c "import pytesseract; print('pytesseract OK - lembre de instalar o Tesseract EXE no Windows')" 2>NUL
pause
