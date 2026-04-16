import django, os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'escolta_system.settings')
django.setup()

from cadastros.models import OrdemServico, AssinaturaOS, DespesaOS
os_obj = OrdemServico.objects.get(pk=4)
op = getattr(os_obj, 'operacional', None)
print('os_obj OK:', os_obj)
print('op:', op)

lista = list(AssinaturaOS.objects.filter(os=os_obj).order_by('tipo'))
print('assinaturas_lista:', lista)

despesas = list(DespesaOS.objects.filter(os=os_obj))
print('despesas:', despesas)

# Testa render do template
from django.test import RequestFactory
from cadastros import views
factory = RequestFactory()
request = factory.get('/operacional/os/4/print/')

from django.contrib.auth.models import User
request.user = User.objects.filter(is_superuser=True).first()

try:
    resp = views.os_print(request, pk=4)
    print('STATUS:', resp.status_code)
except Exception as e:
    import traceback
    traceback.print_exc()
