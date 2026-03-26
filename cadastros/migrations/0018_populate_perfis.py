from django.db import migrations


def populate_perfis(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    PerfilUsuario = apps.get_model('cadastros', 'PerfilUsuario')

    # Mapeamento de username → nível
    nivel_map = {
        'demark':          'developer',
        'admin_user':      'admin',
        'admin':           'admin',
        'financeiro_user': 'admin',   # Financeiro usa nível admin para ver boletins
        'operador_user':   'operador',
    }

    for user in User.objects.all():
        nivel = nivel_map.get(user.username.lower(), 'operador')
        oculto = user.username.lower() == 'demark'
        PerfilUsuario.objects.update_or_create(
            user=user,
            defaults={'nivel': nivel, 'oculto': oculto},
        )


def rollback(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0017_osoperacional_token'),
    ]

    operations = [
        migrations.RunPython(populate_perfis, rollback),
    ]
