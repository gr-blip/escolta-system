from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0002_remove_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='Colete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marca', models.CharField(max_length=100, verbose_name='Marca')),
                ('numeracao', models.CharField(max_length=50, verbose_name='Numeracao')),
                ('protecao', models.CharField(
                    choices=[
                        ('Nivel IIA',  'Nível IIA'),
                        ('Nivel II',   'Nível II'),
                        ('Nivel IIIA', 'Nível IIIA'),
                        ('Nivel III',  'Nível III'),
                        ('Nivel IV',   'Nível IV'),
                    ],
                    default='Nivel IIIA',
                    max_length=20,
                    verbose_name='Nivel de Protecao',
                )),
                ('validade', models.DateField(verbose_name='Validade')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Colete',
                'verbose_name_plural': 'Coletes',
                'ordering': ['marca'],
            },
        ),
    ]
