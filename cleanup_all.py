import os

# Remove arquivos temporários
files_to_remove = [
    r'D:\Sistema Escolta\escolta_system\temp_debug.txt',
    r'D:\Sistema Escolta\escolta_system\test.py',
    r'D:\Sistema Escolta\escolta_system\fix_op.py',
    r'D:\Sistema Escolta\escolta_system\fix_views.py',
    r'D:\Sistema Escolta\escolta_system\check_op.py',
    r'D:\Sistema Escolta\escolta_system\cleanup.py',
]
for f in files_to_remove:
    if os.path.exists(f):
        os.remove(f)
        print(f'Removido: {f}')

# Remove rotas de debug do urls.py
urls_path = r'D:\Sistema Escolta\escolta_system\cadastros\urls.py'
content = open(urls_path, encoding='utf-8').read()
# Remove bloco debug-media
content = content.replace("\nurlpatterns += [\n    _path('debug-media/', views.debug_media, name='debug_media'),\n]", '')
# Remove bloco debug-op
content = content.replace("\nurlpatterns += [\n    _path('debug-op/', views.debug_op, name='debug_op'),\n]", '')
open(urls_path, 'w', encoding='utf-8').write(content)
print('urls.py limpo')

# Remove view debug_op do views.py
views_path = r'D:\Sistema Escolta\escolta_system\cadastros\views.py'
content = open(views_path, encoding='utf-8').read()
# Remove debug_op function
import re
content = re.sub(r'\nfrom django\.http import JsonResponse\nfrom cadastros\.models import OSOperacional\n\ndef debug_op\(request\):.*?}\)\n', '', content, flags=re.DOTALL)
open(views_path, 'w', encoding='utf-8').write(content)
print('views.py limpo')

print('TUDO OK')
