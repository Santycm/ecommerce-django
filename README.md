# Steps to run
1. install venv: python -m venv venv
2. activate venv:
   linux: source ./venv/bin/activate
   windows: ./venv/Scripts/activate
4. install django: python -m pip install django
5. install psycopg2: python -m pip install psycopg2
6. install pillow: python -m pip install Pillow
7. create db_market in postgre
8. migrate to postgre: python manage.py migrate
9. create superuser: python manage.py createsuperuser
10. run server: python manage.py runserver
