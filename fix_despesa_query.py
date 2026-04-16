path = r'D:\Sistema Escolta\escolta_system\cadastros\views.py'
content = open(path, encoding='utf-8').read()

old = "    despesas = DespesaOS.objects.filter(os=os_obj).order_by('ocorrido_em')"
new = "    despesas = DespesaOS.objects.filter(os_id=os_obj.pk).order_by('ocorrido_em')"

if old in content:
    content = content.replace(old, new)
    open(path, 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('ERRO')
