path = r'D:\Sistema Escolta\escolta_system\cadastros\views.py'
content = open(path, encoding='utf-8').read()
idx = content.find('termino_operacao')
trecho = content[idx:idx+50]
print([hex(ord(c)) for c in trecho])
