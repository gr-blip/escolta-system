import re

path = r'D:\Sistema Escolta\escolta_system\cadastros\views.py'
content = open(path, encoding='utf-8').read()

# Remove tudo a partir de "from django.conf import settings\ndef debug_media"
marker = '\nfrom django.conf import settings\ndef debug_media(request):'
idx = content.find(marker)
if idx > 0:
    content = content[:idx]
    print(f'Removido bloco debug a partir da posicao {idx}')
else:
    print('Marcador nao encontrado - verificar manualmente')

open(path, 'w', encoding='utf-8').write(content)
print('Ultimas 5 linhas:')
print('\n'.join(content.strip().split('\n')[-5:]))
print('DONE')
