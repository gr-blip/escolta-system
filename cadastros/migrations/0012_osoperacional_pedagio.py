from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0011_equipe_finalizada_os_finalizada'),
    ]

    operations = [
        migrations.AddField(
            model_name='osoperacional',
            name='pedagio',
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10,
                null=True, verbose_name='Pedágio (R$)'
            ),
        ),
    ]
