import django, os, traceback
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'escolta_system.settings')
django.setup()
from cadastros import views
import inspect
src = inspect.getsource(views.os_print)
print(src[:2000])
