from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0001_initial'),
    ]

    operations = [
        # Agente: remove cert_armamento_validade
        migrations.RemoveField(model_name='agente', name='cert_armamento_validade'),

        # Rastreador: remove campos extras
        migrations.RemoveField(model_name='rastreador', name='imei'),
        migrations.RemoveField(model_name='rastreador', name='chip_sim'),
        migrations.RemoveField(model_name='rastreador', name='operadora'),
        migrations.RemoveField(model_name='rastreador', name='viatura'),
        migrations.RemoveField(model_name='rastreador', name='central_monitoramento'),
        migrations.RemoveField(model_name='rastreador', name='data_instalacao'),
        migrations.RemoveField(model_name='rastreador', name='validade_contrato'),
        migrations.RemoveField(model_name='rastreador', name='login_plataforma'),

        # Armamento: remove custódia e status
        migrations.RemoveField(model_name='armamento', name='agente_responsavel'),
        migrations.RemoveField(model_name='armamento', name='status'),
        migrations.RemoveField(model_name='armamento', name='observacoes'),

        # Cliente: remove contato e solicitante
        migrations.RemoveField(model_name='cliente', name='solicitante_nome'),
        migrations.RemoveField(model_name='cliente', name='solicitante_cargo'),
        migrations.RemoveField(model_name='cliente', name='telefone'),
        migrations.RemoveField(model_name='cliente', name='email'),
        migrations.RemoveField(model_name='cliente', name='tipo_contrato'),
        migrations.RemoveField(model_name='cliente', name='rota_padrao'),
        migrations.RemoveField(model_name='cliente', name='status'),
    ]
