import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'escolta_system.settings')
django.setup()

# Verifica qual pk existe no banco local
from cadastros.models import OrdemServico
pks = list(OrdemServico.objects.values_list('pk', flat=True)[:5])
print('PKs disponiveis:', pks)
