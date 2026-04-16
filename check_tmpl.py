path = r'D:\Sistema Escolta\escolta_system\cadastros\templates\cadastros\os_print.html'
content = open(path, encoding='utf-8').read()
# Mostra só a secao de assinaturas
idx = content.find('ASSINATURAS')
print(content[idx:idx+1500])
