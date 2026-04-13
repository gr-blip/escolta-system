path = r'D:\Sistema Escolta\escolta_system\cadastros\views.py'
content = open(path, encoding='utf-8').read()
# Acha a ultima funcao valida - corta tudo apos o return do os_field_veiculo_delete
marker = "    return JsonResponse({'ok': True})\r\n"
idx = content.find(marker)
if idx > 0:
    content = content[:idx + len(marker)]
    print('Cortado na posicao', idx)
else:
    marker = "    return JsonResponse({'ok': True})\n"
    idx = content.find(marker)
    content = content[:idx + len(marker)]
    print('Cortado (LF) na posicao', idx)
open(path, 'w', encoding='utf-8').write(content)
print('Ultimas 3 linhas:')
print(repr(content[-100:]))
print('DONE')
