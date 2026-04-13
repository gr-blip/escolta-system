path = r'D:\Sistema Escolta\escolta_system\cadastros\templates\cadastros\os_field_link.html'
content = open(path, encoding='utf-8').read()

old = '''<script>
/* 
   VEÍCULOS ESCOLTADOS  funções AJAX
    */'''

new = '''<script>
const token = "{{ op.token }}";
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
/* 
   VEÍCULOS ESCOLTADOS  funções AJAX
    */'''

if old in content:
    content = content.replace(old, new)
    open(path, 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('ERRO - trecho nao encontrado')
