path = r'D:\Sistema Escolta\escolta_system\escolta_system\settings.py'
content = open(path, encoding='utf-8').read()
idx = content.find('DEBUG')
print(content[idx:idx+200])
