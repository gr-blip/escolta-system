from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0030_cancelamento_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionariopatrimonial',
            name='curso',
            field=models.CharField(blank=True, max_length=200, verbose_name='Curso'),
        ),
        migrations.AddField(
            model_name='funcionariopatrimonial',
            name='curso_validade',
            field=models.DateField(blank=True, null=True, verbose_name='Validade do Curso'),
        ),
    ]
