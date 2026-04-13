path = r'D:\Sistema Escolta\escolta_system\cadastros\views.py'
content = open(path, encoding='utf-8').read()
idx = content.find('def os_field_link')
print(content[idx:idx+3000])
