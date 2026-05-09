from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0034_funcionariopatrimonial_funcao_brigadista'),
    ]

    operations = [
        migrations.AddField(
            model_name='agente',
            name='certidao_tjdf_status',
            field=models.CharField(blank=True, max_length=20, verbose_name='Certidão TJDF'),
        ),
        migrations.AddField(
            model_name='agente',
            name='certidao_tjdf_consultado_em',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Última consulta TJDF'),
        ),
        migrations.AddField(
            model_name='agente',
            name='certidao_tjdf_detalhe',
            field=models.TextField(blank=True, verbose_name='Detalhe TJDF'),
        ),
    ]
