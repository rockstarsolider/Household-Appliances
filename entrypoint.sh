#!/bin/sh  

# Exit immediately if a command exits with a non-zero status.  
set -e   

# Run migrations  
echo "Running migrations..."  
python manage.py migrate  

# Collect static files (if needed)  
echo "Collecting static files..."  
python manage.py collectstatic --noinput  

# Start the Django application  
echo "Starting Django server..."  
exec python manage.py runserver 0.0.0.0:8000 