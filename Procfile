web: gunicorn main:app
worker: python ./counter/counter_main.py
init: python manage.py db init
migrate: python manage.py db migrate
upgrade: python manage.py db upgrade