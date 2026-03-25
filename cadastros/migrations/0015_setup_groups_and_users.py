from django.db import migrations
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

def setup_groups_and_users(apps, schema_editor):
    # Modelos do app 'cadastros'
    Agente = apps.get_model('cadastros', 'Agente')
    Viatura = apps.get_model('cadastros', 'Viatura')
    Rastreador = apps.get_model('cadastros', 'Rastreador')
    Armamento = apps.get_model('cadastros', 'Armamento')
    Cliente = apps.get_model('cadastros', 'Cliente')
    Equipe = apps.get_model('cadastros', 'Equipe')
    Colete = apps.get_model('cadastros', 'Colete')
    OrdemServico = apps.get_model('cadastros', 'OrdemServico')
    OSOperacional = apps.get_model('cadastros', 'OSOperacional')
    VeiculoEscoltado = apps.get_model('cadastros', 'VeiculoEscoltado')
    TabelaPreco = apps.get_model('cadastros', 'TabelaPreco')
    BoletimMedicao = apps.get_model('cadastros', 'BoletimMedicao')

    # 1. Criar Grupos
    admin_group, _ = Group.objects.get_or_create(name='Administrador')
    operador_group, _ = Group.objects.get_or_create(name='Operador')
    financeiro_group, _ = Group.objects.get_or_create(name='Financeiro')

    # Categorias de modelos
    modelos_cadastros = [Agente, Viatura, Rastreador, Armamento, Cliente, Equipe, Colete]
    modelos_os_equipes = [OrdemServico, OSOperacional, VeiculoEscoltado]
    modelos_faturamento = [TabelaPreco, BoletimMedicao]

    def get_perms(models, actions=['view', 'add', 'change', 'delete']):
        perms = []
        for model in models:
            content_type = ContentType.objects.get_for_model(model)
            for action in actions:
                codename = f'{action}_{model._meta.model_name}'
                try:
                    perm = Permission.objects.get(content_type=content_type, codename=codename)
                    perms.append(perm)
                except Permission.DoesNotExist:
                    pass
        return perms

    # --- Configurar Grupo Operador ---
    operador_perms = get_perms(modelos_cadastros) + get_perms(modelos_os_equipes)
    operador_group.permissions.set(operador_perms)

    # --- Configurar Grupo Financeiro ---
    financeiro_perms = get_perms(modelos_cadastros, ['view']) + \
                       get_perms(modelos_os_equipes, ['view']) + \
                       get_perms(modelos_faturamento)
    financeiro_group.permissions.set(financeiro_perms)

    # --- Configurar Grupo Administrador ---
    admin_perms = get_perms(modelos_cadastros) + \
                  get_perms(modelos_os_equipes) + \
                  get_perms(modelos_faturamento)
    admin_group.permissions.set(admin_perms)

    # 2. Criar Usuários de Exemplo
    users_data = [
        ('admin_user', 'admin123', 'admin@escolta.com', admin_group, True, True),
        ('operador_user', 'op123', 'operador@escolta.com', operador_group, True, False),
        ('financeiro_user', 'fin123', 'financeiro@escolta.com', financeiro_group, True, False),
    ]

    for username, password, email, group, is_staff, is_superuser in users_data:
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_staff = is_staff
            user.is_superuser = is_superuser
            user.save()
            user.groups.add(group)

class Migration(migrations.Migration):
    dependencies = [
        ('cadastros', '0014_os_snapshot_equipe'), # Ajustado para a sua última migração
    ]

    operations = [
        migrations.RunPython(setup_groups_and_users),
    ]
