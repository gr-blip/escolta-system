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
    if form.is_valid():
        form.save()
        messages.success(request, 'Viatura cadastrada com sucesso!')
        return redirect('viatura_list')
    return render(request, 'cadastros/viatura_form.html', {'form': form, 'titulo': 'Nova Viatura'})


@login_required
def viatura_edit(request, pk):
    viatura = get_object_or_404(Viatura, pk=pk)
    form = ViaturaForm(request.POST or None, instance=viatura)
    if form.is_valid():
        form.save()
        messages.success(request, 'Viatura atualizada com sucesso!')
        return redirect('viatura_list')
    return render(request, 'cadastros/viatura_form.html', {'form': form, 'titulo': 'Editar Viatura', 'obj': viatura})


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
        os_obj.save(update_fields=['status', 'finalizada_em'])
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
    return render(request, 'cadastros/os_print.html', {'os': os_obj, 'op': op})



# ══════════════════════════════════════════════════════════════════════════════
# FATURAMENTO — Tabela de Preços
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
                try: return float((v or d).replace(',','.')) 
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
            messages.success(request, 'Tabela de preço criada com sucesso!')
            return redirect('tabela_preco_list')
        except Exception as e:
            messages.error(request, f'Erro: {e}')
    return render(request, 'cadastros/tabela_preco_form.html', {'clientes': clientes, 'titulo': 'Nova Tabela de Preço'})


@login_required
def tabela_preco_edit(request, pk):
    tabela = get_object_or_404(TabelaPreco, pk=pk)
    clientes = Cliente.objects.all().order_by('razao_social')
    if request.method == 'POST':
        try:
            def dec(v, d='0'): 
                try: return float((v or d).replace(',','.')) 
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
        'tabela': tabela, 'clientes': clientes, 'titulo': 'Editar Tabela de Preço'
    })


@login_required
def tabela_preco_delete(request, pk):
    tabela = get_object_or_404(TabelaPreco, pk=pk)
    if request.method == 'POST':
        tabela.delete()
        messages.success(request, 'Tabela removida.')
        return redirect('tabela_preco_list')
    return render(request, 'cadastros/confirm_delete.html', {'obj': tabela, 'tipo': 'Tabela de Preço'})


# ── Boletim de Medição ────────────────────────────────────────────────────────

@login_required
def boletim_list(request):
    q = request.GET.get('q', '')
    status_filtro = request.GET.get('status', '')
    boletins = BoletimMedicao.objects.select_related('os', 'os__cliente', 'os__equipe', 'tabela_preco').all()
    # OS finalizadas sem boletim — criar automaticamente
    os_finalizadas_sem_boletim = OrdemServico.objects.filter(
        status='finalizada'
    ).exclude(boletim__isnull=False)
    for os_obj in os_finalizadas_sem_boletim:
        BoletimMedicao.objects.get_or_create(os=os_obj)
    # Recarregar após criação automática
    boletins = BoletimMedicao.objects.select_related('os', 'os__cliente', 'os__equipe', 'tabela_preco').all()
    if q:
        boletins = boletins.filter(
            Q(os__numero__icontains=q) |
            Q(os__cliente__razao_social__icontains=q) |
            Q(os__solicitante__icontains=q)
        )
    if status_filtro:
        boletins = boletins.filter(status=status_filtro)
    return render(request, 'cadastros/boletim_list.html', {
        'boletins': boletins, 'q': q, 'status_filtro': status_filtro
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
            messages.error(request, 'Boletim já faturado não pode ser alterado.')
            return redirect('boletim_detalhe', pk=pk)

        tabela_id = request.POST.get('tabela_preco')
        if tabela_id:
            boletim.tabela_preco_id = tabela_id
        boletim.acrescimo   = float(request.POST.get('acrescimo', 0) or 0)
        boletim.desconto    = float(request.POST.get('desconto', 0) or 0)
        boletim.numero_nota = request.POST.get('numero_nota', '')
        boletim.observacoes = request.POST.get('observacoes', '')
        action = request.POST.get('action', 'salvar')
        if action == 'calcular' and boletim.tabela_preco_id:
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

    return render(request, 'cadastros/boletim_detalhe.html', {
        'boletim': boletim, 'os': os_obj, 'op': op, 'tabelas': tabelas,
    })
