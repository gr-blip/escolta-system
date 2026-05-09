from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0033_funcionariopatrimonial_tipo_brigadista'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionariopatrimonial',
            name='funcao',
            field=models.CharField(
                max_length=30,
                blank=True,
                choices=[
                    ('vigilante_armado', 'Vigilante Armado'),
                    ('vigilante_desarmado', 'Vigilante Desarmado'),
                    ('lider_vigilancia', 'Lider de Vigilancia'),
                    ('porteiro_diurno', 'Porteiro Diurno'),
                    ('porteiro_noturno', 'Porteiro Noturno'),
                    ('lider_portaria', 'Lider de Portaria'),
                    ('brigadista', 'Brigadista'),
                    ('lider_brigada', 'Lider de Brigada'),
                    ('supervisor', 'Supervisor'),
                    ('coordenador', 'Coordenador'),
                ],
                verbose_name='Funcao',
            ),
        ),
    ]
