path = r'D:\Sistema Escolta\escolta_system\cadastros\views.py'
# Le como latin-1 (interpreta os bytes corrompidos corretamente)
raw = open(path, encoding='utf-8').read()
# Os chars bugados sao unicode box-drawing misturados com latin-1
# Vamos reinterpretar: cada char 0x251c seguido de char latin1 e um erro de double-encoding
# Desfaz o double-encoding utf-8 que foi lido como latin-1
fixed = raw.encode('latin-1', errors='ignore').decode('utf-8', errors='replace')
# Conta chars bugados restantes
remaining = fixed.count(chr(0x251c))
print(f'Chars bugados antes: {raw.count(chr(0x251c))}')
print(f'Chars bugados depois: {remaining}')
open(path, 'w', encoding='utf-8').write(fixed)
print('DONE')
