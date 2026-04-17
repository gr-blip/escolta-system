# Outras importa├º├Áes...
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
    nome_fantasia = models.CharField(max_length=200, blank=True, verbose_name='Nome Fantasia')
    cnpj = models.CharField(max_length=18, unique=True, verbose_name='CNPJ')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
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
        ('em_servico', 'Em Servi├ºo'),
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
    observacoes      = models.TextField(blank=True, verbose_name='Observa├º├Áes')
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
        ('Nivel IIA',  'N├¡vel IIA'),
        ('Nivel II',   'N├¡vel II'),
        ('Nivel IIIA', 'N├¡vel IIIA'),
        ('Nivel III',  'N├¡vel III'),
        ('Nivel IV',   'N├¡vel IV'),
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
        ('em_operacao', 'Em Opera├º├úo'),
        ('encerrando',  'Encerrando'),
        ('concluida',   'Conclu├¡da'),
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
        ('rodoviaria',     'Rodovi├íria'),
        ('administrativa', 'Administrativa'),
    ]

    numero          = models.CharField(max_length=20, unique=True, verbose_name='N┬║ OS', blank=True)
    cliente         = models.ForeignKey('Cliente',  on_delete=models.PROTECT, verbose_name='Cliente')
    solicitante     = models.CharField(max_length=200, blank=True, verbose_name='Solicitante')
    forma_solicitacao = models.CharField(max_length=20, choices=FORMA_CHOICES, verbose_name='Forma de Solicita├º├úo')
    tipo_viagem     = models.CharField(max_length=20, choices=TIPO_VIAGEM_CHOICES, verbose_name='Tipo de Viagem')
    previsao_inicio = models.DateTimeField(verbose_name='Previs├úo de In├¡cio')
    previsao_retorno= models.DateTimeField(blank=True, null=True, verbose_name='Previs├úo de Retorno')
    imediata        = models.BooleanField(default=False, verbose_name='Imediata')
    cidade_origem   = models.CharField(max_length=200, verbose_name='Cidade Origem')
    uf_origem       = models.CharField(max_length=2, default='GO', verbose_name='UF Origem')
    cidade_destino  = models.CharField(max_length=200, verbose_name='Cidade Destino')
    uf_destino      = models.CharField(max_length=2, default='GO', verbose_name='UF Destino')
    equipe          = models.ForeignKey('Equipe', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Equipe')
    # Snapshot da equipe ÔÇö preservado mesmo ap├│s excluir a equipe
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
    observacoes     = models.TextField(blank=True, verbose_name='Observa├º├Áes')
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberta', verbose_name='Status')
    finalizada_em   = models.DateTimeField(null=True, blank=True, verbose_name='Finalizada em')
    criado_em       = models.DateTimeField(auto_now_add=True)
    atualizado_em   = models.DateTimeField(auto_now=True)

    @property
    def is_finalizada(self):
        return self.status == 'finalizada'

    class Meta:
        verbose_name = 'Ordem de Servi├ºo'
        verbose_name_plural = 'Ordens de Servi├ºo'
        ordering = ['-criado_em']

    def __str__(self):
        return f'OS-{self.numero} ÔÇö {self.cliente}'

    def save(self, *args, **kwargs):
        if not self.numero:
            from django.utils import timezone
            ano = timezone.now().year
            ultimo = OrdemServico.objects.filter(numero__startswith=str(ano)).count()
            self.numero = f'{ano}{str(ultimo + 1).zfill(4)}'
        super().save(*args, **kwargs)


class OSOperacional(models.Model):
    """Dados operacionais de execu├º├úo da OS ÔÇö tempos, KM e folha"""
    import uuid as _uuid
    os = models.OneToOneField('OrdemServico', on_delete=models.CASCADE,
                              related_name='operacional', verbose_name='OS')
    numero_folha      = models.CharField(max_length=20, blank=True, verbose_name='N┬║ Folha')
    token      = models.UUIDField(default=_uuid.uuid4, unique=True, editable=False, verbose_name='Token de Acesso Externo')
    link_ativo = models.BooleanField(default=True, verbose_name='Link Externo Ativo')

    # Marcos de data/hora
    inicio_viagem     = models.DateTimeField(null=True, blank=True, verbose_name='In├¡cio de Viagem')
    chegada_operacao  = models.DateTimeField(null=True, blank=True, verbose_name='Chegada Opera├º├úo')
    inicio_operacao   = models.DateTimeField(null=True, blank=True, verbose_name='In├¡cio Opera├º├úo')
    termino_operacao  = models.DateTimeField(null=True, blank=True, verbose_name='T├®rmino Opera├º├úo')
    termino_viagem    = models.DateTimeField(null=True, blank=True, verbose_name='T├®rmino de Viagem')

    # KM em cada marco
    km_inicio_viagem    = models.PositiveIntegerField(null=True, blank=True, verbose_name='KM In├¡cio Viagem')
    km_chegada_operacao = models.PositiveIntegerField(null=True, blank=True, verbose_name='KM Chegada Opera├º├úo')
    km_inicio_operacao  = models.PositiveIntegerField(null=True, blank=True, verbose_name='KM In├¡cio Opera├º├úo')
    km_termino_operacao = models.PositiveIntegerField(null=True, blank=True, verbose_name='KM T├®rmino Opera├º├úo')
    km_termino_viagem   = models.PositiveIntegerField(null=True, blank=True, verbose_name='KM T├®rmino Viagem')
    pedagio             = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Ped├ígio (R$)')

    # Localiza├º├úo GPS de cada marco (lat/lng capturados pelo dispositivo do agente)
    gps_inicio_viagem_lat     = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    gps_inicio_viagem_lng     = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    gps_chegada_operacao_lat  = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    gps_chegada_operacao_lng  = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    gps_inicio_operacao_lat   = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    gps_inicio_operacao_lng   = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    gps_termino_operacao_lat  = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    gps_termino_operacao_lng  = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    gps_termino_viagem_lat    = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    gps_termino_viagem_lng    = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)

    criado_em     = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Operacional da OS'

    def __str__(self):
        return f'Operacional OS-{self.os.numero}'

    # ÔöÇÔöÇ helpers ÔöÇÔöÇ
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
    """Ve├¡culos escoltados na OS (m├íx 4)"""
    os           = models.ForeignKey('OrdemServico', on_delete=models.CASCADE,
                                     related_name='veiculos', verbose_name='OS')
    veiculo      = models.CharField(max_length=100, blank=True, verbose_name='Ve├¡culo')
    placa_cavalo  = models.CharField(max_length=15,  blank=True, verbose_name='Placa Cavalo')
    placa_carreta = models.CharField(max_length=15,  blank=True, verbose_name='Placa Carreta')
    placa_carreta2= models.CharField(max_length=15,  blank=True, verbose_name='Placa Carreta 2')
    motorista     = models.CharField(max_length=200, blank=True, verbose_name='Motorista')
    ordem         = models.PositiveSmallIntegerField(default=1, verbose_name='Ordem')

    class Meta:
        verbose_name = 'Ve├¡culo Escoltado'
        verbose_name_plural = 'Ve├¡culos Escoltados'
        ordering = ['ordem']

    def __str__(self):
        return f'{self.placa_cavalo or self.veiculo}'


# ==============================================================================
# FATURAMENTO
# ==============================================================================

class TabelaPreco(models.Model):
    SITUACAO_CHOICES = [('ativo', 'Ativo'), ('inativo', 'Inativo')]
    TIPO_VIAGEM_CHOICES = [
        ('urbana', 'Urbana'), ('rodoviaria', 'Rodovi├íria'),
        ('administrativa', 'Administrativa'), ('todas', 'Todas'),
    ]
    COBRAR_PEDAGIO_CHOICES = [('sim', 'Sim'), ('nao', 'N├úo')]

    cliente          = models.ForeignKey('Cliente', on_delete=models.PROTECT,
                                          related_name='tabelas_preco', verbose_name='Cliente')
    nome             = models.CharField(max_length=200, verbose_name='Nome da Tabela / Rota')
    tipo_viagem      = models.CharField(max_length=20, choices=TIPO_VIAGEM_CHOICES,
                                         default='todas', verbose_name='Tipo de Viagem')
    situacao         = models.CharField(max_length=10, choices=SITUACAO_CHOICES,
                                         default='ativo', verbose_name='Situa├º├úo')
    data_inclusao    = models.DateField(auto_now_add=True, verbose_name='Inclus├úo')
    inicio_contrato  = models.DateField(null=True, blank=True, verbose_name='In├¡cio Contrato')
    ultimo_reajuste  = models.DateField(null=True, blank=True, verbose_name='├Ültimo Reajuste')
    proximo_reajuste = models.DateField(null=True, blank=True, verbose_name='Pr├│ximo Reajuste')
    valor_escolta    = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor da Escolta (R$)')
    franquia_km      = models.PositiveIntegerField(default=0, verbose_name='Franquia KM')
    franquia_horas   = models.CharField(max_length=6, default='000:00', verbose_name='Franquia Horas (HHH:MM)')
    excedente_km     = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Excedente por KM (R$)')
    excedente_hora   = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Excedente por Hora (R$)')
    cobrar_pedagio   = models.CharField(max_length=3, choices=COBRAR_PEDAGIO_CHOICES, default='sim', verbose_name='Cobrar Ped├ígio')
    pedagio_fixo     = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Ped├ígio Fixo (R$)')
    pedagio_percent  = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='% Ped├ígio')
    criado_em        = models.DateTimeField(auto_now_add=True)
    atualizado_em    = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tabela de Pre├ºo'
        verbose_name_plural = 'Tabelas de Pre├ºo'
        ordering = ['cliente__razao_social', 'nome']

    def __str__(self):
        return f'{self.cliente.razao_social} ÔÇö {self.nome}'

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
                                         related_name='boletins', verbose_name='Tabela de Pre├ºo')
    status          = models.CharField(max_length=15, choices=STATUS_CHOICES, default='aberto', verbose_name='Status')
    horas_realizadas      = models.CharField(max_length=6, default='00:00', verbose_name='Horas Realizadas')
    km_realizado          = models.PositiveIntegerField(default=0, verbose_name='KM Realizado')
    horas_excedentes      = models.CharField(max_length=6, default='00:00', verbose_name='Horas Excedentes')
    km_excedente          = models.PositiveIntegerField(default=0, verbose_name='KM Excedente')
    valor_escolta         = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Valor Escolta (R$)')
    valor_excedente_km    = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Valor Excedente KM (R$)')
    valor_excedente_hora  = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Valor Excedente Hora (R$)')
    valor_pedagio         = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Valor Ped├ígio (R$)')
    acrescimo             = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Acr├®scimo (R$)')
    desconto              = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Desconto (R$)')
    valor_total           = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Valor Total (R$)')
    numero_nota           = models.CharField(max_length=50, blank=True, verbose_name='N┬║ Nota Fiscal')
    observacoes           = models.TextField(blank=True, verbose_name='Observa├º├Áes')
    criado_em             = models.DateTimeField(auto_now_add=True)
    atualizado_em         = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Boletim de Medi├º├úo'
        verbose_name_plural = 'Boletins de Medi├º├úo'
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
        # KM deve ser calculado entre In├¡cio e T├®rmino da Opera├º├úo
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
        # S├│ define ped├ígio autom├ítico se o campo estiver zerado (n├úo foi digitado manualmente)
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
from .models_perfil import PerfilUsuario# ============================================================
# ADICIONAR ao final de cadastros/models.py
# ============================================================
# Cole este bloco inteiro ap├│s a ├║ltima linha do models.py
# (ap├│s a linha: from .models_perfil import PerfilUsuario)
# ============================================================

import uuid as _uuid_mod
import os as _os_mod


def _foto_upload_path(instance, filename):
    """Salva fotos em media/os_fotos/<numero_os>/<tipo>/<filename>"""
    ext = filename.rsplit('.', 1)[-1].lower()
    novo_nome = f"{_uuid_mod.uuid4().hex}.{ext}"
    os_num = getattr(getattr(instance, 'operacional', None), 'os', None)
    if os_num is None:
        os_num = getattr(instance, 'os', None)
    numero = getattr(os_num, 'numero', 'sem_os') if os_num else 'sem_os'
    tipo = instance.__class__.__name__.lower()
    return _os_mod.path.join('os_fotos', numero, tipo, novo_nome)


# ÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇ
# FOTOS DOS MARCOS OPERACIONAIS
# ÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇ
class FotoMarco(models.Model):
    """Foto tirada pelo agente em cada marco da OS (inicio_viagem, chegada_operacao, etc.)"""
    MARCO_CHOICES = [
        ('inicio_viagem',    'In├¡cio de Viagem'),
        ('chegada_operacao', 'Chegada Opera├º├úo'),
        ('inicio_operacao',  'In├¡cio Opera├º├úo'),
        ('termino_operacao', 'T├®rmino Opera├º├úo'),
        ('termino_viagem',   'T├®rmino de Viagem'),
    ]

    os           = models.ForeignKey('OrdemServico', on_delete=models.CASCADE,
                                     related_name='fotos_marcos', verbose_name='OS')
    marco        = models.CharField(max_length=30, choices=MARCO_CHOICES, verbose_name='Marco')
    foto         = models.ImageField(upload_to=_foto_upload_path, verbose_name='Foto')
    latitude     = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude    = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    criado_em    = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Foto de Marco'
        verbose_name_plural = 'Fotos de Marcos'
        ordering = ['marco', 'criado_em']

    def __str__(self):
        return f'{self.get_marco_display()} ÔÇö OS-{self.os.numero}'


# ÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇ
# PARADAS
# ÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇ
class Parada(models.Model):
    """Parada registrada durante a OS ÔÇö com motivo, dura├º├úo e fotos."""
    MOTIVO_CHOICES = [
        ('abastecimento',  'Abastecimento'),
        ('refeicao',       'Refei├º├úo'),
        ('banheiro',       'Banheiro'),
        ('mecanica',       'Mec├ónica / Pane'),
        ('fiscal',         'Fiscaliza├º├úo / Barreira'),
        ('aguardando',     'Aguardando Instru├º├Áes'),
        ('outro',          'Outro'),
    ]

    os          = models.ForeignKey('OrdemServico', on_delete=models.CASCADE,
                                    related_name='paradas', verbose_name='OS')
    motivo      = models.CharField(max_length=20, choices=MOTIVO_CHOICES, verbose_name='Motivo')
    descricao   = models.TextField(blank=True, verbose_name='Descri├º├úo / Observa├º├Áes')
    inicio      = models.DateTimeField(verbose_name='In├¡cio da Parada')
    fim         = models.DateTimeField(null=True, blank=True, verbose_name='Fim da Parada')
    latitude    = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True, verbose_name='Latitude')
    longitude   = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True, verbose_name='Longitude')
    criado_em   = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Parada'
        verbose_name_plural = 'Paradas'
        ordering = ['inicio']

    def __str__(self):
        return f'{self.get_motivo_display()} ÔÇö OS-{self.os.numero}'

    @property
    def duracao_minutos(self):
        if self.inicio and self.fim:
            return int((self.fim - self.inicio).total_seconds() // 60)
        return None


class FotoParada(models.Model):
    """Fotos vinculadas a uma parada."""
    parada    = models.ForeignKey('Parada', on_delete=models.CASCADE,
                                  related_name='fotos', verbose_name='Parada')
    foto      = models.ImageField(upload_to=_foto_upload_path, verbose_name='Foto')
    criado_em = models.DateTimeField(auto_now_add=True)

    # Propriedade auxiliar para _foto_upload_path encontrar o n├║mero da OS
    @property
    def os(self):
        return self.parada.os

    class Meta:
        verbose_name = 'Foto de Parada'
        verbose_name_plural = 'Fotos de Parada'


# ÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇ
# INCIDENTES
# ÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇ
class Incidente(models.Model):
    """Registro de ocorr├¬ncia/incidente durante a OS."""
    TIPO_CHOICES = [
        ('acidente',       'Acidente de Tr├ónsito'),
        ('tentativa_roubo','Tentativa de Roubo'),
        ('avaria_carga',   'Avaria na Carga'),
        ('pane_viatura',   'Pane / Defeito Mec├ónico'),
        ('atividade_suspeita', 'Atividade Suspeita'),
        ('outro',          'Outro'),
    ]
    GRAVIDADE_CHOICES = [
        ('baixa',  'Baixa'),
        ('media',  'M├®dia'),
        ('alta',   'Alta'),
        ('critica','Cr├¡tica'),
    ]

    os          = models.ForeignKey('OrdemServico', on_delete=models.CASCADE,
                                    related_name='incidentes', verbose_name='OS')
    tipo        = models.CharField(max_length=30, choices=TIPO_CHOICES, verbose_name='Tipo')
    gravidade   = models.CharField(max_length=10, choices=GRAVIDADE_CHOICES,
                                   default='media', verbose_name='Gravidade')
    descricao   = models.TextField(verbose_name='Descri├º├úo do Incidente')
    ocorrido_em = models.DateTimeField(verbose_name='Data / Hora do Incidente')
    latitude    = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude   = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    bo_numero   = models.CharField(max_length=50, blank=True, verbose_name='N┬║ Boletim de Ocorr├¬ncia')
    criado_em   = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Incidente'
        verbose_name_plural = 'Incidentes'
        ordering = ['ocorrido_em']

    def __str__(self):
        return f'{self.get_tipo_display()} ({self.get_gravidade_display()}) ÔÇö OS-{self.os.numero}'


class FotoIncidente(models.Model):
    """Fotos vinculadas a um incidente."""
    incidente = models.ForeignKey('Incidente', on_delete=models.CASCADE,
                                  related_name='fotos', verbose_name='Incidente')
    foto      = models.ImageField(upload_to=_foto_upload_path, verbose_name='Foto')
    criado_em = models.DateTimeField(auto_now_add=True)

    @property
    def os(self):
        return self.incidente.os

    class Meta:
        verbose_name = 'Foto de Incidente'
        verbose_name_plural = 'Fotos de Incidente'


# ÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇ
# FOTOS DOS VE├ìCULOS ESCOLTADOS
# ÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇ
class FotoVeiculoEscoltado(models.Model):
    """Fotos do ve├¡culo escoltado (antes/depois da escolta)."""
    MOMENTO_CHOICES = [
        ('antes',  'Antes da Escolta'),
        ('depois', 'Ap├│s a Escolta'),
        ('outro',  'Outro'),
    ]

    veiculo   = models.ForeignKey('VeiculoEscoltado', on_delete=models.CASCADE,
                                  related_name='fotos', verbose_name='Ve├¡culo')
    momento   = models.CharField(max_length=10, choices=MOMENTO_CHOICES, default='antes')
    foto      = models.ImageField(upload_to=_foto_upload_path, verbose_name='Foto')
    criado_em = models.DateTimeField(auto_now_add=True)

    @property
    def os(self):
        return self.veiculo.os

    class Meta:
        verbose_name = 'Foto de Ve├¡culo Escoltado'
        verbose_name_plural = 'Fotos de Ve├¡culos Escoltados'


# ÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇ
# TROCA DE MOTORISTAS
# ÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇ
class TrocaMotorista(models.Model):
    """Registro de troca de motorista durante a OS."""
    os               = models.ForeignKey('OrdemServico', on_delete=models.CASCADE,
                                         related_name='trocas_motorista', verbose_name='OS')
    veiculo_escoltado= models.ForeignKey('VeiculoEscoltado', on_delete=models.SET_NULL,
                                         null=True, blank=True,
                                         related_name='trocas', verbose_name='Ve├¡culo')
    motorista_saindo = models.CharField(max_length=200, verbose_name='Motorista Saindo')
    motorista_entrando= models.CharField(max_length=200, verbose_name='Motorista Entrando')
    ocorrido_em      = models.DateTimeField(verbose_name='Data / Hora da Troca')
    motivo           = models.TextField(blank=True, verbose_name='Motivo')
    latitude         = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude        = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    criado_em        = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Troca de Motorista'
        verbose_name_plural = 'Trocas de Motorista'
        ordering = ['ocorrido_em']

    def __str__(self):
        return f'Troca: {self.motorista_saindo} ÔåÆ {self.motorista_entrando} (OS-{self.os.numero})'


class FotoTrocaMotorista(models.Model):
    """Fotos da troca de motorista (CNH, rosto, etc.)."""
    troca     = models.ForeignKey('TrocaMotorista', on_delete=models.CASCADE,
                                  related_name='fotos', verbose_name='Troca')
    foto      = models.ImageField(upload_to=_foto_upload_path, verbose_name='Foto')
    criado_em = models.DateTimeField(auto_now_add=True)

    @property
    def os(self):
        return self.troca.os

    class Meta:
        verbose_name = 'Foto de Troca de Motorista'
        verbose_name_plural = 'Fotos de Troca de Motorista'


# ÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇ
# ASSINATURAS DIGITAIS
# ÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇ
class AssinaturaOS(models.Model):
    """Assinatura digital capturada via canvas no link do agente."""
    TIPO_CHOICES = [
        ('agente1',    'Agente 1'),
        ('agente2',    'Agente 2'),
        ('motorista',  'Motorista Escoltado'),
        ('supervisor', 'Supervisor'),
    ]

    os        = models.ForeignKey('OrdemServico', on_delete=models.CASCADE,
                                  related_name='assinaturas', verbose_name='OS')
    tipo      = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo')
    nome      = models.CharField(max_length=200, verbose_name='Nome do Signat├írio')
    # Imagem PNG gerada do canvas (base64 ÔåÆ arquivo)
    imagem    = models.ImageField(upload_to=_foto_upload_path, verbose_name='Assinatura')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Assinatura'
        verbose_name_plural = 'Assinaturas'
        unique_together = [('os', 'tipo')]
        ordering = ['tipo']

    def __str__(self):
        return f'{self.get_tipo_display()} ÔÇö OS-{self.os.numero}'


# ÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇ
# CR├ëDITOS E DESPESAS
# ÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇ
class DespesaOS(models.Model):
    """Despesas e cr├®ditos registrados pelo agente durante a OS."""
    TIPO_CHOICES = [
        ('combustivel',  'Combust├¡vel'),
        ('refeicao',     'Refei├º├úo'),
        ('hospedagem',   'Hospedagem'),
        ('pedagio',      'Ped├ígio Avulso'),
        ('estacionamento','Estacionamento'),
        ('outro',        'Outro'),
    ]
    NATUREZA_CHOICES = [
        ('despesa',  'Despesa'),
        ('credito',  'Cr├®dito / Reembolso'),
    ]

    os        = models.ForeignKey('OrdemServico', on_delete=models.CASCADE,
                                  related_name='despesas', verbose_name='OS')
    tipo      = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo')
    natureza  = models.CharField(max_length=10, choices=NATUREZA_CHOICES,
                                 default='despesa', verbose_name='Natureza')
    descricao = models.CharField(max_length=300, blank=True, verbose_name='Descri├º├úo')
    valor     = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor (R$)')
    comprovante = models.ImageField(upload_to=_foto_upload_path, null=True, blank=True,
                                    verbose_name='Comprovante (foto)')
    ocorrido_em = models.DateTimeField(verbose_name='Data / Hora')
    criado_em   = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Despesa / Cr├®dito'
        verbose_name_plural = 'Despesas / Cr├®ditos'
        ordering = ['ocorrido_em']

    def __str__(self):
        return f'{self.get_tipo_display()} R${self.valor} ÔÇö OS-{self.os.numero}'

    @property
    def os(self):  # alias para _foto_upload_path funcionar no comprovante
        return self.__class__.objects.get(pk=self.pk).os if self.pk else None



# ── Espelhamentos enviados (armazenados localmente) ────────────────────────
class EspelhamentoEnviado(models.Model):
    """Registro local de espelhamentos criados por JRS FACILITES via Omnilink.
    A API só retorna espelhamentos onde somos DESTINO, então guardamos
    os que ENVIAMOS aqui para exibi-los na tela."""

    id_sequencia   = models.CharField(max_length=50, unique=True, null=True, blank=True,
                                      help_text='ID retornado pela API ao criar')
    placa          = models.CharField(max_length=20, verbose_name='Placa')
    id_central     = models.CharField(max_length=20, blank=True, verbose_name='ID Central Omnilink')
    nome_central   = models.CharField(max_length=200, blank=True, verbose_name='Nome da Central')
    cnpj_destino   = models.CharField(max_length=20, blank=True, verbose_name='CNPJ Destino')
    data_expiracao = models.CharField(max_length=30, verbose_name='Expiração (dd/MM/yyyy HH:mm:ss)')
    data_criacao   = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    obrigatorio    = models.BooleanField(default=False, verbose_name='Obrigatório')
    cancelado      = models.BooleanField(default=False, verbose_name='Cancelado')

    class Meta:
        verbose_name        = 'Espelhamento Enviado'
        verbose_name_plural = 'Espelhamentos Enviados'
        ordering            = ['-data_criacao']

    def __str__(self):
        destino = self.nome_central or self.cnpj_destino or 'desconhecido'
        return f'{self.placa} → {destino}'
