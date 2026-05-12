release: python manage.py migrate && python manage.py collectstatic --noinput && python manage.py criar_developer --senha Smith26 && python manage.py recomprimir_fotos
web: gunicorn escolta_system.wsgi --log-file - --timeout 120 --workers 2
