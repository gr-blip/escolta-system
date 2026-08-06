# Graph Report - Sistema Escolta  (2026-07-23)

## Corpus Check
- 111 files · ~418,338 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 971 nodes · 1534 edges · 154 communities (74 shown, 80 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 258 edges (avg confidence: 0.61)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e3f655a6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- omnilink.py
- OrdemServico
- views.py
- driverid_service.py
- Boletim List View
- models.py
- Cliente
- os_pdf.py
- Command
- recomprimir_fotos.py
- FuncionarioPatrimonial
- _is_admin_or_developer
- Base Template
- _pode_faturamento
- Tracker List Template
- Command
- OrdemServico
- OSOperacional
- Price Table List Template
- permissoes.py
- OS Detail Form Template
- JR Segurança Employee List
- Contrato de Prestação de Serviços Tecnológicos Especializados Nº 001/2026
- boletim_export_pdf
- Admin User Profile Config
- Mirroring History Migration
- JRS Facilities List Template
- Patrimonial Dashboard Template
- boletim_export.py
- Command
- User List Template
- finalize.mjs
- Command
- _gerar_certidao_pdf
- _comprimir_imagem
- _garantir_tabela_espelhamento
- fix-tour-dangling.mjs
- fix_total_processos.py
- models_perfil.py
- add-project-meta.mjs
- rebuild-graph.mjs
- CadastrosConfig
- Command
- Command
- 0018_populate_perfis.py
- toasts.js
- cadastros_extras.py
- _base64_to_file
- get_item
- 0015_setup_groups_and_users.py
- 0022_despesaos_trocamotorista_parada_incidente_and_more.py
- 0001_initial.py
- 0002_remove_fields.py
- 0003_add_colete.py
- 0004_add_equipe.py
- 0005_equipe_viatura.py
- 0006_ordemservico.py
- 0007_os_operacional_veiculos.py
- 0008_alter_agente_funcao_alter_agente_observacoes_and_more.py
- 0009_status_novos.py
- 0010_merge_20260319_0827.py
- 0011_equipe_finalizada_os_finalizada.py
- 0012_osoperacional_pedagio.py
- 0013_tabela_preco_boletim.py
- 0014_os_snapshot_equipe.py
- 0016_perfilusuario.py
- 0017_osoperacional_token.py
- 0019_osoperacional_gps.py
- 0020_cliente_nome_fantasia.py
- 0021_cliente_ativo.py
- 0023_despesaos_os_fk.py
- 0024_merge_0013_tabela_preco_boletim_0023_despesaos_os_fk.py
- 0026_espelhamentoenviado.py
- 0028_alter_espelhamentoenviado_id.py
- 0029_funcionariopatrimonial.py
- 0030_cancelamento_tipo.py
- 0031_funcionariopatrimonial_curso.py
- 0032_agente_curso.py
- 0033_funcionariopatrimonial_tipo_brigadista.py
- 0034_funcionariopatrimonial_funcao_brigadista.py
- 0035_agente_certidao_tjdf.py
- 0036_agente_certidao_trf.py
- 0037_agente_nome_mae_nome_pai.py
- 0038_agente_certidao_pdfs.py
- 0039_alter_agente_certidao_tjdf_consultado_em_and_more.py
- 0040_consultaprocesso.py
- 0041_consultaprocesso_origem.py
- 0042_agente_endereco.py
- 0043_funcionariopatrimonial_nome_mae.py
- 0044_funcionariopatrimonial_empresa_funcionariopatrimonial_cargo.py
- 0045_funcionariopatrimonial_empresa_freelance.py
- 0046_add_snap_val_endereco_renavan.py
- 0047_tabelapreco_velocidade_media.py
- 0048_diarias_lancamento.py
- FuncionarioPatrimonial
- PerfilUsuario
- agente_export_pdf
- auto_consultar_processos
- clientes_json
- dashboard_operacional
- diarias_agentes
- diarias_export_xlsx
- diarias_lancamento_deletar
- diarias_lancamento_excluir_auto
- diarias_lancamento_salvar
- espelhamento_aceitar_ajax
- espelhamento_cancelar_ajax
- espelhamento_centrais_ajax
- espelhamento_debug_ajax
- espelhamento_list
- omnilink_frota
- omnilink_frota_posicoes
- omnilink_historico
- omnilink_posicao_atual
- os_cancelar
- os_delete
- os_desativar_link
- os_detalhe
- os_detalhe_novo
- os_email_html
- os_field_despesa_salvar
- os_field_foto_marco_delete
- os_field_foto_veiculo_delete
- os_field_incidente_salvar
- os_field_link
- os_field_marco_salvar
- os_field_parada_salvar
- os_field_troca_motorista
- os_field_troca_motorista_delete
- os_field_veiculo_delete
- os_field_veiculo_salvar
- os_gerar_link
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
2. `Base Template` - 36 edges
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
- **Boletim de Medição lifecycle — links OS, client, price table, and status workflow (aberto→faturado)** — model_boletim, model_os, model_cliente, model_tabela_preco, url_boletim_finalizar, url_boletim_export_pdf, url_boletim_export_xlsx [EXTRACTED 0.95]
- **Equipe Composição — agents, armaments, bulletproof vests, and vehicle forming an operational team** — model_equipe, model_agente, model_armamento, model_colete, model_viatura [EXTRACTED 1.00]
- **Patrimonial employee background check — Funcionario Patrimonial, Freelance, and Consulta Processo share judicial process monitoring** — model_funcionario_patrimonial, model_freelance, model_consulta_processo, concept_processos_judiciais [EXTRACTED 0.95]
- **External Access URL Pattern Group** — url_jrsfacilities_reconsultar, url_omnilink_frota_posicoes, url_patrimonial_export_pdf [INFERRED 0.75]
- **JRS Facilities CRUD Templates** — cadastros_templates_cadastros_jrsfacilities_list, cadastros_templates_cadastros_jrsfacilities_detail, cadastros_templates_cadastros_jrsfacilities_form [INFERRED 0.95]
- **OS CRUD Workflow — List, Create, Print, Field** — cadastros_templates_cadastros_os_list, cadastros_templates_cadastros_os_nova, cadastros_templates_cadastros_os_print, cadastros_templates_cadastros_os_field_link, concept_ordem_de_servico [EXTRACTED 0.90]
- **Patrimonial Document Alert Flow — CNH, CNV, Curso Vencimento** — cadastros_templates_cadastros_patrimonial_dashboard, concept_agente, url_funcionario_patrimonial_edit [EXTRACTED 0.90]
- **Viatura-Rastreador Integration — Vehicle linked to Tracker** — cadastros_templates_cadastros_viatura_form, concept_viatura, concept_rastreador, url_rastreador_create [EXTRACTED 0.95]

## Communities (154 total, 80 thin omitted)

### Community 0 - "omnilink.py"
Cohesion: 0.24
Nodes (11): get_historico_operacao(), get_historico_posicoes(), _mct_id_to_terminal(), _parse_datetime(), Converte string de data/hora para datetime. Aceita múltiplos formatos., Retorna lista de posições do veículo no intervalo inicio..fim.      Estratégia, Atalho: busca histórico para o período completo da OS.     Usa inicio_viagem →, Converte MCT ID para IdTerminal hexadecimal (formato usado nos teleeventos). (+3 more)

### Community 2 - "views.py"
Cohesion: 0.06
Nodes (24): agente_create(), agente_delete(), armamento_create(), armamento_delete(), clientes_json(), colete_create(), colete_delete(), dashboard() (+16 more)

### Community 3 - "driverid_service.py"
Cohesion: 0.08
Nodes (38): BytesIO, Command, BaseCommand, cadastros/management/commands/consultar_processos.py ━━━━━━━━━━━━━━━━━━━━━━━━━━, gerar_pdf_consulta(), cadastros/pdf_processo.py ━━━━━━━━━━━━━━━━━━━━━━━━━ Geração de PDF completo pa, Gera PDF com todos os dados da consulta de processos judiciais.      Args:, consultar_cpf() (+30 more)

### Community 4 - "Boletim List View"
Cohesion: 0.18
Nodes (17): Boletim List View, Boletim Export Snippet, Boletim Marco Row Partial, Cliente Force Delete Confirm, Cliente Form View, Generic Confirm Delete View, Boletim de Medição, Cliente (+9 more)

### Community 6 - "Cliente"
Cohesion: 0.05
Nodes (64): AgenteAdmin, ArmamentoAdmin, ClienteAdmin, ColeteAdmin, ConsultaProcessoAdmin, RastreadorAdmin, ViaturaAdmin, AgenteForm (+56 more)

### Community 7 - "os_pdf.py"
Cohesion: 0.10
Nodes (37): _agent_block(), _dados_operacao_block(), _fmt_dt(), _fotos_marcos_block(), _fotos_veiculos_block(), gerar_os_pdf(), _header_block(), _identificacao_os_block() (+29 more)

### Community 8 - "Command"
Cohesion: 0.11
Nodes (12): Command, BaseCommand, Autenticação via Service Account JSON., Autenticação via OAuth2 (legado)., Django dumpdata → JSON comprimido em memória., Compacta /app/media em tarball gzip em memória., Gera Excel com 4 abas: OS, Boletins, Cadastros, Patrimonial., Command (+4 more)

### Community 9 - "recomprimir_fotos.py"
Cohesion: 0.11
Nodes (16): Command, _corrigir_orientacao(), BaseCommand, Management command para recomprimir fotos existentes no sistema.  Uso:     py, Recomprime um arquivo de imagem no disco.     Retorna (antes_kb, depois_kb, nov, _recomprimir_arquivo(), FotoIncidente, FotoMarco (+8 more)

### Community 10 - "FuncionarioPatrimonial"
Cohesion: 0.18
Nodes (8): TabelaPreco, boletim_list(), _pode_faturamento(), Financeiro, admin e developer têm acesso ao módulo de faturamento., tabela_preco_create(), tabela_preco_delete(), tabela_preco_edit(), tabela_preco_list()

### Community 11 - "_is_admin_or_developer"
Cohesion: 0.12
Nodes (16): cliente_create(), cliente_deletar_definitivo(), cliente_inativar(), cliente_list(), _is_admin_or_developer(), Lista usuários. O usuário 'demark' (developer) é invisível para todos exceto ele, Cria um novo usuário. Apenas admin e developer podem criar usuários., Edita dados de um usuário. Admin/developer podem editar qualquer um. Outros só a (+8 more)

### Community 12 - "Base Template"
Cohesion: 0.18
Nodes (16): JRS Facilities Detail Template, JRS Facilities Form Template, JRS Facilities List Template, Login Page Template, Fleet Tracking Map Template, User Delete Template, User Form Template, User Password Change Template (+8 more)

### Community 13 - "_pode_faturamento"
Cohesion: 0.33
Nodes (6): cliente_force_delete(), _get_nivel(), _is_developer(), _is_financeiro(), Retorna o nível do perfil. O usuário 'demark' é sempre developer., Exclusão forçada — apenas developer. Remove OS vinculadas e depois o cliente.

### Community 14 - "Tracker List Template"
Cohesion: 0.18
Nodes (12): Tracker List Template, Vehicle Form Template, Vehicle List Template, Rastreador (Tracker), Viatura (Vehicle), URL: rastreador_create, URL: rastreador_delete, URL: rastreador_edit (+4 more)

### Community 15 - "Command"
Cohesion: 0.24
Nodes (6): main(), run_command(), Command, BaseCommand, cadastros/management/commands/sincronizar_local.py ────────────────────────────, Exception

### Community 16 - "OrdemServico"
Cohesion: 0.08
Nodes (21): Command, BaseCommand, OrdemServico, os_cancelar(), os_desativar_link(), os_detalhe(), os_detalhe_novo(), os_email_html() (+13 more)

### Community 17 - "OSOperacional"
Cohesion: 0.15
Nodes (8): OSOperacional, Dados operacionais de execução da OS — tempos, KM e folha, os_field_despesa_salvar(), os_field_pedagio_salvar(), os_field_troca_motorista_delete(), Remove uma troca de motorista., Cria uma despesa/crédito., Salva o valor do pedagio via AJAX (link externo do agente).

### Community 18 - "Price Table List Template"
Cohesion: 0.33
Nodes (6): Price Table List Template, Cliente (Client), Tabela de Preço (Price Table), URL: tabela_preco_create, URL: tabela_preco_delete, URL: tabela_preco_edit

### Community 19 - "permissoes.py"
Cohesion: 0.24
Nodes (9): admin_required(), developer_required(), _get_nivel(), is_admin(), is_developer(), cadastros/permissoes.py ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━, Retorna o nível do perfil do usuário, ou None se não tiver perfil., Restringe a view apenas ao usuário com nível 'developer'. (+1 more)

### Community 21 - "JR Segurança Employee List"
Cohesion: 0.44
Nodes (10): Freelance Employee Detail, Freelance Employee List, JR Segurança Employee Detail, JR Segurança Employee List, Processos Judiciais Monitoring, Consulta de Processo Judicial, Freelance Employee, Funcionário Patrimonial (JR Segurança) (+2 more)

### Community 22 - "Contrato de Prestação de Serviços Tecnológicos Especializados Nº 001/2026"
Cohesion: 0.25
Nodes (8): _buscar_ultimo_id_post(), _get_eventos_normais(), get_ultima_posicao(), Obtém os IDs sequenciais atuais via BuscarUltimoIdPost.      Retorna dict: {'i, Obtém e cacheia o buffer de eventos normais da plataforma Omnilink.      Compa, Retorna a última posição conhecida do veículo.      Estratégia:       1. Obte, omnilink_posicao_atual(), AJAX — retorna posição atual GPS da viatura da OS.     Tenta ObtemAllPosicoesAt

### Community 23 - "boletim_export_pdf"
Cohesion: 0.16
Nodes (16): _fmt_brl(), gerar_pdf_bytes(), gerar_xlsx_bytes(), _missao_to_row(), cadastros/boletim_export.py ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━, Converte dict da missão para lista de 30 valores (mesma ordem de _COLUNAS)., boletim_export_pdf(), boletim_export_xlsx() (+8 more)

### Community 24 - "Admin User Profile Config"
Cohesion: 0.29
Nodes (5): BaseUserAdmin, PerfilInline, PerfilUsuarioAdmin, Adicione este bloco ao final do seu admin.py existente. Registra o PerfilUsuari, UserAdminCustom

### Community 25 - "Mirroring History Migration"
Cohesion: 0.25
Nodes (5): Migration, Migration de dados: insere espelhamentos enviados históricos no banco local. Ba, seed_historicos(), EspelhamentoEnviado, Registro local de espelhamentos criados por JRS FACILITES via Omnilink.     A A

### Community 26 - "JRS Facilities List Template"
Cohesion: 0.04
Nodes (46): 10. Comandos de Gerenciamento, 11. Dependências, 12. Observações Importantes, 1. Visão Geral, 2. Estrutura do Projeto, 3.1 Cadastros Base, 3.2 Operacional, 3.3 Faturamento (+38 more)

### Community 27 - "Patrimonial Dashboard Template"
Cohesion: 0.17
Nodes (12): OS List Template, OS Print Template, Patrimonial Dashboard Template, Agente de Segurança (Security Agent), Equipe (Team), Ordem de Serviço (OS), Template Tag: cadastros_extras, Freelance List URL (+4 more)

### Community 28 - "boletim_export.py"
Cohesion: 0.22
Nodes (16): Dashboard View, Diárias Agentes View, Equipe Form View, Espelhamento List View, Alertas de Vencimento, Agente, Armamento, Colete Balístico (+8 more)

### Community 29 - "Command"
Cohesion: 0.33
Nodes (3): Command, BaseCommand, management/commands/criar_usuarios.py ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Community 30 - "User List Template"
Cohesion: 0.29
Nodes (7): User List Template, Perfil de Usuário (User Profile), Usuário (User), URL: usuario_create, URL: usuario_delete, URL: usuario_edit, URL: usuario_senha

### Community 31 - "finalize.mjs"
Cohesion: 0.29
Nodes (6): graph, hash, intermediateDir, metadata, tmpDir, uaDir

### Community 32 - "Command"
Cohesion: 0.33
Nodes (3): Command, BaseCommand, Management command para criar/recriar o usuário developer (demark).  Uso:

### Community 33 - "_gerar_certidao_pdf"
Cohesion: 0.33
Nodes (6): agente_certidao_tjdf(), agente_certidao_trf(), _gerar_certidao_pdf(), Gera um PDF de certidão usando ReportLab e retorna os bytes., Consulta certidão TJDF via InfoSimples e salva o resultado no agente., Consulta certidão TRF 1ª Região (Seção DF) via InfoSimples e salva o resultado n

### Community 34 - "_comprimir_imagem"
Cohesion: 0.33
Nodes (6): _comprimir_imagem(), os_field_foto_marco(), os_field_foto_veiculo(), Comprime e redimensiona imagem antes de salvar. Retorna InMemoryUploadedFile., Recebe upload de foto de um marco via POST AJAX (multipart).     Permite apenas, Salva foto de um veículo escoltado.

### Community 35 - "_garantir_tabela_espelhamento"
Cohesion: 0.50
Nodes (4): espelhamento_listar_ajax(), _garantir_tabela_espelhamento(), Cria a tabela EspelhamentoEnviado e semeia dados históricos se ainda não existir, AJAX — lista espelhamentos enviados (banco local) e recebidos (API Omnilink).

### Community 36 - "fix-tour-dangling.mjs"
Cohesion: 0.33
Nodes (5): finalNodeIds, graph, nodeIds, step12, tour

### Community 37 - "fix_total_processos.py"
Cohesion: 0.25
Nodes (8): get_posicao_por_placa(), get_todas_posicoes_atuais(), Geocodificação reversa via Nominatim (OSM). Retorna dict com 'cidade' e 'estado', Chama ObtemAllPosicoesAtuais — retorna posição atual de todas as viaturas., Retorna a posição atual de uma viatura pela placa.     Usa o cache compartilhad, _reverse_geocode(), omnilink_frota_posicoes(), AJAX — retorna a posição atual de todas as viaturas.     Usa ObtemAllPosicoesAt

### Community 38 - "models_perfil.py"
Cohesion: 0.15
Nodes (12): 1. Instalar dependências, 2. Criar o banco de dados e aplicar migrações, 3. Criar o superusuário (acesso ao sistema), 4. Iniciar o servidor, 5. Acessar o sistema, Comandos úteis, Estrutura do projeto, Instalação e execução (+4 more)

### Community 39 - "add-project-meta.mjs"
Cohesion: 0.40
Nodes (4): fullKg, kg, layers, tour

### Community 40 - "rebuild-graph.mjs"
Cohesion: 0.40
Nodes (4): graph, knowledgeGraph, layers, tour

### Community 45 - "toasts.js"
Cohesion: 0.83
Nodes (3): consumeDjangoMessages(), ensureStack(), push()

### Community 47 - "_base64_to_file"
Cohesion: 0.50
Nodes (4): _base64_to_file(), os_field_assinatura(), Converte data:image/png;base64,... → ContentFile para salvar no ImageField., Salva assinatura digital (base64 PNG vindo do canvas).

### Community 51 - "0022_despesaos_trocamotorista_parada_incidente_and_more.py"
Cohesion: 0.13
Nodes (16): Base Template, Cliente Permanent Delete Confirm, Cliente Inativar/Reativar View, Colete Form View, Colete List View, Dashboard Operacional View, Equipe List View, OS Cancel Template (+8 more)

### Community 95 - "FuncionarioPatrimonial"
Cohesion: 0.33
Nodes (5): Equipe, equipe_create(), equipe_delete(), equipe_edit(), equipe_finalizar()

### Community 96 - "PerfilUsuario"
Cohesion: 0.50
Nodes (4): excluir_espelhamento(), Exclui/cancela um espelhamento pelo IdSolicitacao., espelhamento_cancelar_ajax(), AJAX POST — cancela/exclui espelhamento.

### Community 97 - "agente_export_pdf"
Cohesion: 0.18
Nodes (10): Abril/2026, 💾 Backup, 🧠 CONTEXTO DO PROJETO — Sistema de Escolta Grupo JR, 🚀 Deploy, 📁 Estrutura de arquivos, 🔄 Histórico de alterações, 🔐 Permissões (permissoes.py), ⚠️ Regras importantes (+2 more)

### Community 98 - "auto_consultar_processos"
Cohesion: 0.18
Nodes (11): `AssinaturaOS`, `DespesaOS`, `FotoIncidente`, `FotoMarco`, `FotoParada`, `FotoTrocaMotorista`, `FotoVeiculoEscoltado`, `Incidente` (+3 more)

### Community 99 - "clientes_json"
Cohesion: 0.22
Nodes (9): `BoletimMedicao`, `Equipe`, FATURAMENTO, 🗄️ Models (tabelas do banco), OPERACIONAL, `OrdemServico`, `OSOperacional` (OneToOne → OrdemServico), `TabelaPreco` (+1 more)

### Community 102 - "diarias_agentes"
Cohesion: 0.18
Nodes (12): _carregar_centrais_fixture(), criar_espelhamento(), _extrair_centrais_dos_espelhamentos(), listar_espelhamentos(), _parse_espelhamentos_xml(), Parseia XML de ListarEspelhamentosByClienteStatus., Lista espelhamentos da conta via ListarEspelhamentosByClienteStatus.      stat, Cria espelhamento enviado (JR → cliente).      Tenta primeiro CriarEspelhament (+4 more)

### Community 104 - "diarias_lancamento_deletar"
Cohesion: 0.29
Nodes (5): DespesaOS, _foto_upload_path(), Salva fotos em media/os_fotos/<numero_os>/<tipo>/<filename>, Despesas e créditos registrados pelo agente durante a OS., os_field_despesa_delete()

### Community 105 - "diarias_lancamento_excluir_auto"
Cohesion: 0.29
Nodes (7): `Agente`, `Armamento`, CADASTROS, `Cliente`, `Colete`, `Rastreador`, `Viatura`

### Community 106 - "diarias_lancamento_salvar"
Cohesion: 0.40
Nodes (4): DiariasLancamento, Permite editar, excluir ou incluir linhas na planilha de diárias.      - exclu, diarias_lancamento_salvar(), Cria ou edita um DiariasLancamento (salva valor override ou lançamento manual).

### Community 107 - "espelhamento_aceitar_ajax"
Cohesion: 0.50
Nodes (4): aceitar_espelhamento(), Aceita (aceitar=True) ou rejeita (aceitar=False) uma solicitação recebida., espelhamento_aceitar_ajax(), AJAX POST — aceita ou rejeita espelhamento recebido.

### Community 108 - "espelhamento_cancelar_ajax"
Cohesion: 0.20
Nodes (12): descobrir_metodos_wsdl(), _get_client(), listar_centrais_disponiveis(), pede_posicao_avulsa(), Solicita posição sob demanda ao veículo via PedePosicaoAvulsa.      Retorna o, Retorna cliente SOAP zeep com timeout configurado., Lista as centrais/bases disponíveis para espelhamento.     Tenta múltiplos nome, Retorna lista completa de métodos disponíveis no WSDL (diagnóstico). (+4 more)

### Community 109 - "espelhamento_centrais_ajax"
Cohesion: 0.29
Nodes (7): Apagar por categoria individual, Apagar registro individual, Apagar tudo (ordem obrigatória), 🗑️ Comandos para limpeza de dados (banco do Railway), Conectar ao banco de produção, Consultar quantos registros existem, Interpretando resultados

### Community 115 - "omnilink_posicao_atual"
Cohesion: 0.21
Nodes (11): _codmsg_to_int(), _coord_decimal(), _parse_coord(), _parse_posicoes_atuais_xml(), _parse_teleeventos_xml(), Integração com API Omnilink WSTT v1.159 (SOAP/WSDL) Documentação oficial: Manua, Converte CodMsg (sempre hexadecimal no XML, ex: "92") para inteiro.     Valores, Parseia XML de teleeventos retornado pela API Omnilink.      Retorna lista de (+3 more)

### Community 119 - "os_detalhe"
Cohesion: 0.50
Nodes (4): Cliente List View, Cliente Create URL, Cliente Delete URL, Cliente Edit URL

### Community 120 - "os_detalhe_novo"
Cohesion: 0.50
Nodes (4): App principal (cadastros/urls.py), Sub-rotas AJAX do link externo (token), 🌐 URLs principais, URLs raiz (escolta_system/urls.py)

### Community 124 - "os_field_foto_veiculo_delete"
Cohesion: 0.67
Nodes (3): ⚙️ Infraestrutura, Variáveis de ambiente no Railway, Volume de mídia (Railway)

### Community 125 - "os_field_incidente_salvar"
Cohesion: 0.33
Nodes (5): Incidente, Registro de ocorrência/incidente durante a OS., os_field_incidente_delete(), os_field_incidente_salvar(), Cria ou atualiza um incidente.

### Community 128 - "os_field_parada_salvar"
Cohesion: 0.29
Nodes (5): Parada, Parada registrada durante a OS — com motivo, duração e fotos., os_field_parada_delete(), os_field_parada_salvar(), Cria ou atualiza uma parada.

### Community 132 - "os_field_veiculo_delete"
Cohesion: 0.29
Nodes (6): Veículos escoltados na OS (máx 4), VeiculoEscoltado, os_field_veiculo_delete(), os_field_veiculo_salvar(), Cria ou edita um VeiculoEscoltado via AJAX (link externo do agente)., Deleta um VeiculoEscoltado via AJAX (link externo do agente).

## Knowledge Gaps
- **202 isolated node(s):** `kg`, `layers`, `tour`, `fullKg`, `uaDir` (+197 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **80 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FuncionarioPatrimonial` connect `Cliente` to `Command`, `views.py`, `driverid_service.py`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Why does `PerfilUsuario` connect `Cliente` to `Command`, `os_field_parada_salvar`, `os_field_veiculo_delete`, `models.py`, `Command`, `diarias_lancamento_deletar`, `diarias_lancamento_salvar`, `recomprimir_fotos.py`, `FuncionarioPatrimonial`, `OrdemServico`, `OSOperacional`, `os_field_incidente_salvar`, `Mirroring History Migration`, `Command`, `FuncionarioPatrimonial`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `DriverIDError` connect `driverid_service.py` to `views.py`, `Command`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Are the 25 inferred relationships involving `FuncionarioPatrimonial` (e.g. with `AgenteForm` and `ArmamentoForm`) actually correct?**
  _`FuncionarioPatrimonial` has 25 INFERRED edges - model-reasoned connections that need verification._
- **Are the 29 inferred relationships involving `PerfilUsuario` (e.g. with `.handle()` and `Command`) actually correct?**
  _`PerfilUsuario` has 29 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `Cliente` (e.g. with `AgenteAdmin` and `ArmamentoAdmin`) actually correct?**
  _`Cliente` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `OSOperacional` (e.g. with `PerfilUsuario` and `os_field_assinatura()`) actually correct?**
  _`OSOperacional` has 18 INFERRED edges - model-reasoned connections that need verification._