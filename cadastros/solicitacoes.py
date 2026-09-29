"""Solicitações de escolta recebidas de um contratante (hub) e a resposta.

Duas portas:
  API  - o contratante manda a solicitação (POST) e depois pergunta o que deu
         nela (GET). Quem puxa o resultado e o contratante: assim este sistema
         nao precisa guardar credencial nem endereco do hub.
  Tela - a operacao ve, confere e aceita ou recusa. So no aceite a OS nasce.

Autenticacao do POST: `SOLICITACAO_API_KEY`, uma chave SO de escrita. O token
do portal do cliente e de LEITURA e fica em link/planilha - reaproveitar ele
aqui deixaria qualquer um que ja tem um relatorio criar servico no sistema.
"""
import json
import logging
import re
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

logger = logging.getLogger(__name__)

CAMPOS_TEXTO = ('numero_se', 'cliente_nome', 'equipes', 'endereco_origem',
                'endereco_destino', 'placa_veiculo', 'motorista',
                'motorista_telefone', 'conta_espelhamento', 'solicitante',
                'observacoes')


def _chave_exigida():
    return getattr(settings, 'SOLICITACAO_API_KEY', '')


def _data(valor):
    for f in ('%Y-%m-%d', '%d/%m/%Y', '%d/%m/%y'):
        try:
            return datetime.strptime(str(valor).strip(), f).date()
        except (ValueError, TypeError):
            continue
    return None


def _hora(valor):
    for f in ('%H:%M:%S', '%H:%M'):
        try:
            return datetime.strptime(str(valor).strip(), f).time()
        except (ValueError, TypeError):
            continue
    return None


def cidade_uf(endereco):
    """'Posto Alvorada - BR153 KM670 - Goiatuba/GO' -> ('Goiatuba', 'GO').

    E um palpite a partir do texto livre que o contratante digitou; por isso o
    aceite mostra os dois campos preenchidos e EDITAVEIS, em vez de gravar
    calado o que a expressao achou.
    """
    texto = (endereco or '').strip()
    m = re.search(r'([^\-/,]+)\s*/\s*([A-Za-z]{2})\s*$', texto)
    if m:
        return m.group(1).strip(), m.group(2).upper()
    return texto[:200], ''


# ── API: o contratante manda a solicitação ──────────────────────────────────

@csrf_exempt
def api_receber(request):
    if request.method != 'POST':
        return JsonResponse({'erro': 'Método não permitido'}, status=405)

    chave = _chave_exigida()
    if not chave:
        return JsonResponse({'erro': 'Recebimento de solicitações não configurado'},
                            status=503)
    if request.headers.get('X-API-Key') != chave:
        return JsonResponse({'erro': 'Chave inválida'}, status=401)

    try:
        dados = json.loads(request.body.decode('utf-8') or '{}')
    except ValueError:
        return JsonResponse({'erro': 'JSON inválido'}, status=400)

    numero_hub = str(dados.get('numero_os_hub') or '').strip()
    if not numero_hub:
        return JsonResponse({'erro': 'numero_os_hub é obrigatório'}, status=400)

    from .models import SolicitacaoEscolta
    origem = str(dados.get('origem') or 'SPARTACUS').strip()[:60]
    campos = {c: str(dados.get(c) or '').strip()[:300] for c in CAMPOS_TEXTO}
    campos['data_missao'] = _data(dados.get('data_missao'))
    campos['hora_missao'] = _hora(dados.get('hora_missao'))

    try:
        with transaction.atomic():
            sol, criada = SolicitacaoEscolta.objects.get_or_create(
                origem=origem, numero_os_hub=numero_hub, defaults=campos)
    except IntegrityError:            # corrida entre dois envios simultaneos
        sol = SolicitacaoEscolta.objects.get(origem=origem, numero_os_hub=numero_hub)
        criada = False

    if not criada and sol.status == 'aguardando':
        # reenvio antes de alguem responder: atualiza os dados, nao duplica
        for campo, valor in campos.items():
            setattr(sol, campo, valor)
        sol.save()

    if criada:
        _avisar_whatsapp(sol)

    return JsonResponse(_resposta(sol), status=201 if criada else 200)


@csrf_exempt
def api_status(request, pk):
    """O contratante pergunta o que deu na solicitação. Ele puxa - este sistema
    nao empurra, entao nao precisa conhecer o endereco nem a chave do hub."""
    if request.method != 'GET':
        return JsonResponse({'erro': 'Método não permitido'}, status=405)
    if _chave_exigida() and request.headers.get('X-API-Key') != _chave_exigida():
        return JsonResponse({'erro': 'Chave inválida'}, status=401)
    from .models import SolicitacaoEscolta
    sol = get_object_or_404(SolicitacaoEscolta, pk=pk)
    return JsonResponse(_resposta(sol))


def _resposta(sol):
    return {
        'id': sol.pk,
        'prestador': _prestador(),
        'origem': sol.origem,
        'numero_se': sol.numero_se,
        'numero_os_hub': sol.numero_os_hub,
        'numero_os_prestador': sol.os.numero if sol.os else '',
        'status': sol.status,
        'status_display': sol.get_status_display(),
        'motivo_recusa': sol.motivo_recusa,
        'recebida_em': sol.recebida_em.isoformat() if sol.recebida_em else None,
        'respondida_em': sol.respondida_em.isoformat() if sol.respondida_em else None,
    }


def _prestador():
    """Nome desta empresa. O arquivo tambem roda em sistema sem a camada de
    marca, entao cai pro settings antes de desistir."""
    try:
        from .branding import nome
        return nome()
    except Exception:
        return getattr(settings, 'SISTEMA_NOME', '')


def _avisar_whatsapp(sol):
    """Aviso na operação. Falha de WhatsApp nao pode perder a solicitação -
    ela ja esta gravada e aparece na tela de qualquer jeito."""
    numero = getattr(settings, 'SOLICITACAO_WHATSAPP', '')
    if not numero:
        return
    try:
        try:
            from . import whatsapp_provider as cliente
        except ImportError:        # sistema sem o roteador de provider
            from . import wapi_client as cliente
        quando = ' '.join(filter(None, [
            sol.data_missao.strftime('%d/%m/%Y') if sol.data_missao else '',
            sol.hora_missao.strftime('%H:%M') if sol.hora_missao else '']))
        texto = ('🚨 *NOVA SOLICITAÇÃO DE ESCOLTA*\n'
                 '%s · OS %s\n%s\n\n'
                 '*Origem:* %s\n*Destino:* %s\n*Veículo:* %s\n*Motorista:* %s\n\n'
                 'Confira e aceite em Solicitações.') % (
            sol.origem, sol.numero_os_hub, quando,
            sol.endereco_origem or '—', sol.endereco_destino or '—',
            sol.placa_veiculo or '—', sol.motorista or '—')
        cliente.send_text(numero, texto)
    except Exception as e:
        logger.warning('Solicitação %s: aviso no WhatsApp falhou: %s', sol.pk, e)


# ── Tela da operação ────────────────────────────────────────────────────────

def pendentes():
    from .models import SolicitacaoEscolta
    return SolicitacaoEscolta.objects.filter(status='aguardando').count()


@login_required
def lista(request):
    from .models import SolicitacaoEscolta
    from .models import Cliente
    status = request.GET.get('status') or 'aguardando'
    qs = SolicitacaoEscolta.objects.select_related('os', 'respondida_por')
    if status in ('aguardando', 'aceita', 'recusada'):
        qs = qs.filter(status=status)
    contagens = {s: SolicitacaoEscolta.objects.filter(status=s).count()
                 for s in ('aguardando', 'aceita', 'recusada')}
    lista_sol = list(qs[:200])
    for sol in lista_sol:      # palpite de cidade/UF pro formulario de aceite
        sol.sugestao_origem = cidade_uf(sol.endereco_origem)
        sol.sugestao_destino = cidade_uf(sol.endereco_destino)
    return render(request, 'cadastros/solicitacoes.html', {
        'solicitacoes': lista_sol, 'status': status, 'contagens': contagens,
        'clientes': Cliente.objects.filter(ativo=True).order_by('razao_social'),
    })


@login_required
@require_POST
def aceitar(request, pk):
    """Cria a OS com o que veio na solicitação. Cidade/UF vêm do formulário
    (o palpite do endereço é só sugestão) e a OS nasce ABERTA, sem equipe:
    quem escala é a operação, na tela de sempre."""
    from .models import Cliente, OrdemServico, SolicitacaoEscolta, VeiculoEscoltado
    sol = get_object_or_404(SolicitacaoEscolta, pk=pk)
    if sol.status != 'aguardando':
        messages.error(request, 'Esta solicitação já foi respondida.')
        return redirect('solicitacoes')

    cliente_id = request.POST.get('cliente') or ''
    cliente = Cliente.objects.filter(pk=cliente_id).first() if cliente_id else None
    if cliente is None:
        messages.error(request, 'Escolha o cliente para gerar a OS.')
        return redirect('solicitacoes')

    with transaction.atomic():
        sol = SolicitacaoEscolta.objects.select_for_update().get(pk=pk)
        if sol.status != 'aguardando':       # dois operadores clicando junto
            messages.error(request, 'Esta solicitação já foi respondida.')
            return redirect('solicitacoes')

        inicio = None
        if sol.data_missao:
            inicio = timezone.make_aware(datetime.combine(
                sol.data_missao, sol.hora_missao or datetime.min.time()))

        os_obj = OrdemServico.objects.create(
            cliente=cliente,
            status='aberta',
            solicitante=sol.solicitante or sol.origem,
            forma_solicitacao='sistema',
            tipo_viagem=(request.POST.get('tipo_viagem') or 'rodoviaria'),
            previsao_inicio=inicio or timezone.now(),
            cidade_origem=(request.POST.get('cidade_origem') or '').strip(),
            uf_origem=(request.POST.get('uf_origem') or '').strip().upper()[:2],
            cidade_destino=(request.POST.get('cidade_destino') or '').strip(),
            uf_destino=(request.POST.get('uf_destino') or '').strip().upper()[:2],
            observacoes=_observacoes(sol),
            # o JR ainda nao tem 'criado_por' - o arquivo e o mesmo nos 3
            **({'criado_por': request.user}
               if _tem_campo(OrdemServico, 'criado_por') else {}),
        )
        if sol.placa_veiculo or sol.motorista:
            VeiculoEscoltado.objects.create(
                os=os_obj, veiculo='', placa_cavalo=sol.placa_veiculo or '',
                motorista=sol.motorista or '',
                **({'motorista_telefone': sol.motorista_telefone or ''}
                   if _tem_campo(VeiculoEscoltado, 'motorista_telefone') else {}))

        sol.status = 'aceita'
        sol.os = os_obj
        sol.respondida_em = timezone.now()
        sol.respondida_por = request.user
        sol.save()

    messages.success(request, 'Solicitação aceita — OS %s criada.' % os_obj.numero)
    return redirect('os_detalhe', pk=os_obj.pk)


@login_required
@require_POST
def recusar(request, pk):
    from .models import SolicitacaoEscolta
    sol = get_object_or_404(SolicitacaoEscolta, pk=pk)
    if sol.status != 'aguardando':
        messages.error(request, 'Esta solicitação já foi respondida.')
        return redirect('solicitacoes')
    motivo = (request.POST.get('motivo') or '').strip()
    if not motivo:
        messages.error(request, 'Diga o motivo da recusa — é o que o contratante vai ler.')
        return redirect('solicitacoes')
    sol.status = 'recusada'
    sol.motivo_recusa = motivo[:300]
    sol.respondida_em = timezone.now()
    sol.respondida_por = request.user
    sol.save()
    messages.success(request, 'Solicitação recusada.')
    return redirect('solicitacoes')


def _observacoes(sol):
    linhas = ['Solicitação %s · OS %s' % (sol.origem, sol.numero_os_hub)]
    if sol.numero_se:
        linhas.append('Nº S.E.: %s' % sol.numero_se)
    if sol.equipes:
        linhas.append('Equipes/VTR: %s' % sol.equipes)
    if sol.endereco_origem:
        linhas.append('Origem: %s' % sol.endereco_origem)
    if sol.endereco_destino:
        linhas.append('Destino: %s' % sol.endereco_destino)
    if sol.conta_espelhamento:
        linhas.append('Espelhamento: %s' % sol.conta_espelhamento)
    if sol.observacoes:
        linhas.append(sol.observacoes)
    return '\n'.join(linhas)


def _tem_campo(model, nome):
    return nome in {f.name for f in model._meta.get_fields()}
