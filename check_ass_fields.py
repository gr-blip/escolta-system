import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'escolta_system.settings')
django.setup()
from cadastros.models import AssinaturaOS
print('AssinaturaOS:', [f.name for f in AssinaturaOS._meta.get_fields()])
