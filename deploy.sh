#!/bin/bash

cd DocManageSystem
python3 manage.py makemigrations usermanagement
python3 manage.py migrate
python3 manage.py runserver