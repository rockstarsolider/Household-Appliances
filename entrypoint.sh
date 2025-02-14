#!/bin/ash
ulimit -n 10032  
echo "Apply database migrations"
python manage.py migrate

exec "$@"