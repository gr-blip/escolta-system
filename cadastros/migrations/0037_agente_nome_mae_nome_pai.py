from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0036_agente_certidao_trf'),
    ]

    operations = [
        migrations.AddField(
            model_name='agente',
            name='nome_mae',
            field=models.CharField(blank=True, max_length=200, verbose_name='Nome da mãe'),
        ),
        migrations.AddField(
            model_name='agente',
            name='nome_pai',
            field=models.CharField(blank=True, max_length=200, verbose_name='Nome do pai'),
        ),
    ]
