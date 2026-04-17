from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0025_remove_despesaos_os_alter_assinaturaos_imagem_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EspelhamentoEnviado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_sequencia', models.CharField(blank=True, help_text='ID retornado pela API ao criar', max_length=50, null=True, unique=True)),
                ('placa', models.CharField(max_length=20, verbose_name='Placa')),
                ('id_central', models.CharField(blank=True, max_length=20, verbose_name='ID Central Omnilink')),
                ('nome_central', models.CharField(blank=True, max_length=200, verbose_name='Nome da Central')),
                ('cnpj_destino', models.CharField(blank=True, max_length=20, verbose_name='CNPJ Destino')),
                ('data_expiracao', models.CharField(max_length=30, verbose_name='Expiração (dd/MM/yyyy HH:mm:ss)')),
                ('data_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('obrigatorio', models.BooleanField(default=False, verbose_name='Obrigatório')),
                ('cancelado', models.BooleanField(default=False, verbose_name='Cancelado')),
            ],
            options={
                'verbose_name': 'Espelhamento Enviado',
                'verbose_name_plural': 'Espelhamentos Enviados',
                'ordering': ['-data_criacao'],
            },
        ),
    ]
