release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn escolta_system.wsgi --log-file - --timeout 120 --workers 2
