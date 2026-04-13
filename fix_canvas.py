path = r'D:\Sistema Escolta\escolta_system\cadastros\templates\cadastros\os_field_link.html'
content = open(path, encoding='utf-8').read()

# Fix 1: CSS - altura visivel no mobile
content = content.replace(
    'canvas.sig { display: block; width: 100%; cursor: crosshair; }',
    'canvas.sig { display: block; width: 100%; cursor: crosshair; height: 180px; touch-action: none; }'
)

# Fix 2: JS - inicializar width e height corretamente
content = content.replace(
    '    canvas.width = canvas.offsetWidth;\n    let drawing = false',
    '    canvas.width  = canvas.offsetWidth  || 320;\n    canvas.height = canvas.offsetHeight || 180;\n    let drawing = false'
)

open(path, 'w', encoding='utf-8').write(content)
print('OK')
