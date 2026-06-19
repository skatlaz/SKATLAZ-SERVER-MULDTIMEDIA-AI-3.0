@echo off
call venv\Scripts\activate
python -m pip install --upgrade pip wheel setuptools
pip install audiocraft sentencepiece transformers accelerate
pause
