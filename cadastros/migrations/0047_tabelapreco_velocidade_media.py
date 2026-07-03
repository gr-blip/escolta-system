from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0046_add_snap_val_endereco_renavan'),
    ]

    operations = [
        migrations.AddField(
            model_name='tabelapreco',
            name='velocidade_media',
            field=models.PositiveIntegerField(
                blank=True, null=True,
                verbose_name='Velocidade Média (km/h)',
                help_text='Se preenchido, franquia de horas = KM ÷ velocidade e excedente KM = KM total × taxa KM.',
            ),
        ),
    ]
