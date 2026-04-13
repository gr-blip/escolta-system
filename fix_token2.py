path = r'D:\Sistema Escolta\escolta_system\cadastros\templates\cadastros\os_field_link.html'
content = open(path, encoding='utf-8').read()

insert_after = '<script>\n'
insert_pos = content.find('<script>\n/* ')
if insert_pos == -1:
    print('ERRO - nao encontrado')
else:
    inject = '''const token = "{{ op.token }}";
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    for (const cookie of document.cookie.split(';')) {
      const c = cookie.trim();
      if (c.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(c.slice(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
'''
    content = content[:insert_pos+8] + inject + content[insert_pos+8:]
    open(path, 'w', encoding='utf-8').write(content)
    print('OK')
    print(content[insert_pos:insert_pos+300])
