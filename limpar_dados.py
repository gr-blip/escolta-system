"""
Script para limpar OS, Boletins e Equipes do banco de dados.
Execute no PowerShell:
  cd "D:\Sistema Escolta\escolta_system"
  python limpar_dados.py
"""
import os, sys, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'escolta_system.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from cadastros.models import OrdemServico, BoletimMedicao, Equipe, OSOperacional

print("=" * 50)
print("LIMPEZA DE DADOS — DEMARK GESTÃO DE ESCOLTA")
print("=" * 50)

# Contagens antes
os_count   = OrdemServico.objects.count()
bol_count  = BoletimMedicao.objects.count()
op_count   = OSOperacional.objects.count()
eq_count   = Equipe.objects.count()

print(f"\nDados encontrados:")
print(f"  Ordens de Serviço : {os_count}")
print(f"  Dados Operacionais: {op_count}")
print(f"  Boletins de Medição: {bol_count}")
print(f"  Equipes           : {eq_count}")

confirma = input("\nDeseja apagar todos estes registros? (sim/nao): ").strip().lower()

if confirma != 'sim':
    print("Operação cancelada.")
    sys.exit(0)

# Apaga na ordem certa (evitar FK errors)
BoletimMedicao.objects.all().delete()
print("✓ Boletins de Medição apagados")

OSOperacional.objects.all().delete()
print("✓ Dados operacionais apagados")

OrdemServico.objects.all().delete()
print("✓ Ordens de Serviço apagadas")

Equipe.objects.all().delete()
print("✓ Equipes apagadas")

print("\n✅ Dados limpos com sucesso!")
print("   Agentes, Viaturas, Clientes e demais cadastros foram preservados.")
print("=" * 50)
