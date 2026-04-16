path = r'D:\Sistema Escolta\escolta_system\cadastros\views.py'
content = open(path, encoding='utf-8').read()
idx = content.find('def os_field_link')
# Pega do return render em diante
idx2 = content.find("return render(request, 'cadastros/os_field_link", idx)
print(content[idx2:idx2+800])
