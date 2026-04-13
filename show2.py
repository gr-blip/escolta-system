path = r'D:\Sistema Escolta\escolta_system\cadastros\views.py'
content = open(path, encoding='utf-8').read()
idx = content.find('termino_operacao')
print(repr(content[idx:idx+60]))
