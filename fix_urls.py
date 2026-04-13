path = r'D:\Sistema Escolta\escolta_system\cadastros\urls.py'
content = open(path, encoding='utf-8').read()
content = content.replace("\nurlpatterns += [\n    _path('debug-media/', views.debug_media, name='debug_media'),\n]", '')
content = content.replace("\nurlpatterns += [\n    _path('debug-op/', views.debug_op, name='debug_op'),\n]", '')
open(path, 'w', encoding='utf-8').write(content)
print('OK')
