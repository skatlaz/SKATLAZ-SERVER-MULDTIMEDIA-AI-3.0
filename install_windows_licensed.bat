@echo off
py -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python scripts\activate_license.py
python manage.py runserver
