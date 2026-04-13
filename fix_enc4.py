path = r'D:\Sistema Escolta\escolta_system\cadastros\views.py'
content = open(path, encoding='utf-8').read()
broken_t = 'T' + chr(0x251c) + chr(0xae) + 'rmino'
broken_op = chr(0x251c) + chr(0xba) + chr(0x251c) + chr(0xfa) + 'o'
content = content.replace(broken_t + ' Opera' + broken_op, 'T\u00e9rmino Opera\u00e7\u00e3o')
content = content.replace(broken_t + ' de Viagem', 'T\u00e9rmino de Viagem')
open(path, 'w', encoding='utf-8').write(content)
idx = content.find('MARCOS_LISTA')
print(content[idx:idx+300])
print('DONE')
