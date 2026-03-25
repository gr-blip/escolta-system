from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0010_merge_20260319_0827'),
    ]

    operations = [
        # Adicionar status 'finalizada' na Equipe
        migrations.AlterField(
            model_name='equipe',
            name='status',
            field=models.CharField(
                choices=[
                    ('ativa',      'Ativa'),
                    ('inativa',    'Inativa'),
                    ('em_servico', 'Em Serviço'),
                    ('finalizada', 'Finalizada'),
                ],
                default='ativa', max_length=20, verbose_name='Status'
            ),
        ),
        # Adicionar campo finalizada_em na OS
        migrations.AddField(
            model_name='ordemservico',
            name='finalizada_em',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Finalizada em'),
        ),
        # Atualizar status choices da OS
        migrations.AlterField(
            model_name='ordemservico',
            name='status',
            field=models.CharField(
                choices=[
                    ('aberta',      'Aberta'),
                    ('em_viagem',   'Em Viagem'),
                    ('em_operacao', 'Em Operação'),
                    ('encerrando',  'Encerrando'),
                    ('concluida',   'Concluída'),
                    ('finalizada',  'Finalizada'),
                    ('cancelada',   'Cancelada'),
                ],
                default='aberta', max_length=20, verbose_name='Status'
            ),
        ),
    ]
