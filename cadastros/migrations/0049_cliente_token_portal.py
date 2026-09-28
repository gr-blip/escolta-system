import uuid
from django.db import migrations, models


def gerar_tokens_unicos(apps, schema_editor):
    """Atribui um UUID distinto a cada cliente existente."""
    Cliente = apps.get_model('cadastros', 'Cliente')
    for cliente in Cliente.objects.filter(token_portal__isnull=True):
        cliente.token_portal = uuid.uuid4()
        cliente.save(update_fields=['token_portal'])


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0048_diarias_lancamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='token_portal',
            field=models.UUIDField(null=True, blank=True, editable=False,
                                   verbose_name='Token Portal do Cliente'),
        ),
        migrations.RunPython(gerar_tokens_unicos, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='cliente',
            name='token_portal',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True,
                                   verbose_name='Token Portal do Cliente'),
        ),
    ]
