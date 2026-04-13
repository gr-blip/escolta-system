path = r'D:\Sistema Escolta\escolta_system\cadastros\views.py'
content = open(path, encoding='utf-8').read()
broken_t = 'T' + chr(0x251c) + chr(0xae) + 'rmino'
broken_op = chr(0x251c) + chr(0xba) + chr(0x251c) + chr(0xfa) + 'o'
broken_i = 'In' + chr(0x251c) + chr(0xa1) + 'cio'
broken_ch = 'Chegada Opera' + chr(0x251c) + chr(0xba) + chr(0x251c) + chr(0xfa) + 'o'
content = content.replace(broken_t + ' Opera' + broken_op, 'Término Operação')
content = content.replace(broken_t + ' de Viagem', 'Término de Viagem')
content = content.replace(broken_i + ' Opera' + chr(0x251c) + chr(0xba) + chr(0x251c) + chr(0xfa) + 'o', 'Início Operação')
content = content.replace(broken_i + ' de Viagem', 'Início de Viagem')
content = content.replace(broken_ch, 'Chegada Operação')
open(path, 'w', encoding='utf-8').write(content)
idx = content.find('MARCOS_LISTA')
print(content[idx:idx+300])
print('DONE')
