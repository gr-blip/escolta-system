# Mostra o os_print.html completo para eu inspecionar
path = r'D:\Sistema Escolta\escolta_system\cadastros\templates\cadastros\os_print.html'
content = open(path, encoding='utf-8').read()
# Mostra linha 1 a 10 (loads e tags)
lines = content.split('\n')
for i, l in enumerate(lines[:15], 1):
    print(f'{i}: {l}')
print('...')
# Mostra area de despesas/assinaturas
idx = content.find('DESPESAS')
print(content[idx-50:idx+200])
