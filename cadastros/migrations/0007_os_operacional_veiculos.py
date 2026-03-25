from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0006_ordemservico'),
    ]

    operations = [
        migrations.CreateModel(
            name='OSOperacional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_folha', models.CharField(blank=True, max_length=20, verbose_name='Nº Folha')),
                ('inicio_viagem', models.DateTimeField(blank=True, null=True, verbose_name='Início de Viagem')),
                ('chegada_operacao', models.DateTimeField(blank=True, null=True, verbose_name='Chegada Operação')),
                ('inicio_operacao', models.DateTimeField(blank=True, null=True, verbose_name='Início Operação')),
                ('termino_operacao', models.DateTimeField(blank=True, null=True, verbose_name='Término Operação')),
                ('termino_viagem', models.DateTimeField(blank=True, null=True, verbose_name='Término de Viagem')),
                ('km_inicio_viagem', models.PositiveIntegerField(blank=True, null=True, verbose_name='KM Início Viagem')),
                ('km_chegada_operacao', models.PositiveIntegerField(blank=True, null=True, verbose_name='KM Chegada Operação')),
                ('km_inicio_operacao', models.PositiveIntegerField(blank=True, null=True, verbose_name='KM Início Operação')),
                ('km_termino_operacao', models.PositiveIntegerField(blank=True, null=True, verbose_name='KM Término Operação')),
                ('km_termino_viagem', models.PositiveIntegerField(blank=True, null=True, verbose_name='KM Término Viagem')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('os', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,
                                            related_name='operacional', to='cadastros.ordemservico',
                                            verbose_name='OS')),
            ],
            options={'verbose_name': 'Operacional da OS'},
        ),
        migrations.CreateModel(
            name='VeiculoEscoltado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('veiculo', models.CharField(blank=True, max_length=100, verbose_name='Veículo')),
                ('placa_cavalo', models.CharField(blank=True, max_length=15, verbose_name='Placa Cavalo')),
                ('placa_carreta', models.CharField(blank=True, max_length=15, verbose_name='Placa Carreta')),
                ('placa_carreta2', models.CharField(blank=True, max_length=15, verbose_name='Placa Carreta 2')),
                ('motorista', models.CharField(blank=True, max_length=200, verbose_name='Motorista')),
                ('ordem', models.PositiveSmallIntegerField(default=1, verbose_name='Ordem')),
                ('os', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                         related_name='veiculos', to='cadastros.ordemservico',
                                         verbose_name='OS')),
            ],
            options={'verbose_name': 'Veículo Escoltado', 'verbose_name_plural': 'Veículos Escoltados',
                     'ordering': ['ordem']},
        ),
    ]
