path = r'D:\Sistema Escolta\escolta_system\cadastros\models.py'
content = open(path, encoding='utf-8').read()
idx = content.find('class DespesaOS')
print(content[idx:idx+1000])
