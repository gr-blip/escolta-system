path = r'D:\Sistema Escolta\escolta_system\cadastros\views.py'
content = open(path, encoding='utf-8').read()

old = """        'gps': {
            'inicio_viagem':    fmt_gps(op.gps_inicio_viagem_lat,    op.gps_inicio_viagem_lng),
            'chegada_operacao': fmt_gps(op.gps_chegada_operacao_lat, op.gps_chegada_operacao_lng),
            'inicio_operacao':  fmt_gps(op.gps_inicio_operacao_lat,  op.gps_inicio_operacao_lng),
            'termino_operacao': fmt_gps(op.gps_termino_operacao_lat, op.gps_termino_operacao_lng),
            'termino_viagem':   fmt_gps(op.gps_termino_viagem_lat,   op.gps_termino_viagem_lng),
        },
    })"""

new = """        'gps': {
            'inicio_viagem':    fmt_gps(op.gps_inicio_viagem_lat,    op.gps_inicio_viagem_lng),
            'chegada_operacao': fmt_gps(op.gps_chegada_operacao_lat, op.gps_chegada_operacao_lng),
            'inicio_operacao':  fmt_gps(op.gps_inicio_operacao_lat,  op.gps_inicio_operacao_lng),
            'termino_operacao': fmt_gps(op.gps_termino_operacao_lat, op.gps_termino_operacao_lng),
            'termino_viagem':   fmt_gps(op.gps_termino_viagem_lat,   op.gps_termino_viagem_lng),
        },
        'assinatura_tipos': AssinaturaOS.TIPO_CHOICES if hasattr(AssinaturaOS, 'TIPO_CHOICES') else [
            ('agente1', 'Agente 1'), ('agente2', 'Agente 2'),
            ('motorista', 'Motorista'), ('supervisor', 'Supervisor'),
        ],
        'assinaturas_dict': {a.tipo: a for a in AssinaturaOS.objects.filter(os=os_obj)},
    })"""

if old in content:
    content = content.replace(old, new)
    # Garante que AssinaturaOS esta importado
    if 'AssinaturaOS' not in content[:500]:
        content = content.replace('from .models import', 'from .models import AssinaturaOS,', 1)
    open(path, 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('ERRO - trecho nao encontrado')
