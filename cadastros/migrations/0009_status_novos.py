from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0007_os_operacional_veiculos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordemservico',
            name='status',
            field=models.CharField(
                choices=[
                    ('aberta',        'Aberta'),
                    ('em_viagem',     'Em Viagem'),
                    ('em_operacao',   'Em Operação'),
                    ('encerrando',    'Encerrando'),
                    ('concluida',     'Concluída'),
                    ('cancelada',     'Cancelada'),
                ],
                default='aberta',
                max_length=20,
                verbose_name='Status'
            ),
        ),
    ]
