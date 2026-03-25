from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0004_add_equipe'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipe',
            name='viatura',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='equipe_viatura',
                to='cadastros.viatura',
                verbose_name='Viatura'
            ),
        ),
    ]
