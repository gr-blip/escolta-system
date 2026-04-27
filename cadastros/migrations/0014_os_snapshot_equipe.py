# Cole este arquivo em:
# D:\Sistema Escolta\escolta_system\cadastros\migrations\0014_os_snapshot_equipe.py

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0013_tabela_preco_boletim'),
    ]

    operations = [
        migrations.AddField(model_name='ordemservico', name='snap_equipe_nome',     field=models.CharField(blank=True, max_length=100, verbose_name='Equipe (snapshot)')),
        migrations.AddField(model_name='ordemservico', name='snap_agente1_nome',    field=models.CharField(blank=True, max_length=200, verbose_name='Agente 1 (snapshot)')),
        migrations.AddField(model_name='ordemservico', name='snap_agente1_cpf',     field=models.CharField(blank=True, max_length=20)),
        migrations.AddField(model_name='ordemservico', name='snap_agente1_rg',      field=models.CharField(blank=True, max_length=20)),
        migrations.AddField(model_name='ordemservico', name='snap_agente1_telefone',field=models.CharField(blank=True, max_length=20)),
        migrations.AddField(model_name='ordemservico', name='snap_agente1_cnh',     field=models.CharField(blank=True, max_length=20)),
        migrations.AddField(model_name='ordemservico', name='snap_agente1_cnv',     field=models.CharField(blank=True, max_length=20)),
        migrations.AddField(model_name='ordemservico', name='snap_agente1_foto',    field=models.CharField(blank=True, max_length=500)),
        migrations.AddField(model_name='ordemservico', name='snap_agente2_nome',    field=models.CharField(blank=True, max_length=200, verbose_name='Agente 2 (snapshot)')),
        migrations.AddField(model_name='ordemservico', name='snap_agente2_cpf',     field=models.CharField(blank=True, max_length=20)),
        migrations.AddField(model_name='ordemservico', name='snap_agente2_rg',      field=models.CharField(blank=True, max_length=20)),
        migrations.AddField(model_name='ordemservico', name='snap_agente2_telefone',field=models.CharField(blank=True, max_length=20)),
        migrations.AddField(model_name='ordemservico', name='snap_agente2_cnh',     field=models.CharField(blank=True, max_length=20)),
        migrations.AddField(model_name='ordemservico', name='snap_agente2_cnv',     field=models.CharField(blank=True, max_length=20)),
        migrations.AddField(model_name='ordemservico', name='snap_agente2_foto',    field=models.CharField(blank=True, max_length=500)),
        migrations.AddField(model_name='ordemservico', name='snap_viatura_modelo',  field=models.CharField(blank=True, max_length=100)),
        migrations.AddField(model_name='ordemservico', name='snap_viatura_placa',   field=models.CharField(blank=True, max_length=20)),
        migrations.AddField(model_name='ordemservico', name='snap_viatura_cor',     field=models.CharField(blank=True, max_length=50)),
        migrations.AddField(model_name='ordemservico', name='snap_viatura_frota',   field=models.CharField(blank=True, max_length=20)),
        migrations.AddField(model_name='ordemservico', name='snap_viatura_mct',     field=models.CharField(blank=True, max_length=20)),
    ]
