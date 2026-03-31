release: echo "Running migrations..." && python manage.py migrate && echo "Migrations completed."
web: gunicorn project.wsgi:application