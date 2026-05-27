from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0045_funcionariopatrimonial_empresa_freelance'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordemservico',
            name='snap_agente1_val_cnh',
            field=models.DateField(blank=True, null=True, verbose_name='Val. CNH Ag.1'),
        ),
        migrations.AddField(
            model_name='ordemservico',
            name='snap_agente1_val_cnv',
            field=models.DateField(blank=True, null=True, verbose_name='Val. CNV Ag.1'),
        ),
        migrations.AddField(
            model_name='ordemservico',
            name='snap_agente1_endereco',
            field=models.TextField(blank=True, verbose_name='Endereço Ag.1'),
        ),
        migrations.AddField(
            model_name='ordemservico',
            name='snap_agente2_val_cnh',
            field=models.DateField(blank=True, null=True, verbose_name='Val. CNH Ag.2'),
        ),
        migrations.AddField(
            model_name='ordemservico',
            name='snap_agente2_val_cnv',
            field=models.DateField(blank=True, null=True, verbose_name='Val. CNV Ag.2'),
        ),
        migrations.AddField(
            model_name='ordemservico',
            name='snap_agente2_endereco',
            field=models.TextField(blank=True, verbose_name='Endereço Ag.2'),
        ),
        migrations.AddField(
            model_name='ordemservico',
            name='snap_viatura_renavan',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
