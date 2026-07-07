from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0047_tabelapreco_velocidade_media'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DiariasLancamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(verbose_name='Data')),
                ('agente_nome', models.CharField(max_length=200, verbose_name='Agente')),
                ('os_pk', models.IntegerField(blank=True, null=True, verbose_name='PK da OS')),
                ('os_numero', models.CharField(blank=True, max_length=20, verbose_name='Nº OS')),
                ('cliente', models.CharField(blank=True, max_length=200, verbose_name='Cliente')),
                ('rota', models.CharField(blank=True, max_length=500, verbose_name='Origem → Destino')),
                ('missao', models.CharField(
                    choices=[
                        ('ESCOLTA', 'Escolta'),
                        ('INTERESTADUAL', 'Interestadual'),
                        ('OPERAÇÃO CANCELADA', 'Op. Cancelada'),
                        ('OUTRO', 'Outro'),
                    ],
                    default='ESCOLTA',
                    max_length=30,
                    verbose_name='Missão',
                )),
                ('valor', models.DecimalField(decimal_places=2, default=100, max_digits=8, verbose_name='Valor (R$)')),
                ('obs', models.TextField(blank=True, verbose_name='Observação')),
                ('excluido', models.BooleanField(default=False, verbose_name='Excluir linha auto')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('criado_por', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Criado por',
                )),
            ],
            options={
                'verbose_name': 'Diárias — Lançamento',
                'verbose_name_plural': 'Diárias — Lançamentos',
                'ordering': ['data', 'agente_nome'],
            },
        ),
    ]
