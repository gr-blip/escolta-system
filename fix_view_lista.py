path = r'D:\Sistema Escolta\escolta_system\cadastros\views.py'
content = open(path, encoding='utf-8').read()

old = "        'assinaturas': assinaturas,"
new = "        'assinaturas_lista': list(AssinaturaOS.objects.filter(os=os_obj).order_by('tipo')),"

if old in content:
    content = content.replace(old, new)
    open(path, 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('ERRO - trecho nao encontrado')
    # Mostra o que tem perto de assinaturas no contexto
    idx = content.find("'assinaturas'")
    print(repr(content[idx:idx+200]))
