# Outras importações...
from .models_perfil import PerfilUsuario
from django.db import models


class Agente(models.Model):
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('afastado', 'Afastado'),
        ('inativo', 'Inativo'),
    ]
    FUNCAO_CHOICES = [
        ('agente_escolta', 'Agente de Escolta'),
        ('motorista_escolta', 'Motorista Escolta'),
        ('supervisor', 'Supervisor'),
        ('coordenador', 'Coordenador'),
    ]

    foto = models.ImageField(upload_to='agentes/', blank=True, null=True)
    nome = models.CharField(max_length=200, verbose_name='Nome completo')
    cpf = models.CharField(max_length=14, unique=True, verbose_name='CPF')
    rg = models.CharField(max_length=20, verbose_name='RG')
    telefone = models.CharField(max_length=20, verbose_name='Telefone / Contato')
    data_nascimento = models.DateField(blank=True, null=True, verbose_name='Data de nascimento')
    cnh = models.CharField(max_length=20, blank=True, verbose_name='CNH')
    cnh_validade = models.DateField(blank=True, null=True, verbose_name='Val. CNH')
    cnh_categoria = models.CharField(max_length=5, blank=True, default='B', verbose_name='Categoria CNH')
    cnv = models.CharField(max_length=20, blank=True, verbose_name='CNV')
    cnv_validade = models.DateField(blank=True, null=True, verbose_name='Val. CNV')
    funcao = models.CharField(max_length=30, choices=FUNCAO_CHOICES, default='agente_escolta', verbose_name='Funcao')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='ativo', verbose_name='Status')
    observacoes = models.TextField(blank=True, verbose_name='Observacoes')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Agente'
        verbose_name_plural = 'Agentes'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Viatura(models.Model):
    STATUS_CHOICES = [
        ('ativa', 'Ativa'),
        ('manutencao', 'Em manutencao'),
        ('inativa', 'Inativa'),
    ]
    TIPO_CHOICES = [
        ('VW Polo', 'VW Polo'),
        ('VW Gol', 'VW Gol'),
        ('Fiat Strada', 'Fiat Strada'),
        ('Toyota Hilux', 'Toyota Hilux'),
        ('Outro', 'Outro'),
    ]

    tipo = models.CharField(max_length=50, verbose_name='Tipo')
    marca_modelo = models.CharField(max_length=100, verbose_name='Marca / Modelo')
    ano = models.CharField(max_length=4, verbose_name='Ano')
    cor = models.CharField(max_length=50, verbose_name='Cor')
    placa = models.CharField(max_length=10, unique=True, verbose_name='Placa')
    frota = models.CharField(max_length=20, blank=True, verbose_name='Frota')
    mct_id = models.CharField(max_length=20, blank=True, verbose_name='MCT / ID')
    renavam = models.CharField(max_length=15, blank=True, verbose_name='RENAVAM')
    chassi = models.CharField(max_length=30, blank=True, verbose_name='Chassi')
    crlv_validade = models.DateField(blank=True, null=True, verbose_name='CRLV Vencimento')
    seguro_validade = models.DateField(blank=True, null=True, verbose_name='Seguro Vencimento')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='ativa', verbose_name='Status')
    observacoes = models.TextField(blank=True, verbose_name='Observacoes')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Viatura'
        verbose_name_plural = 'Viaturas'
        ordering = ['placa']

    def __str__(self):
        return f'{self.marca_modelo} - {self.placa}'


class Rastreador(models.Model):
    STATUS_CHOICES = [
        ('online', 'Ativo / Online'),
        ('offline', 'Offline'),
        ('manutencao', 'Em manutencao'),
    ]

    marca = models.CharField(max_length=100, verbose_name='Marca / Fabricante')
    modelo = models.CharField(max_length=100, verbose_name='Modelo')
    numero_serie = models.CharField(max_length=50, unique=True, verbose_name='Nr de Serie')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='online', verbose_name='Status')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Rastreador'
        verbose_name_plural = 'Rastreadores'
        ordering = ['marca', 'modelo']

    def __str__(self):
        return f'{self.marca} {self.modelo} - {self.numero_serie}'


class Armamento(models.Model):
    TIPO_CHOICES = [
        ('pistola', 'Pistola'),
        ('revolver', 'Revolver'),
        ('espingarda', 'Espingarda'),
        ('rifle', 'Rifle'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo')
    marca = models.CharField(max_length=100, verbose_name='Marca / Fabricante')
    modelo = models.CharField(max_length=100, verbose_name='Modelo')
    calibre = models.CharField(max_length=20, verbose_name='Calibre')
    numero_serie = models.CharField(max_length=50, unique=True, verbose_name='Nr de Serie')
    numero_cano = models.CharField(max_length=50, blank=True, verbose_name='Nr do Cano')
    registro_cr = models.CharField(max_length=50, blank=True, verbose_name='Registro CR/SINARM')
    registro_validade = models.DateField(blank=True, null=True, verbose_name='Val. Registro')
    data_aquisicao = models.DateField(blank=True, null=True, verbose_name='Data de Aquisicao')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Armamento'
        verbose_name_plural = 'Armamentos'
        ordering = ['tipo', 'marca']

    def __str__(self):
        return f'{self.get_tipo_display()} {self.marca} {self.modelo} - {self.numero_serie}'


class Cliente(models.Model):
    razao_social = models.CharField(max_length=200, verbose_name='Razao Social')
    cnpj = models.CharField(max_length=18, unique=True, verbose_name='CNPJ')
    inscricao_estadual = models.CharField(max_length=30, blank=True, verbose_name='IE / IM')
    endereco = models.CharField(max_length=300, blank=True, verbose_name='Endereco')
    cidade_uf = models.CharField(max_length=100, blank=True, verbose_name='Cidade / UF')
    cep = models.CharField(max_length=9, blank=True, verbose_name='CEP')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['razao_social']

    def __str__(self):
        return self.razao_social


class Equipe(models.Model):
    STATUS_CHOICES = [
        ('ativa',      'Ativa'),
        ('inativa',    'Inativa'),
        ('em_servico', 'Em Serviço'),
        ('finalizada', 'Finalizada'),
    ]

    nome             = models.CharField(max_length=100, verbose_name='Nome da Equipe')
    agente1          = models.ForeignKey('Agente',    on_delete=models.PROTECT, related_name='equipe_agente1',   verbose_name='Agente 1')
    agente2          = models.ForeignKey('Agente',    on_delete=models.PROTECT, related_name='equipe_agente2',   verbose_name='Agente 2')
    armamento_agente1= models.ForeignKey('Armamento', on_delete=models.PROTECT, related_name='equipe_arm_ag1',   verbose_name='Armamento Agente 1')
    armamento_agente2= models.ForeignKey('Armamento', on_delete=models.PROTECT, related_name='equipe_arm_ag2',   verbose_name='Armamento Agente 2')
    armamento_extra  = models.ForeignKey('Armamento', on_delete=models.SET_NULL, null=True, blank=True, related_name='equipe_arm_extra', verbose_name='Armamento Extra (Equipe)')
    colete1          = models.ForeignKey('Colete',    on_delete=models.PROTECT, related_name='equipe_colete1',   verbose_name='Colete Agente 1')
    colete2          = models.ForeignKey('Colete',    on_delete=models.PROTECT, related_name='equipe_colete2',   verbose_name='Colete Agente 2')
    viatura          = models.ForeignKey('Viatura',   on_delete=models.SET_NULL, null=True, blank=True, related_name='equipe_viatura', verbose_name='Viatura')
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativa', verbose_name='Status')
    observacoes      = models.TextField(blank=True, verbose_name='Observações')
    criado_em        = models.DateTimeField(auto_now_add=True)
    atualizado_em    = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Equipe'
        verbose_name_plural = 'Equipes'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Colete(models.Model):
    PROTECAO_CHOICES = [
        ('Nivel IIA',  'Nível IIA'),
        ('Nivel II',   'Nível II'),
        ('Nivel IIIA', 'Nível IIIA'),
        ('Nivel III',  'Nível III'),
        ('Nivel IV',   'Nível IV'),
    ]

    marca       = models.CharField(max_length=100, verbose_name='Marca')
    numeracao   = models.CharField(max_length=50,  verbose_name='Numeracao')
    protecao    = models.CharField(max_length=20, choices=PROTECAO_CHOICES, default='Nivel IIIA', verbose_name='Nivel de Protecao')
    validade    = models.DateField(verbose_name='Validade')
    criado_em   = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Colete'
        verbose_name_plural = 'Coletes'
        ordering = ['marca']

    def __str__(self):
        return f'{self.marca} - {self.numeracao} ({self.get_protecao_display()})'


class OrdemServico(models.Model):
    STATUS_CHOICES = [
        ('aberta',      'Aberta'),
        ('em_viagem',   'Em Viagem'),
        ('em_operacao', 'Em Operação'),
        ('encerrando',  'Encerrando'),
        ('concluida',   'Concluída'),
        ('finalizada',  'Finalizada'),
        ('cancelada',   'Cancelada'),
    ]
    FORMA_CHOICES = [
        ('email',    'E-mail'),
        ('telefone', 'Telefone'),
        ('whatsapp', 'WhatsApp'),
    ]
    TIPO_VIAGEM_CHOICES = [
        ('urbana',         'Urbana'),
        ('rodoviaria',     'Rodoviária'),
        ('administrativa', 'Administrativa'),
    ]

    numero          = models.CharField(max_length=20, unique=True, verbose_name='Nº OS', blank=True)
    cliente         = models.ForeignKey('Cliente',  on_delete=models.PROTECT, verbose_name='Cliente')
    solicitante     = models.CharField(max_length=200, blank=True, verbose_name='Solicitante')
    forma_solicitacao = models.CharField(max_length=20, choices=FORMA_CHOICES, verbose_name='Forma de Solicitação')
    tipo_viagem     = models.CharField(max_length=20, choices=TIPO_VIAGEM_CHOICES, verbose_name='Tipo de Viagem')
    previsao_inicio = models.DateTimeField(verbose_name='Previsão de Início')
    previsao_retorno= models.DateTimeField(blank=True, null=True, verbose_name='Previsão de Retorno')
    imediata        = models.BooleanField(default=False, verbose_name='Imediata')
    cidade_origem   = models.CharField(max_length=200, verbose_name='Cidade Origem')
    uf_origem       = models.CharField(max_length=2, default='GO', verbose_name='UF Origem')
    cidade_destino  = models.CharField(max_length=200, verbose_name='Cidade Destino')
    uf_destino      = models.CharField(max_length=2, default='GO', verbose_name='UF Destino')
    equipe          = models.ForeignKey('Equipe', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Equipe')
    # Snapshot da equipe — preservado mesmo após excluir a equipe
    snap_equipe_nome     = models.CharField(max_length=100, blank=True, verbose_name='Equipe (snapshot)')
    snap_agente1_nome    = models.CharField(max_length=200, blank=True, verbose_name='Agente 1 (snapshot)')
    snap_agente1_cpf     = models.CharField(max_length=20,  blank=True)
    snap_agente1_rg      = models.CharField(max_length=20,  blank=True)
    snap_agente1_telefone= models.CharField(max_length=20,  blank=True)
    snap_agente1_cnh     = models.CharField(max_length=20,  blank=True)
    snap_agente1_cnv     = models.CharField(max_length=20,  blank=True)
    snap_agente1_foto    = models.CharField(max_length=500, blank=True)
    snap_agente2_nome    = models.CharField(max_length=200, blank=True, verbose_name='Agente 2 (snapshot)')
    snap_agente2_cpf     = models.CharField(max_length=20,  blank=True)
    snap_agente2_rg      = models.CharField(max_length=20,  blank=True)
    snap_agente2_telefone= models.CharField(max_length=20,  blank=True)
    snap_agente2_cnh     = models.CharField(max_length=20,  blank=True)
    snap_agente2_cnv     = models.CharField(max_length=20,  blank=True)
    snap_agente2_foto    = models.CharField(max_length=500, blank=True)
    snap_viatura_modelo  = models.CharField(max_length=100, blank=True)
    snap_viatura_placa   = models.CharField(max_length=20,  blank=True)
    snap_viatura_cor     = models.CharField(max_length=50,  blank=True)
    snap_viatura_frota   = models.CharField(max_length=20,  blank=True)
    snap_viatura_mct     = models.CharField(max_length=20,  blank=True)
    observacoes     = models.TextField(blank=True, verbose_name='Observações')
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberta', verbose_name='Status')
    finalizada_em   = models.DateTimeField(null=True, blank=True, verbose_name='Finalizada em')
    criado_em       = models.DateTimeField(auto_now_add=True)
    atualizado_em   = models.DateTimeField(auto_now=True)

    @property
    def is_finalizada(self):
        return self.status == 'finalizada'

    class Meta:
        verbose_name = 'Ordem de Serviço'
        verbose_name_plural = 'Ordens de Serviço'
        ordering = ['-criado_em']

    def __str__(self):
        return f'OS-{self.numero} — {self.cliente}'

    def save(self, *args, **kwargs):
        if not self.numero:
            from django.utils import timezone
            ano = timezone.now().year
            ultimo = OrdemServico.objects.filter(numero__startswith=str(ano)).count()
            self.numero = f'{ano}{str(ultimo + 1).zfill(4)}'
        super().save(*args, **kwargs)


class OSOperacional(models.Model):
    """Dados operacionais de execução da OS — tempos, KM e folha"""
    os = models.OneToOneField('OrdemServico', on_delete=models.CASCADE,
                              related_name='operacional', verbose_name='OS')
    numero_folha      = models.CharField(max_length=20, blank=True, verbose_name='Nº Folha')

    # Marcos de data/hora
    inicio_viagem     = models.DateTimeField(null=True, blank=True, verbose_name='Início de Viagem')
    chegada_operacao  = models.DateTimeField(null=True, blank=True, verbose_name='Chegada Operação')
    inicio_operacao   = models.DateTimeField(null=True, blank=True, verbose_name='Início Operação')
    termino_operacao  = models.DateTimeField(null=True, blank=True, verbose_name='Término Operação')
    termino_viagem    = models.DateTimeField(null=True, blank=True, verbose_name='Término de Viagem')

    # KM em cada marco
    km_inicio_viagem    = models.PositiveIntegerField(null=True, blank=True, verbose_name='KM Início Viagem')
    km_chegada_operacao = models.PositiveIntegerField(null=True, blank=True, verbose_name='KM Chegada Operação')
    km_inicio_operacao  = models.PositiveIntegerField(null=True, blank=True, verbose_name='KM Início Operação')
    km_termino_operacao = models.PositiveIntegerField(null=True, blank=True, verbose_name='KM Término Operação')
    km_termino_viagem   = models.PositiveIntegerField(null=True, blank=True, verbose_name='KM Término Viagem')
    pedagio             = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Pedágio (R$)')

    criado_em     = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Operacional da OS'

    def __str__(self):
        return f'Operacional OS-{self.os.numero}'

    # ── helpers ──
    @staticmethod
    def _diff_hhmm(dt1, dt2):
        if dt1 and dt2:
            delta = abs((dt2 - dt1).total_seconds())
            h = int(delta // 3600)
            m = int((delta % 3600) // 60)
            return f'{h:02d}:{m:02d}'
        return '00:00'

    @property
    def tempo_chegada(self):
        return self._diff_hhmm(self.inicio_viagem, self.chegada_operacao)

    @property
    def tempo_inicio_op(self):
        return self._diff_hhmm(self.chegada_operacao, self.inicio_operacao)

    @property
    def tempo_termino_op(self):
        return self._diff_hhmm(self.inicio_operacao, self.termino_operacao)

    @property
    def tempo_termino_viagem(self):
        return self._diff_hhmm(self.inicio_viagem, self.termino_viagem)

    @property
    def km_trecho_chegada(self):
        if self.km_chegada_operacao and self.km_inicio_viagem:
            return self.km_chegada_operacao - self.km_inicio_viagem
        return 0

    @property
    def km_trecho_termino_op(self):
        if self.km_termino_operacao and self.km_inicio_operacao:
            return self.km_termino_operacao - self.km_inicio_operacao
        return 0

    @property
    def km_total(self):
        if self.km_termino_viagem and self.km_inicio_viagem:
            return self.km_termino_viagem - self.km_inicio_viagem
        return 0


class VeiculoEscoltado(models.Model):
    """Veículos escoltados na OS (máx 4)"""
    os           = models.ForeignKey('OrdemServico', on_delete=models.CASCADE,
                                     related_name='veiculos', verbose_name='OS')
    veiculo      = models.CharField(max_length=100, blank=True, verbose_name='Veículo')
    placa_cavalo  = models.CharField(max_length=15,  blank=True, verbose_name='Placa Cavalo')
    placa_carreta = models.CharField(max_length=15,  blank=True, verbose_name='Placa Carreta')
    placa_carreta2= models.CharField(max_length=15,  blank=True, verbose_name='Placa Carreta 2')
    motorista     = models.CharField(max_length=200, blank=True, verbose_name='Motorista')
    ordem         = models.PositiveSmallIntegerField(default=1, verbose_name='Ordem')

    class Meta:
        verbose_name = 'Veículo Escoltado'
        verbose_name_plural = 'Veículos Escoltados'
        ordering = ['ordem']

    def __str__(self):
        return f'{self.placa_cavalo or self.veiculo}'


# ==============================================================================
# FATURAMENTO
# ==============================================================================

class TabelaPreco(models.Model):
    SITUACAO_CHOICES = [('ativo', 'Ativo'), ('inativo', 'Inativo')]
    TIPO_VIAGEM_CHOICES = [
        ('urbana', 'Urbana'), ('rodoviaria', 'Rodoviária'),
        ('administrativa', 'Administrativa'), ('todas', 'Todas'),
    ]
    COBRAR_PEDAGIO_CHOICES = [('sim', 'Sim'), ('nao', 'Não')]

    cliente          = models.ForeignKey('Cliente', on_delete=models.PROTECT,
                                          related_name='tabelas_preco', verbose_name='Cliente')
    nome             = models.CharField(max_length=200, verbose_name='Nome da Tabela / Rota')
    tipo_viagem      = models.CharField(max_length=20, choices=TIPO_VIAGEM_CHOICES,
                                         default='todas', verbose_name='Tipo de Viagem')
    situacao         = models.CharField(max_length=10, choices=SITUACAO_CHOICES,
                                         default='ativo', verbose_name='Situação')
    data_inclusao    = models.DateField(auto_now_add=True, verbose_name='Inclusão')
    inicio_contrato  = models.DateField(null=True, blank=True, verbose_name='Início Contrato')
    ultimo_reajuste  = models.DateField(null=True, blank=True, verbose_name='Último Reajuste')
    proximo_reajuste = models.DateField(null=True, blank=True, verbose_name='Próximo Reajuste')
    valor_escolta    = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor da Escolta (R$)')
    franquia_km      = models.PositiveIntegerField(default=0, verbose_name='Franquia KM')
    franquia_horas   = models.CharField(max_length=6, default='000:00', verbose_name='Franquia Horas (HHH:MM)')
    excedente_km     = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Excedente por KM (R$)')
    excedente_hora   = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Excedente por Hora (R$)')
    cobrar_pedagio   = models.CharField(max_length=3, choices=COBRAR_PEDAGIO_CHOICES, default='sim', verbose_name='Cobrar Pedágio')
    pedagio_fixo     = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Pedágio Fixo (R$)')
    pedagio_percent  = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='% Pedágio')
    criado_em        = models.DateTimeField(auto_now_add=True)
    atualizado_em    = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tabela de Preço'
        verbose_name_plural = 'Tabelas de Preço'
        ordering = ['cliente__razao_social', 'nome']

    def __str__(self):
        return f'{self.cliente.razao_social} — {self.nome}'

    def franquia_horas_minutos(self):
        try:
            h, m = self.franquia_horas.split(':')
            return int(h) * 60 + int(m)
        except Exception:
            return 0


class BoletimMedicao(models.Model):
    STATUS_CHOICES = [
        ('aberto', 'Em Aberto'),
        ('faturado', 'Faturado'),
        ('cancelado', 'Cancelado'),
    ]

    os              = models.OneToOneField('OrdemServico', on_delete=models.PROTECT,
                                            related_name='boletim', verbose_name='OS')
    tabela_preco    = models.ForeignKey('TabelaPreco', on_delete=models.PROTECT,
                                         null=True, blank=True,
                                         related_name='boletins', verbose_name='Tabela de Preço')
    status          = models.CharField(max_length=15, choices=STATUS_CHOICES, default='aberto', verbose_name='Status')
    horas_realizadas      = models.CharField(max_length=6, default='00:00', verbose_name='Horas Realizadas')
    km_realizado          = models.PositiveIntegerField(default=0, verbose_name='KM Realizado')
    horas_excedentes      = models.CharField(max_length=6, default='00:00', verbose_name='Horas Excedentes')
    km_excedente          = models.PositiveIntegerField(default=0, verbose_name='KM Excedente')
    valor_escolta         = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Valor Escolta (R$)')
    valor_excedente_km    = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Valor Excedente KM (R$)')
    valor_excedente_hora  = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Valor Excedente Hora (R$)')
    valor_pedagio         = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Valor Pedágio (R$)')
    acrescimo             = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Acréscimo (R$)')
    desconto              = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Desconto (R$)')
    valor_total           = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Valor Total (R$)')
    numero_nota           = models.CharField(max_length=50, blank=True, verbose_name='Nº Nota Fiscal')
    observacoes           = models.TextField(blank=True, verbose_name='Observações')
    criado_em             = models.DateTimeField(auto_now_add=True)
    atualizado_em         = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Boletim de Medição'
        verbose_name_plural = 'Boletins de Medição'
        ordering = ['-criado_em']

    def __str__(self):
        return f'Boletim OS-{self.os.numero}'

    def calcular(self):
        from decimal import Decimal
        op = getattr(self.os, 'operacional', None)
        tabela = self.tabela_preco
        if not tabela or not op:
            return
        inicio_base = self.os.previsao_inicio
        if op.chegada_operacao and op.chegada_operacao > self.os.previsao_inicio:
            inicio_base = op.chegada_operacao
        fim_base = op.termino_operacao
        if inicio_base and fim_base and fim_base > inicio_base:
            total_min = int((fim_base - inicio_base).total_seconds() // 60)
        else:
            total_min = 0
        self.horas_realizadas = f'{total_min // 60:02d}:{total_min % 60:02d}'
        # KM deve ser calculado entre Início e Término da Operação
        km_real = op.km_trecho_termino_op or 0
        self.km_realizado = km_real
        franquia_min = tabela.franquia_horas_minutos()
        excedente_min = max(0, total_min - franquia_min)
        self.horas_excedentes = f'{excedente_min // 60:02d}:{excedente_min % 60:02d}'
        km_exc = max(0, km_real - tabela.franquia_km)
        self.km_excedente = km_exc
        self.valor_escolta = tabela.valor_escolta
        exc_horas_dec = Decimal(excedente_min) / Decimal(60)
        self.valor_excedente_hora = (exc_horas_dec * tabela.excedente_hora).quantize(Decimal('0.01'))
        self.valor_excedente_km = (Decimal(km_exc) * tabela.excedente_km).quantize(Decimal('0.01'))
        # Só define pedágio automático se o campo estiver zerado (não foi digitado manualmente)
        if self.valor_pedagio == 0:
            if tabela.cobrar_pedagio == 'sim':
                if tabela.pedagio_fixo > 0:
                    self.valor_pedagio = tabela.pedagio_fixo
                elif op.pedagio:
                    self.valor_pedagio = Decimal(str(op.pedagio))
                else:
                    self.valor_pedagio = Decimal('0')
            else:
                self.valor_pedagio = Decimal('0')
        self.valor_total = (
            self.valor_escolta + self.valor_excedente_km +
            self.valor_excedente_hora + Decimal(str(self.valor_pedagio)) +
            Decimal(str(self.acrescimo)) - Decimal(str(self.desconto))
        ).quantize(Decimal('0.01'))
        self.save()
# No final do seu cadastros/models.py
from .models_perfil import PerfilUsuario