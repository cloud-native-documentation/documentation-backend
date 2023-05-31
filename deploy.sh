#!/bin/sh

cd DocManageSystem

if [ "$1" = "delete" ]; then
  rm -rf store/db/*
  rm -rf store/files
else
  python3 manage.py migrate
  python3 manage.py runserver 0.0.0.0:8000
fi