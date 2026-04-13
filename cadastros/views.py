from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Agente, Viatura, Rastreador, Armamento, Cliente, Colete, Equipe
from .forms import AgenteForm, ViaturaForm, RastreadorForm, ArmamentoForm, ClienteForm


@login_required
def dashboard(request):
    context = {
        'total_agentes': Agente.objects.filter(status='ativo').count(),
        'total_viaturas': Viatura.objects.filter(status='ativa').count(),
        'total_clientes': Cliente.objects.count(),
        'total_armamentos': Armamento.objects.count(),
        'agentes_recentes': Agente.objects.order_by('-criado_em')[:5],
        'viaturas': Viatura.objects.order_by('-criado_em')[:5],
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
    clientes = Cliente.objects.all()
    if q:
        clientes = clientes.filter(Q(razao_social__icontains=q) | Q(cnpj__icontains=q))
    return render(request, 'cadastros/cliente_list.html', {'clientes': clientes, 'q': q})


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
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente removido.')
        return redirect('cliente_list')
    return render(request, 'cadastros/confirm_delete.html', {'obj': cliente, 'tipo': 'Cliente'})


@login_required
def cliente_inativar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.ativo = not cliente.ativo
        cliente.save()
        status = 'reativado' if cliente.ativo else 'inativado'
        messages.success(request, f'Cliente {status} com sucesso!')
        return redirect('cliente_list')
    return render(request, 'cadastros/confirm_delete.html', {
        'obj': cliente,
        'tipo': 'Cliente',
        'acao': 'Reativar' if not cliente.ativo else 'Inativar',
        'mensagem': f'Deseja {"reativar" if not cliente.ativo else "inativar"} o cliente "{cliente}"?',
    })


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
    q = request.GET.get('q', '')
    ordens = OrdemServico.objects.select_related('cliente', 'equipe').all()
    if q:
        ordens = ordens.filter(
            Q(numero__icontains=q) |
            Q(cliente__razao_social__icontains=q) |
            Q(solicitante__icontains=q)
        )
    return render(request, 'cadastros/os_list.html', {'ordens': ordens, 'q': q})


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
        request.session['os_draft'] = {
            'cliente_id':        request.POST.get('cliente'),
            'solicitante':       request.POST.get('solicitante', ''),
            'forma_solicitacao': request.POST.get('forma_solicitacao'),
            'tipo_viagem':       request.POST.get('tipo_viagem'),
            'previsao_inicio':   request.POST.get('previsao_inicio'),
            'previsao_retorno':  request.POST.get('previsao_retorno', ''),
            'imediata':          request.POST.get('imediata', ''),
            'cidade_origem':     request.POST.get('cidade_origem', ''),
            'uf_origem':         request.POST.get('uf_origem', 'GO'),
            'cidade_destino':    request.POST.get('cidade_destino', ''),
            'uf_destino':        request.POST.get('uf_destino', 'GO'),
        }
        return redirect('os_detalhe_novo')
    return render(request, 'cadastros/os_nova.html', {'clientes': clientes, 'ufs': UFS})


@login_required
def os_detalhe_novo(request):
    """Passo 2 — detalhe completo da OS com equipe"""
    draft = request.session.get('os_draft')
    if not draft:
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
            del request.session['os_draft']
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

    return render(request, 'cadastros/os_detalhe.html', {
        'os': os,
        'clientes': clientes,
        'equipes': equipes,
        'ufs': UFS,
        'novo': False,
        'forma_choices': OrdemServico.FORMA_CHOICES,
        'operacional': getattr(os, 'operacional', None),
        'op': getattr(os, 'operacional', None),
        'veiculos': veiculos_qs,
        'veiculo_slots': veiculo_slots,
    })


@login_required
def os_delete(request, pk):
    os = get_object_or_404(OrdemServico, pk=pk)
    if request.method == 'POST':
        os.delete()
        messages.success(request, 'OS removida.')
        return redirect('os_list')
    return render(request, 'cadastros/confirm_delete.html', {'obj': os, 'tipo': 'Ordem de Serviço'})


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
    op, _ = OSOperacional.objects.get_or_create(os=os_obj)
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
    # Pedágio
    pedagio_val = request.POST.get('pedagio', '').strip().replace(',', '.')
    try:
        op.pedagio = float(pedagio_val) if pedagio_val else None
    except ValueError:
        op.pedagio = None
    op.save()

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

    status_atual = os_obj.status
    if status_atual != 'cancelada':
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

    status_atual = os_obj.status
    if status_atual != 'cancelada':
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
    return render(request, 'cadastros/os_print.html', {
        'os': os_obj, 'op': op, 'rastreador_viatura': rastreador_viatura
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
def boletim_list(request):
    from datetime import datetime
    q = request.GET.get('q', '')
    status_filtro = request.GET.get('status', '')
    clientes_filtro = request.GET.getlist('clientes')
    data_ini = request.GET.get('data_ini', '')
    data_fim = request.GET.get('data_fim', '')
    # Criar boletins automaticamente para OS finalizadas que ainda nao tem boletim
    os_sem_boletim = OrdemServico.objects.filter(status='finalizada').exclude(boletim__isnull=False)
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

    # Agentes (snapshot)
    agentes_parts = []
    if os_obj.snap_agente1_nome:
        agentes_parts.append(os_obj.snap_agente1_nome)
    if os_obj.snap_agente2_nome:
        agentes_parts.append(os_obj.snap_agente2_nome)
    agentes_str = ' / '.join(agentes_parts) if agentes_parts else '---'

    # Viatura (snapshot)
    viatura_str = os_obj.snap_viatura_placa or '---'

    # Veículos escoltados (placas)
    veiculos = os_obj.veiculos.all()
    escoltados = ', '.join(
        v.placa_cavalo for v in veiculos if v.placa_cavalo
    ) or '---'

    def fmt_dt(d):
        return d.strftime('%d/%m/%y %H:%M') if d else '---'

    return {
        'n':          str(idx).zfill(3),
        'os':         os_obj.numero,
        'agentes':    agentes_str,
        'origem':     f"{os_obj.cidade_origem}/{os_obj.uf_origem}",
        'destino':    f"{os_obj.cidade_destino}/{os_obj.uf_destino}",
        'viatura':    viatura_str,
        'escoltado':  escoltados,
        # Datas corretas conforme marcos operacionais
        'programada': fmt_dt(os_obj.previsao_inicio),
        'chegada':    fmt_dt(op.chegada_operacao if op else None),
        'inicio':     fmt_dt(op.inicio_operacao if op else None),
        'termino':    fmt_dt(op.termino_operacao if op else None),
        'total_h':    b.horas_realizadas or '00:00',
        'franq_h':    str(tab.franquia_horas) if tab else '00:00',
        'exced_h':    b.horas_excedentes or '00:00',
        'total_km':   b.km_realizado or 0,
        'franq_km':   tab.franquia_km if tab else 0,
        'exced_km':   b.km_excedente or 0,
        'desloc':     (op.km_trecho_chegada if op else 0) or 0,
        'hr_exc':     float(b.valor_excedente_hora),
        'km_exc':     float(b.valor_excedente_km),
        'escolta':    float(b.valor_escolta),
        'desloc_val': 0.0,
        'pedagio':    float(b.valor_pedagio),
        'total':      float(b.valor_total),
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
        total        += b.valor_total

    return {
        'missoes':   len(boletins_list),
        'total_h':   min_to_hhmm(total_hr_min),
        'exced_h':   min_to_hhmm(exced_hr_min),
        'total_km':  total_km,
        'exced_km':  exced_km,
        'desloc_km': desloc_km,
        'hr_exc':    float(hr_exc),
        'km_exc':    float(km_exc),
        'escolta':   float(escolta),
        'desloc_val':0.0,
        'pedagio':   float(pedagio),
        'total':     float(total),
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


# ── LINK EXTERNO DO AGENTE DE CAMPO ──────────────────────────────────────────

def os_field_link(request, token):
    """Página pública para agente externo preencher dados operacionais da OS."""
    from datetime import datetime
    from .models import FotoMarco, Parada, FotoParada, Incidente, FotoIncidente, \
        FotoVeiculoEscoltado, AssinaturaOS
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

        def parse_dec(val):
            try:
                return float(val) if val and val.strip() else None
            except (ValueError, TypeError):
                return None

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
        op.save()

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

    def fmt_dt(val):
        if not val:
            return ''
        try:
            import pytz
            from django.conf import settings as dj_settings
            tz = pytz.timezone(dj_settings.TIME_ZONE)
            if hasattr(val, 'astimezone'):
                val = val.astimezone(tz)
            return val.strftime('%Y-%m-%dT%H:%M')
        except Exception:
            return str(val)[:16]

    def fmt_gps(lat, lng):
        if lat and lng:
            return f'https://www.google.com/maps?q={lat},{lng}'
        return ''

    MARCOS_LISTA = [
        ('inicio_viagem',    'Início de Viagem'),
        ('chegada_operacao', 'Chegada Operação'),
        ('inicio_operacao',  'Início Operação'),
        ('termino_operacao', 'Término Operação'),
        ('termino_viagem',   'Término de Viagem'),
    ]

    from .models import FotoMarco, Parada, Incidente, FotoVeiculoEscoltado, AssinaturaOS
    fotos_marco = {}
    for marco_key, _ in MARCOS_LISTA:
        foto_qs = FotoMarco.objects.filter(os=os_obj, marco=marco_key).first()
        if foto_qs:
            fotos_marco[marco_key] = foto_qs.foto.url

    paradas    = Parada.objects.filter(os=os_obj).prefetch_related('fotos')
    incidentes = Incidente.objects.filter(os=os_obj).prefetch_related('fotos')
    veiculos_campo = VeiculoEscoltado.objects.filter(os=os_obj).prefetch_related('fotos')

    assinatura_tipos = AssinaturaOS.TIPO_CHOICES if hasattr(AssinaturaOS, 'TIPO_CHOICES') else [
        ('agente1', 'Agente 1'), ('agente2', 'Agente 2'),
        ('motorista', 'Motorista'), ('supervisor', 'Supervisor'),
    ]
    assinaturas_dict = {a.tipo: a for a in AssinaturaOS.objects.filter(os=os_obj)}

    return render(request, 'cadastros/os_field_link.html', {
        'os':            os_obj,
        'op':            op,
        'sucesso':       sucesso,
        'erro':          erro,
        'fmt': {
            'inicio_viagem':    fmt_dt(op.inicio_viagem),
            'chegada_operacao': fmt_dt(op.chegada_operacao),
            'inicio_operacao':  fmt_dt(op.inicio_operacao),
            'termino_operacao': fmt_dt(op.termino_operacao),
            'termino_viagem':   fmt_dt(op.termino_viagem),
        },
        'gps': {
            'inicio_viagem':    fmt_gps(op.gps_inicio_viagem_lat,    op.gps_inicio_viagem_lng),
            'chegada_operacao': fmt_gps(op.gps_chegada_operacao_lat, op.gps_chegada_operacao_lng),
            'inicio_operacao':  fmt_gps(op.gps_inicio_operacao_lat,  op.gps_inicio_operacao_lng),
            'termino_operacao': fmt_gps(op.gps_termino_operacao_lat, op.gps_termino_operacao_lng),
            'termino_viagem':   fmt_gps(op.gps_termino_viagem_lat,   op.gps_termino_viagem_lng),
        },
        'fotos_marco':       fotos_marco,
        'fotos_marco_lista': MARCOS_LISTA,
        'paradas':           paradas,
        'incidentes':        incidentes,
        'veiculos_campo':    veiculos_campo,
        'assinatura_tipos':  assinatura_tipos,
        'assinaturas_dict':  assinaturas_dict,
    })


@login_required
def os_gerar_link(request, pk):
    """Garante que existe um OSOperacional com token e retorna JSON com o link."""
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


# ── FOTOS DOS MARCOS ──────────────────────────────────────────────────────────

def os_field_foto_marco_upload(request, token, marco):
    """Recebe upload de foto de marco via AJAX."""
    from .models import FotoMarco
    op = get_object_or_404(OSOperacional, token=token)
    if not op.link_ativo:
        return JsonResponse({'ok': False, 'erro': 'Link inativo.'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'erro': 'Método inválido.'}, status=405)
    foto = request.FILES.get('foto')
    if not foto:
        return JsonResponse({'ok': False, 'erro': 'Nenhuma foto enviada.'}, status=400)

    substituida = False
    obj_existente = FotoMarco.objects.filter(os=op.os, marco=marco).first()
    if obj_existente:
        obj_existente.foto.delete(save=False)
        obj_existente.delete()
        substituida = True

    obj = FotoMarco.objects.create(os=op.os, marco=marco, foto=foto)
    return JsonResponse({
        'ok':          True,
        'url':         obj.foto.url,
        'marco':       marco,
        'substituida': substituida,
    })


def os_field_foto_marco_delete(request, token, foto_pk):
    """Remove uma foto de marco."""
    from .models import FotoMarco
    op  = get_object_or_404(OSOperacional, token=token)
    obj = get_object_or_404(FotoMarco, pk=foto_pk, os=op.os)
    if request.method == 'POST':
        obj.foto.delete(save=False)
        obj.delete()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False, 'erro': 'Método inválido.'}, status=405)


# ── PARADAS ───────────────────────────────────────────────────────────────────

def os_field_parada_salvar(request, token):
    """Cria ou edita uma Parada via AJAX."""
    from .models import Parada
    from datetime import datetime
    op = get_object_or_404(OSOperacional, token=token)
    if not op.link_ativo:
        return JsonResponse({'ok': False, 'erro': 'Link inativo.'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'erro': 'Método inválido.'}, status=405)

    def parse_dt(val):
        if not val:
            return None
        for fmt in ('%Y-%m-%dT%H:%M', '%d/%m/%Y %H:%M', '%Y-%m-%d %H:%M'):
            try:
                return datetime.strptime(val, fmt)
            except ValueError:
                continue
        return None

    pk_val  = request.POST.get('pk') or None
    cidade  = request.POST.get('cidade', '').strip()
    motivo  = request.POST.get('motivo', '').strip()
    chegada = parse_dt(request.POST.get('chegada'))
    saida   = parse_dt(request.POST.get('saida'))

    if pk_val:
        obj = get_object_or_404(Parada, pk=pk_val, os=op.os)
        obj.cidade  = cidade
        obj.motivo  = motivo
        obj.chegada = chegada
        obj.saida   = saida
        obj.save()
    else:
        obj = Parada.objects.create(
            os=op.os, cidade=cidade, motivo=motivo,
            chegada=chegada, saida=saida,
        )
    return JsonResponse({'ok': True, 'pk': obj.pk})


def os_field_parada_delete(request, token, pk):
    """Deleta uma Parada via AJAX."""
    from .models import Parada
    op  = get_object_or_404(OSOperacional, token=token)
    if not op.link_ativo:
        return JsonResponse({'ok': False, 'erro': 'Link inativo.'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'erro': 'Método inválido.'}, status=405)
    obj = get_object_or_404(Parada, pk=pk, os=op.os)
    obj.delete()
    return JsonResponse({'ok': True})


def os_field_foto_parada_upload(request, token, parada_pk):
    """Upload de foto de parada via AJAX."""
    from .models import FotoParada, Parada
    op     = get_object_or_404(OSOperacional, token=token)
    parada = get_object_or_404(Parada, pk=parada_pk, os=op.os)
    if not op.link_ativo:
        return JsonResponse({'ok': False, 'erro': 'Link inativo.'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'erro': 'Método inválido.'}, status=405)
    foto = request.FILES.get('foto')
    if not foto:
        return JsonResponse({'ok': False, 'erro': 'Nenhuma foto enviada.'}, status=400)
    obj = FotoParada.objects.create(parada=parada, foto=foto)
    return JsonResponse({'ok': True, 'url': obj.foto.url, 'pk': obj.pk})


def os_field_foto_parada_delete(request, token, foto_pk):
    """Remove foto de parada via AJAX."""
    from .models import FotoParada
    op  = get_object_or_404(OSOperacional, token=token)
    obj = get_object_or_404(FotoParada, pk=foto_pk, parada__os=op.os)
    if request.method == 'POST':
        obj.foto.delete(save=False)
        obj.delete()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False, 'erro': 'Método inválido.'}, status=405)


# ── INCIDENTES ────────────────────────────────────────────────────────────────

def os_field_incidente_salvar(request, token):
    """Cria ou edita um Incidente via AJAX."""
    from .models import Incidente
    from datetime import datetime
    op = get_object_or_404(OSOperacional, token=token)
    if not op.link_ativo:
        return JsonResponse({'ok': False, 'erro': 'Link inativo.'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'erro': 'Método inválido.'}, status=405)

    def parse_dt(val):
        if not val:
            return None
        for fmt in ('%Y-%m-%dT%H:%M', '%d/%m/%Y %H:%M', '%Y-%m-%d %H:%M'):
            try:
                return datetime.strptime(val, fmt)
            except ValueError:
                continue
        return None

    pk_val      = request.POST.get('pk') or None
    tipo        = request.POST.get('tipo', '').strip()
    descricao   = request.POST.get('descricao', '').strip()
    ocorrido_em = parse_dt(request.POST.get('ocorrido_em'))

    if pk_val:
        obj = get_object_or_404(Incidente, pk=pk_val, os=op.os)
        obj.tipo        = tipo
        obj.descricao   = descricao
        obj.ocorrido_em = ocorrido_em
        obj.save()
    else:
        obj = Incidente.objects.create(
            os=op.os, tipo=tipo,
            descricao=descricao, ocorrido_em=ocorrido_em,
        )
    return JsonResponse({'ok': True, 'pk': obj.pk})


def os_field_incidente_delete(request, token, pk):
    """Deleta um Incidente via AJAX."""
    from .models import Incidente
    op  = get_object_or_404(OSOperacional, token=token)
    if not op.link_ativo:
        return JsonResponse({'ok': False, 'erro': 'Link inativo.'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'erro': 'Método inválido.'}, status=405)
    obj = get_object_or_404(Incidente, pk=pk, os=op.os)
    obj.delete()
    return JsonResponse({'ok': True})


def os_field_foto_incidente_upload(request, token, incidente_pk):
    """Upload de foto de incidente via AJAX."""
    from .models import FotoIncidente, Incidente
    op        = get_object_or_404(OSOperacional, token=token)
    incidente = get_object_or_404(Incidente, pk=incidente_pk, os=op.os)
    if not op.link_ativo:
        return JsonResponse({'ok': False, 'erro': 'Link inativo.'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'erro': 'Método inválido.'}, status=405)
    foto = request.FILES.get('foto')
    if not foto:
        return JsonResponse({'ok': False, 'erro': 'Nenhuma foto enviada.'}, status=400)
    obj = FotoIncidente.objects.create(incidente=incidente, foto=foto)
    return JsonResponse({'ok': True, 'url': obj.foto.url, 'pk': obj.pk})


def os_field_foto_incidente_delete(request, token, foto_pk):
    """Remove foto de incidente via AJAX."""
    from .models import FotoIncidente
    op  = get_object_or_404(OSOperacional, token=token)
    obj = get_object_or_404(FotoIncidente, pk=foto_pk, incidente__os=op.os)
    if request.method == 'POST':
        obj.foto.delete(save=False)
        obj.delete()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False, 'erro': 'Método inválido.'}, status=405)


# ── VEÍCULOS ESCOLTADOS (campo) ───────────────────────────────────────────────

def os_field_veiculo_salvar(request, token):
    """Cria ou edita um VeiculoEscoltado via AJAX (link externo do agente)."""
    op = get_object_or_404(OSOperacional, token=token)
    if not op.link_ativo:
        return JsonResponse({'ok': False, 'erro': 'Link inativo.'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'erro': 'Método inválido.'}, status=405)

    pk_val      = request.POST.get('pk') or None
    veiculo     = request.POST.get('veiculo', '').strip()
    placa_cav   = request.POST.get('placa_cavalo', '').strip().upper()
    placa_car   = request.POST.get('placa_carreta', '').strip().upper()
    placa_car2  = request.POST.get('placa_carreta2', '').strip().upper()
    motorista   = request.POST.get('motorista', '').strip()

    if pk_val:
        obj = get_object_or_404(VeiculoEscoltado, pk=pk_val, os=op.os)
        obj.veiculo        = veiculo
        obj.placa_cavalo   = placa_cav
        obj.placa_carreta  = placa_car
        obj.placa_carreta2 = placa_car2
        obj.motorista      = motorista
        obj.save()
    else:
        max_ordem = VeiculoEscoltado.objects.filter(os=op.os).count()
        obj = VeiculoEscoltado.objects.create(
            os=op.os,
            ordem=max_ordem + 1,
            veiculo=veiculo,
            placa_cavalo=placa_cav,
            placa_carreta=placa_car,
            placa_carreta2=placa_car2,
            motorista=motorista,
        )
    return JsonResponse({'ok': True, 'pk': obj.pk})


def os_field_veiculo_foto_upload(request, token, veiculo_pk):
    """Upload de foto de veículo escoltado via AJAX."""
    from .models import FotoVeiculoEscoltado
    op      = get_object_or_404(OSOperacional, token=token)
    veiculo = get_object_or_404(VeiculoEscoltado, pk=veiculo_pk, os=op.os)
    if not op.link_ativo:
        return JsonResponse({'ok': False, 'erro': 'Link inativo.'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'erro': 'Método inválido.'}, status=405)
    foto    = request.FILES.get('foto')
    momento = request.POST.get('momento', 'antes')
    if not foto:
        return JsonResponse({'ok': False, 'erro': 'Nenhuma foto enviada.'}, status=400)
    obj = FotoVeiculoEscoltado.objects.create(veiculo=veiculo, momento=momento, foto=foto)
    return JsonResponse({'ok': True, 'url': obj.foto.url, 'pk': obj.pk})


def os_field_foto_veiculo_delete(request, token, foto_pk):
    """Remove foto de veículo escoltado via AJAX."""
    from .models import FotoVeiculoEscoltado
    op  = get_object_or_404(OSOperacional, token=token)
    obj = get_object_or_404(FotoVeiculoEscoltado, pk=foto_pk, veiculo__os=op.os)
    if request.method == 'POST':
        obj.foto.delete(save=False)
        obj.delete()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False, 'erro': 'Método inválido.'}, status=405)


def os_field_veiculo_delete(request, token, pk):
    """Deleta um VeiculoEscoltado via AJAX (link externo do agente)."""
    op = get_object_or_404(OSOperacional, token=token)
    if not op.link_ativo:
        return JsonResponse({'ok': False, 'erro': 'Link inativo.'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'erro': 'Método inválido.'}, status=405)
    obj = get_object_or_404(VeiculoEscoltado, pk=pk, os=op.os)
    obj.delete()
    return JsonResponse({'ok': True})


# ── os_detalhe: adiciona 'op' no contexto ────────────────────────────────────
# NOTA: a view os_detalhe acima já passa 'operacional', mas o template usa 'op'.
# O fix foi aplicado diretamente na view os_detalhe — certifique-se de que o
# contexto contém: 'op': getattr(os, 'operacional', None)



# ── USUÁRIOS ──────────────────────────────────────────────────────────────────

@login_required
def usuario_list(request):
    from django.contrib.auth.models import User
    usuarios = User.objects.all().order_by('username')
    return render(request, 'cadastros/usuario_list.html', {'usuarios': usuarios})


@login_required
def usuario_create(request):
    from django.contrib.auth.models import User
    from django.contrib.auth.forms import UserCreationForm
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email    = request.POST.get('email', '').strip()
        password = request.POST.get('password1', '')
        is_staff = bool(request.POST.get('is_staff'))
        erros = []
        if not username:
            erros.append('Nome de usuário é obrigatório.')
        if User.objects.filter(username=username).exists():
            erros.append('Nome de usuário já existe.')
        if not password:
            erros.append('Senha é obrigatória.')
        if erros:
            return render(request, 'cadastros/usuario_form.html', {'erros': erros, 'values': request.POST})
        u = User.objects.create_user(username=username, email=email, password=password)
        u.is_staff = is_staff
        u.save()
        messages.success(request, f'Usuário {username} criado com sucesso.')
        return redirect('usuario_list')
    return render(request, 'cadastros/usuario_form.html', {})


@login_required
def usuario_edit(request, pk):
    from django.contrib.auth.models import User
    u = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        u.username = request.POST.get('username', u.username).strip()
        u.email    = request.POST.get('email', u.email).strip()
        u.is_staff = bool(request.POST.get('is_staff'))
        u.save()
        messages.success(request, 'Usuário atualizado.')
        return redirect('usuario_list')
    return render(request, 'cadastros/usuario_form.html', {'usuario': u})


@login_required
def usuario_senha(request, pk):
    from django.contrib.auth.models import User
    u = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        senha = request.POST.get('password1', '')
        if senha:
            u.set_password(senha)
            u.save()
            messages.success(request, 'Senha alterada com sucesso.')
        else:
            messages.error(request, 'Senha não pode ser vazia.')
        return redirect('usuario_list')
    return render(request, 'cadastros/usuario_senha_form.html', {'usuario': u})


@login_required
def usuario_delete(request, pk):
    from django.contrib.auth.models import User
    u = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        u.delete()
        messages.success(request, 'Usuário removido.')
        return redirect('usuario_list')
    return render(request, 'cadastros/confirm_delete.html', {'obj': u, 'tipo': 'Usuário'})


# ── ALIASES para compatibilidade com urls.py ──────────────────────────────────

def os_field_foto_marco(request, token):
    """Alias — o urls.py usa este nome para upload de foto de marco."""
    marco = request.POST.get('marco') or request.GET.get('marco', '')
    return os_field_foto_marco_upload(request, token, marco)


def os_field_foto_veiculo(request, token):
    """Alias — o urls.py usa este nome para upload de foto de veículo."""
    veiculo_pk = request.POST.get('veiculo_pk') or request.GET.get('veiculo_pk')
    return os_field_veiculo_foto_upload(request, token, veiculo_pk)


# ── TROCA DE MOTORISTAS ───────────────────────────────────────────────────────

def os_field_troca_motorista(request, token):
    """Cria ou edita uma TrocaMotorista via AJAX."""
    from .models import TrocaMotorista
    from datetime import datetime
    op = get_object_or_404(OSOperacional, token=token)
    if not op.link_ativo:
        return JsonResponse({'ok': False, 'erro': 'Link inativo.'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'erro': 'Método inválido.'}, status=405)

    def parse_dt(val):
        if not val:
            return None
        for fmt in ('%Y-%m-%dT%H:%M', '%d/%m/%Y %H:%M', '%Y-%m-%d %H:%M'):
            try:
                return datetime.strptime(val, fmt)
            except ValueError:
                continue
        return None

    pk_val        = request.POST.get('pk') or None
    motorista_ant = request.POST.get('motorista_anterior', '').strip()
    motorista_nov = request.POST.get('motorista_novo', '').strip()
    ocorrido_em   = parse_dt(request.POST.get('ocorrido_em'))
    motivo        = request.POST.get('motivo', '').strip()

    if pk_val:
        obj = get_object_or_404(TrocaMotorista, pk=pk_val, os=op.os)
        obj.motorista_anterior = motorista_ant
        obj.motorista_novo     = motorista_nov
        obj.ocorrido_em        = ocorrido_em
        obj.motivo             = motivo
        obj.save()
    else:
        obj = TrocaMotorista.objects.create(
            os=op.os,
            motorista_anterior=motorista_ant,
            motorista_novo=motorista_nov,
            ocorrido_em=ocorrido_em,
            motivo=motivo,
        )
    return JsonResponse({'ok': True, 'pk': obj.pk})


def os_field_troca_motorista_delete(request, token, pk):
    """Deleta uma TrocaMotorista via AJAX."""
    from .models import TrocaMotorista
    op  = get_object_or_404(OSOperacional, token=token)
    if not op.link_ativo:
        return JsonResponse({'ok': False, 'erro': 'Link inativo.'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'erro': 'Método inválido.'}, status=405)
    obj = get_object_or_404(TrocaMotorista, pk=pk, os=op.os)
    obj.delete()
    return JsonResponse({'ok': True})


# ── ASSINATURAS DIGITAIS ──────────────────────────────────────────────────────

def os_field_assinatura(request, token):
    """Salva assinatura digital (base64 PNG) via AJAX."""
    from .models import AssinaturaOS
    import base64
    from django.core.files.base import ContentFile
    op = get_object_or_404(OSOperacional, token=token)
    if not op.link_ativo:
        return JsonResponse({'ok': False, 'erro': 'Link inativo.'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'erro': 'Método inválido.'}, status=405)

    tipo      = request.POST.get('tipo', '').strip()
    nome      = request.POST.get('nome', '').strip()
    dados_b64 = request.POST.get('assinatura', '')

    if not tipo or not dados_b64:
        return JsonResponse({'ok': False, 'erro': 'Tipo e assinatura são obrigatórios.'}, status=400)

    try:
        if ',' in dados_b64:
            dados_b64 = dados_b64.split(',', 1)[1]
        img_bytes = base64.b64decode(dados_b64)
        img_file  = ContentFile(img_bytes, name=f'assinatura_{tipo}.png')
    except Exception:
        return JsonResponse({'ok': False, 'erro': 'Dados de assinatura inválidos.'}, status=400)

    obj, _ = AssinaturaOS.objects.get_or_create(os=op.os, tipo=tipo)
    obj.nome = nome
    obj.assinatura.save(f'assinatura_{tipo}.png', img_file, save=True)
    return JsonResponse({'ok': True, 'url': obj.assinatura.url})


# ── DESPESAS / CRÉDITOS ───────────────────────────────────────────────────────

def os_field_despesa_salvar(request, token):
    """Cria ou edita uma DespesaOS via AJAX."""
    from .models import DespesaOS
    op = get_object_or_404(OSOperacional, token=token)
    if not op.link_ativo:
        return JsonResponse({'ok': False, 'erro': 'Link inativo.'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'erro': 'Método inválido.'}, status=405)

    pk_val    = request.POST.get('pk') or None
    tipo      = request.POST.get('tipo', '').strip()
    descricao = request.POST.get('descricao', '').strip()
    valor_str = request.POST.get('valor', '').strip().replace(',', '.')
    try:
        valor = float(valor_str) if valor_str else 0
    except ValueError:
        valor = 0

    if pk_val:
        obj = get_object_or_404(DespesaOS, pk=pk_val, os=op.os)
        obj.tipo      = tipo
        obj.descricao = descricao
        obj.valor     = valor
        obj.save()
    else:
        obj = DespesaOS.objects.create(
            os=op.os, tipo=tipo, descricao=descricao, valor=valor,
        )
    return JsonResponse({'ok': True, 'pk': obj.pk})


def os_field_despesa_delete(request, token, pk):
    """Deleta uma DespesaOS via AJAX."""
    from .models import DespesaOS
    op  = get_object_or_404(OSOperacional, token=token)
    if not op.link_ativo:
        return JsonResponse({'ok': False, 'erro': 'Link inativo.'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'erro': 'Método inválido.'}, status=405)
    obj = get_object_or_404(DespesaOS, pk=pk, os=op.os)
    obj.delete()
    return JsonResponse({'ok': True})

