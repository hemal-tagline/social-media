python manage.py migrate

gunicorn social_media.wsgi --bind 0.0.0.0:8000 --access-logfile '-'
