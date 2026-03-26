from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0018_populate_perfis'),
    ]

    operations = [
        migrations.AddField(
            model_name='osoperacional',
            name='gps_inicio_viagem_lat',
            field=models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='osoperacional',
            name='gps_inicio_viagem_lng',
            field=models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='osoperacional',
            name='gps_chegada_operacao_lat',
            field=models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='osoperacional',
            name='gps_chegada_operacao_lng',
            field=models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='osoperacional',
            name='gps_inicio_operacao_lat',
            field=models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='osoperacional',
            name='gps_inicio_operacao_lng',
            field=models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='osoperacional',
            name='gps_termino_operacao_lat',
            field=models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='osoperacional',
            name='gps_termino_operacao_lng',
            field=models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='osoperacional',
            name='gps_termino_viagem_lat',
            field=models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='osoperacional',
            name='gps_termino_viagem_lng',
            field=models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True),
        ),
    ]
