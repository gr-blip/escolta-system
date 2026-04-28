from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Q, Count, Case, When, IntegerField
from django.http import JsonResponse
from django.utils import timezone
from datetime import date, timedelta
from .models import Agente, Viatura, Rastreador, Armamento, Cliente, Colete, Equipe, \
    FotoMarco, Parada, FotoParada, Incidente, FotoIncidente, FotoVeiculoEscoltado, \
    TrocaMotorista, FotoTrocaMotorista, AssinaturaOS, DespesaOS, FuncionarioPatrimonial
from .forms import AgenteForm, ViaturaForm, RastreadorForm, ArmamentoForm, ClienteForm, \
    FuncionarioPatrimonialForm


# ─────────────────────────────────────────────────────────────────────────────
# Helper: situação da frota em 1 query usando Case/When
# ─────────────────────────────────────────────────────────────────────────────
def _fleet_data():
    agg = Viatura.objects.aggregate(
        ativa=Count(Case(When(status='ativa', then=1), output_field=IntegerField())),
        manutencao=Count(Case(When(status='manutencao', then=1), output_field=IntegerField())),
        inativa=Count(Case(When(status='inativa', then=1), output_field=IntegerField())),
    )
    return {k: (v or 0) for k, v in agg.items()}


# ─────────────────────────────────────────────────────────────────────────────
# Helper: agrega Ordens de Serviço por dia nos últimos N dias (zeros preenchidos)
# ─────────────────────────────────────────────────────────────────────────────
def _os_por_dia(n_dias=14):
    # Import local para evitar dependência caso OrdemServico seja movido
    from .models import OrdemServico

    hoje = timezone.localdate()
    inicio = hoje - timedelta(days=n_dias - 1)

    buckets = {(inicio + timedelta(days=i)): 0 for i in range(n_dias)}

    qs = OrdemServico.objects.filter(criado_em__date__gte=inicio).values_list('criado_em', flat=True)
    for dt in qs:
        d = timezone.localtime(dt).date() if timezone.is_aware(dt) else dt.date()
        if d in buckets:
            buckets[d] += 1

    dias_ord = sorted(buckets.keys())
    return {
        'labels': [d.strftime('%d/%m') for d in dias_ord],
        'values': [buckets[d] for d in dias_ord],
    }


# ─────────────────────────────────────────────────────────────────────────────
# Endpoint JSON: OS por cliente com filtro de data (usado pelo gráfico do dashboard)
# ─────────────────────────────────────────────────────────────────────────────
@login_required
def dashboard_os_por_cliente(request):
    from .models import OrdemServico
    from django.db.models import Count as _Count

    hoje = timezone.localdate()

    raw_ini = request.GET.get('inicio', '')
    raw_fim = request.GET.get('fim', '')

    try:
        dt_ini = date.fromisoformat(raw_ini) if raw_ini else hoje.replace(day=1)
    except ValueError:
        dt_ini = hoje.replace(day=1)

    try:
        dt_fim = date.fromisoformat(raw_fim) if raw_fim else hoje
    except ValueError:
        dt_fim = hoje

    qs = (
        OrdemServico.objects
        .filter(criado_em__date__gte=dt_ini, criado_em__date__lte=dt_fim)
        .values('cliente__razao_social')
        .annotate(total=_Count('id'))
        .order_by('-total')[:20]
    )

    labels = [item['cliente__razao_social'] or '—' for item in qs]
    values = [item['total'] for item in qs]

    return JsonResponse({
        'labels': labels,
        'values': values,
        'inicio': dt_ini.isoformat(),
        'fim':    dt_fim.isoformat(),
    })


@login_required
def dashboard(request):
    hoje = date.today()
    limite = hoje + timedelta(days=60)  # 2 meses à frente

    # CNH vencida ou vencendo em até 2 meses (agentes ativos) — com .only()
    alertas_cnh = (
        Agente.objects
        .filter(status='ativo')
        .exclude(cnh_validade__isnull=True)
        .filter(cnh_validade__lte=limite)
        .order_by('cnh_validade')
        .only('id', 'nome', 'cnh_validade')
    )

    # CNV vencida ou vencendo em até 2 meses (agentes ativos) — com .only()
    alertas_cnv = (
        Agente.objects
        .filter(status='ativo')
        .exclude(cnv_validade__isnull=True)
        .filter(cnv_validade__lte=limite)
        .order_by('cnv_validade')
        .only('id', 'nome', 'cnv_validade')
    )

    # Coletes vencidos ou vencendo em até 2 meses — com .only()
    alertas_coletes = (
        Colete.objects
        .exclude(validade__isnull=True)
        .filter(validade__lte=limite)
        .order_by('validade')
        .only('id', 'marca', 'numeracao', 'validade')
    )

    context = {
        'total_agentes': Agente.objects.filter(status='ativo').count(),
        'total_viaturas': Viatura.objects.filter(status='ativa').count(),
        'total_clientes': Cliente.objects.count(),
        'total_armamentos': Armamento.objects.count(),
        'agentes_recentes': Agente.objects.order_by('-criado_em')[:5]
                                          .only('id', 'nome', 'funcao', 'status'),
        'viaturas': Viatura.objects.order_by('-criado_em')[:5]
                                    .only('id', 'placa', 'marca_modelo', 'status'),
        'alertas_cnh': alertas_cnh,
        'alertas_cnv': alertas_cnv,
        'alertas_coletes': alertas_coletes,
        'hoje': hoje,
        # NOVO — dados para os gráficos Chart.js do dashboard.html
        'fleet_data': _fleet_data(),
        'os_por_dia': _os_por_dia(14),
    }
    return render(request, 'cadastros/dashboard.html', context)


# ── AGENTES ──────────────────────────────────────────────────────────────────

@login_required
def agente_list(request):
    q = request.GET.get('q', '')
    agentes = Agente.objects.all()
    if q:
        agentes = agentes.filter(Q(nome__icontains=q) | Q(cpf__icontains=q) | Q(rg__icontains=q))
    return render(request, 'cadastros/agente_list.html', {'agentes': agentes, 'q': q})


@login_required
def agente_create(request):
    form = AgenteForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Agente cadastrado com sucesso!')
        return redirect('agente_list')
    return render(request, 'cadastros/agente_form.html', {'form': form, 'titulo': 'Novo Agente'})


@login_required
def agente_edit(request, pk):
    agente = get_object_or_404(Agente, pk=pk)
    form = AgenteForm(request.POST or None, request.FILES or None, instance=agente)
    if form.is_valid():
        form.save()
        messages.success(request, 'Agente atualizado com sucesso!')
        return redirect('agente_list')
    return render(request, 'cadastros/agente_form.html', {'form': form, 'titulo': 'Editar Agente', 'obj': agente})


@login_required
def agente_delete(request, pk):
    agente = get_object_or_404(Agente, pk=pk)
    if request.method == 'POST':
        agente.delete()
        messages.success(request, 'Agente removido.')
        return redirect('agente_list')
    return render(request, 'cadastros/confirm_delete.html', {'obj': agente, 'tipo': 'Agente'})


# ── VIATURAS ─────────────────────────────────────────────────────────────────

@login_required
def viatura_list(request):
    q = request.GET.get('q', '')
    viaturas = Viatura.objects.all()
    if q:
        viaturas = viaturas.filter(Q(placa__icontains=q) | Q(marca_modelo__icontains=q) | Q(frota__icontains=q))
    return render(request, 'cadastros/viatura_list.html', {'viaturas': viaturas, 'q': q})


@login_required
def viatura_create(request):
    form = ViaturaForm(request.POST or None)
    rastreadores = Rastreador.objects.all().order_by('marca', 'modelo')
    if form.is_valid():
        form.save()
        messages.success(request, 'Viatura cadastrada com sucesso!')
        return redirect('viatura_list')
    return render(request, 'cadastros/viatura_form.html', {'form': form, 'titulo': 'Nova Viatura', 'rastreadores': rastreadores})


@login_required
def viatura_edit(request, pk):
    viatura = get_object_or_404(Viatura, pk=pk)
    form = ViaturaForm(request.POST or None, instance=viatura)
    rastreadores = Rastreador.objects.all().order_by('marca', 'modelo')
    if form.is_valid():
        form.save()
        messages.success(request, 'Viatura atualizada com sucesso!')
        return redirect('viatura_list')
    return render(request, 'cadastros/viatura_form.html', {'form': form, 'titulo': 'Editar Viatura', 'obj': viatura, 'rastreadores': rastreadores})


@login_required
def viatura_delete(request, pk):
    viatura = get_object_or_404(Viatura, pk=pk)
    if request.method == 'POST':
        viatura.delete()
        messages.success(request, 'Viatura removida.')
        return redirect('viatura_list')
    return render(request, 'cadastros/confirm_delete.html', {'obj': viatura, 'tipo': 'Viatura'})


# ── RASTREADORES ──────────────────────────────────────────────────────────────

@login_required
def rastreador_list(request):
    q = request.GET.get('q', '')
    rastreadores = Rastreador.objects.all()
    if q:
        rastreadores = rastreadores.filter(Q(marca__icontains=q) | Q(numero_serie__icontains=q) | Q(modelo__icontains=q))
    return render(request, 'cadastros/rastreador_list.html', {'rastreadores': rastreadores, 'q': q})


@login_required
def rastreador_create(request):
    form = RastreadorForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Rastreador cadastrado com sucesso!')
        return redirect('rastreador_list')
    return render(request, 'cadastros/rastreador_form.html', {'form': form, 'titulo': 'Novo Rastreador'})


@login_required
def rastreador_edit(request, pk):
    rastreador = get_object_or_404(Rastreador, pk=pk)
    form = RastreadorForm(request.POST or None, instance=rastreador)
    if form.is_valid():
        form.save()
        messages.success(request, 'Rastreador atualizado com sucesso!')
        return redirect('rastreador_list')
    return render(request, 'cadastros/rastreador_form.html', {'form': form, 'titulo': 'Editar Rastreador', 'obj': rastreador})


@login_required
def rastreador_delete(request, pk):
    rastreador = get_object_or_404(Rastreador, pk=pk)
    if request.method == 'POST':
        rastreador.delete()
        messages.success(request, 'Rastreador removido.')
        return redirect('rastreador_list')
    return render(request, 'cadastros/confirm_delete.html', {'obj': rastreador, 'tipo': 'Rastreador'})


# ── ARMAMENTO ─────────────────────────────────────────────────────────────────

@login_required
def armamento_list(request):
    q = request.GET.get('q', '')
    armamentos = Armamento.objects.all()
    if q:
        armamentos = armamentos.filter(Q(marca__icontains=q) | Q(numero_serie__icontains=q) | Q(registro_cr__icontains=q))
    return render(request, 'cadastros/armamento_list.html', {'armamentos': armamentos, 'q': q})


@login_required
def armamento_create(request):
    form = ArmamentoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Armamento cadastrado com sucesso!')
        return redirect('armamento_list')
    return render(request, 'cadastros/armamento_form.html', {'form': form, 'titulo': 'Novo Armamento'})


@login_required
def armamento_edit(request, pk):
    armamento = get_object_or_404(Armamento, pk=pk)
    form = ArmamentoForm(request.POST or None, instance=armamento)
    if form.is_valid():
        form.save()
        messages.success(request, 'Armamento atualizado com sucesso!')
        return redirect('armamento_list')
    return render(request, 'cadastros/armamento_form.html', {'form': form, 'titulo': 'Editar Armamento', 'obj': armamento})


@login_required
def armamento_delete(request, pk):
    armamento = get_object_or_404(Armamento, pk=pk)
    if request.method == 'POST':
        armamento.delete()
        messages.success(request, 'Armamento removido.')
        return redirect('armamento_list')
    return render(request, 'cadastros/confirm_delete.html', {'obj': armamento, 'tipo': 'Armamento'})


# ── CLIENTES ──────────────────────────────────────────────────────────────────

@login_required
def cliente_list(request):
    q = request.GET.get('q', '')
    mostrar_inativos = request.GET.get('inativos') == '1'
    clientes = Cliente.objects.all() if mostrar_inativos else Cliente.objects.filter(ativo=True)
    if q:
        clientes = clientes.filter(Q(razao_social__icontains=q) | Q(cnpj__icontains=q))
    return render(request, 'cadastros/cliente_list.html', {
        'clientes': clientes, 'q': q, 'mostrar_inativos': mostrar_inativos,
        'is_admin': _is_admin_or_developer(request.user),
    })


@login_required
def cliente_create(request):
    form = ClienteForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Cliente cadastrado com sucesso!')
        return redirect('cliente_list')
    return render(request, 'cadastros/cliente_form.html', {'form': form, 'titulo': 'Novo Cliente'})


@login_required
def cliente_edit(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    form = ClienteForm(request.POST or None, instance=cliente)
    if form.is_valid():
        form.save()
        messages.success(request, 'Cliente atualizado com sucesso!')
        return redirect('cliente_list')
    return render(request, 'cadastros/cliente_form.html', {'form': form, 'titulo': 'Editar Cliente', 'obj': cliente})


@login_required
def cliente_inativar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.ativo = not cliente.ativo
        cliente.save()
        status = 'reativado' if cliente.ativo else 'inativado'
        messages.success(request, f'Cliente {status} com sucesso.')
        return redirect('cliente_list')
    return render(request, 'cadastros/cliente_inativar.html', {'obj': cliente})


@login_required
def cliente_deletar_definitivo(request, pk):
    """Exclusão permanente do cliente — somente admin/developer.
    Bloqueado se houver OS ou tabelas de preço vinculadas."""
    if not _is_admin_or_developer(request.user):
        messages.error(request, 'Sem permissão para esta ação.')
        return redirect('cliente_list')

    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        total_os = cliente.ordens_servico.count()
        total_tp = cliente.tabelas_preco.count()
        if total_os or total_tp:
            msgs = []
            if total_os: msgs.append(f'{total_os} Ordem(ns) de Serviço')
            if total_tp: msgs.append(f'{total_tp} Tabela(s) de Preço')
            messages.error(request,
                f'Não é possível excluir: cliente possui {" e ".join(msgs)} vinculada(s).')
            return redirect('cliente_list')
        nome = cliente.razao_social
        cliente.delete()
        messages.success(request, f'Cliente "{nome}" excluído definitivamente.')
        return redirect('cliente_list')

    return render(request, 'cadastros/cliente_deletar_confirm.html', {'obj': cliente})


# ── COLETES ───────────────────────────────────────────────────────────────────

from .forms import ColeteForm

@login_required
def colete_list(request):
    q = request.GET.get('q', '')
    coletes = Colete.objects.all()
    if q:
        coletes = coletes.filter(Q(marca__icontains=q) | Q(numeracao__icontains=q))
    return render(request, 'cadastros/colete_list.html', {'coletes': coletes, 'q': q})


@login_required
def colete_create(request):
    form = ColeteForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Colete cadastrado com sucesso!')
        return redirect('colete_list')
    return render(request, 'cadastros/colete_form.html', {'form': form, 'titulo': 'Novo Colete'})


@login_required
def colete_edit(request, pk):
    colete = get_object_or_404(Colete, pk=pk)
    form = ColeteForm(request.POST or None, instance=colete)
    if form.is_valid():
        form.save()
        messages.success(request, 'Colete atualizado com sucesso!')
        return redirect('colete_list')
    return render(request, 'cadastros/colete_form.html', {'form': form, 'titulo': 'Editar Colete', 'obj': colete})


@login_required
def colete_delete(request, pk):
    colete = get_object_or_404(Colete, pk=pk)
    if request.method == 'POST':
        colete.delete()
        messages.success(request, 'Colete removido.')
        return redirect('colete_list')
    return render(request, 'cadastros/confirm_delete.html', {'obj': colete, 'tipo': 'Colete'})


# ── EQUIPES ───────────────────────────────────────────────────────────────────

@login_required
def equipe_list(request):
    q = request.GET.get('q', '')
    mostrar_finalizadas = request.GET.get('finalizadas', '') == '1'
    equipes = Equipe.objects.select_related(
        'agente1', 'agente2',
        'armamento_agente1', 'armamento_agente2', 'armamento_extra',
        'colete1', 'colete2'
    ).all()
    if not mostrar_finalizadas:
        equipes = equipes.exclude(status='finalizada')
    if q:
        equipes = equipes.filter(
            Q(nome__icontains=q) |
            Q(agente1__nome__icontains=q) |
            Q(agente2__nome__icontains=q)
        )
    return render(request, 'cadastros/equipe_list.html', {
        'equipes': equipes, 'q': q,
        'mostrar_finalizadas': mostrar_finalizadas,
    })


@login_required
def equipe_finalizar(request, pk):
    equipe = get_object_or_404(Equipe, pk=pk)
    if request.method == 'POST':
        equipe.status = 'finalizada'
        equipe.save(update_fields=['status'])
        messages.success(request, f'Equipe {equipe.nome} finalizada.')
        return redirect('equipe_list')
    return render(request, 'cadastros/confirm_delete.html', {
        'obj': equipe,
        'tipo': 'Equipe',
        'acao': 'Finalizar',
        'msg': 'Ao finalizar, a equipe não aparecerá mais na listagem padrão. Os dados das Ordens de Serviço vinculadas serão preservados.',
        'btn_label': 'Confirmar Finalização',
        'btn_class': 'btn-warning',
    })


@login_required
def equipe_create(request):
    agentes    = Agente.objects.filter(status='ativo').order_by('nome')
    armamentos = Armamento.objects.all().order_by('tipo', 'marca')
    coletes    = Colete.objects.all().order_by('marca')
    viaturas   = Viatura.objects.filter(status='ativa').order_by('marca_modelo')

    if request.method == 'POST':
        try:
            equipe = Equipe(
                nome              = request.POST['nome'],
                agente1_id        = request.POST['agente1'],
                agente2_id        = request.POST['agente2'],
                armamento_agente1_id = request.POST['armamento_agente1'],
                armamento_agente2_id = request.POST['armamento_agente2'],
                armamento_extra_id   = request.POST.get('armamento_extra') or None,
                colete1_id        = request.POST['colete1'],
                colete2_id        = request.POST['colete2'],
                viatura_id        = request.POST.get('viatura') or None,
                status            = request.POST.get('status', 'ativa'),
                observacoes       = request.POST.get('observacoes', ''),
            )
            equipe.save()
            messages.success(request, 'Equipe criada com sucesso!')
            return redirect('equipe_list')
        except Exception as e:
            messages.error(request, f'Erro ao salvar equipe: {e}')

    return render(request, 'cadastros/equipe_form.html', {
        'titulo': 'Nova Equipe',
        'agentes': agentes,
        'armamentos': armamentos,
        'coletes': coletes,
        'viaturas': viaturas,
    })


@login_required
def equipe_edit(request, pk):
    equipe     = get_object_or_404(Equipe, pk=pk)
    agentes    = Agente.objects.filter(status='ativo').order_by('nome')
    armamentos = Armamento.objects.all().order_by('tipo', 'marca')
    coletes    = Colete.objects.all().order_by('marca')
    viaturas   = Viatura.objects.filter(status='ativa').order_by('marca_modelo')

    if request.method == 'POST':
        try:
            equipe.nome               = request.POST['nome']
            equipe.agente1_id         = request.POST['agente1']
            equipe.agente2_id         = request.POST['agente2']
            equipe.armamento_agente1_id = request.POST['armamento_agente1']
            equipe.armamento_agente2_id = request.POST['armamento_agente2']
            equipe.armamento_extra_id  = request.POST.get('armamento_extra') or None
            equipe.colete1_id         = request.POST['colete1']
            equipe.colete2_id         = request.POST['colete2']
            equipe.viatura_id         = request.POST.get('viatura') or None
            equipe.status             = request.POST.get('status', 'ativa')
            equipe.observacoes        = request.POST.get('observacoes', '')
            equipe.save()
            messages.success(request, 'Equipe atualizada com sucesso!')
            return redirect('equipe_list')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar equipe: {e}')

    return render(request, 'cadastros/equipe_form.html', {
        'titulo': 'Editar Equipe',
        'obj': equipe,
        'agentes': agentes,
        'armamentos': armamentos,
        'coletes': coletes,
        'viaturas': viaturas,
    })


@login_required
def equipe_delete(request, pk):
    equipe = get_object_or_404(Equipe, pk=pk)
    # Bloqueia exclusão se houver OS abertas vinculadas
    STATUS_ABERTOS = ['aberta', 'em_viagem', 'em_operacao', 'encerrando', 'concluida']
    os_abertas = OrdemServico.objects.filter(equipe=equipe, status__in=STATUS_ABERTOS)
    if os_abertas.exists():
        messages.error(request, f'Não é possível excluir: equipe vinculada a {os_abertas.count()} OS em aberto. Finalize as OS antes de excluir.')
        return redirect('equipe_list')
    if request.method == 'POST':
        equipe.delete()
        messages.success(request, 'Equipe removida.')
        return redirect('equipe_list')
    return render(request, 'cadastros/confirm_delete.html', {'obj': equipe, 'tipo': 'Equipe'})


# ── ORDENS DE SERVIÇO ─────────────────────────────────────────────────────────

from .models import OrdemServico

@login_required
def os_list(request):
    """
    Listagem de Ordens de Serviço.

    Por padrão (sem filtros), esconde OS com status='finalizada' ou 'cancelada'
    — finalizadas ficam visíveis na tela de Boletim de Medição, canceladas
    só fazem sentido via consulta explícita.

    Quando qualquer filtro é aplicado (q, data_de, data_ate ou clientes), a
    lista passa a mostrar TODOS os status, incluindo finalizadas/canceladas,
    pra permitir consulta histórica.
    """
    from django.utils.dateparse import parse_date

    q = request.GET.get('q', '').strip()
    data_de_str = request.GET.get('data_de', '').strip()
    data_ate_str = request.GET.get('data_ate', '').strip()
    # Multi-select de clientes: espera `clientes=1&clientes=7&...`.
    # getlist preserva múltiplos valores do mesmo name no GET.
    # Sanitização: aceita só dígitos pra não explodir o queryset com valor
    # inválido vindo de URL manipulada.
    clientes_ids = [c for c in request.GET.getlist('clientes') if c.isdigit()]

    # parse_date retorna None se a string estiver vazia ou mal formatada
    data_de = parse_date(data_de_str) if data_de_str else None
    data_ate = parse_date(data_ate_str) if data_ate_str else None

    ordens = OrdemServico.objects.select_related('cliente', 'equipe').all()

    tem_filtro = bool(q or data_de or data_ate or clientes_ids)

    if q:
        ordens = ordens.filter(
            Q(numero__icontains=q) |
            Q(cliente__razao_social__icontains=q) |
            Q(solicitante__icontains=q)
        )
    if data_de:
        ordens = ordens.filter(previsao_inicio__date__gte=data_de)
    if data_ate:
        ordens = ordens.filter(previsao_inicio__date__lte=data_ate)
    if clientes_ids:
        ordens = ordens.filter(cliente_id__in=clientes_ids)

    if not tem_filtro:
        # Sem filtros: esconde finalizadas (vão pra Boletim) e canceladas.
        ordens = ordens.exclude(status__in=['finalizada', 'cancelada'])

    # Lista completa (ativos + inativos) pro dropdown do filtro.
    # Inativos entram pra permitir consulta histórica de OS de clientes
    # que foram desativados depois. O template marca visualmente inativos.
    todos_clientes = Cliente.objects.all().order_by('razao_social')

    return render(request, 'cadastros/os_list.html', {
        'ordens': ordens,
        'q': q,
        'data_de': data_de_str,
        'data_ate': data_ate_str,
        'tem_filtro': tem_filtro,
        'todos_clientes': todos_clientes,
        'clientes_selecionados': clientes_ids,  # lista de strings de IDs
    })


@login_required
def os_finalizar(request, pk):
    from django.utils import timezone
    os_obj = get_object_or_404(OrdemServico, pk=pk)
    if os_obj.status == 'finalizada':
        messages.warning(request, 'Esta OS já está finalizada.')
        return redirect('os_list')
    if request.method == 'POST':
        os_obj.status = 'finalizada'
        os_obj.finalizada_em = timezone.now()
        # Salva snapshot da equipe antes de finalizar
        eq = os_obj.equipe
        if eq:
            os_obj.snap_equipe_nome = eq.nome or ''
            a1 = eq.agente1
            if a1:
                os_obj.snap_agente1_nome     = a1.nome or ''
                os_obj.snap_agente1_cpf      = a1.cpf or ''
                os_obj.snap_agente1_rg       = a1.rg or ''
                os_obj.snap_agente1_telefone = a1.telefone or ''
                os_obj.snap_agente1_cnh      = a1.cnh or ''
                os_obj.snap_agente1_cnv      = a1.cnv or ''
                os_obj.snap_agente1_foto     = a1.foto.name if a1.foto else ''
            a2 = eq.agente2
            if a2:
                os_obj.snap_agente2_nome     = a2.nome or ''
                os_obj.snap_agente2_cpf      = a2.cpf or ''
                os_obj.snap_agente2_rg       = a2.rg or ''
                os_obj.snap_agente2_telefone = a2.telefone or ''
                os_obj.snap_agente2_cnh      = a2.cnh or ''
                os_obj.snap_agente2_cnv      = a2.cnv or ''
                os_obj.snap_agente2_foto     = a2.foto.name if a2.foto else ''
            v = eq.viatura
            if v:
                os_obj.snap_viatura_modelo = v.marca_modelo or ''
                os_obj.snap_viatura_placa  = v.placa or ''
                os_obj.snap_viatura_cor    = v.cor or ''
                os_obj.snap_viatura_frota  = v.frota or ''
                os_obj.snap_viatura_mct    = v.mct_id or ''
        os_obj.save()
        messages.success(request, f'OS-{os_obj.numero} finalizada com sucesso. Dados bloqueados para edição.')
        return redirect('os_list')
    return render(request, 'cadastros/confirm_delete.html', {
        'obj': os_obj,
        'tipo': 'Ordem de Serviço',
        'acao': 'Finalizar',
        'msg': 'Ao finalizar, todos os dados desta OS serão bloqueados e não poderão ser alterados.',
        'btn_label': 'Confirmar Finalização',
        'btn_class': 'btn-warning',
    })


@login_required
def os_nova(request):
    """Passo 1 — formulário rápido de abertura"""
    clientes = Cliente.objects.all().order_by('razao_social')
    UFS = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG',
           'PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO']
    if request.method == 'POST':
        from urllib.parse import urlencode
        params = urlencode({
            'cliente_id':        request.POST.get('cliente', ''),
            'solicitante':       request.POST.get('solicitante', ''),
            'forma_solicitacao': request.POST.get('forma_solicitacao', ''),
            'tipo_viagem':       request.POST.get('tipo_viagem', ''),
            'previsao_inicio':   request.POST.get('previsao_inicio', ''),
            'previsao_retorno':  request.POST.get('previsao_retorno', ''),
            'imediata':          request.POST.get('imediata', ''),
            'cidade_origem':     request.POST.get('cidade_origem', ''),
            'uf_origem':         request.POST.get('uf_origem', 'GO'),
            'cidade_destino':    request.POST.get('cidade_destino', ''),
            'uf_destino':        request.POST.get('uf_destino', 'GO'),
        })
        return redirect(f'/operacional/os/nova/detalhe/?{params}')
    return render(request, 'cadastros/os_nova.html', {'clientes': clientes, 'ufs': UFS})


@login_required
def os_detalhe_novo(request):
    """Passo 2 — detalhe completo da OS com equipe"""
    # Lê dados do GET (passados pelo passo 1 via query string, sem session)
    draft = {
        'cliente_id':        request.GET.get('cliente_id', ''),
        'solicitante':       request.GET.get('solicitante', ''),
        'forma_solicitacao': request.GET.get('forma_solicitacao', ''),
        'tipo_viagem':       request.GET.get('tipo_viagem', ''),
        'previsao_inicio':   request.GET.get('previsao_inicio', ''),
        'previsao_retorno':  request.GET.get('previsao_retorno', ''),
        'imediata':          request.GET.get('imediata', ''),
        'cidade_origem':     request.GET.get('cidade_origem', ''),
        'uf_origem':         request.GET.get('uf_origem', 'GO'),
        'cidade_destino':    request.GET.get('cidade_destino', ''),
        'uf_destino':        request.GET.get('uf_destino', 'GO'),
    }
    if not draft.get('cliente_id') and request.method != 'POST':
        return redirect('os_nova')

    clientes = Cliente.objects.all().order_by('razao_social')
    equipes  = Equipe.objects.select_related('agente1','agente2','viatura').filter(status__in=['ativa','em_servico'])

    cliente_obj = None
    if draft.get('cliente_id'):
        try:
            cliente_obj = Cliente.objects.get(pk=draft['cliente_id'])
        except Cliente.DoesNotExist:
            pass

    UFS = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG',
           'PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO']

    if request.method == 'POST':
        from django.utils import timezone as tz
        from datetime import datetime
        def parse_dt(val):
            if not val:
                return None
            for fmt in ('%Y-%m-%dT%H:%M', '%d/%m/%Y %H:%M', '%Y-%m-%d %H:%M'):
                try:
                    return datetime.strptime(val, fmt)
                except ValueError:
                    continue
            return None

        try:
            os = OrdemServico(
                cliente_id        = request.POST.get('cliente'),
                solicitante       = request.POST.get('solicitante', ''),
                forma_solicitacao = request.POST.get('forma_solicitacao'),
                tipo_viagem       = request.POST.get('tipo_viagem'),
                previsao_inicio   = parse_dt(request.POST.get('previsao_inicio')),
                previsao_retorno  = parse_dt(request.POST.get('previsao_retorno')),
                imediata          = bool(request.POST.get('imediata')),
                cidade_origem     = request.POST.get('cidade_origem', ''),
                uf_origem         = request.POST.get('uf_origem', 'GO'),
                cidade_destino    = request.POST.get('cidade_destino', ''),
                uf_destino        = request.POST.get('uf_destino', 'GO'),
                equipe_id         = request.POST.get('equipe') or None,
                observacoes       = request.POST.get('observacoes', ''),
                status            = 'aberta',
            )
            os.save()
            messages.success(request, f'OS {os.numero} aberta com sucesso!')
            return redirect('os_detalhe', pk=os.pk)
        except Exception as e:
            messages.error(request, f'Erro ao salvar OS: {e}')

    return render(request, 'cadastros/os_detalhe.html', {
        'draft': draft,
        'cliente_obj': cliente_obj,
        'clientes': clientes,
        'equipes': equipes,
        'ufs': UFS,
        'novo': True,
        'forma_choices': OrdemServico.FORMA_CHOICES,
    })


@login_required
def os_detalhe(request, pk):
    """Visualizar / editar OS existente"""
    os = get_object_or_404(OrdemServico, pk=pk)
    clientes = Cliente.objects.all().order_by('razao_social')
    equipes  = Equipe.objects.select_related('agente1','agente2','viatura').filter(status__in=['ativa','em_servico'])
    UFS = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG',
           'PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO']

    if request.method == 'POST':
        if os.status == 'finalizada':
            messages.error(request, 'Esta OS está finalizada e não pode ser alterada.')
            return redirect('os_detalhe', pk=os.pk)
        from datetime import datetime
        def parse_dt(val):
            if not val:
                return None
            for fmt in ('%Y-%m-%dT%H:%M', '%d/%m/%Y %H:%M', '%Y-%m-%d %H:%M'):
                try:
                    return datetime.strptime(val, fmt)
                except ValueError:
                    continue
            return None
        try:
            os.cliente_id        = request.POST.get('cliente')
            os.solicitante       = request.POST.get('solicitante', '')
            os.forma_solicitacao = request.POST.get('forma_solicitacao')
            os.tipo_viagem       = request.POST.get('tipo_viagem')
            os.previsao_inicio   = parse_dt(request.POST.get('previsao_inicio'))
            os.previsao_retorno  = parse_dt(request.POST.get('previsao_retorno'))
            os.imediata          = bool(request.POST.get('imediata'))
            os.cidade_origem     = request.POST.get('cidade_origem', '')
            os.uf_origem         = request.POST.get('uf_origem', 'GO')
            os.cidade_destino    = request.POST.get('cidade_destino', '')
            os.uf_destino        = request.POST.get('uf_destino', 'GO')
            os.equipe_id         = request.POST.get('equipe') or None
            os.observacoes       = request.POST.get('observacoes', '')
            os.status            = request.POST.get('status', os.status)
            os.save()
            messages.success(request, 'OS atualizada com sucesso!')
            return redirect('os_detalhe', pk=os.pk)
        except Exception as e:
            messages.error(request, f'Erro ao atualizar OS: {e}')

    veiculos_qs = list(os.veiculos.all()) if hasattr(os, 'veiculos') else []
    veiculos_map = {v.ordem: v for v in veiculos_qs}
    veiculo_slots = []
    for i in range(1, 5):
        v = veiculos_map.get(i)
        veiculo_slots.append({
            'num': i,
            'veiculo':      v.veiculo      if v else '',
            'placa_cavalo': v.placa_cavalo if v else '',
            'placa_carreta':v.placa_carreta if v else '',
            'placa_carreta2':v.placa_carreta2 if v else '',
            'motorista':    v.motorista    if v else '',
        })

    # Fotos dos marcos operacionais
    MARCOS_LISTA = [
        ('inicio_viagem',     'Início de Viagem'),
        ('chegada_operacao',  'Chegada Operação'),
        ('inicio_operacao',   'Início Operação'),
        ('termino_operacao',  'Término Operação'),
        ('termino_viagem',    'Término de Viagem'),
    ]
    fotos_marco = {}
    op_obj = getattr(os, 'operacional', None)
    if op_obj:
        for foto in FotoMarco.objects.filter(os=os):
            fotos_marco[foto.marco] = foto.foto.url

    # Assinaturas digitais
    assinaturas_lista = list(AssinaturaOS.objects.filter(os=os).order_by('tipo'))

    # Veículos escoltados com fotos
    from .models import VeiculoEscoltado, FotoVeiculoEscoltado
    veiculos_print = []
    for v in os.veiculos.order_by('ordem'):
        fotos = list(FotoVeiculoEscoltado.objects.filter(veiculo=v))
        veiculos_print.append({'veiculo': v, 'fotos': fotos})

    return render(request, 'cadastros/os_detalhe.html', {
        'os': os,
        'clientes': clientes,
        'equipes': equipes,
        'ufs': UFS,
        'novo': False,
        'forma_choices': OrdemServico.FORMA_CHOICES,
        'operacional': OSOperacional.objects.filter(os=os).first(),
        'op': OSOperacional.objects.filter(os=os).first(),
        'veiculos': veiculos_qs,
        'veiculo_slots': veiculo_slots,
        'fotos_marco': fotos_marco,
        'fotos_marco_lista': MARCOS_LISTA,
        'assinaturas_lista': assinaturas_lista,
        'veiculos_print': veiculos_print,
    })


@login_required
def os_delete(request, pk):
    """Mantido por compatibilidade — redireciona para os_cancelar."""
    return redirect('os_cancelar', pk=pk)


@login_required
def os_cancelar(request, pk):
    """
    Cancela uma OS sem excluí-la do banco.
    POST com campo 'tipo': 'com_deslocamento' | 'sem_deslocamento'.
    Após cancelar, cria um BoletimMedicao (se não existir) para que o
    financeiro consiga visualizar a OS cancelada no Boletim de Medição.
    """
    from django.utils import timezone

    os_obj = get_object_or_404(OrdemServico, pk=pk)

    if os_obj.status == 'cancelada':
        messages.warning(request, 'Esta OS já está cancelada.')
        return redirect('os_list')

    if os_obj.status == 'finalizada':
        messages.error(request, 'Não é possível cancelar uma OS já finalizada.')
        return redirect('os_list')

    if request.method == 'POST':
        tipo = request.POST.get('tipo', '')
        if tipo not in ('com_deslocamento', 'sem_deslocamento'):
            messages.error(request, 'Selecione o tipo de cancelamento.')
            return redirect('os_cancelar', pk=pk)

        os_obj.status = 'cancelada'
        os_obj.tipo_cancelamento = tipo
        os_obj.cancelada_em = timezone.now()
        os_obj.save()

        # Garante que a OS apareça no Boletim de Medição para o financeiro
        from .models import BoletimMedicao
        if not hasattr(os_obj, 'boletim'):
            BoletimMedicao.objects.create(os=os_obj)

        tipo_label = 'com deslocamento' if tipo == 'com_deslocamento' else 'sem deslocamento'
        messages.success(request, f'OS {os_obj.numero} cancelada ({tipo_label}).')
        return redirect('os_list')

    return render(request, 'cadastros/os_cancelar.html', {'os': os_obj})


# ── OS OPERACIONAL + VEÍCULOS ─────────────────────────────────────────────────

from .models import OSOperacional, VeiculoEscoltado

@login_required
def os_operacional_save(request, pk):
    """Salva dados operacionais (tempos/km) e veículos escoltados via POST"""
    os_obj = get_object_or_404(OrdemServico, pk=pk)
    if request.method != 'POST':
        return redirect('os_detalhe', pk=pk)
    if os_obj.status == 'finalizada':
        messages.error(request, 'Esta OS está finalizada e não pode ser alterada.')
        return redirect('os_detalhe', pk=pk)

    from datetime import datetime
    def parse_dt(val):
        if not val:
            return None
        for fmt in ('%Y-%m-%dT%H:%M', '%d/%m/%Y %H:%M', '%Y-%m-%d %H:%M'):
            try:
                return datetime.strptime(val, fmt)
            except ValueError:
                continue
        return None

    def parse_int(val):
        try:
            return int(val) if val else None
        except (ValueError, TypeError):
            return None

    # Salvar / atualizar OSOperacional
    # update_fields explícito → GPS coords do agente nunca são sobrescritos
    op, _ = OSOperacional.objects.get_or_create(os=os_obj)
    op.numero_folha        = request.POST.get('numero_folha', '')
    op.inicio_viagem       = parse_dt(request.POST.get('inicio_viagem'))
    op.chegada_operacao    = parse_dt(request.POST.get('chegada_operacao'))
    op.inicio_operacao     = parse_dt(request.POST.get('inicio_operacao'))
    op.termino_operacao    = parse_dt(request.POST.get('termino_operacao'))
    op.termino_viagem      = parse_dt(request.POST.get('termino_viagem'))
    op.km_inicio_viagem    = parse_int(request.POST.get('km_inicio_viagem'))
    op.km_chegada_operacao = parse_int(request.POST.get('km_chegada_operacao'))
    op.km_inicio_operacao  = parse_int(request.POST.get('km_inicio_operacao'))
    op.km_termino_operacao = parse_int(request.POST.get('km_termino_operacao'))
    op.km_termino_viagem   = parse_int(request.POST.get('km_termino_viagem'))
    # Pedágio
    pedagio_val = request.POST.get('pedagio', '').strip().replace(',', '.')
    if pedagio_val:
        try:
            op.pedagio = float(pedagio_val)
        except ValueError:
            pass

    # Salva APENAS os campos editáveis pelo operador — GPS do agente intocado
    op.save(update_fields=[
        'numero_folha',
        'inicio_viagem', 'chegada_operacao', 'inicio_operacao',
        'termino_operacao', 'termino_viagem',
        'km_inicio_viagem', 'km_chegada_operacao', 'km_inicio_operacao',
        'km_termino_operacao', 'km_termino_viagem',
        'pedagio',
    ])

    # Salvar veículos escoltados (máx 4)
    os_obj.veiculos.all().delete()
    for i in range(1, 5):
        placa = request.POST.get(f'placa_cavalo_{i}', '').strip()
        veiculo = request.POST.get(f'veiculo_{i}', '').strip()
        motorista = request.POST.get(f'motorista_{i}', '').strip()
        placa_carreta = request.POST.get(f'placa_carreta_{i}', '').strip()
        placa_carreta2 = request.POST.get(f'placa_carreta2_{i}', '').strip()
        if placa or veiculo or motorista:
            VeiculoEscoltado.objects.create(
                os=os_obj,
                ordem=i,
                veiculo=veiculo,
                placa_cavalo=placa,
                placa_carreta=placa_carreta,
                placa_carreta2=placa_carreta2,
                motorista=motorista,
            )

    if os_obj.status != 'cancelada':
        if op.termino_viagem:
            os_obj.status = 'concluida'
        elif op.termino_operacao:
            os_obj.status = 'encerrando'
        elif op.chegada_operacao or op.inicio_operacao:
            os_obj.status = 'em_operacao'
        elif op.inicio_viagem:
            os_obj.status = 'em_viagem'
        else:
            os_obj.status = 'aberta'
        os_obj.save(update_fields=['status'])

    messages.success(request, 'Dados operacionais salvos com sucesso!')
    return redirect('os_detalhe', pk=pk)


# -- OS IMPRESSAO --
@login_required
def os_print(request, pk):
    os_obj = get_object_or_404(OrdemServico, pk=pk)
    op = getattr(os_obj, 'operacional', None)
    rastreador_viatura = None
    if os_obj.equipe and os_obj.equipe.viatura and os_obj.equipe.viatura.mct_id:
        rastreador_viatura = Rastreador.objects.filter(
            numero_serie=os_obj.equipe.viatura.mct_id
        ).first()

    # Fotos dos marcos operacionais
    MARCOS_LISTA = [
        ('inicio_viagem',     'Início de Viagem'),
        ('chegada_operacao',  'Chegada Operação'),
        ('inicio_operacao',   'Início Operação'),
        ('termino_operacao',  'Término Operação'),
        ('termino_viagem',    'Término de Viagem'),
    ]
    fotos_marco = {}
    if op:
        for foto in FotoMarco.objects.filter(os=os_obj):
            fotos_marco[foto.marco] = foto.foto.url

    # Assinaturas digitais — passa como lista para o template usar {% for a in assinaturas_lista %}
    assinaturas_lista = list(AssinaturaOS.objects.filter(os=os_obj).order_by('tipo'))

    # Veículos escoltados com fotos
    from .models import VeiculoEscoltado, FotoVeiculoEscoltado
    veiculos_print = []
    for v in os_obj.veiculos.order_by('ordem'):
        fotos = FotoVeiculoEscoltado.objects.filter(veiculo=v)
        veiculos_print.append({'veiculo': v, 'fotos': fotos})

    return render(request, 'cadastros/os_print.html', {
        'os': os_obj,
        'op': op,
        'rastreador_viatura': rastreador_viatura,
        'fotos_marco': fotos_marco,
        'fotos_marco_lista': MARCOS_LISTA,
        'assinaturas_lista': assinaturas_lista,
        'veiculos_print': veiculos_print,
    })


@login_required
def os_email_html(request, pk):
    """Retorna HTML da OS formatado para copiar e colar em e-mail."""
    os_obj = get_object_or_404(OrdemServico, pk=pk)
    op = getattr(os_obj, 'operacional', None)
    rastreador_viatura = None
    if os_obj.equipe and os_obj.equipe.viatura and os_obj.equipe.viatura.mct_id:
        rastreador_viatura = Rastreador.objects.filter(
            numero_serie=os_obj.equipe.viatura.mct_id
        ).first()
    from django.http import HttpResponse
    html = render(request, 'cadastros/os_email.html', {
        'os': os_obj, 'op': op, 'rastreador_viatura': rastreador_viatura,
        'host': request.build_absolute_uri('/'),
    })
    return html


# ══════════════════════════════════════════════════════════════════════════════
# RASTREAMENTO OMNILINK — endpoints AJAX
# ══════════════════════════════════════════════════════════════════════════════

@login_required
def omnilink_posicao_atual(request, pk):
    """AJAX — retorna posição atual GPS da viatura da OS.
    Tenta ObtemAllPosicoesAtuais (por placa) primeiro; fallback ObtemEventosNormais."""
    from django.http import JsonResponse
    from .omnilink import get_posicao_por_placa, get_ultima_posicao

    os_obj = get_object_or_404(OrdemServico, pk=pk)
    viatura = os_obj.equipe.viatura if os_obj.equipe else None
    mct_id  = viatura.mct_id if viatura and viatura.mct_id else None

    if not mct_id:
        return JsonResponse({'ok': False, 'erro': 'Viatura sem MCT ID cadastrado.'})

    import logging as _logging
    _log = _logging.getLogger(__name__)

    # Tenta método novo (por placa) — mais preciso e mais rápido
    dados = None
    if viatura and viatura.placa:
        dados = get_posicao_por_placa(viatura.placa)

    # Fallback: método antigo por MCT ID
    if dados is None and mct_id:
        dados = get_ultima_posicao(mct_id)

    if not dados:
        _log.warning(f"omnilink_posicao_atual: sem dados para viatura MCT={mct_id}")
        return JsonResponse({'ok': False, 'erro': f'Sem posição atual para esta viatura. Verifique se o rastreador está transmitindo.'})

    return JsonResponse({'ok': True, 'mct_id': mct_id, **dados})


@login_required
def omnilink_historico(request, pk):
    """AJAX — retorna histórico de posições da viatura durante a OS."""
    from django.http import JsonResponse
    from datetime import datetime, timedelta
    from xml.etree import ElementTree as ET
    from .omnilink import (get_historico_operacao, get_historico_posicoes,
                           _get_client, _buscar_ultimo_id_post,
                           _mct_id_to_terminal, _parse_teleeventos_xml,
                           USUARIO, SENHA_MD5)

    os_obj = get_object_or_404(OrdemServico, pk=pk)

    # ── Modo diagnóstico: ?debug=1 ───────────────────────────────────────────
    # Retorna todos os IdTerminals encontrados no buffer da API (sem filtrar),
    # útil para descobrir o ID correto do veículo.
    if request.GET.get('debug') == '1':
        viatura = os_obj.equipe.viatura if os_obj.equipe else None
        mct_id  = viatura.mct_id if viatura and viatura.mct_id else '?'
        try:
            id_terminal_esperado = _mct_id_to_terminal(mct_id)
        except Exception:
            id_terminal_esperado = None

        diagnostico = {
            'mct_id': mct_id,
            'id_terminal_esperado': id_terminal_esperado,
            'ultimo_id_post': None,
            'total_eventos_xml': 0,
            'id_terminals_encontrados': [],
            'cod_msgs_encontrados': [],
            'erro': None,
            'xml_inicio': '',
        }
        try:
            ids = _buscar_ultimo_id_post()
            diagnostico['ultimo_id_post'] = ids

            client = _get_client()
            # UltimoSequencial=0 é inválido (-204); lookback de 100M ≈ 7 dias na plataforma global
            seq_diag = max(1, ids.get('id', 1) - 100_000_000) if ids.get('id', 0) > 0 else 1
            xml_str = client.service.ObtemEventosNormais(
                Usuario=USUARIO,
                Senha=SENHA_MD5,
                UltimoSequencial=seq_diag,
            )
            import re as _re
            xml_str = str(xml_str) if xml_str else ''
            diagnostico['xml_inicio'] = xml_str[:600]

            # Normaliza PascalCase → lowercase (API retorna <TeleEvento>, <IdTerminal> etc.)
            xml_low = _re.sub(
                r'<(/?)([A-Za-z][A-Za-z0-9_]*)',
                lambda m: f'<{m.group(1)}{m.group(2).lower()}',
                xml_str
            )
            xml_wrap = f'<root>{xml_low}</root>'
            try:
                root = ET.fromstring(xml_wrap)
                eventos = list(root.iter('teleevento'))
                diagnostico['total_eventos_xml'] = len(eventos)

                ids_set  = set()
                msgs_set = set()
                for ev in eventos:
                    it = ev.findtext('idterminal') or ''
                    cm = ev.findtext('codmsg') or ''
                    if it:
                        ids_set.add(it.strip())
                    if cm:
                        msgs_set.add(cm.strip())

                diagnostico['id_terminals_encontrados'] = sorted(ids_set)
                diagnostico['cod_msgs_encontrados'] = sorted(msgs_set)
            except ET.ParseError as e:
                diagnostico['erro'] = f'XML parse error: {e}'

        except Exception as e:
            diagnostico['erro'] = str(e)

        return JsonResponse({'ok': True, 'diagnostico': diagnostico})
    # ── fim modo diagnóstico ─────────────────────────────────────────────────

    # Tenta primeiro usando o período da OS
    pontos = get_historico_operacao(os_obj)

    # Se vazio, tenta as últimas 24h (OS pode não ter inicio_viagem preenchido ainda)
    if not pontos:
        viatura = os_obj.equipe.viatura if os_obj.equipe else None
        mct_id  = viatura.mct_id if viatura and viatura.mct_id else None
        if mct_id:
            fim    = datetime.now()
            inicio = fim - timedelta(hours=24)
            pontos = get_historico_posicoes(mct_id, inicio, fim)
            if pontos:
                return JsonResponse({'ok': True, 'pontos': pontos, 'aviso': 'Exibindo últimas 24h (OS sem horário de viagem registrado).'})

    return JsonResponse({'ok': True, 'pontos': pontos})


# ══════════════════════════════════════════════════════════════════════════════
# RASTREAMENTO — Página de frota (mapa com todas as viaturas)
# ══════════════════════════════════════════════════════════════════════════════

@login_required
def omnilink_frota(request):
    """Página de rastreamento da frota — mapa com todas as viaturas."""
    from .models import Viatura
    viaturas = Viatura.objects.filter(mct_id__isnull=False).exclude(mct_id='').order_by('placa')
    return render(request, 'cadastros/omnilink_frota.html', {'viaturas': viaturas})


@login_required
def omnilink_frota_posicoes(request):
    """
    AJAX — retorna a posição atual de todas as viaturas.
    Usa ObtemAllPosicoesAtuais (placa como chave). Fallback para
    ObtemEventosNormais (MCT ID → hex) se o novo método não retornar dados.
    """
    from django.http import JsonResponse
    from .models import Viatura
    from .omnilink import (get_todas_posicoes_atuais, _get_eventos_normais,
                           _mct_id_to_terminal, _reverse_geocode)

    viaturas = Viatura.objects.filter(mct_id__isnull=False).exclude(mct_id='')

    # ── Estratégia principal: ObtemAllPosicoesAtuais ──────────────────────────
    posicoes_atuais = get_todas_posicoes_atuais()
    pos_por_placa   = {p['placa']: p for p in posicoes_atuais if p.get('placa')}

    # ── Fallback: buffer de eventos normais (se o novo método não retornar nada)
    usar_fallback = not pos_por_placa
    ultimo_por_terminal: dict = {}
    if usar_fallback:
        logger.info("omnilink_frota_posicoes: ObtemAllPosicoesAtuais sem dados — usando fallback ObtemEventosNormais")
        todos_eventos = _get_eventos_normais()
        for ev in todos_eventos:
            tid = ev.get('id_terminal', '')
            if tid:
                ultimo_por_terminal[tid] = ev

    resultado = []
    for v in viaturas:
        placa_norm = (v.placa or '').strip().upper()

        # Tenta pelo novo método (por placa)
        pos = pos_por_placa.get(placa_norm)

        # Fallback por MCT ID → hex
        if pos is None and usar_fallback:
            try:
                id_terminal = _mct_id_to_terminal(v.mct_id)
                ev = ultimo_por_terminal.get(id_terminal)
                if ev:
                    pos = ev
            except Exception:
                pass

        # Geocodificação reversa via Nominatim quando cidade não vem da API
        cidade = pos.get('cidade', '') if pos else ''
        if pos and not cidade and pos.get('lat') and pos.get('lng'):
            geo = _reverse_geocode(pos['lat'], pos['lng'])
            cidade = geo.get('cidade', '')

        resultado.append({
            'mct_id':     v.mct_id,
            'placa':      v.placa,
            'modelo':     v.marca_modelo,
            'lat':        pos.get('lat')        if pos else None,
            'lng':        pos.get('lng')        if pos else None,
            'velocidade': pos.get('velocidade') if pos else None,
            'odometro':   pos.get('odometro')   if pos else None,
            'ignicao':    pos.get('ignicao')    if pos else None,
            'data_hora':  pos.get('data_hora')  if pos else None,
            'endereco':   pos.get('endereco')   if pos else '',
            'cidade':     cidade,
            'online':     pos is not None,
        })

    return JsonResponse({'ok': True, 'viaturas': resultado})


# ══════════════════════════════════════════════════════════════════════════════
# ESPELHAMENTOS OMNILINK
# ══════════════════════════════════════════════════════════════════════════════

@login_required
def espelhamento_list(request):
    """Página de gestão de espelhamentos."""
    from .models import Viatura
    viaturas = Viatura.objects.filter(mct_id__isnull=False).exclude(mct_id='').order_by('placa')
    return render(request, 'cadastros/espelhamento_list.html', {'viaturas': viaturas})


def _garantir_tabela_espelhamento():
    """Cria a tabela EspelhamentoEnviado e semeia dados históricos se ainda não existir."""
    from django.db import connection, OperationalError, ProgrammingError
    from datetime import datetime as _dt

    _HISTORICOS = [
        ('SSR0E93', 'NORISK',                     '17/04/2026 23:59:00', _dt(2026, 4, 16, 22, 30, 21)),
        ('SIS6B65', 'SKYMARK',                    '17/04/2026 23:59:00', _dt(2026, 4, 16, 22, 30,  4)),
        ('SUU7D41', 'SKYMARK',                    '17/04/2026 23:59:00', _dt(2026, 4, 16, 22, 29, 43)),
        ('SUI1G21', 'SMITH SEGURANÇA PRIVADA',    '30/11/2027 20:51:00', _dt(2024, 7, 30, 18, 49, 53)),
        ('REU2F04', 'SMITH SEGURANÇA PRIVADA',    '30/11/2027 20:51:00', _dt(2024, 7, 30, 18, 49, 53)),
        ('REK3J23', 'SMITH SEGURANÇA PRIVADA',    '30/11/2027 20:51:00', _dt(2024, 7, 30, 18, 49, 53)),
        ('REU2F12', 'SMITH SEGURANÇA PRIVADA',    '30/11/2027 20:51:00', _dt(2024, 7, 30, 18, 49, 53)),
        ('SGN4B76', 'SMITH SEGURANÇA PRIVADA',    '30/11/2027 20:51:00', _dt(2024, 7, 30, 18, 49, 53)),
        ('REU2F12', 'JR SEGURANÇA E VIGILÂNCIA',  '30/12/2063 23:59:00', _dt(2024, 6, 30,  9, 17, 19)),
        ('SGN4B76', 'JR SEGURANÇA E VIGILÂNCIA',  '31/12/2030 09:55:00', _dt(2024, 1, 29,  9, 55, 46)),
    ]

    with connection.cursor() as cur:
        # Detecta banco (postgres vs sqlite)
        vendor = connection.vendor  # 'postgresql' ou 'sqlite'

        # Verifica se a tabela existe
        if vendor == 'postgresql':
            cur.execute("""
                SELECT EXISTS(
                    SELECT 1 FROM information_schema.tables
                    WHERE table_name = 'cadastros_espelhamentoenviado'
                )
            """)
            existe = cur.fetchone()[0]
        else:
            cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='cadastros_espelhamentoenviado'"
            )
            existe = bool(cur.fetchone())

        if existe:
            return  # já existe, nada a fazer

        # Cria a tabela
        if vendor == 'postgresql':
            cur.execute("""
                CREATE TABLE cadastros_espelhamentoenviado (
                    id            SERIAL PRIMARY KEY,
                    id_sequencia  VARCHAR(50) UNIQUE,
                    placa         VARCHAR(20) NOT NULL,
                    id_central    VARCHAR(20) NOT NULL DEFAULT '',
                    nome_central  VARCHAR(200) NOT NULL DEFAULT '',
                    cnpj_destino  VARCHAR(20) NOT NULL DEFAULT '',
                    data_expiracao VARCHAR(30) NOT NULL,
                    data_criacao  TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                    obrigatorio   BOOLEAN NOT NULL DEFAULT FALSE,
                    cancelado     BOOLEAN NOT NULL DEFAULT FALSE
                )
            """)
        else:
            cur.execute("""
                CREATE TABLE cadastros_espelhamentoenviado (
                    id             INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_sequencia   TEXT UNIQUE,
                    placa          TEXT NOT NULL,
                    id_central     TEXT NOT NULL DEFAULT '',
                    nome_central   TEXT NOT NULL DEFAULT '',
                    cnpj_destino   TEXT NOT NULL DEFAULT '',
                    data_expiracao TEXT NOT NULL,
                    data_criacao   TEXT NOT NULL DEFAULT (datetime('now')),
                    obrigatorio    INTEGER NOT NULL DEFAULT 0,
                    cancelado      INTEGER NOT NULL DEFAULT 0
                )
            """)

        # Semeia dados históricos
        for placa, nome_central, data_exp, data_cad in _HISTORICOS:
            cur.execute("""
                INSERT INTO cadastros_espelhamentoenviado
                    (placa, nome_central, data_expiracao, data_criacao, cancelado, obrigatorio, id_central, cnpj_destino)
                VALUES (%s, %s, %s, %s, FALSE, FALSE, '', '')
            """ if vendor == 'postgresql' else """
                INSERT INTO cadastros_espelhamentoenviado
                    (placa, nome_central, data_expiracao, data_criacao, cancelado, obrigatorio, id_central, cnpj_destino)
                VALUES (?, ?, ?, ?, 0, 0, '', '')
            """, [placa, nome_central, data_exp, data_cad.isoformat()])

        # Registra na tabela de migrations do Django para evitar conflito futuro
        for num in ('0026_espelhamentoenviado', '0027_seed_espelhamentos_historicos'):
            try:
                cur.execute(
                    "INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, NOW())"
                    if vendor == 'postgresql' else
                    "INSERT INTO django_migrations (app, name, applied) VALUES (?, ?, datetime('now'))",
                    ['cadastros', num]
                )
            except Exception:
                pass  # já registrada


@login_required
def espelhamento_listar_ajax(request):
    """AJAX — lista espelhamentos enviados (banco local) e recebidos (API Omnilink)."""
    from django.http import JsonResponse
    from datetime import datetime, timedelta
    from .omnilink import listar_espelhamentos
    from .models import EspelhamentoEnviado
    import traceback

    # Garante que a tabela existe (auto-cria se migration não rodou no Railway)
    try:
        _garantir_tabela_espelhamento()
    except Exception as _te:
        import logging
        logging.getLogger(__name__).error(f'_garantir_tabela_espelhamento: {_te}')

    inicio = request.GET.get('inicio', '')
    fim    = request.GET.get('fim', '')
    status = request.GET.get('status', '')

    hoje   = datetime.now()
    amanha = hoje + timedelta(days=1)
    data_inicio_dt = datetime.strptime(inicio, '%Y-%m-%d') if inicio else (hoje - timedelta(days=30))
    data_fim_dt    = datetime.strptime(fim,    '%Y-%m-%d') if fim    else amanha

    # ── ENVIADOS: banco de dados local ────────────────────────────────────────
    _enviados_erro = None
    _total_db = -1
    try:
        _total_db = EspelhamentoEnviado.objects.count()
        qs = EspelhamentoEnviado.objects.filter(
            data_criacao__gte=data_inicio_dt,
            data_criacao__lte=data_fim_dt,
            cancelado=False,
        )
        enviados = [
            {
                'id':           str(e.id),
                'placa':        e.placa,
                'nome_central': e.nome_central or e.cnpj_destino or e.id_central or '—',
                'cnpj_central': e.cnpj_destino,
                'id_central':   e.id_central,
                'data_cad':     e.data_criacao.strftime('%Y-%m-%d %H:%M:%S'),
                'data_exp':     e.data_expiracao,
                'status_aceite': '0',   # default: aguardando (será enriquecido abaixo via API)
                'status':       '',
                'data_aceite':  '',
                'user_aceite':  '',
                'id_sequencia': e.id_sequencia or '',
            }
            for e in qs
        ]
    except Exception as exc:
        import logging
        _enviados_erro = str(exc)
        logging.getLogger(__name__).error(f'EspelhamentoEnviado.query: {exc}\n{traceback.format_exc()}')
        enviados = []

    # ── API Omnilink: ListarEspelhamentosByClienteStatus ──────────────────────
    # Segundo o manual (seção 29.4) esse método retorna TODOS os espelhamentos
    # da conta — tanto os enviados (id_cliente=nós) quanto os recebidos
    # (id_cliente_destino=nós). Usamos o resultado para:
    #   1) Enriquecer os ENVIADOS locais com o status real (aceito/aguardando/recusado)
    #   2) Separar o restante como RECEBIDOS
    MAX_DIAS = 90
    if (data_fim_dt - data_inicio_dt).days > MAX_DIAS:
        data_inicio_api = data_fim_dt - timedelta(days=MAX_DIAS)
    else:
        data_inicio_api = data_inicio_dt

    statuses_buscar = ('0', '1', '2') if not status else (status,)

    def _buscar_status(s, di_dt, df_dt):
        resultados = []
        vistos = set()
        cursor = di_dt
        while cursor < df_dt:
            chunk_fim = min(cursor + timedelta(days=28), df_dt)
            di_str = cursor.strftime('%d/%m/%Y')
            df_str = chunk_fim.strftime('%d/%m/%Y')
            try:
                for e in listar_espelhamentos(status=s, data_inicio=di_str, data_fim=df_str):
                    eid = e.get('id') or str(e)
                    if eid and eid not in vistos:
                        vistos.add(eid)
                        resultados.append(e)
            except Exception as exc:
                import logging
                logging.getLogger(__name__).error(
                    f'listar_espelhamentos status={s!r} {di_str}-{df_str}: {exc}')
            cursor = chunk_fim + timedelta(days=1)
        return resultados

    # Mapas de lookup:
    #   - por id_sequencia (funciona quando o id retornado ao criar = <id> da listagem)
    #   - por placa (fallback principal, usa data_cad como desempate em ambiguidade)
    enviados_by_seq = {e['id_sequencia']: e for e in enviados if e['id_sequencia']}
    enviados_by_placa = {}
    for e in enviados:
        p = (e['placa'] or '').upper().strip()
        if p:
            enviados_by_placa.setdefault(p, []).append(e)

    def _parse_dt(s):
        """Tenta parsear várias variações de formato de data que a API/DB podem trazer."""
        if not s:
            return None
        for fmt in ('%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M',
                    '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M',
                    '%d/%m/%Y', '%Y-%m-%d'):
            try:
                return datetime.strptime(s.strip(), fmt)
            except (ValueError, TypeError, AttributeError):
                continue
        return None

    api_results = []
    vistos_api = set()
    try:
        for s in statuses_buscar:
            for e in _buscar_status(s, data_inicio_api, data_fim_dt):
                eid = e.get('id') or str(e)
                if eid not in vistos_api:
                    vistos_api.add(eid)
                    api_results.append(e)
    except Exception as exc:
        import logging
        logging.getLogger(__name__).error(f'API espelhamentos: {exc}\n{traceback.format_exc()}')

    # Enriquece enviados com status real da API + separa o que é recebido
    recebidos = []
    _matched = 0
    _match_erro = None
    try:
        for api_item in api_results:
            try:
                api_id    = api_item.get('id', '') if isinstance(api_item, dict) else ''
                api_placa = (api_item.get('placa') or '').upper().strip() if isinstance(api_item, dict) else ''
                api_dt    = _parse_dt(api_item.get('data_cad', '')) if isinstance(api_item, dict) else None

                # 1) Match exato por id_sequencia
                local = enviados_by_seq.get(api_id) if api_id else None

                # 2) Fallback: match por placa (com data_cad como desempate quando há múltiplos)
                if local is None and api_placa:
                    candidates = enviados_by_placa.get(api_placa, [])
                    if len(candidates) == 1:
                        local = candidates[0]
                    elif candidates and api_dt:
                        def _delta(c, _api=api_dt):
                            cdt = _parse_dt(c.get('data_cad', ''))
                            return abs((cdt - _api).total_seconds()) if cdt else float('inf')
                        local = min(candidates, key=_delta)

                if local is not None:
                    if api_item.get('status_aceite') not in (None, ''):
                        local['status_aceite'] = api_item['status_aceite']
                    local['status']      = api_item.get('status', '') or local.get('status', '')
                    local['data_aceite'] = api_item.get('data_aceite', '') or local.get('data_aceite', '')
                    local['user_aceite'] = api_item.get('user_aceite', '') or local.get('user_aceite', '')
                    _matched += 1
                else:
                    recebidos.append(api_item)
            except Exception as _e_item:
                import logging
                logging.getLogger(__name__).error(f'match api_item falhou: {_e_item} — item={api_item!r}')
                # Em caso de erro em um item específico, joga em recebidos para não perder dado
                recebidos.append(api_item)
    except Exception as _e_loop:
        _match_erro = f'{type(_e_loop).__name__}: {_e_loop}'
        import logging
        logging.getLogger(__name__).error(f'match loop: {_match_erro}\n{traceback.format_exc()}')

    # Diagnóstico seguro (qualquer erro aqui vira string, não derruba a response)
    try:
        _placas_locais = sorted(enviados_by_placa.keys())
    except Exception:
        _placas_locais = []
    try:
        _placas_api = sorted({(i.get('placa') or '').upper().strip()
                              for i in api_results
                              if isinstance(i, dict) and i.get('placa')})
    except Exception:
        _placas_api = []

    return JsonResponse({
        'ok': True,
        'enviados': enviados,
        'recebidos': recebidos,
        '_debug': {
            'total_db': _total_db,
            'erro_db': _enviados_erro,
            'range': f'{data_inicio_dt} → {data_fim_dt}',
            'api_total': len(api_results),
            'enviados_match_api': _matched,
            'match_erro': _match_erro,
            'placas_locais': _placas_locais,
            'placas_api': _placas_api,
        },
    })


@login_required
def espelhamento_debug_ajax(request):
    """
    Debug temporário — retorna:
      - XML bruto de ListarEspelhamentosByClienteStatus nos 3 status
      - Lista completa de métodos do WSDL
      - Subconjunto de métodos cujo nome parece relacionado a
        espelhamento / compartilhamento / solicitação / status
      - Se a query string tiver ?testar=<NomeDoMetodo>&placa=XXX o endpoint
        tenta invocar o método com várias assinaturas comuns e devolve a
        resposta crua (primeiros 3000 chars) para inspecionarmos o XML.
    """
    from django.http import JsonResponse
    from .omnilink import _get_client, USUARIO, SENHA_MD5, descobrir_metodos_wsdl
    from datetime import datetime, timedelta

    hoje = datetime.now()
    data_fim    = hoje.strftime('%d/%m/%Y')
    data_inicio = (hoje - timedelta(days=7)).strftime('%d/%m/%Y')

    saida = {'ok': True, 'periodo': f'{data_inicio} → {data_fim}'}

    # 1) Lista de métodos do WSDL + filtro por palavras-chave
    try:
        metodos = descobrir_metodos_wsdl()
        saida['metodos_total'] = len(metodos)
        saida['metodos'] = metodos
        chaves = ('espelh', 'compart', 'solicit', 'status', 'consult', 'buscar', 'list')
        saida['metodos_candidatos'] = [
            m for m in metodos if any(k in m.lower() for k in chaves)
        ]
    except Exception as e_m:
        saida['metodos_erro'] = str(e_m)

    # 2) XML bruto do ListarEspelhamentosByClienteStatus nos 3 status
    try:
        client = _get_client()
        resultados = {}
        for s in ('0', '1', '2'):
            try:
                xml_str = client.service.ListarEspelhamentosByClienteStatus(
                    Usuario=USUARIO,
                    Senha=SENHA_MD5,
                    Status=s,
                    data_inicio=data_inicio,
                    data_fim=data_fim,
                )
                resultados[f'status_{s}'] = str(xml_str)[:2000]
            except Exception as e_s:
                resultados[f'status_{s}_erro'] = str(e_s)
        saida['raw'] = resultados
    except Exception as exc:
        saida['raw_erro'] = str(exc)

    # 3) Teste sob demanda de um método específico
    testar = request.GET.get('testar', '').strip()
    if testar:
        placa   = request.GET.get('placa', '').strip()
        id_req  = request.GET.get('id', '').strip()
        try:
            client = _get_client()
            op = getattr(client.service, testar, None)
            if op is None:
                saida['teste'] = {'metodo': testar, 'erro': 'método inexistente no WSDL'}
            else:
                # Tenta várias combinações de argumentos
                tentativas = [
                    {'Usuario': USUARIO, 'Senha': SENHA_MD5, 'Placa': placa},
                    {'Usuario': USUARIO, 'Senha': SENHA_MD5, 'placa': placa},
                    {'Usuario': USUARIO, 'Senha': SENHA_MD5, 'IdSolicitacao': id_req},
                    {'Usuario': USUARIO, 'Senha': SENHA_MD5, 'IdSequencia':   id_req},
                    {'Usuario': USUARIO, 'Senha': SENHA_MD5, 'Id':            id_req},
                    {'Usuario': USUARIO, 'Senha': SENHA_MD5},
                ]
                respostas = []
                for kwargs in tentativas:
                    try:
                        r = op(**kwargs)
                        respostas.append({'args': list(kwargs.keys()), 'resp': str(r)[:3000]})
                        break  # a primeira assinatura que não estourar já serve
                    except Exception as e_t:
                        respostas.append({'args': list(kwargs.keys()), 'erro': str(e_t)[:300]})
                saida['teste'] = {'metodo': testar, 'placa': placa, 'id': id_req, 'tentativas': respostas}
        except Exception as e_test:
            saida['teste'] = {'metodo': testar, 'erro': str(e_test)}

    return JsonResponse(saida)


@login_required
def espelhamento_centrais_ajax(request):
    """AJAX — lista centrais disponíveis para espelhamento."""
    from django.http import JsonResponse
    from .omnilink import listar_centrais_disponiveis, descobrir_metodos_wsdl

    centrais = listar_centrais_disponiveis()
    if not centrais:
        # Retorna lista de métodos para diagnóstico
        metodos = descobrir_metodos_wsdl()
        metodos_central = [m for m in metodos if any(x in m.lower() for x in ['central','base','lista'])]
        return JsonResponse({
            'ok': False,
            'centrais': [],
            'aviso': 'Método de listar centrais não encontrado na API.',
            'metodos_disponiveis': metodos_central,
        })
    return JsonResponse({'ok': True, 'centrais': centrais})


@login_required
def espelhamento_criar_ajax(request):
    """AJAX POST — cria novo espelhamento."""
    from django.http import JsonResponse
    import json
    from .omnilink import criar_espelhamento

    try:
        _garantir_tabela_espelhamento()
    except Exception:
        pass

    if request.method != 'POST':
        return JsonResponse({'ok': False, 'mensagem': 'Método inválido.'})

    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({'ok': False, 'mensagem': 'JSON inválido.'})

    placa         = data.get('placa', '').strip()
    cnpj_destino  = data.get('cnpj_destino', '').strip()
    id_central    = data.get('id_central', '').strip()
    data_exp      = data.get('data_expiracao', '').strip()
    obrigatorio   = int(data.get('obrigatorio', 0))

    if not placa or not data_exp:
        return JsonResponse({'ok': False, 'mensagem': 'Placa e data de expiração são obrigatórios.'})

    resultado = criar_espelhamento(
        placa=placa,
        data_expiracao=data_exp,
        cnpj_destino=cnpj_destino,
        id_central=id_central,
        obrigatorio=obrigatorio,
    )

    # Se criado com sucesso, persiste no banco local (a API não retorna
    # espelhamentos enviados em ListarEspelhamentosByClienteStatus).
    if resultado.get('ok'):
        try:
            from .models import EspelhamentoEnviado
            from .omnilink import _carregar_centrais_fixture
            nome_central = ''
            if id_central:
                try:
                    mapa = {str(c['id']): c['nome'] for c in _carregar_centrais_fixture()}
                    nome_central = mapa.get(id_central, '')
                except Exception:
                    pass
            EspelhamentoEnviado.objects.create(
                id_sequencia=resultado.get('id_sequencia') or None,
                placa=placa.upper(),
                id_central=id_central,
                nome_central=nome_central,
                cnpj_destino=cnpj_destino,
                data_expiracao=data_exp,
                obrigatorio=bool(obrigatorio),
            )
        except Exception as ex:
            import logging
            logging.getLogger(__name__).error(f'EspelhamentoEnviado.create: {ex}')

    return JsonResponse(resultado)


@login_required
def espelhamento_aceitar_ajax(request):
    """AJAX POST — aceita ou rejeita espelhamento recebido."""
    from django.http import JsonResponse
    import json
    from .omnilink import aceitar_espelhamento

    if request.method != 'POST':
        return JsonResponse({'ok': False, 'mensagem': 'Método inválido.'})

    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({'ok': False, 'mensagem': 'JSON inválido.'})

    resultado = aceitar_espelhamento(
        id_solicitacao=int(data.get('id', 0)),
        aceitar=bool(data.get('aceitar', True)),
    )
    return JsonResponse(resultado)


@login_required
def espelhamento_cancelar_ajax(request):
    """AJAX POST — cancela/exclui espelhamento."""
    from django.http import JsonResponse
    import json
    from .omnilink import excluir_espelhamento

    if request.method != 'POST':
        return JsonResponse({'ok': False, 'mensagem': 'Método inválido.'})

    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({'ok': False, 'mensagem': 'JSON inválido.'})

    id_solicitacao = data.get('id', 0)

    # Se o ID começa com dígitos pequenos pode ser do banco local (pk do Django)
    # Se for um número grande é id da API Omnilink
    resultado = {'ok': False, 'mensagem': 'ID inválido.'}
    try:
        id_int = int(id_solicitacao)
    except (ValueError, TypeError):
        return JsonResponse(resultado)

    # Tenta cancelar no banco local primeiro (espelhamentos enviados por nós)
    from .models import EspelhamentoEnviado
    local = EspelhamentoEnviado.objects.filter(pk=id_int).first()
    if local:
        local.cancelado = True
        local.save()
        resultado = {'ok': True, 'mensagem': f'Espelhamento da placa {local.placa} cancelado.'}
    else:
        # Cancela na API Omnilink (espelhamentos recebidos)
        resultado = excluir_espelhamento(id_solicitacao=id_int)

    return JsonResponse(resultado)


# ══════════════════════════════════════════════════════════════════════════════
# FATURAMENTO — Tabela de Precos
# ══════════════════════════════════════════════════════════════════════════════

from .models import TabelaPreco, BoletimMedicao

@login_required
def tabela_preco_list(request):
    if not _pode_faturamento(request.user):
        messages.error(request, 'Sem permissão para acessar Faturamento.')
        return redirect('dashboard')
    q = request.GET.get('q', '')
    tabelas = TabelaPreco.objects.select_related('cliente').all()
    if q:
        tabelas = tabelas.filter(
            Q(nome__icontains=q) | Q(cliente__razao_social__icontains=q)
        )
    return render(request, 'cadastros/tabela_preco_list.html', {'tabelas': tabelas, 'q': q})


@login_required
def tabela_preco_create(request):
    if not _pode_faturamento(request.user):
        messages.error(request, 'Sem permissão para acessar Faturamento.')
        return redirect('dashboard')
    clientes = Cliente.objects.all().order_by('razao_social')
    if request.method == 'POST':
        try:
            def dec(v, d='0'):
                try: return float((v or d).replace(',', '.'))
                except: return 0
            TabelaPreco.objects.create(
                cliente_id       = request.POST['cliente'],
                nome             = request.POST['nome'],
                tipo_viagem      = request.POST.get('tipo_viagem', 'todas'),
                situacao         = request.POST.get('situacao', 'ativo'),
                inicio_contrato  = request.POST.get('inicio_contrato') or None,
                ultimo_reajuste  = request.POST.get('ultimo_reajuste') or None,
                proximo_reajuste = request.POST.get('proximo_reajuste') or None,
                valor_escolta    = dec(request.POST.get('valor_escolta')),
                franquia_km      = int(request.POST.get('franquia_km') or 0),
                franquia_horas   = request.POST.get('franquia_horas', '000:00'),
                excedente_km     = dec(request.POST.get('excedente_km')),
                excedente_hora   = dec(request.POST.get('excedente_hora')),
                cobrar_pedagio   = request.POST.get('cobrar_pedagio', 'sim'),
                pedagio_fixo     = dec(request.POST.get('pedagio_fixo')),
                pedagio_percent  = dec(request.POST.get('pedagio_percent')),
            )
            messages.success(request, 'Tabela de preco criada com sucesso!')
            return redirect('tabela_preco_list')
        except Exception as e:
            messages.error(request, f'Erro: {e}')
    return render(request, 'cadastros/tabela_preco_form.html', {'clientes': clientes, 'titulo': 'Nova Tabela de Preco'})


@login_required
def tabela_preco_edit(request, pk):
    if not _pode_faturamento(request.user):
        messages.error(request, 'Sem permissão para acessar Faturamento.')
        return redirect('dashboard')
    tabela = get_object_or_404(TabelaPreco, pk=pk)
    clientes = Cliente.objects.all().order_by('razao_social')
    if request.method == 'POST':
        try:
            def dec(v, d='0'):
                try: return float((v or d).replace(',', '.'))
                except: return 0
            tabela.cliente_id       = request.POST['cliente']
            tabela.nome             = request.POST['nome']
            tabela.tipo_viagem      = request.POST.get('tipo_viagem', 'todas')
            tabela.situacao         = request.POST.get('situacao', 'ativo')
            tabela.inicio_contrato  = request.POST.get('inicio_contrato') or None
            tabela.ultimo_reajuste  = request.POST.get('ultimo_reajuste') or None
            tabela.proximo_reajuste = request.POST.get('proximo_reajuste') or None
            tabela.valor_escolta    = dec(request.POST.get('valor_escolta'))
            tabela.franquia_km      = int(request.POST.get('franquia_km') or 0)
            tabela.franquia_horas   = request.POST.get('franquia_horas', '000:00')
            tabela.excedente_km     = dec(request.POST.get('excedente_km'))
            tabela.excedente_hora   = dec(request.POST.get('excedente_hora'))
            tabela.cobrar_pedagio   = request.POST.get('cobrar_pedagio', 'sim')
            tabela.pedagio_fixo     = dec(request.POST.get('pedagio_fixo'))
            tabela.pedagio_percent  = dec(request.POST.get('pedagio_percent'))
            tabela.save()
            messages.success(request, 'Tabela atualizada com sucesso!')
            return redirect('tabela_preco_list')
        except Exception as e:
            messages.error(request, f'Erro: {e}')
    return render(request, 'cadastros/tabela_preco_form.html', {
        'tabela': tabela, 'clientes': clientes, 'titulo': 'Editar Tabela de Preco'
    })


@login_required
def tabela_preco_delete(request, pk):
    if not _pode_faturamento(request.user):
        messages.error(request, 'Sem permissão para acessar Faturamento.')
        return redirect('dashboard')
    tabela = get_object_or_404(TabelaPreco, pk=pk)
    if request.method == 'POST':
        tabela.delete()
        messages.success(request, 'Tabela removida.')
        return redirect('tabela_preco_list')
    return render(request, 'cadastros/confirm_delete.html', {'obj': tabela, 'tipo': 'Tabela de Preco'})


# ══════════════════════════════════════════════════════════════════════════════
# FATURAMENTO — Boletim de Medicao
# ══════════════════════════════════════════════════════════════════════════════

@login_required
def boletim_list(request):
    if not _pode_faturamento(request.user):
        messages.error(request, 'Sem permissão para acessar Faturamento.')
        return redirect('dashboard')
    from datetime import datetime
    q = request.GET.get('q', '')
    status_filtro = request.GET.get('status', '')
    clientes_filtro = request.GET.getlist('clientes')
    data_ini = request.GET.get('data_ini', '')
    data_fim = request.GET.get('data_fim', '')
    # Criar boletins automaticamente para OS finalizadas ou canceladas sem boletim ainda
    os_sem_boletim = OrdemServico.objects.filter(
        status__in=['finalizada', 'cancelada']
    ).exclude(boletim__isnull=False)
    for os_obj in os_sem_boletim:
        BoletimMedicao.objects.get_or_create(os=os_obj)
    boletins = BoletimMedicao.objects.select_related('os', 'os__cliente', 'os__equipe', 'tabela_preco').all()
    if q:
        boletins = boletins.filter(
            Q(os__numero__icontains=q) |
            Q(os__cliente__razao_social__icontains=q) |
            Q(os__solicitante__icontains=q)
        )
    if status_filtro:
        boletins = boletins.filter(status=status_filtro)
    if clientes_filtro:
        boletins = boletins.filter(os__cliente__id__in=clientes_filtro)
    if data_ini:
        try:
            boletins = boletins.filter(os__previsao_inicio__date__gte=datetime.strptime(data_ini, '%Y-%m-%d').date())
        except ValueError:
            pass
    if data_fim:
        try:
            boletins = boletins.filter(os__previsao_inicio__date__lte=datetime.strptime(data_fim, '%Y-%m-%d').date())
        except ValueError:
            pass
    todos_clientes = Cliente.objects.all().order_by('razao_social')
    return render(request, 'cadastros/boletim_list.html', {
        'boletins': boletins,
        'q': q,
        'status_filtro': status_filtro,
        'clientes_filtro': clientes_filtro,
        'data_ini': data_ini,
        'data_fim': data_fim,
        'todos_clientes': todos_clientes,
    })


@login_required
def boletim_detalhe(request, pk):
    boletim = get_object_or_404(BoletimMedicao, pk=pk)
    os_obj  = boletim.os
    op      = getattr(os_obj, 'operacional', None)
    tabelas = TabelaPreco.objects.filter(
        cliente=os_obj.cliente, situacao='ativo'
    ).order_by('nome')

    if request.method == 'POST':
        if boletim.status == 'faturado':
            messages.error(request, 'Boletim ja faturado nao pode ser alterado.')
            return redirect('boletim_detalhe', pk=pk)
        tabela_id = request.POST.get('tabela_preco')
        if tabela_id:
            boletim.tabela_preco_id = tabela_id
        def to_float(val):
            try:
                return float(str(val or '0').replace(',', '.'))
            except (ValueError, TypeError):
                return 0.0
        boletim.acrescimo    = to_float(request.POST.get('acrescimo', '0'))
        boletim.desconto     = to_float(request.POST.get('desconto', '0'))
        boletim.valor_pedagio = to_float(request.POST.get('valor_pedagio', '0'))
        boletim.numero_nota  = request.POST.get('numero_nota', '')
        boletim.observacoes  = request.POST.get('observacoes', '')
        action = request.POST.get('action', 'salvar')
        if action == 'calcular' and boletim.tabela_preco_id:
            # Salva o pedágio manual antes de calcular para não ser sobrescrito
            boletim.save()
            boletim.calcular()
            messages.success(request, 'Valores calculados com sucesso!')
        elif action == 'faturar':
            boletim.status = 'faturado'
            boletim.save()
            messages.success(request, f'Boletim OS-{os_obj.numero} marcado como Faturado!')
            return redirect('boletim_list')
        else:
            boletim.save()
            messages.success(request, 'Boletim salvo!')
        return redirect('boletim_detalhe', pk=pk)

    # Pré-preenche pedágio da OS se o boletim ainda não tiver valor
    pedagio_sugerido = boletim.valor_pedagio
    if pedagio_sugerido == 0 and op and op.pedagio:
        pedagio_sugerido = op.pedagio

    return render(request, 'cadastros/boletim_detalhe.html', {
        'boletim': boletim, 'os': os_obj, 'op': op, 'tabelas': tabelas,
        'pedagio_sugerido': pedagio_sugerido,
    })


# ══════════════════════════════════════════════════════════════════════════════
# FATURAMENTO — Tabela de Precos
# ══════════════════════════════════════════════════════════════════════════════

from .models import TabelaPreco, BoletimMedicao

@login_required
def tabela_preco_list(request):
    q = request.GET.get('q', '')
    tabelas = TabelaPreco.objects.select_related('cliente').all()
    if q:
        tabelas = tabelas.filter(
            Q(nome__icontains=q) | Q(cliente__razao_social__icontains=q)
        )
    return render(request, 'cadastros/tabela_preco_list.html', {'tabelas': tabelas, 'q': q})


@login_required
def tabela_preco_create(request):
    clientes = Cliente.objects.all().order_by('razao_social')
    if request.method == 'POST':
        try:
            def dec(v, d='0'):
                try: return float((v or d).replace(',', '.'))
                except: return 0
            TabelaPreco.objects.create(
                cliente_id       = request.POST['cliente'],
                nome             = request.POST['nome'],
                tipo_viagem      = request.POST.get('tipo_viagem', 'todas'),
                situacao         = request.POST.get('situacao', 'ativo'),
                inicio_contrato  = request.POST.get('inicio_contrato') or None,
                ultimo_reajuste  = request.POST.get('ultimo_reajuste') or None,
                proximo_reajuste = request.POST.get('proximo_reajuste') or None,
                valor_escolta    = dec(request.POST.get('valor_escolta')),
                franquia_km      = int(request.POST.get('franquia_km') or 0),
                franquia_horas   = request.POST.get('franquia_horas', '000:00'),
                excedente_km     = dec(request.POST.get('excedente_km')),
                excedente_hora   = dec(request.POST.get('excedente_hora')),
                cobrar_pedagio   = request.POST.get('cobrar_pedagio', 'sim'),
                pedagio_fixo     = dec(request.POST.get('pedagio_fixo')),
                pedagio_percent  = dec(request.POST.get('pedagio_percent')),
            )
            messages.success(request, 'Tabela de preco criada com sucesso!')
            return redirect('tabela_preco_list')
        except Exception as e:
            messages.error(request, f'Erro: {e}')
    return render(request, 'cadastros/tabela_preco_form.html', {'clientes': clientes, 'titulo': 'Nova Tabela de Preco'})


@login_required
def tabela_preco_edit(request, pk):
    tabela = get_object_or_404(TabelaPreco, pk=pk)
    clientes = Cliente.objects.all().order_by('razao_social')
    if request.method == 'POST':
        try:
            def dec(v, d='0'):
                try: return float((v or d).replace(',', '.'))
                except: return 0
            tabela.cliente_id       = request.POST['cliente']
            tabela.nome             = request.POST['nome']
            tabela.tipo_viagem      = request.POST.get('tipo_viagem', 'todas')
            tabela.situacao         = request.POST.get('situacao', 'ativo')
            tabela.inicio_contrato  = request.POST.get('inicio_contrato') or None
            tabela.ultimo_reajuste  = request.POST.get('ultimo_reajuste') or None
            tabela.proximo_reajuste = request.POST.get('proximo_reajuste') or None
            tabela.valor_escolta    = dec(request.POST.get('valor_escolta'))
            tabela.franquia_km      = int(request.POST.get('franquia_km') or 0)
            tabela.franquia_horas   = request.POST.get('franquia_horas', '000:00')
            tabela.excedente_km     = dec(request.POST.get('excedente_km'))
            tabela.excedente_hora   = dec(request.POST.get('excedente_hora'))
            tabela.cobrar_pedagio   = request.POST.get('cobrar_pedagio', 'sim')
            tabela.pedagio_fixo     = dec(request.POST.get('pedagio_fixo'))
            tabela.pedagio_percent  = dec(request.POST.get('pedagio_percent'))
            tabela.save()
            messages.success(request, 'Tabela atualizada com sucesso!')
            return redirect('tabela_preco_list')
        except Exception as e:
            messages.error(request, f'Erro: {e}')
    return render(request, 'cadastros/tabela_preco_form.html', {
        'tabela': tabela, 'clientes': clientes, 'titulo': 'Editar Tabela de Preco'
    })


@login_required
def tabela_preco_delete(request, pk):
    tabela = get_object_or_404(TabelaPreco, pk=pk)
    if request.method == 'POST':
        tabela.delete()
        messages.success(request, 'Tabela removida.')
        return redirect('tabela_preco_list')
    return render(request, 'cadastros/confirm_delete.html', {'obj': tabela, 'tipo': 'Tabela de Preco'})


# ══════════════════════════════════════════════════════════════════════════════
# FATURAMENTO — Boletim de Medicao
# ══════════════════════════════════════════════════════════════════════════════

@login_required
def clientes_json(request):
    """Endpoint JSON usado pelo filtro de clientes no Boletim de Medicao."""
    from django.http import JsonResponse
    clientes = Cliente.objects.all().order_by('razao_social').values('id', 'razao_social')
    return JsonResponse({'clientes': list(clientes)})


@login_required
def boletim_detalhe(request, pk):
    boletim = get_object_or_404(BoletimMedicao, pk=pk)
    os_obj  = boletim.os
    op      = getattr(os_obj, 'operacional', None)
    tabelas = TabelaPreco.objects.filter(
        cliente=os_obj.cliente, situacao='ativo'
    ).order_by('nome')

    if request.method == 'POST':
        if boletim.status == 'faturado':
            messages.error(request, 'Boletim ja faturado nao pode ser alterado.')
            return redirect('boletim_detalhe', pk=pk)
        tabela_id = request.POST.get('tabela_preco')
        if tabela_id:
            boletim.tabela_preco_id = tabela_id
        def to_float(val):
            try:
                return float(str(val or '0').replace(',', '.'))
            except (ValueError, TypeError):
                return 0.0
        boletim.acrescimo    = to_float(request.POST.get('acrescimo', '0'))
        boletim.desconto     = to_float(request.POST.get('desconto', '0'))
        boletim.valor_pedagio = to_float(request.POST.get('valor_pedagio', '0'))
        boletim.numero_nota  = request.POST.get('numero_nota', '')
        boletim.observacoes  = request.POST.get('observacoes', '')
        action = request.POST.get('action', 'salvar')
        if action == 'calcular' and boletim.tabela_preco_id:
            # Salva o pedágio manual antes de calcular para não ser sobrescrito
            boletim.save()
            boletim.calcular()
            messages.success(request, 'Valores calculados com sucesso!')
        elif action == 'faturar':
            boletim.status = 'faturado'
            boletim.save()
            messages.success(request, f'Boletim OS-{os_obj.numero} marcado como Faturado!')
            return redirect('boletim_list')
        else:
            boletim.save()
            messages.success(request, 'Boletim salvo!')
        return redirect('boletim_detalhe', pk=pk)

    # Pré-preenche pedágio da OS se o boletim ainda não tiver valor
    pedagio_sugerido = boletim.valor_pedagio
    if pedagio_sugerido == 0 and op and op.pedagio:
        pedagio_sugerido = op.pedagio

    return render(request, 'cadastros/boletim_detalhe.html', {
        'boletim': boletim, 'os': os_obj, 'op': op, 'tabelas': tabelas,
        'pedagio_sugerido': pedagio_sugerido,
    })


# ══════════════════════════════════════════════════════════════════════════════
# EXPORTAÇÃO — Boletim de Medição (PDF e XLSX)
# ══════════════════════════════════════════════════════════════════════════════

def _boletim_queryset(request):
    """Aplica os mesmos filtros da boletim_list e retorna (qs, cliente_label, periodo_label)."""
    from datetime import datetime as dt
    q             = request.GET.get('q', '')
    status_filtro = request.GET.get('status', '')
    clientes_filtro = request.GET.getlist('clientes')
    data_ini      = request.GET.get('data_ini', '')
    data_fim      = request.GET.get('data_fim', '')

    boletins = BoletimMedicao.objects.select_related(
        'os', 'os__cliente', 'os__equipe', 'os__operacional', 'tabela_preco'
    ).all()

    if q:
        boletins = boletins.filter(
            Q(os__numero__icontains=q) |
            Q(os__cliente__razao_social__icontains=q) |
            Q(os__solicitante__icontains=q)
        )
    if status_filtro:
        boletins = boletins.filter(status=status_filtro)
    if clientes_filtro:
        boletins = boletins.filter(os__cliente__id__in=clientes_filtro)
    if data_ini:
        try:
            boletins = boletins.filter(
                os__previsao_inicio__date__gte=dt.strptime(data_ini, '%Y-%m-%d').date()
            )
        except ValueError:
            pass
    if data_fim:
        try:
            boletins = boletins.filter(
                os__previsao_inicio__date__lte=dt.strptime(data_fim, '%Y-%m-%d').date()
            )
        except ValueError:
            pass

    # Labels de cabeçalho
    if clientes_filtro and len(clientes_filtro) == 1:
        try:
            c = Cliente.objects.get(pk=clientes_filtro[0])
            cliente_label = f"{c.razao_social} — {c.cnpj}"
        except Exception:
            cliente_label = "Todos os Clientes"
    else:
        cliente_label = "Todos os Clientes"

    if data_ini or data_fim:
        ini_fmt = dt.strptime(data_ini, '%Y-%m-%d').strftime('%d/%m/%Y') if data_ini else '...'
        fim_fmt = dt.strptime(data_fim, '%Y-%m-%d').strftime('%d/%m/%Y') if data_fim else '...'
        periodo_label = f"{ini_fmt} a {fim_fmt}"
    else:
        periodo_label = "Período não informado"

    return boletins, cliente_label, periodo_label


def _boletim_to_missao(idx, b):
    """Converte um BoletimMedicao em dict compatível com o exportador."""
    os_obj = b.os
    op     = getattr(os_obj, 'operacional', None)
    tab    = b.tabela_preco

    # ── Agentes: dois agentes separados por " / " ──────────────────────────
    equipe = os_obj.equipe
    if equipe:
        nomes = []
        if equipe.agente1:
            nomes.append(equipe.agente1.nome.upper())
        if equipe.agente2:
            nomes.append(equipe.agente2.nome.upper())
        agentes_str = ' / '.join(nomes) if nomes else '---'
    else:
        # fallback: snapshot do nome da equipe se equipe foi deletada
        agentes_str = os_obj.snap_equipe_nome or '---'

    # ── Viatura: placa da viatura da equipe ────────────────────────────────
    if equipe and equipe.viatura:
        viatura_str = equipe.viatura.placa or os_obj.snap_viatura_placa or '---'
    else:
        viatura_str = os_obj.snap_viatura_placa or '---'

    # ── Veículos escoltados (concatena placas) ─────────────────────────────
    veiculos = os_obj.veiculos.all()
    escoltados = ', '.join(
        v.placa_cavalo for v in veiculos if v.placa_cavalo
    ) or '---'

    def fmt_dt(d):
        if not d:
            return "---"
        from django.utils.timezone import localtime, is_aware
        if is_aware(d):
            d = localtime(d)
        return d.strftime("%d/%m/%y %H:%M")

    # Prestador: nome da equipe ou fallback
    prestador = (equipe.nome if equipe and equipe.nome else os_obj.snap_equipe_nome) or 'JR SEGURANÇA'

    return {
        # ── Identificação ──────────────────────────────────────────
        'os':           str(os_obj.numero) if os_obj.numero else '',
        'cliente':      os_obj.cliente.razao_social if os_obj.cliente else '',
        'prestador':    prestador,
        'placa':        viatura_str,
        'escoltado':    escoltados,
        # ── Datas ──────────────────────────────────────────────────
        'agendamento':  fmt_dt(os_obj.previsao_inicio),
        'chegada_vtr':  fmt_dt(op.chegada_operacao  if op else None),
        'inicio_op':    fmt_dt(op.inicio_operacao    if op else None),
        'termino_op':   fmt_dt(op.termino_operacao   if op else None),
        # ── Horas ─────────────────────────────────────────────────
        'total_h':      b.horas_realizadas or '00:00',
        # ── Hodômetros ────────────────────────────────────────────
        'base_km':      (op.km_inicio_viagem       if op else None) or '',
        'hod_ini':      (op.km_chegada_operacao    if op else None) or '',
        'hod_fim':      (op.km_termino_operacao    if op else None) or '',
        'total_km':     b.km_realizado or 0,
        # ── Origem / Destino ───────────────────────────────────────
        'cidade_ori':   os_obj.cidade_origem or '',
        'uf_ori':       os_obj.uf_origem or '',
        'cidade_dst':   os_obj.cidade_destino or '',
        'uf_dst':       os_obj.uf_destino or '',
        # ── Franquia ───────────────────────────────────────────────
        'valor_franq':  float(tab.valor_escolta)  if tab else 0.0,
        'franq_km':     tab.franquia_km           if tab else 0,
        'franq_horas':  tab.franquia_horas        if tab else '00:00',
        # ── KM Excedente ───────────────────────────────────────────
        'total_os':     float(b.valor_excedente_km),     # TOTAL OS (vermelho)
        'exced_km':     b.km_excedente or 0,
        'taxa_km':      float(tab.excedente_km)   if tab else 0.0,
        'subtotal_km':  float(b.valor_excedente_km),     # TOTAL km (laranja)
        # ── Horas Excedentes ───────────────────────────────────────
        'exced_h':      b.horas_excedentes or '00:00',
        'taxa_hora':    float(tab.excedente_hora) if tab else 0.0,
        'subtotal_h':   float(b.valor_excedente_hora),   # TOTAL horas (laranja)
        # ── Encerramento ───────────────────────────────────────────
        'despesas':     float(b.acrescimo),
        'fechamento':   b.observacoes or '',
        'dt_pagamento': '',
        'nota_fiscal':  b.numero_nota or 'SEM',
        'total':        float(b.valor_total),
    }


def _calcular_totais(boletins_list):
    """Calcula linha de totais a partir da lista de boletins."""
    from decimal import Decimal
    total_hr_min = 0
    exced_hr_min = 0
    total_km     = 0
    exced_km     = 0
    desloc_km    = 0
    hr_exc       = Decimal('0')
    km_exc       = Decimal('0')
    escolta      = Decimal('0')
    pedagio      = Decimal('0')
    total        = Decimal('0')

    def hhmm_to_min(s):
        try:
            h, m = str(s).split(':')
            return int(h) * 60 + int(m)
        except Exception:
            return 0

    def min_to_hhmm(m):
        return f'{m // 60:03d}:{m % 60:02d}'

    despesas = Decimal('0')

    for b in boletins_list:
        op = getattr(b.os, 'operacional', None)
        total_hr_min += hhmm_to_min(b.horas_realizadas)
        exced_hr_min += hhmm_to_min(b.horas_excedentes)
        total_km     += b.km_realizado or 0
        exced_km     += b.km_excedente or 0
        desloc_km    += (op.km_trecho_chegada if op else 0) or 0
        hr_exc       += b.valor_excedente_hora
        km_exc       += b.valor_excedente_km
        escolta      += b.valor_escolta
        pedagio      += b.valor_pedagio
        despesas     += b.acrescimo
        total        += b.valor_total

    return {
        'missoes':      len(boletins_list),
        'total_h':      min_to_hhmm(total_hr_min),
        'exced_h':      min_to_hhmm(exced_hr_min),
        'total_km':     total_km,
        'exced_km':     exced_km,
        'desloc_km':    desloc_km,
        'hr_exc':       float(hr_exc),
        'km_exc':       float(km_exc),
        'subtotal_km':  float(km_exc),
        'subtotal_h':   float(hr_exc),
        'despesas':     float(despesas),
        'escolta':      float(escolta),
        'desloc_val':   0.0,
        'pedagio':      float(pedagio),
        'total':        float(total),
    }


@login_required
def boletim_export_pdf(request):
    """Gera o Boletim de Medição em PDF com os filtros ativos da listagem."""
    from django.http import HttpResponse
    from datetime import datetime
    from .boletim_export import gerar_pdf_bytes

    boletins_qs, cliente_label, periodo_label = _boletim_queryset(request)
    boletins_list = list(boletins_qs)
    missoes = [_boletim_to_missao(i + 1, b) for i, b in enumerate(boletins_list)]
    totais  = _calcular_totais(boletins_list)

    pdf_bytes = gerar_pdf_bytes(cliente_label, periodo_label, missoes, totais)
    filename  = f"BoletimMedicao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    response  = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@login_required
def boletim_export_xlsx(request):
    """Gera o Boletim de Medição em XLSX com os filtros ativos da listagem."""
    from django.http import HttpResponse
    from datetime import datetime
    from .boletim_export import gerar_xlsx_bytes

    boletins_qs, cliente_label, periodo_label = _boletim_queryset(request)
    boletins_list = list(boletins_qs)
    missoes = [_boletim_to_missao(i + 1, b) for i, b in enumerate(boletins_list)]
    totais  = _calcular_totais(boletins_list)

    xlsx_bytes = gerar_xlsx_bytes(cliente_label, periodo_label, missoes, totais)
    filename   = f"BoletimMedicao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    ct = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response   = HttpResponse(xlsx_bytes, content_type=ct)
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


# ── CONFIGURAÇÃO DE USUÁRIOS ─────────────────────────────────────────────────

from django.contrib.auth.models import User
from django.db.models import Q as QUser


def _get_nivel(user):
    """Retorna o nível do perfil. O usuário 'demark' é sempre developer."""
    if user.username.lower() == 'demark':
        return 'developer'
    try:
        return user.perfil.nivel
    except Exception:
        return 'operador'

def _is_admin_or_developer(user):
    return _get_nivel(user) in ('admin', 'developer')

def _is_developer(user):
    return _get_nivel(user) == 'developer'

def _is_financeiro(user):
    return _get_nivel(user) == 'financeiro'

def _pode_faturamento(user):
    """Financeiro, admin e developer têm acesso ao módulo de faturamento."""
    return _get_nivel(user) in ('financeiro', 'admin', 'developer')


@login_required
def usuario_list(request):
    """Lista usuários. O usuário 'demark' (developer) é invisível para todos exceto ele mesmo."""
    q = request.GET.get('q', '')

    # Buscar os IDs do usuário demark (case-insensitive) para exclusão segura
    demark_ids = list(
        User.objects.filter(username__iexact='demark').values_list('id', flat=True)
    )

    qs = User.objects.select_related('perfil').order_by('username')

    # Sempre ocultar o usuário demark para quem não é o próprio demark
    if request.user.username.lower() != 'demark' and demark_ids:
        qs = qs.exclude(id__in=demark_ids)

    if q:
        qs = qs.filter(
            QUser(username__icontains=q) |
            QUser(first_name__icontains=q) |
            QUser(last_name__icontains=q) |
            QUser(email__icontains=q)
        )

    total = qs.count()
    ativos = qs.filter(is_active=True).count()
    admins = qs.filter(perfil__nivel='admin').count()

    return render(request, 'cadastros/usuario_list.html', {
        'usuarios': qs,
        'q': q,
        'total': total,
        'ativos': ativos,
        'admins': admins,
        'pode_gerenciar': _is_admin_or_developer(request.user),
    })


@login_required
def usuario_create(request):
    """Cria um novo usuário. Apenas admin e developer podem criar usuários."""
    if not _is_admin_or_developer(request.user):
        messages.error(request, 'Você não tem permissão para criar usuários.')
        return redirect('usuario_list')

    from django.contrib.auth import get_user_model

    class FakeForm:
        def __init__(self, data=None):
            self._data = data or {}
            self.errors = {}
            for f in ('username', 'first_name', 'last_name', 'email',
                      'password1', 'password2', 'nivel', 'is_active'):
                setattr(self, f, type('F', (), {'value': lambda s, k=f: self._data.get(k, ''), 'errors': []})())
            self.is_active = type('F', (), {'value': lambda: self._data.get('is_active', '1'), 'errors': []})()

    if request.method == 'POST':
        errors = {}
        username = request.POST.get('username', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        nivel = request.POST.get('nivel', 'operador')
        is_active = request.POST.get('is_active') == '1'

        # Ninguém pode criar outro developer (apenas demark pode ser developer)
        if nivel == 'developer':
            nivel = 'operador'

        # Proteger username 'demark'
        if username.lower() == 'demark':
            errors['username'] = ['Este nome de usuário é reservado.']

        if not username:
            errors['username'] = ['Nome de usuário é obrigatório.']
        elif not errors.get('username') and User.objects.filter(username=username).exists():
            errors['username'] = ['Este nome de usuário já está em uso.']

        if not password1:
            errors['password1'] = ['Senha é obrigatória.']
        elif len(password1) < 8:
            errors['password1'] = ['A senha deve ter no mínimo 8 caracteres.']
        elif password1 != password2:
            errors['password2'] = ['As senhas não conferem.']

        if not errors:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password1,
                is_active=is_active,
            )
            try:
                user.perfil.nivel = nivel
                user.perfil.save()
            except Exception:
                pass

            messages.success(request, f'Usuário "{username}" criado com sucesso!')
            return redirect('usuario_list')

        form = FakeForm(request.POST)
        for field, errs in errors.items():
            getattr(form, field).errors = errs

        return render(request, 'cadastros/usuario_form.html', {'form': form, 'sou_admin': _is_admin_or_developer(request.user)})

    form = FakeForm()
    return render(request, 'cadastros/usuario_form.html', {'form': form, 'sou_admin': _is_admin_or_developer(request.user)})


@login_required
def usuario_edit(request, pk):
    """Edita dados de um usuário. Admin/developer podem editar qualquer um. Outros só a si mesmos."""
    u = get_object_or_404(User, pk=pk)
    eu_mesmo = (request.user.pk == u.pk)
    sou_admin = _is_admin_or_developer(request.user)

    # Proteger o usuário demark: só o próprio demark pode editar seu perfil
    if u.username.lower() == 'demark' and request.user.username.lower() != 'demark':
        messages.error(request, 'Sem permissão.')
        return redirect('usuario_list')

    # Operador só pode editar a si mesmo
    if not sou_admin and not eu_mesmo:
        messages.error(request, 'Você só pode editar sua própria conta.')
        return redirect('usuario_list')

    class FakeForm:
        def __init__(self, data=None, instance=None):
            self._data = data
            self._inst = instance
            for f in ('username', 'first_name', 'last_name', 'email', 'nivel'):
                setattr(self, f, type('F', (), {
                    'value': lambda s, k=f: (data or {}).get(k, getattr(instance, k, '') if instance else ''),
                    'errors': []
                })())
            if instance:
                try:
                    self.nivel.value = lambda: (data or {}).get('nivel', instance.perfil.nivel)
                except Exception:
                    self.nivel.value = lambda: 'operador'
            self.is_active = type('F', (), {
                'value': lambda: (data or {}).get('is_active', '1' if (instance and instance.is_active) else ''),
                'errors': []
            })()
            self.errors = {}

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        errors = {}

        if not username:
            errors['username'] = ['Nome de usuário é obrigatório.']
        elif User.objects.filter(username=username).exclude(pk=pk).exists():
            errors['username'] = ['Este nome de usuário já está em uso.']

        if not errors:
            u.username = username
            u.first_name = request.POST.get('first_name', '').strip()
            u.last_name = request.POST.get('last_name', '').strip()
            u.email = request.POST.get('email', '').strip()

            # Só admin pode mudar is_active e nivel
            if sou_admin:
                u.is_active = request.POST.get('is_active') == '1'
                nivel = request.POST.get('nivel', 'operador')
                # Ninguém pode promover outro a developer
                if nivel == 'developer' and u.username != 'demark':
                    nivel = 'operador'
                try:
                    u.perfil.nivel = nivel
                    u.perfil.save()
                except Exception:
                    pass

            u.save()
            messages.success(request, f'Usuário "{u.username}" atualizado com sucesso!')
            return redirect('usuario_list')

        form = FakeForm(request.POST, u)
        for field, errs in errors.items():
            getattr(form, field).errors = errs
        return render(request, 'cadastros/usuario_form.html', {'form': form, 'obj': u, 'sou_admin': sou_admin})

    form = FakeForm(instance=u)
    return render(request, 'cadastros/usuario_form.html', {'form': form, 'obj': u, 'sou_admin': sou_admin})


@login_required
def usuario_senha(request, pk):
    """Altera senha. Cada usuário pode alterar a própria. Admin/developer podem alterar de qualquer um."""
    u = get_object_or_404(User, pk=pk)
    eu_mesmo = (request.user.pk == u.pk)
    sou_admin = _is_admin_or_developer(request.user)

    # Proteger demark: só o próprio demark altera sua senha
    if u.username.lower() == 'demark' and request.user.username.lower() != 'demark':
        messages.error(request, 'Sem permissão.')
        return redirect('usuario_list')

    # Operador só pode alterar a própria senha
    if not sou_admin and not eu_mesmo:
        messages.error(request, 'Você só pode alterar sua própria senha.')
        return redirect('usuario_list')

    class FakeForm:
        def __init__(self):
            self.password1 = type('F', (), {'errors': []})()
            self.password2 = type('F', (), {'errors': []})()
            self.errors = {}

    if request.method == 'POST':
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        form = FakeForm()
        errors = False

        if not password1 or len(password1) < 8:
            form.password1.errors = ['A senha deve ter no mínimo 8 caracteres.']
            errors = True
        elif password1 != password2:
            form.password2.errors = ['As senhas não conferem.']
            errors = True

        if not errors:
            u.set_password(password1)
            u.save()
            # Se alterou a própria senha, mantém logado
            if eu_mesmo:
                from django.contrib.auth import update_session_auth_hash
                update_session_auth_hash(request, u)
                messages.success(request, 'Sua senha foi alterada com sucesso!')
            else:
                messages.success(request, f'Senha do usuário "{u.username}" alterada com sucesso!')
            return redirect('usuario_list')

        return render(request, 'cadastros/usuario_senha.html', {'form': form, 'obj': u})

    form = FakeForm()
    return render(request, 'cadastros/usuario_senha.html', {'form': form, 'obj': u})


@login_required
def usuario_delete(request, pk):
    """Exclui um usuário. Apenas admin/developer podem excluir. Não pode excluir demark ou a si mesmo."""
    u = get_object_or_404(User, pk=pk)

    if not _is_admin_or_developer(request.user):
        messages.error(request, 'Você não tem permissão para excluir usuários.')
        return redirect('usuario_list')

    if u == request.user:
        messages.error(request, 'Você não pode excluir sua própria conta.')
        return redirect('usuario_list')

    if u.username.lower() == 'demark':
        messages.error(request, 'Este usuário não pode ser excluído.')
        return redirect('usuario_list')

    if request.method == 'POST':
        nome = u.username
        u.delete()
        messages.success(request, f'Usuário "{nome}" removido com sucesso.')
        return redirect('usuario_list')

    return render(request, 'cadastros/usuario_delete.html', {'obj': u})


# ==============================================================================
# LINK EXTERNO — Agente de campo preenche OS sem login
# ==============================================================================


@csrf_exempt
def os_field_marco_salvar(request, token):
    """Salva um marco individual (data + km + gps + foto) via AJAX do link do agente."""
    from django.http import JsonResponse
    from datetime import datetime

    if request.method != 'POST':
        return JsonResponse({'ok': False, 'erro': 'Metodo invalido.'})

    try:
        op = OSOperacional.objects.get(token=token, link_ativo=True)
    except OSOperacional.DoesNotExist:
        return JsonResponse({'ok': False, 'erro': 'Link invalido ou inativo.'})

    marco = request.POST.get('marco', '').strip()
    campos_validos = ['inicio_viagem', 'chegada_operacao', 'inicio_operacao', 'termino_operacao', 'termino_viagem']
    if marco not in campos_validos:
        return JsonResponse({'ok': False, 'erro': 'Marco invalido.'})

    dt_val  = request.POST.get('dt',  '').strip()
    km_val  = request.POST.get('km',  '').strip()
    lat_val = request.POST.get('lat', '').strip()
    lng_val = request.POST.get('lng', '').strip()

    def parse_dt(val):
        if not val: return None
        for fmt in ('%Y-%m-%dT%H:%M', '%d/%m/%Y %H:%M', '%Y-%m-%d %H:%M'):
            try: return datetime.strptime(val, fmt)
            except ValueError: continue
        return None

    def parse_float(val):
        try: return float(val) if val else None
        except (ValueError, TypeError): return None

    def parse_int(val):
        try: return int(val) if val else None
        except (ValueError, TypeError): return None

    setattr(op, marco,           parse_dt(dt_val))
    setattr(op, f'km_{marco}',   parse_int(km_val))
    setattr(op, f'gps_{marco}_lat', parse_float(lat_val))
    setattr(op, f'gps_{marco}_lng', parse_float(lng_val))
    op.save()

    foto_id = None
    foto_url = None
    foto = request.FILES.get('foto')
    if foto:
        FotoMarco.objects.filter(os=op.os, marco=marco).delete()
        fm = FotoMarco.objects.create(os=op.os, marco=marco, foto=foto)
        foto_id = fm.pk
        foto_url = fm.foto.url

    return JsonResponse({'ok': True, 'foto_id': foto_id, 'foto_url': foto_url})

def os_field_link(request, token):
    """Página pública para agente externo preencher dados operacionais da OS."""
    from datetime import datetime

    op = get_object_or_404(OSOperacional, token=token)
    os_obj = op.os

    if not op.link_ativo:
        return render(request, 'cadastros/os_field_desativado.html', {'os': os_obj})

    if os_obj.status == 'finalizada':
        return render(request, 'cadastros/os_field_desativado.html', {'os': os_obj, 'finalizada': True})

    erro = None
    sucesso = False

    if request.method == 'POST':
        def parse_dt(val):
            if not val:
                return None
            for fmt in ('%Y-%m-%dT%H:%M', '%d/%m/%Y %H:%M', '%Y-%m-%d %H:%M'):
                try:
                    return datetime.strptime(val, fmt)
                except ValueError:
                    continue
            return None

        def parse_int(val):
            try:
                return int(val) if val else None
            except (ValueError, TypeError):
                return None

        op.numero_folha       = request.POST.get('numero_folha', '')
        op.inicio_viagem      = parse_dt(request.POST.get('inicio_viagem'))
        op.chegada_operacao   = parse_dt(request.POST.get('chegada_operacao'))
        op.inicio_operacao    = parse_dt(request.POST.get('inicio_operacao'))
        op.termino_operacao   = parse_dt(request.POST.get('termino_operacao'))
        op.termino_viagem     = parse_dt(request.POST.get('termino_viagem'))
        op.km_inicio_viagem    = parse_int(request.POST.get('km_inicio_viagem'))
        op.km_chegada_operacao = parse_int(request.POST.get('km_chegada_operacao'))
        op.km_inicio_operacao  = parse_int(request.POST.get('km_inicio_operacao'))
        op.km_termino_operacao = parse_int(request.POST.get('km_termino_operacao'))
        op.km_termino_viagem   = parse_int(request.POST.get('km_termino_viagem'))

        # Pedagio
        pedagio_raw = request.POST.get('pedagio', '').strip().replace(',', '.')
        try:
            op.pedagio = float(pedagio_raw) if pedagio_raw else None
        except ValueError:
            op.pedagio = None


        # GPS — capturado pelo browser do agente
        def parse_dec(val):
            try:
                return float(val) if val and val.strip() else None
            except (ValueError, TypeError):
                return None

        op.gps_inicio_viagem_lat    = parse_dec(request.POST.get('gps_inicio_viagem_lat'))
        op.gps_inicio_viagem_lng    = parse_dec(request.POST.get('gps_inicio_viagem_lng'))
        op.gps_chegada_operacao_lat = parse_dec(request.POST.get('gps_chegada_operacao_lat'))
        op.gps_chegada_operacao_lng = parse_dec(request.POST.get('gps_chegada_operacao_lng'))
        op.gps_inicio_operacao_lat  = parse_dec(request.POST.get('gps_inicio_operacao_lat'))
        op.gps_inicio_operacao_lng  = parse_dec(request.POST.get('gps_inicio_operacao_lng'))
        op.gps_termino_operacao_lat = parse_dec(request.POST.get('gps_termino_operacao_lat'))
        op.gps_termino_operacao_lng = parse_dec(request.POST.get('gps_termino_operacao_lng'))
        op.gps_termino_viagem_lat   = parse_dec(request.POST.get('gps_termino_viagem_lat'))
        op.gps_termino_viagem_lng   = parse_dec(request.POST.get('gps_termino_viagem_lng'))

        pedagio_val = request.POST.get('pedagio', '').strip().replace(',', '.')
        try:
            op.pedagio = float(pedagio_val) if pedagio_val else None
        except ValueError:
            op.pedagio = None
        op.save()

        # Atualizar status da OS
        if os_obj.status != 'cancelada':
            if op.termino_viagem:
                os_obj.status = 'concluida'
            elif op.termino_operacao:
                os_obj.status = 'encerrando'
            elif op.chegada_operacao or op.inicio_operacao:
                os_obj.status = 'em_operacao'
            elif op.inicio_viagem:
                os_obj.status = 'em_viagem'
            os_obj.save(update_fields=['status'])

        sucesso = True

    def fmt_dt(dt):
        if dt:
            return dt.strftime('%Y-%m-%dT%H:%M')
        return ''

    def fmt_gps(lat, lng):
        if lat and lng:
            return {'lat': float(lat), 'lng': float(lng),
                    'url': f'https://www.google.com/maps?q={lat},{lng}'}
        return None

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
    })


@login_required
def os_gerar_link(request, pk):
    """Garante que existe um OSOperacional com token e retorna JSON com o link."""
    import json
    os_obj = get_object_or_404(OrdemServico, pk=pk)
    op, _ = OSOperacional.objects.get_or_create(os=os_obj)
    op.link_ativo = True
    op.save(update_fields=['link_ativo'])
    url = request.build_absolute_uri(f'/os/field/{op.token}/')
    return JsonResponse({'url': url, 'token': str(op.token)})


@login_required
def os_desativar_link(request, pk):
    """Desativa o link externo da OS."""
    os_obj = get_object_or_404(OrdemServico, pk=pk)
    op = getattr(os_obj, 'operacional', None)
    if op:
        op.link_ativo = False
        op.save(update_fields=['link_ativo'])
        messages.success(request, 'Link externo desativado com sucesso.')
    return redirect('os_detalhe', pk=pk)



# ============================================================
# ADICIONAR ao final de cadastros/views.py
# ============================================================
# Também adicione este import no TOPO do views.py, junto com os outros:
#   from .models import (... FotoMarco, Parada, FotoParada,
#       Incidente, FotoIncidente, FotoVeiculoEscoltado,
#       TrocaMotorista, FotoTrocaMotorista, AssinaturaOS, DespesaOS)
# ============================================================

import base64
import io
from django.core.files.base import ContentFile


# ────────────────────────────────────────────────────────────
# HELPER: salvar foto base64 (assinaturas enviadas via canvas)
# ────────────────────────────────────────────────────────────
def _base64_to_file(data_url, nome_base='assinatura'):
    """Converte data:image/png;base64,... → ContentFile para salvar no ImageField."""
    if not data_url or not data_url.startswith('data:'):
        return None
    header, encoded = data_url.split(',', 1)
    return ContentFile(base64.b64decode(encoded), name=f'{nome_base}.png')


# ────────────────────────────────────────────────────────────
# FOTOS DE MARCOS — upload AJAX
# ────────────────────────────────────────────────────────────
def os_field_foto_marco(request, token):
    """Recebe upload de foto de um marco via POST AJAX (multipart).
    Permite apenas UMA foto por marco: se já existir, substitui a antiga."""
    from .models import FotoMarco, OSOperacional
    op = get_object_or_404(OSOperacional, token=token)
    if not op.link_ativo:
        return JsonResponse({'ok': False, 'erro': 'Link inativo.'}, status=403)

    if request.method != 'POST':
        return JsonResponse({'ok': False}, status=405)

    marco = request.POST.get('marco', '').strip()
    foto  = request.FILES.get('foto')
    lat   = request.POST.get('lat', '').strip() or None
    lng   = request.POST.get('lng', '').strip() or None

    MARCOS_VALIDOS = {'inicio_viagem','chegada_operacao','inicio_operacao',
                      'termino_operacao','termino_viagem'}
    if marco not in MARCOS_VALIDOS or not foto:
        return JsonResponse({'ok': False, 'erro': 'Dados inválidos.'}, status=400)

    # Se já existe foto para este marco, apaga o arquivo físico e reutiliza o registro
    existente = FotoMarco.objects.filter(os=op.os, marco=marco).first()
    if existente:
        existente.foto.delete(save=False)   # remove arquivo físico do storage
        existente.foto      = foto
        existente.latitude  = lat
        existente.longitude = lng
        existente.save()
        obj = existente
        substituida = True
    else:
        obj = FotoMarco.objects.create(
            os=op.os,
            marco=marco,
            foto=foto,
            latitude=lat,
            longitude=lng,
        )
        substituida = False

    return JsonResponse({
        'ok': True,
        'id': obj.pk,
        'url': obj.foto.url,
        'marco': marco,
        'substituida': substituida,
    })


def os_field_foto_marco_delete(request, token, foto_pk):
    """Remove uma foto de marco."""
    from .models import FotoMarco, OSOperacional
    op  = get_object_or_404(OSOperacional, token=token)
    obj = get_object_or_404(FotoMarco, pk=foto_pk, os=op.os)
    if request.method == 'POST':
        obj.foto.delete(save=False)
        obj.delete()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False}, status=405)


# ────────────────────────────────────────────────────────────
# PARADAS
# ────────────────────────────────────────────────────────────
def os_field_parada_salvar(request, token):
    """Cria ou atualiza uma parada."""
    from .models import Parada, FotoParada, OSOperacional
    from datetime import datetime

    op = get_object_or_404(OSOperacional, token=token)
    if not op.link_ativo:
        return JsonResponse({'ok': False, 'erro': 'Link inativo.'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'ok': False}, status=405)

    def parse_dt(val):
        if not val:
            return None
        for fmt in ('%Y-%m-%dT%H:%M', '%d/%m/%Y %H:%M', '%Y-%m-%d %H:%M'):
            try:
                return datetime.strptime(val, fmt)
            except ValueError:
                continue
        return None

    pk      = request.POST.get('pk') or None
    motivo  = request.POST.get('motivo', 'outro')
    descr   = request.POST.get('descricao', '')
    inicio  = parse_dt(request.POST.get('inicio', ''))
    fim     = parse_dt(request.POST.get('fim', ''))
    lat     = request.POST.get('lat', '').strip() or None
    lng     = request.POST.get('lng', '').strip() or None

    if not inicio:
        return JsonResponse({'ok': False, 'erro': 'Informe a data/hora de início.'}, status=400)

    if pk:
        parada = get_object_or_404(Parada, pk=pk, os=op.os)
        parada.motivo    = motivo
        parada.descricao = descr
        parada.inicio    = inicio
        parada.fim       = fim
        parada.latitude  = lat
        parada.longitude = lng
        parada.save()
    else:
        parada = Parada.objects.create(
            os=op.os, motivo=motivo, descricao=descr,
            inicio=inicio, fim=fim, latitude=lat, longitude=lng,
        )

    # Salvar fotos (múltiplas, campo name="fotos")
    for foto in request.FILES.getlist('fotos'):
        FotoParada.objects.create(parada=parada, foto=foto)

    return JsonResponse({
        'ok': True,
        'pk': parada.pk,
        'motivo_display': parada.get_motivo_display(),
        'inicio': parada.inicio.strftime('%d/%m/%Y %H:%M'),
        'duracao': parada.duracao_minutos,
    })


def os_field_parada_delete(request, token, pk):
    """Remove uma parada."""
    from .models import Parada, OSOperacional
    op = get_object_or_404(OSOperacional, token=token)
    parada = get_object_or_404(Parada, pk=pk, os=op.os)
    if request.method == 'POST':
        for f in parada.fotos.all():
            f.foto.delete(save=False)
        parada.delete()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False}, status=405)


# ────────────────────────────────────────────────────────────
# INCIDENTES
# ────────────────────────────────────────────────────────────
def os_field_incidente_salvar(request, token):
    """Cria ou atualiza um incidente."""
    from .models import Incidente, FotoIncidente, OSOperacional
    from datetime import datetime

    op = get_object_or_404(OSOperacional, token=token)
    if not op.link_ativo:
        return JsonResponse({'ok': False, 'erro': 'Link inativo.'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'ok': False}, status=405)

    def parse_dt(val):
        if not val:
            return None
        for fmt in ('%Y-%m-%dT%H:%M', '%d/%m/%Y %H:%M', '%Y-%m-%d %H:%M'):
            try:
                return datetime.strptime(val, fmt)
            except ValueError:
                continue
        return None

    pk        = request.POST.get('pk') or None
    tipo      = request.POST.get('tipo', 'outro')
    gravidade = request.POST.get('gravidade', 'media')
    descricao = request.POST.get('descricao', '').strip()
    ocorrido  = parse_dt(request.POST.get('ocorrido_em', ''))
    bo        = request.POST.get('bo_numero', '').strip()
    lat       = request.POST.get('lat', '').strip() or None
    lng       = request.POST.get('lng', '').strip() or None

    if not descricao or not ocorrido:
        return JsonResponse({'ok': False, 'erro': 'Informe a descrição e a data/hora.'}, status=400)

    if pk:
        inc = get_object_or_404(Incidente, pk=pk, os=op.os)
        inc.tipo = tipo; inc.gravidade = gravidade; inc.descricao = descricao
        inc.ocorrido_em = ocorrido; inc.bo_numero = bo
        inc.latitude = lat; inc.longitude = lng
        inc.save()
    else:
        inc = Incidente.objects.create(
            os=op.os, tipo=tipo, gravidade=gravidade, descricao=descricao,
            ocorrido_em=ocorrido, bo_numero=bo, latitude=lat, longitude=lng,
        )

    for foto in request.FILES.getlist('fotos'):
        FotoIncidente.objects.create(incidente=inc, foto=foto)

    return JsonResponse({
        'ok': True,
        'pk': inc.pk,
        'tipo_display': inc.get_tipo_display(),
        'gravidade': inc.gravidade,
        'ocorrido': inc.ocorrido_em.strftime('%d/%m/%Y %H:%M'),
    })


def os_field_incidente_delete(request, token, pk):
    """Remove um incidente."""
    from .models import Incidente, OSOperacional
    op  = get_object_or_404(OSOperacional, token=token)
    inc = get_object_or_404(Incidente, pk=pk, os=op.os)
    if request.method == 'POST':
        for f in inc.fotos.all():
            f.foto.delete(save=False)
        inc.delete()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False}, status=405)


# ────────────────────────────────────────────────────────────
# FOTOS DE VEÍCULOS ESCOLTADOS
# ────────────────────────────────────────────────────────────
def os_field_foto_veiculo(request, token):
    """Salva foto de um veículo escoltado."""
    from .models import FotoVeiculoEscoltado, VeiculoEscoltado, OSOperacional
    op = get_object_or_404(OSOperacional, token=token)
    if not op.link_ativo:
        return JsonResponse({'ok': False, 'erro': 'Link inativo.'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'ok': False}, status=405)

    veiculo_pk = request.POST.get('veiculo_pk')
    momento    = request.POST.get('momento', 'antes')
    foto       = request.FILES.get('foto')

    if not foto or not veiculo_pk:
        return JsonResponse({'ok': False, 'erro': 'Dados inválidos.'}, status=400)

    veiculo = get_object_or_404(VeiculoEscoltado, pk=veiculo_pk, os=op.os)
    obj = FotoVeiculoEscoltado.objects.create(veiculo=veiculo, momento=momento, foto=foto)
    return JsonResponse({'ok': True, 'id': obj.pk, 'url': obj.foto.url})


def os_field_foto_veiculo_delete(request, token, foto_pk):
    """Remove uma foto de veículo escoltado."""
    from .models import FotoVeiculoEscoltado, OSOperacional
    op  = get_object_or_404(OSOperacional, token=token)
    obj = get_object_or_404(FotoVeiculoEscoltado, pk=foto_pk, veiculo__os=op.os)
    if request.method == 'POST':
        obj.foto.delete(save=False)
        obj.delete()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False}, status=405)


# ────────────────────────────────────────────────────────────
# TROCA DE MOTORISTAS
# ────────────────────────────────────────────────────────────
def os_field_troca_motorista(request, token):
    """Registra troca de motorista."""
    from .models import TrocaMotorista, FotoTrocaMotorista, VeiculoEscoltado, OSOperacional
    from datetime import datetime

    op = get_object_or_404(OSOperacional, token=token)
    if not op.link_ativo:
        return JsonResponse({'ok': False, 'erro': 'Link inativo.'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'ok': False}, status=405)

    def parse_dt(val):
        if not val:
            return None
        for fmt in ('%Y-%m-%dT%H:%M', '%d/%m/%Y %H:%M', '%Y-%m-%d %H:%M'):
            try:
                return datetime.strptime(val, fmt)
            except ValueError:
                continue
        return None

    veiculo_pk  = request.POST.get('veiculo_pk') or None
    saindo      = request.POST.get('motorista_saindo', '').strip()
    entrando    = request.POST.get('motorista_entrando', '').strip()
    ocorrido    = parse_dt(request.POST.get('ocorrido_em', ''))
    motivo      = request.POST.get('motivo', '').strip()
    lat         = request.POST.get('lat', '').strip() or None
    lng         = request.POST.get('lng', '').strip() or None

    if not saindo or not entrando or not ocorrido:
        return JsonResponse({'ok': False,
                             'erro': 'Informe motorista saindo, entrando e data/hora.'}, status=400)

    veiculo = None
    if veiculo_pk:
        veiculo = VeiculoEscoltado.objects.filter(pk=veiculo_pk, os=op.os).first()

    troca = TrocaMotorista.objects.create(
        os=op.os,
        veiculo_escoltado=veiculo,
        motorista_saindo=saindo,
        motorista_entrando=entrando,
        ocorrido_em=ocorrido,
        motivo=motivo,
        latitude=lat,
        longitude=lng,
    )
    for foto in request.FILES.getlist('fotos'):
        FotoTrocaMotorista.objects.create(troca=troca, foto=foto)

    return JsonResponse({
        'ok': True,
        'pk': troca.pk,
        'saindo': saindo,
        'entrando': entrando,
        'ocorrido': troca.ocorrido_em.strftime('%d/%m/%Y %H:%M'),
    })


def os_field_troca_motorista_delete(request, token, pk):
    """Remove uma troca de motorista."""
    from .models import TrocaMotorista, OSOperacional
    op    = get_object_or_404(OSOperacional, token=token)
    troca = get_object_or_404(TrocaMotorista, pk=pk, os=op.os)
    if request.method == 'POST':
        for f in troca.fotos.all():
            f.foto.delete(save=False)
        troca.delete()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False}, status=405)


# ────────────────────────────────────────────────────────────
# ASSINATURAS DIGITAIS
# ────────────────────────────────────────────────────────────
def os_field_assinatura(request, token):
    """Salva assinatura digital (base64 PNG vindo do canvas)."""
    from .models import AssinaturaOS, OSOperacional
    import json

    op = get_object_or_404(OSOperacional, token=token)
    if not op.link_ativo:
        return JsonResponse({'ok': False, 'erro': 'Link inativo.'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'ok': False}, status=405)

    try:
        body = json.loads(request.body)
    except (ValueError, TypeError):
        body = request.POST

    tipo      = body.get('tipo', '')
    nome      = body.get('nome', '').strip()
    data_url  = body.get('assinatura', '')

    TIPOS = {c[0] for c in AssinaturaOS.TIPO_CHOICES}
    if tipo not in TIPOS or not nome or not data_url:
        return JsonResponse({'ok': False, 'erro': 'Dados inválidos.'}, status=400)

    arquivo = _base64_to_file(data_url, nome_base=f'ass_{tipo}')
    if not arquivo:
        return JsonResponse({'ok': False, 'erro': 'Assinatura inválida.'}, status=400)

    obj, created = AssinaturaOS.objects.get_or_create(
        os=op.os, tipo=tipo,
        defaults={'nome': nome}
    )
    if not created:
        # Atualiza — apaga a imagem anterior
        if obj.imagem:
            obj.imagem.delete(save=False)
        obj.nome = nome
    obj.imagem.save(arquivo.name, arquivo, save=True)

    return JsonResponse({
        'ok': True,
        'tipo': tipo,
        'tipo_display': obj.get_tipo_display(),
        'nome': nome,
        'url': obj.imagem.url,
    })


# ────────────────────────────────────────────────────────────
# DESPESAS / CRÉDITOS
# ────────────────────────────────────────────────────────────
def os_field_despesa_salvar(request, token):
    """Cria uma despesa/crédito."""
    from .models import DespesaOS, OSOperacional
    from datetime import datetime
    from decimal import Decimal, InvalidOperation

    op = get_object_or_404(OSOperacional, token=token)
    if not op.link_ativo:
        return JsonResponse({'ok': False, 'erro': 'Link inativo.'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'ok': False}, status=405)

    def parse_dt(val):
        if not val:
            return None
        for fmt in ('%Y-%m-%dT%H:%M', '%d/%m/%Y %H:%M', '%Y-%m-%d %H:%M'):
            try:
                return datetime.strptime(val, fmt)
            except ValueError:
                continue
        return None

    tipo        = request.POST.get('tipo', 'outro')
    natureza    = request.POST.get('natureza', 'despesa')
    descricao   = request.POST.get('descricao', '').strip()
    valor_raw   = request.POST.get('valor', '0').replace(',', '.').strip()
    ocorrido    = parse_dt(request.POST.get('ocorrido_em', ''))
    comprovante = request.FILES.get('comprovante')

    try:
        valor = Decimal(valor_raw)
        if valor <= 0:
            raise ValueError
    except (InvalidOperation, ValueError):
        return JsonResponse({'ok': False, 'erro': 'Valor inválido.'}, status=400)

    if not ocorrido:
        return JsonResponse({'ok': False, 'erro': 'Informe a data/hora.'}, status=400)

    desp = DespesaOS.objects.create(
        os=op.os,
        tipo=tipo,
        natureza=natureza,
        descricao=descricao,
        valor=valor,
        ocorrido_em=ocorrido,
    )
    if comprovante:
        desp.comprovante = comprovante
        desp.save(update_fields=['comprovante'])

    return JsonResponse({
        'ok': True,
        'pk': desp.pk,
        'tipo_display': desp.get_tipo_display(),
        'natureza': natureza,
        'valor': str(desp.valor),
        'ocorrido': desp.ocorrido_em.strftime('%d/%m/%Y %H:%M'),
    })


def os_field_despesa_delete(request, token, pk):
    """Remove uma despesa."""
    from .models import DespesaOS, OSOperacional
    op   = get_object_or_404(OSOperacional, token=token)
    desp = get_object_or_404(DespesaOS, pk=pk, os=op.os)
    if request.method == 'POST':
        if desp.comprovante:
            desp.comprovante.delete(save=False)
        desp.delete()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False}, status=405)

@csrf_exempt
def os_field_pedagio_salvar(request, token):
    """Salva o valor do pedagio via AJAX (link externo do agente)."""
    from .models import OSOperacional
    op = get_object_or_404(OSOperacional, token=token)
    if not op.link_ativo:
        return JsonResponse({'ok': False, 'erro': 'Link inativo.'}, status=403)
    if request.method == 'POST':
        pedagio_raw = request.POST.get('pedagio', '').strip().replace(',', '.')
        try:
            op.pedagio = float(pedagio_raw) if pedagio_raw else None
        except ValueError:
            return JsonResponse({'ok': False, 'erro': 'Valor inválido.'})
        op.save(update_fields=['pedagio'])
        return JsonResponse({'ok': True, 'pedagio': str(op.pedagio)})
    return JsonResponse({'ok': False}, status=405)
@csrf_exempt
def os_field_veiculo_salvar(request, token):
    """Cria ou edita um VeiculoEscoltado via AJAX (link externo do agente)."""
    from .models import VeiculoEscoltado, OSOperacional
    op = get_object_or_404(OSOperacional, token=token)
    if not op.link_ativo:
        return JsonResponse({'ok': False, 'erro': 'Link inativo.'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'erro': 'Método inválido.'}, status=405)

    pk          = request.POST.get('pk') or None          # se preenchido → edita
    veiculo     = request.POST.get('veiculo', '').strip()
    placa_cav   = request.POST.get('placa_cavalo', '').strip().upper()
    placa_car   = request.POST.get('placa_carreta', '').strip().upper()
    placa_car2  = request.POST.get('placa_carreta2', '').strip().upper()
    motorista   = request.POST.get('motorista', '').strip()

    if not (veiculo or placa_cav or motorista):
        return JsonResponse({'ok': False, 'erro': 'Preencha ao menos tipo, placa ou motorista.'})

    if pk:
        obj = get_object_or_404(VeiculoEscoltado, pk=pk, os=op.os)
    else:
        # ordem = próximo disponível
        ultima = op.os.veiculos.order_by('-ordem').first()
        obj = VeiculoEscoltado(os=op.os, ordem=(ultima.ordem + 1 if ultima else 1))

    obj.veiculo       = veiculo
    obj.placa_cavalo  = placa_cav
    obj.placa_carreta = placa_car
    obj.placa_carreta2 = placa_car2
    obj.motorista     = motorista
    obj.save()

    return JsonResponse({
        'ok': True,
        'pk': obj.pk,
        'label': obj.placa_cavalo or obj.veiculo or f'Veículo {obj.pk}',
        'motorista': obj.motorista,
        'placa_carreta': obj.placa_carreta,
        'placa_carreta2': obj.placa_carreta2,
        'veiculo': obj.veiculo,
    })


@csrf_exempt
def os_field_veiculo_delete(request, token, pk):
    """Deleta um VeiculoEscoltado via AJAX (link externo do agente)."""
    from .models import VeiculoEscoltado, OSOperacional
    op = get_object_or_404(OSOperacional, token=token)
    if not op.link_ativo:
        return JsonResponse({'ok': False, 'erro': 'Link inativo.'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'erro': 'Método inválido.'}, status=405)
    obj = get_object_or_404(VeiculoEscoltado, pk=pk, os=op.os)
    obj.delete()
    return JsonResponse({'ok': True})


# ─────────────────────────────────────────────────────────────────────────────
# PATRIMONIAL — cadastro de vigilantes patrimoniais e porteiros
# Modulo independente de OS/escolta. CRUD puro com filtros e alertas de
# vencimento de documentos (CNV, CNH, Curso).
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def patrimonial_dashboard(request):
    """Painel de avisos do módulo patrimonial — vencimentos próximos (60 dias)."""
    hoje = date.today()
    limite = hoje + timedelta(days=60)

    ativos = FuncionarioPatrimonial.objects.filter(status='ativo')

    alertas_cnh = (
        ativos
        .exclude(cnh_validade__isnull=True)
        .filter(cnh_validade__lte=limite)
        .order_by('cnh_validade')
        .only('id', 'nome', 'cnh_validade', 'posto_trabalho')
    )
    alertas_cnv = (
        ativos
        .exclude(cnv_validade__isnull=True)
        .filter(cnv_validade__lte=limite)
        .order_by('cnv_validade')
        .only('id', 'nome', 'cnv_validade', 'posto_trabalho')
    )
    alertas_curso = (
        ativos
        .exclude(curso_validade__isnull=True)
        .filter(curso_validade__lte=limite)
        .order_by('curso_validade')
        .only('id', 'nome', 'curso', 'curso_validade', 'posto_trabalho')
    )

    total        = FuncionarioPatrimonial.objects.count()
    total_ativos = ativos.count()
    total_afastados = FuncionarioPatrimonial.objects.filter(status='afastado').count()
    total_alertas = (
        ativos.filter(
            Q(cnh_validade__lte=limite, cnh_validade__isnull=False)
            | Q(cnv_validade__lte=limite, cnv_validade__isnull=False)
            | Q(curso_validade__lte=limite, curso_validade__isnull=False)
        ).distinct().count()
    )

    return render(request, 'cadastros/patrimonial_dashboard.html', {
        'hoje':             hoje,
        'alertas_cnh':      alertas_cnh,
        'alertas_cnv':      alertas_cnv,
        'alertas_curso':    alertas_curso,
        'total':            total,
        'total_ativos':     total_ativos,
        'total_afastados':  total_afastados,
        'total_alertas':    total_alertas,
    })


@login_required
def funcionario_patrimonial_list(request):
    q = request.GET.get('q', '').strip()
    tipo = request.GET.get('tipo', '').strip()
    status_filtro = request.GET.get('status', '').strip()

    qs = FuncionarioPatrimonial.objects.all()

    if q:
        qs = qs.filter(
            Q(nome__icontains=q)
            | Q(cpf__icontains=q)
            | Q(rg__icontains=q)
            | Q(posto_trabalho__icontains=q)
        )
    if tipo in ('vigilante', 'porteiro'):
        qs = qs.filter(tipo=tipo)
    if status_filtro in ('ativo', 'afastado', 'inativo'):
        qs = qs.filter(status=status_filtro)

    context = {
        'funcionarios': qs,
        'q': q,
        'tipo': tipo,
        'status_filtro': status_filtro,
        'total': qs.count(),
    }
    return render(request, 'cadastros/funcionario_patrimonial_list.html', context)


@login_required
def funcionario_patrimonial_create(request):
    form = FuncionarioPatrimonialForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Funcionario cadastrado com sucesso!')
        return redirect('funcionario_patrimonial_list')
    return render(request, 'cadastros/funcionario_patrimonial_form.html', {
        'form': form,
        'titulo': 'Novo Funcionario Patrimonial',
    })


@login_required
def funcionario_patrimonial_edit(request, pk):
    func = get_object_or_404(FuncionarioPatrimonial, pk=pk)
    form = FuncionarioPatrimonialForm(request.POST or None, request.FILES or None, instance=func)
    if form.is_valid():
        form.save()
        messages.success(request, 'Funcionario atualizado com sucesso!')
        return redirect('funcionario_patrimonial_list')
    return render(request, 'cadastros/funcionario_patrimonial_form.html', {
        'form': form,
        'titulo': 'Editar Funcionario Patrimonial',
        'obj': func,
    })


@login_required
def funcionario_patrimonial_detail(request, pk):
    func = get_object_or_404(FuncionarioPatrimonial, pk=pk)
    return render(request, 'cadastros/funcionario_patrimonial_detail.html', {'obj': func})


@login_required
def funcionario_patrimonial_delete(request, pk):
    func = get_object_or_404(FuncionarioPatrimonial, pk=pk)
    if request.method == 'POST':
        func.delete()
        messages.success(request, 'Funcionario removido.')
        return redirect('funcionario_patrimonial_list')
    return render(request, 'cadastros/confirm_delete.html', {
        'obj': func,
        'tipo': 'Funcionario Patrimonial',
    })

