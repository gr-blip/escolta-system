path = r'D:\Sistema Escolta\escolta_system\cadastros\views.py'
content = open(path, encoding='utf-8').read()

fixes = {
    'In\u251ccio de Viagem': 'In\u00edcio de Viagem',
    'Chegada Opera\u251c\u00ba\u251c\u00fao': 'Chegada Opera\u00e7\u00e3o',
    'In\u251ccio Opera\u251c\u00ba\u251c\u00fao': 'In\u00edcio Opera\u00e7\u00e3o',
    'T\u251c\u00aeRmino Opera\u251c\u00ba\u251c\u00fao': 'T\u00e9rmino Opera\u00e7\u00e3o',
    'T\u251c\u00aeRmino de Viagem': 'T\u00e9rmino de Viagem',
}

for broken, fixed in fixes.items():
    if broken in content:
        content = content.replace(broken, fixed)
        print(f'Corrigido: {fixed}')

open(path, 'w', encoding='utf-8').write(content)
print('DONE')
