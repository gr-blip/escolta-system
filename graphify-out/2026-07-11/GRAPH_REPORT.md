# Graph Report - .  (2026-07-11)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 857 nodes · 1435 edges · 138 communities (62 shown, 76 thin omitted)
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 261 edges (avg confidence: 0.61)
- Token cost: 8,061 input · 5,929 output

## Graph Freshness
- Built from commit: `1e9e0295`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Admin CRUD Models
- PDF Report Generation
- Dashboard and List Views
- OS PDF Generation
- Agente/Colete CRUD Views
- Patrimonial Employee Management
- OS Workflow Commands
- Photo Recompression
- Billing Measurement Corrections
- Boletim PDF/XLSX Export
- Backup and Drive Upload
- Frontend Templates
- Client and User CRUD
- Omnilink GPS Position Parsing
- Vehicle Mirroring Management
- Omnilink SOAP API Integration
- Tracker and Vehicle CRUD
- Drive Sync and Standalone Backup
- OS Operational Data
- Omnilink Position History
- OS and Price Table CRUD
- Permission Decorators
- OS and Team Templates
- Employee and Legal Process Views
- Admin User Profile Config
- Mirroring History Migration
- Omnilink Current Position
- Fleet Real-Time Positions
- JRS Facilities CRUD
- Patrimonial Dashboard and Print
- User Creation Command
- OS Stop Registration
- Escorted Vehicle Management
- User Profile CRUD
- Graph Build Pipeline
- Developer User Seed
- OS Incident Registration
- Agent Certificate Queries
- Client Force Delete Logic
- OS Photo Upload Handling
- Tour Fix Dangling Nodes
- Daily Allowance Management
- Project Meta Injection
- Knowledge Graph Rebuild
- Django App Config
- Import Judicial Queries
- Import Patrimonial Data
- Populate Profiles Migration
- Accept/Reject Mirroring
- Cancel Mirroring
- Toast Notifications JS
- Template Helpers
- Signature Upload Handling
- Mirroring List AJAX
- Template Dictionary Filter
- Groups and Users Migration
- Initial Migration
- Remove Fields Migration
- Add Colete Migration
- Add Equipe Migration
- Equipe Viatura Migration
- OrdemServico Migration
- OS Operacional Veiculos Migration
- Alter Agent Fields Migration
- Status Novos Migration
- Merge Migration
- Equipe OS Finalizada Migration
- OS Operacional Pedagio Migration
- Tabela Preco Boletim Migration
- OS Snapshot Equipe Migration
- PerfilUsuario Migration
- OS Operacional Token Migration
- OS Operacional GPS Migration
- Cliente Nome Fantasia Migration
- Cliente Ativo Migration
- DespesaOS FK Migration
- Merge Preco Despesa Migration
- EspelhamentoEnviado Migration
- Alter Espelhamento ID Migration
- FuncionarioPatrimonial Migration
- Cancelamento Tipo Migration
- Funcionario Curso Migration
- Agente Curso Migration
- Funcionario Tipo Brigadista Migration
- Funcionario Funcao Brigadista Migration
- Agente Certidao TJDF Migration
- Agente Certidao TRF Migration
- Agente Nome Mae Pai Migration
- Agente Certidao PDFs Migration
- Alter Certidao Timestamps Migration
- ConsultaProcesso Migration
- ConsultaProcesso Origem Migration
- Agente Endereco Migration
- Funcionario Nome Mae Migration
- Funcionario Empresa Migration
- Funcionario Empresa Freelance Migration
- Add Snap Val Endereco Renavan Migration
- TabelaPreco Velocidade Media Migration
- 0048_diarias_lancamento.py
- agente_export_pdf
- auto_consultar_processos
- Team CRUD Views
- dashboard_operacional
- diarias_export_xlsx
- diarias_lancamento_deletar
- omnilink_frota
- os_delete
- os_field_despesa_salvar
- os_field_foto_marco_delete
- os_field_link
- os_field_pedagio_salvar
- os_field_troca_motorista
- os_field_troca_motorista_delete
- os_list
- os_nova
- patrimonial_export_pdf
- settings.py
- OS Field Link Template
- Painel de Avisos
- Dashboard Operacional
- Espelhamento Shared Pattern
- Agente List URL
- Armamento List URL
- Cliente List URL
- Equipe List URL

## God Nodes (most connected - your core abstractions)
1. `FuncionarioPatrimonial` - 39 edges
2. `Base Template` - 37 edges
3. `PerfilUsuario` - 35 edges
4. `Cliente` - 32 edges
5. `OSOperacional` - 32 edges
6. `Agente` - 30 edges
7. `Viatura` - 28 edges
8. `Rastreador` - 26 edges
9. `Armamento` - 26 edges
10. `Colete` - 26 edges

## Surprising Connections (you probably didn't know these)
- `agente_delete()` --indirect_call--> `Agente`  [INFERRED]
  cadastros/views.py → cadastros/models.py
- `viatura_delete()` --indirect_call--> `Viatura`  [INFERRED]
  cadastros/views.py → cadastros/models.py
- `rastreador_delete()` --indirect_call--> `Rastreador`  [INFERRED]
  cadastros/views.py → cadastros/models.py
- `armamento_delete()` --indirect_call--> `Armamento`  [INFERRED]
  cadastros/views.py → cadastros/models.py
- `colete_delete()` --indirect_call--> `Colete`  [INFERRED]
  cadastros/views.py → cadastros/models.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Equipe Composição — agents, armaments, bulletproof vests, and vehicle forming an operational team** — model_equipe, model_agente, model_armamento, model_colete, model_viatura [EXTRACTED 1.00]
- **Boletim de Medição lifecycle — links OS, client, price table, and status workflow (aberto→faturado)** — model_boletim, model_os, model_cliente, model_tabela_preco, url_boletim_finalizar, url_boletim_export_pdf, url_boletim_export_xlsx [EXTRACTED 0.95]
- **Patrimonial employee background check — Funcionario Patrimonial, Freelance, and Consulta Processo share judicial process monitoring** — model_funcionario_patrimonial, model_freelance, model_consulta_processo, concept_processos_judiciais [EXTRACTED 0.95]
- **JRS Facilities CRUD Templates** — cadastros_templates_cadastros_jrsfacilities_list, cadastros_templates_cadastros_jrsfacilities_detail, cadastros_templates_cadastros_jrsfacilities_form [INFERRED 0.95]
- **Ordem de Serviço Management Templates** — cadastros_templates_cadastros_os_detalhe, cadastros_templates_cadastros_os_cancelar, cadastros_templates_cadastros_os_email, cadastros_templates_cadastros_os_field_desativado [INFERRED 0.90]
- **External Access URL Pattern Group** — url_jrsfacilities_reconsultar, url_omnilink_frota_posicoes, url_patrimonial_export_pdf [INFERRED 0.75]
- **OS CRUD Workflow — List, Create, Print, Field** — cadastros_templates_cadastros_os_list, cadastros_templates_cadastros_os_nova, cadastros_templates_cadastros_os_print, cadastros_templates_cadastros_os_field_link, concept_ordem_de_servico [EXTRACTED 0.90]
- **Patrimonial Document Alert Flow — CNH, CNV, Curso Vencimento** — cadastros_templates_cadastros_patrimonial_dashboard, concept_agente, url_funcionario_patrimonial_edit [EXTRACTED 0.90]
- **Viatura-Rastreador Integration — Vehicle linked to Tracker** — cadastros_templates_cadastros_viatura_form, concept_viatura, concept_rastreador, url_rastreador_create [EXTRACTED 0.95]

## Communities (138 total, 76 thin omitted)

### Community 0 - "Admin CRUD Models"
Cohesion: 0.07
Nodes (54): AgenteAdmin, ArmamentoAdmin, ClienteAdmin, ColeteAdmin, ConsultaProcessoAdmin, RastreadorAdmin, ViaturaAdmin, AgenteForm (+46 more)

### Community 1 - "PDF Report Generation"
Cohesion: 0.08
Nodes (38): BytesIO, Command, BaseCommand, cadastros/management/commands/consultar_processos.py ━━━━━━━━━━━━━━━━━━━━━━━━━━, gerar_pdf_consulta(), cadastros/pdf_processo.py ━━━━━━━━━━━━━━━━━━━━━━━━━ Geração de PDF completo pa, Gera PDF com todos os dados da consulta de processos judiciais.      Args:, consultar_cpf() (+30 more)

### Community 2 - "Dashboard and List Views"
Cohesion: 0.08
Nodes (40): Boletim List View, Boletim Export Snippet, Boletim Marco Row Partial, Cliente Force Delete Confirm, Cliente Form View, Cliente List View, Colete List View, Generic Confirm Delete View (+32 more)

### Community 3 - "OS PDF Generation"
Cohesion: 0.11
Nodes (36): _agent_block(), _dados_operacao_block(), _fmt_dt(), _fotos_marcos_block(), _fotos_veiculos_block(), gerar_os_pdf(), _header_block(), _identificacao_os_block() (+28 more)

### Community 4 - "Agente/Colete CRUD Views"
Cohesion: 0.05
Nodes (28): agente_create(), agente_delete(), armamento_create(), armamento_delete(), clientes_json(), colete_create(), colete_delete(), dashboard() (+20 more)

### Community 5 - "Patrimonial Employee Management"
Cohesion: 0.08
Nodes (17): Command, BaseCommand, Command, BaseCommand, FuncionarioPatrimonial, Retorna o status de vencimento de uma data:           - 'vencido'  : ja passou, True se qualquer documento esta vencido ou vencendo., Retorna a ConsultaProcesso mais recente deste funcionário. (+9 more)

### Community 6 - "OS Workflow Commands"
Cohesion: 0.08
Nodes (21): Command, BaseCommand, OrdemServico, os_cancelar(), os_desativar_link(), os_detalhe(), os_detalhe_novo(), os_email_html() (+13 more)

### Community 7 - "Photo Recompression"
Cohesion: 0.11
Nodes (16): Command, _corrigir_orientacao(), BaseCommand, Management command para recomprimir fotos existentes no sistema.  Uso:     py, Recomprime um arquivo de imagem no disco.     Retorna (antes_kb, depois_kb, nov, _recomprimir_arquivo(), FotoIncidente, FotoMarco (+8 more)

### Community 8 - "Billing Measurement Corrections"
Cohesion: 0.12
Nodes (13): Command, BaseCommand, BoletimMedicao, TabelaPreco, boletim_detalhe(), boletim_finalizar(), boletim_list(), _pode_faturamento() (+5 more)

### Community 9 - "Boletim PDF/XLSX Export"
Cohesion: 0.18
Nodes (15): _fmt_brl(), gerar_pdf_bytes(), gerar_xlsx_bytes(), _missao_to_row(), cadastros/boletim_export.py ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━, Converte dict da missão para lista de 30 valores (mesma ordem de _COLUNAS)., boletim_export_pdf(), boletim_export_xlsx() (+7 more)

### Community 10 - "Backup and Drive Upload"
Cohesion: 0.18
Nodes (7): Command, BaseCommand, Autenticação via Service Account JSON., Autenticação via OAuth2 (legado)., Django dumpdata → JSON comprimido em memória., Compacta /app/media em tarball gzip em memória., Gera Excel com 4 abas: OS, Boletins, Cadastros, Patrimonial.

### Community 11 - "Frontend Templates"
Cohesion: 0.17
Nodes (16): Base Template, Cliente Permanent Delete Confirm, Cliente Inativar/Reativar View, Colete Form View, Login Page Template, Fleet Tracking Map Template, Tracker Form Template, Price Table Form Template (+8 more)

### Community 12 - "Client and User CRUD"
Cohesion: 0.12
Nodes (16): cliente_create(), cliente_deletar_definitivo(), cliente_inativar(), cliente_list(), _is_admin_or_developer(), Lista usuários. O usuário 'demark' (developer) é invisível para todos exceto ele, Cria um novo usuário. Apenas admin e developer podem criar usuários., Edita dados de um usuário. Admin/developer podem editar qualquer um. Outros só a (+8 more)

### Community 13 - "Omnilink GPS Position Parsing"
Cohesion: 0.21
Nodes (11): _codmsg_to_int(), _coord_decimal(), _parse_coord(), _parse_posicoes_atuais_xml(), _parse_teleeventos_xml(), Integração com API Omnilink WSTT v1.159 (SOAP/WSDL) Documentação oficial: Manua, Converte CodMsg (sempre hexadecimal no XML, ex: "92") para inteiro.     Valores, Parseia XML de teleeventos retornado pela API Omnilink.      Retorna lista de (+3 more)

### Community 14 - "Vehicle Mirroring Management"
Cohesion: 0.18
Nodes (12): _carregar_centrais_fixture(), criar_espelhamento(), _extrair_centrais_dos_espelhamentos(), listar_espelhamentos(), _parse_espelhamentos_xml(), Parseia XML de ListarEspelhamentosByClienteStatus., Lista espelhamentos da conta via ListarEspelhamentosByClienteStatus.      stat, Cria espelhamento enviado (JR → cliente).      Tenta primeiro CriarEspelhament (+4 more)

### Community 15 - "Omnilink SOAP API Integration"
Cohesion: 0.20
Nodes (12): descobrir_metodos_wsdl(), _get_client(), listar_centrais_disponiveis(), pede_posicao_avulsa(), Solicita posição sob demanda ao veículo via PedePosicaoAvulsa.      Retorna o, Retorna cliente SOAP zeep com timeout configurado., Lista as centrais/bases disponíveis para espelhamento.     Tenta múltiplos nome, Retorna lista completa de métodos disponíveis no WSDL (diagnóstico). (+4 more)

### Community 16 - "Tracker and Vehicle CRUD"
Cohesion: 0.18
Nodes (12): Tracker List Template, Vehicle Form Template, Vehicle List Template, Rastreador (Tracker), Viatura (Vehicle), URL: rastreador_create, URL: rastreador_delete, URL: rastreador_edit (+4 more)

### Community 17 - "Drive Sync and Standalone Backup"
Cohesion: 0.24
Nodes (6): main(), run_command(), Command, BaseCommand, cadastros/management/commands/sincronizar_local.py ────────────────────────────, Exception

### Community 19 - "Omnilink Position History"
Cohesion: 0.24
Nodes (11): get_historico_operacao(), get_historico_posicoes(), _mct_id_to_terminal(), _parse_datetime(), Converte string de data/hora para datetime. Aceita múltiplos formatos., Retorna lista de posições do veículo no intervalo inicio..fim.      Estratégia, Atalho: busca histórico para o período completo da OS.     Usa inicio_viagem →, Converte MCT ID para IdTerminal hexadecimal (formato usado nos teleeventos). (+3 more)

### Community 20 - "OS and Price Table CRUD"
Cohesion: 0.18
Nodes (11): OS List Template, New OS Form Template, Price Table List Template, Cliente (Client), Equipe (Team), Ordem de Serviço (OS), Tabela de Preço (Price Table), URL: os_nova (+3 more)

### Community 21 - "Permission Decorators"
Cohesion: 0.24
Nodes (9): admin_required(), developer_required(), _get_nivel(), is_admin(), is_developer(), cadastros/permissoes.py ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━, Retorna o nível do perfil do usuário, ou None se não tiver perfil., Restringe a view apenas ao usuário com nível 'developer'. (+1 more)

### Community 22 - "OS and Team Templates"
Cohesion: 0.22
Nodes (10): Equipe List View, OS Cancel Template, OS Detail Form Template, OS Email Notification Template, Deactivated Link Page Template, Equipe Create URL, OS Delete URL, OS List URL (+2 more)

### Community 23 - "Employee and Legal Process Views"
Cohesion: 0.44
Nodes (10): Freelance Employee Detail, Freelance Employee List, JR Segurança Employee Detail, JR Segurança Employee List, Processos Judiciais Monitoring, Consulta de Processo Judicial, Freelance Employee, Funcionário Patrimonial (JR Segurança) (+2 more)

### Community 24 - "Admin User Profile Config"
Cohesion: 0.29
Nodes (5): BaseUserAdmin, PerfilInline, PerfilUsuarioAdmin, Adicione este bloco ao final do seu admin.py existente. Registra o PerfilUsuari, UserAdminCustom

### Community 25 - "Mirroring History Migration"
Cohesion: 0.25
Nodes (5): Migration, Migration de dados: insere espelhamentos enviados históricos no banco local. Ba, seed_historicos(), EspelhamentoEnviado, Registro local de espelhamentos criados por JRS FACILITES via Omnilink.     A A

### Community 26 - "Omnilink Current Position"
Cohesion: 0.25
Nodes (8): _buscar_ultimo_id_post(), _get_eventos_normais(), get_ultima_posicao(), Obtém os IDs sequenciais atuais via BuscarUltimoIdPost.      Retorna dict: {'i, Obtém e cacheia o buffer de eventos normais da plataforma Omnilink.      Compa, Retorna a última posição conhecida do veículo.      Estratégia:       1. Obte, omnilink_posicao_atual(), AJAX — retorna posição atual GPS da viatura da OS.     Tenta ObtemAllPosicoesAt

### Community 27 - "Fleet Real-Time Positions"
Cohesion: 0.25
Nodes (8): get_posicao_por_placa(), get_todas_posicoes_atuais(), Geocodificação reversa via Nominatim (OSM). Retorna dict com 'cidade' e 'estado', Chama ObtemAllPosicoesAtuais — retorna posição atual de todas as viaturas., Retorna a posição atual de uma viatura pela placa.     Usa o cache compartilhad, _reverse_geocode(), omnilink_frota_posicoes(), AJAX — retorna a posição atual de todas as viaturas.     Usa ObtemAllPosicoesAt

### Community 28 - "JRS Facilities CRUD"
Cohesion: 0.36
Nodes (8): JRS Facilities Detail Template, JRS Facilities Form Template, JRS Facilities List Template, JRS Facilities Create URL, JRS Facilities Detail URL, JRS Facilities Edit URL, JRS Facilities List URL, JRS Facilities Reconsult URL

### Community 29 - "Patrimonial Dashboard and Print"
Cohesion: 0.25
Nodes (8): OS Print Template, Patrimonial Dashboard Template, Agente de Segurança (Security Agent), Template Tag: cadastros_extras, Freelance List URL, Funcionario Patrimonial Create URL, URL: funcionario_patrimonial_edit, Funcionario Patrimonial List URL

### Community 30 - "User Creation Command"
Cohesion: 0.33
Nodes (3): Command, BaseCommand, management/commands/criar_usuarios.py ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Community 31 - "OS Stop Registration"
Cohesion: 0.29
Nodes (5): Parada, Parada registrada durante a OS — com motivo, duração e fotos., os_field_parada_delete(), os_field_parada_salvar(), Cria ou atualiza uma parada.

### Community 32 - "Escorted Vehicle Management"
Cohesion: 0.29
Nodes (6): Veículos escoltados na OS (máx 4), VeiculoEscoltado, os_field_veiculo_delete(), os_field_veiculo_salvar(), Cria ou edita um VeiculoEscoltado via AJAX (link externo do agente)., Deleta um VeiculoEscoltado via AJAX (link externo do agente).

### Community 33 - "User Profile CRUD"
Cohesion: 0.29
Nodes (7): User List Template, Perfil de Usuário (User Profile), Usuário (User), URL: usuario_create, URL: usuario_delete, URL: usuario_edit, URL: usuario_senha

### Community 34 - "Graph Build Pipeline"
Cohesion: 0.29
Nodes (6): graph, hash, intermediateDir, metadata, tmpDir, uaDir

### Community 35 - "Developer User Seed"
Cohesion: 0.33
Nodes (3): Command, BaseCommand, Management command para criar/recriar o usuário developer (demark).  Uso:

### Community 36 - "OS Incident Registration"
Cohesion: 0.33
Nodes (5): Incidente, Registro de ocorrência/incidente durante a OS., os_field_incidente_delete(), os_field_incidente_salvar(), Cria ou atualiza um incidente.

### Community 37 - "Agent Certificate Queries"
Cohesion: 0.33
Nodes (6): agente_certidao_tjdf(), agente_certidao_trf(), _gerar_certidao_pdf(), Gera um PDF de certidão usando ReportLab e retorna os bytes., Consulta certidão TJDF via InfoSimples e salva o resultado no agente., Consulta certidão TRF 1ª Região (Seção DF) via InfoSimples e salva o resultado n

### Community 38 - "Client Force Delete Logic"
Cohesion: 0.33
Nodes (6): cliente_force_delete(), _get_nivel(), _is_developer(), _is_financeiro(), Retorna o nível do perfil. O usuário 'demark' é sempre developer., Exclusão forçada — apenas developer. Remove OS vinculadas e depois o cliente.

### Community 39 - "OS Photo Upload Handling"
Cohesion: 0.33
Nodes (6): _comprimir_imagem(), os_field_foto_marco(), os_field_foto_veiculo(), Comprime e redimensiona imagem antes de salvar. Retorna InMemoryUploadedFile., Recebe upload de foto de um marco via POST AJAX (multipart).     Permite apenas, Salva foto de um veículo escoltado.

### Community 40 - "Tour Fix Dangling Nodes"
Cohesion: 0.33
Nodes (5): finalNodeIds, graph, nodeIds, step12, tour

### Community 41 - "Daily Allowance Management"
Cohesion: 0.40
Nodes (4): DiariasLancamento, Permite editar, excluir ou incluir linhas na planilha de diárias.      - exclu, diarias_lancamento_salvar(), Cria ou edita um DiariasLancamento (salva valor override ou lançamento manual).

### Community 42 - "Project Meta Injection"
Cohesion: 0.40
Nodes (4): fullKg, kg, layers, tour

### Community 43 - "Knowledge Graph Rebuild"
Cohesion: 0.40
Nodes (4): graph, knowledgeGraph, layers, tour

### Community 48 - "Accept/Reject Mirroring"
Cohesion: 0.50
Nodes (4): aceitar_espelhamento(), Aceita (aceitar=True) ou rejeita (aceitar=False) uma solicitação recebida., espelhamento_aceitar_ajax(), AJAX POST — aceita ou rejeita espelhamento recebido.

### Community 49 - "Cancel Mirroring"
Cohesion: 0.50
Nodes (4): excluir_espelhamento(), Exclui/cancela um espelhamento pelo IdSolicitacao., espelhamento_cancelar_ajax(), AJAX POST — cancela/exclui espelhamento.

### Community 50 - "Toast Notifications JS"
Cohesion: 0.83
Nodes (3): consumeDjangoMessages(), ensureStack(), push()

### Community 52 - "Signature Upload Handling"
Cohesion: 0.50
Nodes (4): _base64_to_file(), os_field_assinatura(), Converte data:image/png;base64,... → ContentFile para salvar no ImageField., Salva assinatura digital (base64 PNG vindo do canvas).

### Community 53 - "Mirroring List AJAX"
Cohesion: 0.50
Nodes (4): espelhamento_listar_ajax(), _garantir_tabela_espelhamento(), Cria a tabela EspelhamentoEnviado e semeia dados históricos se ainda não existir, AJAX — lista espelhamentos enviados (banco local) e recebidos (API Omnilink).

### Community 102 - "Team CRUD Views"
Cohesion: 0.33
Nodes (5): Equipe, equipe_create(), equipe_delete(), equipe_edit(), equipe_finalizar()

## Knowledge Gaps
- **115 isolated node(s):** `kg`, `layers`, `tour`, `fullKg`, `uaDir` (+110 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **76 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FuncionarioPatrimonial` connect `Patrimonial Employee Management` to `Admin CRUD Models`, `PDF Report Generation`, `Backup and Drive Upload`, `Agente/Colete CRUD Views`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `PerfilUsuario` connect `Admin CRUD Models` to `Escorted Vehicle Management`, `Developer User Seed`, `OS Incident Registration`, `Patrimonial Employee Management`, `Team CRUD Views`, `Photo Recompression`, `Billing Measurement Corrections`, `Daily Allowance Management`, `OS Workflow Commands`, `OS Operational Data`, `Mirroring History Migration`, `User Creation Command`, `OS Stop Registration`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `DriverIDError` connect `PDF Report Generation` to `Drive Sync and Standalone Backup`, `Agente/Colete CRUD Views`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Are the 25 inferred relationships involving `FuncionarioPatrimonial` (e.g. with `AgenteForm` and `ArmamentoForm`) actually correct?**
  _`FuncionarioPatrimonial` has 25 INFERRED edges - model-reasoned connections that need verification._
- **Are the 29 inferred relationships involving `PerfilUsuario` (e.g. with `.handle()` and `Command`) actually correct?**
  _`PerfilUsuario` has 29 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `Cliente` (e.g. with `AgenteAdmin` and `ArmamentoAdmin`) actually correct?**
  _`Cliente` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `OSOperacional` (e.g. with `PerfilUsuario` and `os_field_assinatura()`) actually correct?**
  _`OSOperacional` has 18 INFERRED edges - model-reasoned connections that need verification._