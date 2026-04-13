import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'escolta_system.settings')
django.setup()

try:
    from django.template import engines
    engine = engines['django']
    t = engine.get_template('cadastros/os_print.html')
    print('Template carregou OK')
except Exception as e:
    import traceback
    traceback.print_exc()
