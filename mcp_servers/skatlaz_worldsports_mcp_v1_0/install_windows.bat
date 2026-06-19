@echo off
echo Installing Skatlaz WorldSports MCP v1.0...
py -3.11 -m venv venv
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
echo Done.
pause
