path = r'D:\Sistema Escolta\escolta_system\cadastros\templates\cadastros\os_field_link.html'
content = open(path, encoding='utf-8').read()
idx = content.find('<script')
print(content[idx:idx+300])
