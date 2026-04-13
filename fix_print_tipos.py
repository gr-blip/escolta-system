path = r'D:\Sistema Escolta\escolta_system\cadastros\views.py'
content = open(path, encoding='utf-8').read()

old = "        'assinaturas': assinaturas,"
new = """        'assinaturas': assinaturas,
        'assinatura_tipos_lista': [
            ('agente1', 'Agente 1'), ('agente2', 'Agente 2'),
            ('motorista', 'Motorista Escoltado'), ('supervisor', 'Supervisor'),
        ],"""

if old in content:
    content = content.replace(old, new)
    open(path, 'w', encoding='utf-8').write(content)
    print('OK tipos')
else:
    print('ERRO')
