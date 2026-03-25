from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0016_perfilusuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='osoperacional',
            name='token',
            field=models.UUIDField(default=uuid.uuid4, unique=True, editable=False, verbose_name='Token de Acesso Externo'),
        ),
        migrations.AddField(
            model_name='osoperacional',
            name='link_ativo',
            field=models.BooleanField(default=True, verbose_name='Link Externo Ativo'),
        ),
    ]
