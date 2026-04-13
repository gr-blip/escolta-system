path = r'D:\Sistema Escolta\escolta_system\cadastros\views.py'
content = open(path, encoding='utf-8').read()
content = content.replace('T\u251c\u00aeRmino Opera\u251c\u00ba\u251c\u00fao', 'T\u00e9rmino Opera\u00e7\u00e3o')
content = content.replace('T\u251c\u00aeRmino de Viagem', 'T\u00e9rmino de Viagem')
content = content.replace('T\u251c\xaeRmino Opera\u251c\xba\u251c\xfao', 'T\u00e9rmino Opera\u00e7\u00e3o')
content = content.replace('T\u251c\xaeRmino de Viagem', 'T\u00e9rmino de Viagem')
open(path, 'w', encoding='utf-8').write(content)
idx = content.find('MARCOS_LISTA')
print(content[idx:idx+300])
