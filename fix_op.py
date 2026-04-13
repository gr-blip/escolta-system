content = open(r'D:\Sistema Escolta\escolta_system\cadastros\views.py', encoding='utf-8').read()
old = "        'operacional': getattr(os, 'operacional', None),"
new = "        'operacional': getattr(os, 'operacional', None),\n        'op': getattr(os, 'operacional', None),"
content = content.replace(old, new)
open(r'D:\Sistema Escolta\escolta_system\cadastros\views.py', 'w', encoding='utf-8').write(content)
print('OK' if "'op': getattr" in content else 'ERRO')
