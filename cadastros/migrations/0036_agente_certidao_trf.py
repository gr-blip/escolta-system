from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0035_agente_certidao_tjdf'),
    ]

    operations = [
        migrations.AddField(
            model_name='agente',
            name='certidao_trf_status',
            field=models.CharField(blank=True, max_length=20, verbose_name='Certidão TRF'),
        ),
        migrations.AddField(
            model_name='agente',
            name='certidao_trf_consultado_em',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Última consulta TRF'),
        ),
        migrations.AddField(
            model_name='agente',
            name='certidao_trf_detalhe',
            field=models.TextField(blank=True, verbose_name='Detalhe TRF'),
        ),
    ]
