path = r'D:\Sistema Escolta\escolta_system\cadastros\templates\cadastros\os_field_link.html'
content = open(path, encoding='utf-8').read()
print('getCookie definida:', 'function getCookie' in content)
print('token definido:', 'const token' in content or 'var token' in content or "token =" in content)
idx = content.find("token")
print(content[idx:idx+100])
