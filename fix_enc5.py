path = r'D:\Sistema Escolta\escolta_system\cadastros\views.py'
content = open(path, encoding='utf-8').read()
broken_t = 'T' + chr(0x251c) + chr(0xae) + 'rmino'
broken_op = chr(0x251c) + chr(0xba) + chr(0x251c) + chr(0xfa) + 'o'
broken_i = 'In' + chr(0x251c) + chr(0xa1) + 'cio'
content = content.replace(broken_t + ' Opera' + broken_op, 'T\u00e9rmino Opera\u00e7\u00e3o')
content = content.replace(broken_t + ' de Viagem', 'T\u00e9rmino de Viagem')
content = content.replace(broken_i + ' Opera' + chr(0x251c) + chr(0xba) + chr(0x251c) + chr(0xfa) + 'o', 'In\u00edcio Opera\u00e7\u00e3o')
content = content.replace(broken_i + ' de Viagem', 'In\u00edcio de Viagem')
content = content.replace('Chegada Opera' + chr(0x251c) + chr(0xba) + chr(0x251c) + chr(0xfa) + 'o', 'Chegada Opera\u00e7\u00e3o')
open(path, 'w', encoding='utf-8').write(content)
print('Ocorrencias restantes com encoding ruim:', content.count(chr(0x251c)))
print('DONE')
