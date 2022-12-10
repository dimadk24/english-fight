web: daphne -b 0.0.0.0 -p $PORT enfight.asgi:application
release: python manage.py collectstatic --no-input && python manage.py migrate
