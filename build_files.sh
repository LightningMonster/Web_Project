#!/bin/bash
pip install -r requirements.txt
python manage.py collectstatic
python manage.py migrate
