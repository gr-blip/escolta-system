path = r'D:\Sistema Escolta\escolta_system\cadastros\views.py'
content = open(path, encoding='utf-8').read()
idx = content.find('assinatura_tipos')
print(content[idx-50:idx+200])
