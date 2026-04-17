from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0012_osoperacional_pedagio'),
    ]

    operations = [
        migrations.CreateModel(
            name='TabelaPreco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=200, verbose_name='Nome da Tabela / Rota')),
                ('tipo_viagem', models.CharField(choices=[('urbana','Urbana'),('rodoviaria','Rodoviária'),('administrativa','Administrativa'),('todas','Todas')], default='todas', max_length=20, verbose_name='Tipo de Viagem')),
                ('situacao', models.CharField(choices=[('ativo','Ativo'),('inativo','Inativo')], default='ativo', max_length=10, verbose_name='Situação')),
                ('data_inclusao', models.DateField(auto_now_add=True, verbose_name='Inclusão')),
                ('inicio_contrato', models.DateField(blank=True, null=True, verbose_name='Início Contrato')),
                ('ultimo_reajuste', models.DateField(blank=True, null=True, verbose_name='Último Reajuste')),
                ('proximo_reajuste', models.DateField(blank=True, null=True, verbose_name='Próximo Reajuste')),
                ('valor_escolta', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor da Escolta (R$)')),
                ('franquia_km', models.PositiveIntegerField(default=0, verbose_name='Franquia KM')),
                ('franquia_horas', models.CharField(default='000:00', max_length=6, verbose_name='Franquia Horas (HH:MM)')),
                ('excedente_km', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Excedente por KM (R$)')),
                ('excedente_hora', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Excedente por Hora (R$)')),
                ('cobrar_pedagio', models.CharField(choices=[('sim','Sim'),('nao','Não')], default='sim', max_length=3, verbose_name='Cobrar Pedágio')),
                ('pedagio_fixo', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Pedágio Fixo (R$)')),
                ('pedagio_percent', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='% Pedágio')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tabelas_preco', to='cadastros.cliente', verbose_name='Cliente')),
            ],
            options={'verbose_name': 'Tabela de Preço', 'verbose_name_plural': 'Tabelas de Preço', 'ordering': ['cliente__razao_social', 'nome']},
        ),
        migrations.CreateModel(
            name='BoletimMedicao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('aberto','Em Aberto'),('faturado','Faturado'),('cancelado','Cancelado')], default='aberto', max_length=15, verbose_name='Status')),
                ('horas_realizadas', models.CharField(default='00:00', max_length=6, verbose_name='Horas Realizadas')),
                ('km_realizado', models.PositiveIntegerField(default=0, verbose_name='KM Realizado')),
                ('horas_excedentes', models.CharField(default='00:00', max_length=6, verbose_name='Horas Excedentes')),
                ('km_excedente', models.PositiveIntegerField(default=0, verbose_name='KM Excedente')),
                ('valor_escolta', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Valor Escolta (R$)')),
                ('valor_excedente_km', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Valor Excedente KM (R$)')),
                ('valor_excedente_hora', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Valor Excedente Hora (R$)')),
                ('valor_pedagio', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Valor Pedágio (R$)')),
                ('acrescimo', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Acréscimo (R$)')),
                ('desconto', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Desconto (R$)')),
                ('valor_total', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Valor Total (R$)')),
                ('numero_nota', models.CharField(blank=True, max_length=50, verbose_name='Nº Nota Fiscal')),
                ('observacoes', models.TextField(blank=True, verbose_name='Observações')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('os', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='boletim', to='cadastros.ordemservico', verbose_name='OS')),
                ('tabela_preco', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='boletins', to='cadastros.tabelapreco', verbose_name='Tabela de Preço')),
            ],
            options={'verbose_name': 'Boletim de Medição', 'verbose_name_plural': 'Boletins de Medição', 'ordering': ['-criado_em']},
        ),
    ]
