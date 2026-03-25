from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0005_equipe_viatura'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrdemServico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(blank=True, max_length=20, unique=True, verbose_name='Nº OS')),
                ('solicitante', models.CharField(blank=True, max_length=200, verbose_name='Solicitante')),
                ('forma_solicitacao', models.CharField(choices=[('email', 'E-mail'), ('telefone', 'Telefone'), ('whatsapp', 'WhatsApp')], max_length=20, verbose_name='Forma de Solicitação')),
                ('tipo_viagem', models.CharField(choices=[('urbana', 'Urbana'), ('rodoviaria', 'Rodoviária'), ('administrativa', 'Administrativa')], max_length=20, verbose_name='Tipo de Viagem')),
                ('previsao_inicio', models.DateTimeField(verbose_name='Previsão de Início')),
                ('previsao_retorno', models.DateTimeField(blank=True, null=True, verbose_name='Previsão de Retorno')),
                ('imediata', models.BooleanField(default=False, verbose_name='Imediata')),
                ('cidade_origem', models.CharField(max_length=200, verbose_name='Cidade Origem')),
                ('uf_origem', models.CharField(default='GO', max_length=2, verbose_name='UF Origem')),
                ('cidade_destino', models.CharField(max_length=200, verbose_name='Cidade Destino')),
                ('uf_destino', models.CharField(default='GO', max_length=2, verbose_name='UF Destino')),
                ('observacoes', models.TextField(blank=True, verbose_name='Observações')),
                ('status', models.CharField(choices=[('aberta', 'Aberta'), ('em_andamento', 'Em Andamento'), ('concluida', 'Concluída'), ('cancelada', 'Cancelada')], default='aberta', max_length=20, verbose_name='Status')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cadastros.cliente', verbose_name='Cliente')),
                ('equipe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cadastros.equipe', verbose_name='Equipe')),
            ],
            options={
                'verbose_name': 'Ordem de Serviço',
                'verbose_name_plural': 'Ordens de Serviço',
                'ordering': ['-criado_em'],
            },
        ),
    ]
