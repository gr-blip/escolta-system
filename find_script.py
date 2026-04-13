path = r'D:\Sistema Escolta\escolta_system\cadastros\templates\cadastros\os_field_link.html'
content = open(path, encoding='utf-8').read()

# Acha o primeiro <script> que tem o conteudo JS (nao o comentario)
idx = content.find('<script>\n/* ')
print('Encontrado em:', idx)
print(repr(content[idx:idx+100]))
