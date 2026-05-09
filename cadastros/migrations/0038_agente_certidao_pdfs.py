from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0037_agente_nome_mae_nome_pai'),
    ]

    operations = [
        migrations.AddField(
            model_name='agente',
            name='certidao_tjdf_pdf',
            field=models.FileField(blank=True, null=True, upload_to='certidoes/', verbose_name='PDF TJDFT'),
        ),
        migrations.AddField(
            model_name='agente',
            name='certidao_trf_pdf',
            field=models.FileField(blank=True, null=True, upload_to='certidoes/', verbose_name='PDF TRF'),
        ),
    ]
