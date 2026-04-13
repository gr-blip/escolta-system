path = r'D:\Sistema Escolta\escolta_system\cadastros\views.py'
content = open(path, encoding='utf-8').read()
idx = content.find('MARCOS_LISTA')
print(content[idx:idx+300])
