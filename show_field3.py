path = r'D:\Sistema Escolta\escolta_system\cadastros\views.py'
content = open(path, encoding='utf-8').read()
idx2 = content.find("return render(request, 'cadastros/os_field_link")
print(content[idx2:idx2+1800])
