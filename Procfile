release: python manage.py migrate
web: run-program waitress-serve --port=$PORT gunicorn qr_reader.wsgi
