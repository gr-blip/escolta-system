path = r'D:\Sistema Escolta\escolta_system\cadastros\views.py'
content = open(path, encoding='utf-8').read()
import re
# Acha todos os trechos com o char bugado
matches = re.findall(r'.{0,20}' + chr(0x251c) + r'.{0,20}', content)
for m in set(matches):
    print(repr(m))
