from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0003_add_colete'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome da Equipe')),
                ('status', models.CharField(
                    choices=[('ativa', 'Ativa'), ('inativa', 'Inativa'), ('em_servico', 'Em Serviço')],
                    default='ativa', max_length=20, verbose_name='Status'
                )),
                ('observacoes', models.TextField(blank=True, verbose_name='Observações')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('agente1', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='equipe_agente1',
                    to='cadastros.agente',
                    verbose_name='Agente 1'
                )),
                ('agente2', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='equipe_agente2',
                    to='cadastros.agente',
                    verbose_name='Agente 2'
                )),
                ('armamento_agente1', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='equipe_arm_ag1',
                    to='cadastros.armamento',
                    verbose_name='Armamento Agente 1'
                )),
                ('armamento_agente2', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='equipe_arm_ag2',
                    to='cadastros.armamento',
                    verbose_name='Armamento Agente 2'
                )),
                ('armamento_extra', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='equipe_arm_extra',
                    to='cadastros.armamento',
                    verbose_name='Armamento Extra (Equipe)'
                )),
                ('colete1', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='equipe_colete1',
                    to='cadastros.colete',
                    verbose_name='Colete Agente 1'
                )),
                ('colete2', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='equipe_colete2',
                    to='cadastros.colete',
                    verbose_name='Colete Agente 2'
                )),
            ],
            options={
                'verbose_name': 'Equipe',
                'verbose_name_plural': 'Equipes',
                'ordering': ['nome'],
            },
        ),
    ]
