# ============================================================
# GUIA DE INTEGRAÇÃO — Novas funcionalidades do link do agente
# ============================================================

# ── PASSO 1 — Adicionar os novos models ao models.py ────────
# Cole o conteúdo de models_novos.py ANTES da linha final:
#   from .models_perfil import PerfilUsuario
# (ou após o bloco de BoletimMedicao — antes da última linha)

# ── PASSO 2 — Atualizar o import no TOPO de views.py ────────
# Localize a linha que importa os models (ex: from .models import ...)
# e adicione os novos nomes:

from .models import (
    Agente, Viatura, Rastreador, Armamento, Cliente, Colete,
    Equipe, OrdemServico, OSOperacional, VeiculoEscoltado,
    TabelaPreco, BoletimMedicao,
    # ── NOVOS ──
    FotoMarco, Parada, FotoParada,
    Incidente, FotoIncidente,
    FotoVeiculoEscoltado,
    TrocaMotorista, FotoTrocaMotorista,
    AssinaturaOS, DespesaOS,
)

# ── PASSO 3 — Atualizar a view os_field_link para passar ────
# contexto extra (assinaturas e veículos) ao template.
# Substitua o bloco "return render(...)" no final da view
# os_field_link pelo código abaixo:

    # (dentro de os_field_link, substituir o return render final)
    return render(request, 'cadastros/os_field_link.html', {
        'os': os_obj,
        'op': op,
        'sucesso': sucesso,
        'erro': erro,
        'fmt': {
            'inicio_viagem':     fmt_dt(op.inicio_viagem),
            'chegada_operacao':  fmt_dt(op.chegada_operacao),
            'inicio_operacao':   fmt_dt(op.inicio_operacao),
            'termino_operacao':  fmt_dt(op.termino_operacao),
            'termino_viagem':    fmt_dt(op.termino_viagem),
        },
        'gps': {
            'inicio_viagem':    fmt_gps(op.gps_inicio_viagem_lat,    op.gps_inicio_viagem_lng),
            'chegada_operacao': fmt_gps(op.gps_chegada_operacao_lat, op.gps_chegada_operacao_lng),
            'inicio_operacao':  fmt_gps(op.gps_inicio_operacao_lat,  op.gps_inicio_operacao_lng),
            'termino_operacao': fmt_gps(op.gps_termino_operacao_lat, op.gps_termino_operacao_lng),
            'termino_viagem':   fmt_gps(op.gps_termino_viagem_lat,   op.gps_termino_viagem_lng),
        },
        # ── NOVOS ──
        'assinatura_tipos': AssinaturaOS.TIPO_CHOICES,
    })

# ── PASSO 4 — Adicionar conteúdo de views_novos.py ao views.py
# Cole o conteúdo inteiro de views_novos.py no final do views.py
# (após a view os_desativar_link)

# ── PASSO 5 — Adicionar URLs ────────────────────────────────
# Cole o conteúdo de urls_novos.py no final do urls.py

# ── PASSO 6 — Substituir o template ─────────────────────────
# Renomeie o template atual:
#   cadastros/templates/cadastros/os_field_link.html → os_field_link_backup.html
# Copie o novo template:
#   os_field_link_novo.html → cadastros/templates/cadastros/os_field_link.html

# ── PASSO 7 — Migrations ────────────────────────────────────
# No terminal do projeto:
#
#   python manage.py makemigrations cadastros
#   python manage.py migrate
#
# Isso criará as tabelas:
#   cadastros_fotomarco
#   cadastros_parada
#   cadastros_fotoparada
#   cadastros_incidente
#   cadastros_fotoincidente
#   cadastros_fotoveiculoescoltado
#   cadastros_trocamotorista
#   cadastros_fototrocamotorista
#   cadastros_assinatura_os
#   cadastros_despesaos

# ── PASSO 8 — settings.py (verificar MEDIA) ─────────────────
# Confirme que no settings.py existe:
#
#   MEDIA_URL  = '/media/'
#   MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
#
# E que no urls.py PRINCIPAL (escolta_system/urls.py) existe:
#
#   from django.conf import settings
#   from django.conf.urls.static import static
#   ...
#   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#
# Isso é necessário para servir as fotos em desenvolvimento.
# Em produção (Railway), o WhiteNoise NÃO serve MEDIA — use
# um bucket S3/Cloudflare R2 ou configure o Railway para
# montar volume persistente.

# ── PASSO 9 — Registrar novos models no admin ───────────────
# Adicione ao cadastros/admin.py:
#
#   from .models import (FotoMarco, Parada, Incidente,
#       FotoVeiculoEscoltado, TrocaMotorista, AssinaturaOS, DespesaOS)
#
#   @admin.register(Parada)
#   class ParadaAdmin(admin.ModelAdmin):
#       list_display = ['os', 'motivo', 'inicio', 'fim']
#       list_filter  = ['motivo']
#
#   @admin.register(Incidente)
#   class IncidenteAdmin(admin.ModelAdmin):
#       list_display = ['os', 'tipo', 'gravidade', 'ocorrido_em']
#       list_filter  = ['tipo', 'gravidade']
#
#   @admin.register(DespesaOS)
#   class DespesaAdmin(admin.ModelAdmin):
#       list_display = ['os', 'tipo', 'natureza', 'valor', 'ocorrido_em']
#
#   @admin.register(AssinaturaOS)
#   class AssinaturaAdmin(admin.ModelAdmin):
#       list_display = ['os', 'tipo', 'nome', 'criado_em']
#
#   @admin.register(TrocaMotorista)
#   class TrocaMotoristaAdmin(admin.ModelAdmin):
#       list_display = ['os', 'motorista_saindo', 'motorista_entrando', 'ocorrido_em']

# ── CHECKLIST FINAL ─────────────────────────────────────────
# [ ] models_novos.py colado em models.py
# [ ] import de models atualizado em views.py
# [ ] return render de os_field_link atualizado (contexto novo)
# [ ] views_novos.py colado em views.py
# [ ] urls_novos.py colado em urls.py
# [ ] template novo copiado para templates/cadastros/
# [ ] python manage.py makemigrations && migrate
# [ ] MEDIA_URL/ROOT no settings.py conferidos
# [ ] static(MEDIA_URL) no urls.py principal conferido
# [ ] Admin registrado (opcional mas recomendado)
