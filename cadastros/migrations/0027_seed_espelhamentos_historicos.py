"""
Migration de dados: insere espelhamentos enviados históricos no banco local.
Baseado nas telas do AMNLink capturadas em 17/04/2026.
"""
from django.db import migrations
from datetime import datetime


HISTORICOS = [
    # placa, nome_central, data_exp, data_criacao, cancelado
    ('SSR0E93', 'NORISK',                     '17/04/2026 23:59:00', datetime(2026, 4, 16, 22, 30, 21), False),
    ('SIS6B65', 'SKYMARK',                    '17/04/2026 23:59:00', datetime(2026, 4, 16, 22, 30,  4), False),
    ('SUU7D41', 'SKYMARK',                    '17/04/2026 23:59:00', datetime(2026, 4, 16, 22, 29, 43), False),
    ('SUI1G21', 'SMITH SEGURANÇA PRIVADA',    '30/11/2027 20:51:00', datetime(2024, 7, 30, 18, 49, 53), False),
    ('REU2F04', 'SMITH SEGURANÇA PRIVADA',    '30/11/2027 20:51:00', datetime(2024, 7, 30, 18, 49, 53), False),
    ('REK3J23', 'SMITH SEGURANÇA PRIVADA',    '30/11/2027 20:51:00', datetime(2024, 7, 30, 18, 49, 53), False),
    ('REU2F12', 'SMITH SEGURANÇA PRIVADA',    '30/11/2027 20:51:00', datetime(2024, 7, 30, 18, 49, 53), False),
    ('SGN4B76', 'SMITH SEGURANÇA PRIVADA',    '30/11/2027 20:51:00', datetime(2024, 7, 30, 18, 49, 53), False),
    ('REU2F12', 'JR SEGURANÇA E VIGILÂNCIA',  '30/12/2063 23:59:00', datetime(2024, 6, 30,  9, 17, 19), False),
    ('SGN4B76', 'JR SEGURANÇA E VIGILÂNCIA',  '31/12/2030 09:55:00', datetime(2024, 1, 29,  9, 55, 46), False),
]


def seed_historicos(apps, schema_editor):
    EspelhamentoEnviado = apps.get_model('cadastros', 'EspelhamentoEnviado')
    for placa, nome_central, data_exp, data_criacao, cancelado in HISTORICOS:
        obj = EspelhamentoEnviado(
            placa=placa,
            nome_central=nome_central,
            data_expiracao=data_exp,
            cancelado=cancelado,
        )
        # auto_now_add impede setar no save — usamos update() após
        obj.save()
        EspelhamentoEnviado.objects.filter(pk=obj.pk).update(data_criacao=data_criacao)


def remove_historicos(apps, schema_editor):
    EspelhamentoEnviado = apps.get_model('cadastros', 'EspelhamentoEnviado')
    placas = [p for p, *_ in HISTORICOS]
    EspelhamentoEnviado.objects.filter(placa__in=placas, id_sequencia__isnull=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0026_espelhamentoenviado'),
    ]

    operations = [
        migrations.RunPython(seed_historicos, remove_historicos),
    ]
