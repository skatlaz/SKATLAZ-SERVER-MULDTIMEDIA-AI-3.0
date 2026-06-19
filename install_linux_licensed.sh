#!/usr/bin/env bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python scripts/activate_license.py
python manage.py runserver 0.0.0.0:8000
