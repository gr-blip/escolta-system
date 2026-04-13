from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0022_despesaos_trocamotorista_parada_incidente_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='despesaos',
            name='os',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='despesas',
                to='cadastros.ordemservico',
                verbose_name='OS',
                null=True,
            ),
        ),
    ]
