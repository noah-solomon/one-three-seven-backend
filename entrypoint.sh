#!/usr/bin/env bash
echo "Database Url:"
heroku config:get DATABASE_URL -a ots-tasks-backend
flask db init
flask db migrate
flask db upgrade
gunicorn app:app