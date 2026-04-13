path = r'D:\Sistema Escolta\escolta_system\cadastros\views.py'
content = open(path, encoding='utf-8').read()
old = "        'operacional': getattr(os, 'operacional', None),"
new = "        'operacional': getattr(os, 'operacional', None),\n        'op': getattr(os, 'operacional', None),"
if old in content:
    content = content.replace(old, new)
    open(path, 'w', encoding='utf-8').write(content)
    print('OK - fix aplicado')
else:
    print('ERRO - trecho nao encontrado')
