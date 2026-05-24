# -*- coding: utf-8 -*-
"""VIEW TEMPORÁRIA para importar JRS Facilities — REMOVER APÓS USO"""
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from cadastros.models import FuncionarioPatrimonial


@csrf_exempt
def importar_jrs_temp(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    importados = 0
    pulados = 0
    erros = []

    for row in data:
        nome = row.get('nome', '').strip()
        cpf = row.get('cpf', '').strip()
        cargo = row.get('cargo', '').strip()
        mae = row.get('mae', '').strip()
        nasc = row.get('nasc', '').strip()

        if not nome or not cpf:
            pulados += 1
            continue

        data_nascimento = None
        if nasc:
            for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y'):
                try:
                    data_nascimento = datetime.strptime(nasc, fmt).date()
                    break
                except ValueError:
                    continue

        if FuncionarioPatrimonial.objects.filter(cpf=cpf).exists():
            pulados += 1
            continue

        try:
            FuncionarioPatrimonial.objects.create(
                empresa='jrs_facilities',
                nome=nome,
                cpf=cpf,
                cargo=cargo,
                nome_mae=mae,
                data_nascimento=data_nascimento,
                status='ativo',
            )
            importados += 1
        except Exception as e:
            erros.append(f'{nome}: {str(e)}')

    return JsonResponse({
        'importados': importados,
        'pulados': pulados,
        'erros': erros,
    })
