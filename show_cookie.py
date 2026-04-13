path = r'D:\Sistema Escolta\escolta_system\cadastros\templates\cadastros\os_field_link.html'
content = open(path, encoding='utf-8').read()
idx = content.find('getCookie')
print(content[idx:idx+300])
idx2 = content.find('const token')
print(content[idx2:idx2+100])
