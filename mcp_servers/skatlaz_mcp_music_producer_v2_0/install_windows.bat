@echo off
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
echo.
echo Instalacao concluida. Se usar stems, rode: python -m pip install demucs
echo FFmpeg deve estar em C:\ffmpeg\bin ou no PATH.
pause
