path = r'D:\Sistema Escolta\escolta_system\cadastros\views.py'
content = open(path, encoding='utf-8').read()
# Acha todas as ocorrencias
import re
for m in re.finditer(r"return JsonResponse\(\{'ok': True\}\)", content):
    print(m.start(), repr(content[m.start()-50:m.start()+40]))
    print('---')
