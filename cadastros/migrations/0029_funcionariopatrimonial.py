# Generated manually — Deploy 3a — Modulo Patrimonial v1
# Cria model FuncionarioPatrimonial (vigilantes + porteiros).
# Modulo independente de OS/escolta: puro cadastro + controle documental.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0028_alter_espelhamentoenviado_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='FuncionarioPatrimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('vigilante', 'Vigilante Patrimonial'), ('porteiro', 'Porteiro')], max_length=20, verbose_name='Tipo')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='funcionarios_patrimonial/')),
                ('nome', models.CharField(max_length=200, verbose_name='Nome completo')),
                ('cpf', models.CharField(max_length=14, unique=True, verbose_name='CPF')),
                ('rg', models.CharField(blank=True, max_length=20, verbose_name='RG')),
                ('telefone', models.CharField(blank=True, max_length=20, verbose_name='Telefone / Contato')),
                ('data_nascimento', models.DateField(blank=True, null=True, verbose_name='Data de nascimento')),
                ('cnh', models.CharField(blank=True, max_length=20, verbose_name='CNH')),
                ('cnh_validade', models.DateField(blank=True, null=True, verbose_name='Validade CNH')),
                ('cnh_categoria', models.CharField(blank=True, default='B', max_length=5, verbose_name='Categoria CNH')),
                ('cnv', models.CharField(blank=True, max_length=20, verbose_name='CNV')),
                ('cnv_validade', models.DateField(blank=True, null=True, verbose_name='Validade CNV')),
                ('posto_trabalho', models.CharField(blank=True, max_length=200, verbose_name='Posto de trabalho')),
                ('escala', models.CharField(blank=True, choices=[('12x36_diurno', '12x36 Diurno'), ('12x36_noturno', '12x36 Noturno'), ('24x48', '24x48'), ('5x2', '5x2 (Comercial)'), ('6x1', '6x1'), ('outro', 'Outro (descrever em observacoes)')], max_length=20, verbose_name='Escala')),
                ('data_admissao', models.DateField(blank=True, null=True, verbose_name='Data de admissao')),
                ('registro_drt', models.CharField(blank=True, max_length=30, verbose_name='Registro DRT/MTE')),
                ('funcao', models.CharField(blank=True, choices=[('vigilante_armado', 'Vigilante Armado'), ('vigilante_desarmado', 'Vigilante Desarmado'), ('lider_vigilancia', 'Lider de Vigilancia'), ('porteiro_diurno', 'Porteiro Diurno'), ('porteiro_noturno', 'Porteiro Noturno'), ('lider_portaria', 'Lider de Portaria'), ('supervisor', 'Supervisor'), ('coordenador', 'Coordenador')], max_length=30, verbose_name='Funcao')),
                ('status', models.CharField(choices=[('ativo', 'Ativo'), ('afastado', 'Afastado'), ('inativo', 'Inativo')], default='ativo', max_length=15, verbose_name='Status')),
                ('observacoes', models.TextField(blank=True, verbose_name='Observacoes')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Funcionario Patrimonial',
                'verbose_name_plural': 'Funcionarios Patrimoniais',
                'ordering': ['nome'],
            },
        ),
    ]
