path = r'D:\Sistema Escolta\escolta_system\cadastros\views.py'
content = open(path, encoding='utf-8').read()

old = """    return render(request, 'cadastros/os_print.html', {
        'os': os_obj,
        'op': op,
        'rastreador_viatura': rastreador_viatura,
        'fotos_marco': fotos_marco,
        'fotos_marco_lista': MARCOS_LISTA,
    })"""

new = """    # Assinaturas digitais
    assinaturas = {a.tipo: a for a in AssinaturaOS.objects.filter(os=os_obj)}

    # Despesas / Creditos
    despesas = DespesaOS.objects.filter(os=os_obj).order_by('ocorrido_em')

    return render(request, 'cadastros/os_print.html', {
        'os': os_obj,
        'op': op,
        'rastreador_viatura': rastreador_viatura,
        'fotos_marco': fotos_marco,
        'fotos_marco_lista': MARCOS_LISTA,
        'assinaturas': assinaturas,
        'despesas': despesas,
    })"""

if old in content:
    content = content.replace(old, new)
    open(path, 'w', encoding='utf-8').write(content)
    print('OK views.py')
else:
    print('ERRO - trecho nao encontrado')
