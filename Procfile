release: python manage.py migrate && python manage.py collectstatic --noinput && python manage.py criar_developer --senha Smith26
web: gunicorn escolta_system.wsgi --log-file - --timeout 300 --workers 2 --worker-class gthread --threads 4
