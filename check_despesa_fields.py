import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'escolta_system.settings')
django.setup()
from cadastros.models import DespesaOS
print([f.name for f in DespesaOS._meta.get_fields()])
