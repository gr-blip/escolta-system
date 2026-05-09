from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0032_agente_curso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionariopatrimonial',
            name='tipo',
            field=models.CharField(
                max_length=20,
                choices=[
                    ('vigilante', 'Vigilante Patrimonial'),
                    ('porteiro', 'Porteiro'),
                    ('brigadista', 'Brigadista'),
                ],
                verbose_name='Tipo',
            ),
        ),
    ]
