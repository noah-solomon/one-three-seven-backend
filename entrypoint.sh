#!/usr/bin/env bash
heroku pg:wait -a ots-tasks-backend
flask db init
flask db migrate
flask db upgrade
gunicorn app:app