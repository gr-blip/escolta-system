# Graph Report - D:\Sistema Escolta  (2026-07-16)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 923 nodes · 1341 edges · 162 communities (53 shown, 109 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 193 edges (avg confidence: 0.54)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4f299c2d`
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
- consulta_processo_reconsultar
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
- os_field_pedagio_salvar
- os_field_troca_motorista
- os_field_troca_motorista_delete
- os_field_veiculo_delete
- os_field_veiculo_salvar
- os_gerar_link
- os_list
- os_nova
- os_observacoes_save
- os_operacional_save
- os_pdf_download
- patrimonial_dashboard
- patrimonial_export_pdf
- OS Field Link Template
- Painel de Avisos
- Dashboard Operacional
- Espelhamento Shared Pattern
- manage.py
- Agente List URL
- Armamento List URL
- Cliente List URL
- Equipe List URL

## God Nodes (most connected - your core abstractions)
1. `Base Template` - 37 edges
2. `PerfilUsuario` - 35 edges
3. `FuncionarioPatrimonial` - 28 edges
4. `Cliente` - 27 edges
5. `Agente` - 25 edges
6. `Viatura` - 25 edges
7. `Rastreador` - 23 edges
8. `Armamento` - 23 edges
9. `Colete` - 23 edges
10. `Dashboard URL` - 19 edges

## Surprising Connections (you probably didn't know these)
- `AgenteForm` --uses--> `FuncionarioPatrimonial`  [INFERRED]
  cadastros/forms.py → cadastros/models.py
- `Meta` --uses--> `FuncionarioPatrimonial`  [INFERRED]
  cadastros/forms.py → cadastros/models.py
- `ViaturaForm` --uses--> `FuncionarioPatrimonial`  [INFERRED]
  cadastros/forms.py → cadastros/models.py
- `RastreadorForm` --uses--> `FuncionarioPatrimonial`  [INFERRED]
  cadastros/forms.py → cadastros/models.py
- `ArmamentoForm` --uses--> `FuncionarioPatrimonial`  [INFERRED]
  cadastros/forms.py → cadastros/models.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Boletim de Medição lifecycle — links OS, client, price table, and status workflow (aberto→faturado)** — model_boletim, model_os, model_cliente, model_tabela_preco, url_boletim_finalizar, url_boletim_export_pdf, url_boletim_export_xlsx [EXTRACTED 0.95]
- **Equipe Composição — agents, armaments, bulletproof vests, and vehicle forming an operational team** — model_equipe, model_agente, model_armamento, model_colete, model_viatura [EXTRACTED 1.00]
- **Patrimonial employee background check — Funcionario Patrimonial, Freelance, and Consulta Processo share judicial process monitoring** — model_funcionario_patrimonial, model_freelance, model_consulta_processo, concept_processos_judiciais [EXTRACTED 0.95]
- **External Access URL Pattern Group** — url_jrsfacilities_reconsultar, url_omnilink_frota_posicoes, url_patrimonial_export_pdf [INFERRED 0.75]
- **JRS Facilities CRUD Templates** — cadastros_templates_cadastros_jrsfacilities_list, cadastros_templates_cadastros_jrsfacilities_detail, cadastros_templates_cadastros_jrsfacilities_form [INFERRED 0.95]
- **Ordem de Serviço Management Templates** — cadastros_templates_cadastros_os_detalhe, cadastros_templates_cadastros_os_cancelar, cadastros_templates_cadastros_os_email, cadastros_templates_cadastros_os_field_desativado [INFERRED 0.90]
- **OS CRUD Workflow — List, Create, Print, Field** — cadastros_templates_cadastros_os_list, cadastros_templates_cadastros_os_nova, cadastros_templates_cadastros_os_print, cadastros_templates_cadastros_os_field_link, concept_ordem_de_servico [EXTRACTED 0.90]
- **Patrimonial Document Alert Flow — CNH, CNV, Curso Vencimento** — cadastros_templates_cadastros_patrimonial_dashboard, concept_agente, url_funcionario_patrimonial_edit [EXTRACTED 0.90]
- **Viatura-Rastreador Integration — Vehicle linked to Tracker** — cadastros_templates_cadastros_viatura_form, concept_viatura, concept_rastreador, url_rastreador_create [EXTRACTED 0.95]
- **Serviços Tecnológicos Especializados** — graphify_out_converted_contrato_jr_wilker_001_2026_revisado_2_c5a6b0ec_suporte_tecnico, graphify_out_converted_contrato_jr_wilker_001_2026_revisado_2_c5a6b0ec_desenvolvimento, graphify_out_converted_contrato_jr_wilker_001_2026_revisado_2_c5a6b0ec_hospedagem [INFERRED 0.80]
- **Field Link Data Flow — Agent Mobile Interface** — feature_field_link, view_os_field_link, cadastros_os_field_link_html, cadastros_model_osoperacional, cadastros_model_ordemservico, cadastros_model_fotomarco, cadastros_model_parada, cadastros_model_incidente, cadastros_model_assinaturaos, cadastros_model_despesaos, cadastros_model_trocamotorista [EXTRACTED 0.95]
- **Omnilink GPS Tracking Feature** — integration_omnilink, view_omnilink_frota, view_omnilink_frota_posicoes, cadastros_model_viatura, cadastros_model_ordemservico, cadastros_model_osoperacional, cadastros_model_espelhamentoenviado, tech_leaflet, tech_zeep [EXTRACTED 0.95]
- **Deploy Pipeline — GitHub to Railway** — deployment_flow, tech_github, tech_railway, tech_gunicorn, tech_postgresql, tech_django, cmd_criar_developer [EXTRACTED 1.00]

## Communities (162 total, 109 thin omitted)

### Community 0 - "omnilink.py"
Cohesion: 0.06
Nodes (54): aceitar_espelhamento(), _buscar_ultimo_id_post(), _carregar_centrais_fixture(), _codmsg_to_int(), _coord_decimal(), criar_espelhamento(), descobrir_metodos_wsdl(), excluir_espelhamento() (+46 more)

### Community 1 - "OrdemServico"
Cohesion: 0.05
Nodes (52): Agente, Armamento, AssinaturaOS, BoletimMedicao, Cliente, Colete Balístico, DespesaOS, Equipe (+44 more)

### Community 2 - "views.py"
Cohesion: 0.04
Nodes (3): dashboard(), _fleet_data(), _os_por_dia()

### Community 3 - "driverid_service.py"
Cohesion: 0.08
Nodes (35): BytesIO, Command, BaseCommand, gerar_pdf_consulta(), cadastros/pdf_processo.py ━━━━━━━━━━━━━━━━━━━━━━━━━ Geração de PDF completo pa, Gera PDF com todos os dados da consulta de processos judiciais.      Args:, consultar_cpf(), _decode_jwt_exp() (+27 more)

### Community 4 - "Boletim List View"
Cohesion: 0.08
Nodes (40): Boletim List View, Boletim Export Snippet, Boletim Marco Row Partial, Cliente Force Delete Confirm, Cliente Form View, Cliente List View, Colete List View, Generic Confirm Delete View (+32 more)

### Community 5 - "models.py"
Cohesion: 0.08
Nodes (21): Migration, AssinaturaOS, DespesaOS, DiariasLancamento, Equipe, _foto_upload_path(), Incidente, Meta (+13 more)

### Community 6 - "Cliente"
Cohesion: 0.25
Nodes (26): AgenteAdmin, ArmamentoAdmin, ClienteAdmin, ColeteAdmin, ConsultaProcessoAdmin, RastreadorAdmin, ViaturaAdmin, AgenteForm (+18 more)

### Community 7 - "os_pdf.py"
Cohesion: 0.11
Nodes (34): _agent_block(), _dados_operacao_block(), _fmt_dt(), _fotos_marcos_block(), _fotos_veiculos_block(), gerar_os_pdf(), _header_block(), _identificacao_os_block() (+26 more)

### Community 8 - "Command"
Cohesion: 0.11
Nodes (10): Command, BaseCommand, Autenticação via Service Account JSON., Autenticação via OAuth2 (legado)., Django dumpdata → JSON comprimido em memória., Compacta /app/media em tarball gzip em memória., Gera Excel com 4 abas: OS, Boletins, Cadastros, Patrimonial., Command (+2 more)

### Community 9 - "recomprimir_fotos.py"
Cohesion: 0.11
Nodes (16): Command, _corrigir_orientacao(), BaseCommand, Management command para recomprimir fotos existentes no sistema.  Uso:     py, Recomprime um arquivo de imagem no disco.     Retorna (antes_kb, depois_kb, nov, _recomprimir_arquivo(), FotoIncidente, FotoMarco (+8 more)

### Community 10 - "FuncionarioPatrimonial"
Cohesion: 0.11
Nodes (9): cadastros/management/commands/consultar_processos.py ━━━━━━━━━━━━━━━━━━━━━━━━━━, Command, BaseCommand, Command, BaseCommand, FuncionarioPatrimonial, Retorna o status de vencimento de uma data:           - 'vencido'  : ja passou, True se qualquer documento esta vencido ou vencendo. (+1 more)

### Community 11 - "_is_admin_or_developer"
Cohesion: 0.12
Nodes (17): cliente_create(), cliente_deletar_definitivo(), cliente_edit(), cliente_inativar(), cliente_list(), _is_admin_or_developer(), Lista usuários. O usuário 'demark' (developer) é invisível para todos exceto ele, Cria um novo usuário. Apenas admin e developer podem criar usuários. (+9 more)

### Community 12 - "Base Template"
Cohesion: 0.17
Nodes (16): Base Template, Cliente Permanent Delete Confirm, Cliente Inativar/Reativar View, Colete Form View, Login Page Template, Fleet Tracking Map Template, Tracker Form Template, Price Table Form Template (+8 more)

### Community 13 - "_pode_faturamento"
Cohesion: 0.14
Nodes (14): boletim_finalizar(), boletim_list(), cliente_force_delete(), _get_nivel(), _is_developer(), _is_financeiro(), _pode_faturamento(), Retorna o nível do perfil. O usuário 'demark' é sempre developer. (+6 more)

### Community 14 - "Tracker List Template"
Cohesion: 0.18
Nodes (12): Tracker List Template, Vehicle Form Template, Vehicle List Template, Rastreador (Tracker), Viatura (Vehicle), URL: rastreador_create, URL: rastreador_delete, URL: rastreador_edit (+4 more)

### Community 15 - "Command"
Cohesion: 0.24
Nodes (6): main(), run_command(), Command, BaseCommand, cadastros/management/commands/sincronizar_local.py ────────────────────────────, Exception

### Community 16 - "OrdemServico"
Cohesion: 0.20
Nodes (5): cadastros/management/commands/backup_to_google.py ─────────────────────────────, Command, BaseCommand, Comando de uso único: remove o cliente de teste WILKER e a OS vinculada. Uso: p, OrdemServico

### Community 18 - "Price Table List Template"
Cohesion: 0.18
Nodes (11): OS List Template, New OS Form Template, Price Table List Template, Cliente (Client), Equipe (Team), Ordem de Serviço (OS), Tabela de Preço (Price Table), URL: os_nova (+3 more)

### Community 19 - "permissoes.py"
Cohesion: 0.24
Nodes (9): admin_required(), developer_required(), _get_nivel(), is_admin(), is_developer(), cadastros/permissoes.py ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━, Retorna o nível do perfil do usuário, ou None se não tiver perfil., Restringe a view apenas ao usuário com nível 'developer'. (+1 more)

### Community 20 - "OS Detail Form Template"
Cohesion: 0.22
Nodes (10): Equipe List View, OS Cancel Template, OS Detail Form Template, OS Email Notification Template, Deactivated Link Page Template, Equipe Create URL, OS Delete URL, OS List URL (+2 more)

### Community 21 - "JR Segurança Employee List"
Cohesion: 0.44
Nodes (10): Freelance Employee Detail, Freelance Employee List, JR Segurança Employee Detail, JR Segurança Employee List, Processos Judiciais Monitoring, Consulta de Processo Judicial, Freelance Employee, Funcionário Patrimonial (JR Segurança) (+2 more)

### Community 22 - "Contrato de Prestação de Serviços Tecnológicos Especializados Nº 001/2026"
Cohesion: 0.20
Nodes (10): Backup e Recuperação de Dados, Wilker Montalvao da Silva (Contratado), JR Segurança e Vigilância Patrimonial LTDA - ME (Contratante), Contrato de Prestação de Serviços Tecnológicos Especializados Nº 001/2026, Desenvolvimento e Customizações, Hospedagem e Infraestrutura Cloud, Lei Geral de Proteção de Dados (LGPD), Acordo de Nível de Serviço (SLA) (+2 more)

### Community 23 - "boletim_export_pdf"
Cohesion: 0.31
Nodes (9): boletim_export_pdf(), boletim_export_xlsx(), _boletim_queryset(), _boletim_to_missao(), _calcular_totais(), Aplica os mesmos filtros da boletim_list e retorna (qs, cliente_label, periodo_l, Converte um BoletimMedicao em dict compatível com o exportador., Calcula linha de totais a partir da lista de boletins. (+1 more)

### Community 24 - "Admin User Profile Config"
Cohesion: 0.29
Nodes (5): BaseUserAdmin, PerfilInline, PerfilUsuarioAdmin, Adicione este bloco ao final do seu admin.py existente. Registra o PerfilUsuari, UserAdminCustom

### Community 25 - "Mirroring History Migration"
Cohesion: 0.25
Nodes (5): Migration, Migration de dados: insere espelhamentos enviados históricos no banco local. Ba, seed_historicos(), EspelhamentoEnviado, Registro local de espelhamentos criados por JRS FACILITES via Omnilink.     A A

### Community 26 - "JRS Facilities List Template"
Cohesion: 0.36
Nodes (8): JRS Facilities Detail Template, JRS Facilities Form Template, JRS Facilities List Template, JRS Facilities Create URL, JRS Facilities Detail URL, JRS Facilities Edit URL, JRS Facilities List URL, JRS Facilities Reconsult URL

### Community 27 - "Patrimonial Dashboard Template"
Cohesion: 0.25
Nodes (8): OS Print Template, Patrimonial Dashboard Template, Agente de Segurança (Security Agent), Template Tag: cadastros_extras, Freelance List URL, Funcionario Patrimonial Create URL, URL: funcionario_patrimonial_edit, Funcionario Patrimonial List URL

### Community 28 - "boletim_export.py"
Cohesion: 0.43
Nodes (6): _fmt_brl(), gerar_pdf_bytes(), gerar_xlsx_bytes(), _missao_to_row(), cadastros/boletim_export.py ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━, Converte dict da missão para lista de 30 valores (mesma ordem de _COLUNAS).

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
Cohesion: 0.33
Nodes (6): espelhamento_criar_ajax(), espelhamento_listar_ajax(), _garantir_tabela_espelhamento(), Cria a tabela EspelhamentoEnviado e semeia dados históricos se ainda não existir, AJAX — lista espelhamentos enviados (banco local) e recebidos (API Omnilink)., AJAX POST — cria novo espelhamento.

### Community 36 - "fix-tour-dangling.mjs"
Cohesion: 0.33
Nodes (5): finalNodeIds, graph, nodeIds, step12, tour

### Community 37 - "fix_total_processos.py"
Cohesion: 0.40
Nodes (3): Command, BaseCommand, Management command: fix_total_processos ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

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

## Knowledge Gaps
- **147 isolated node(s):** `kg`, `layers`, `tour`, `fullKg`, `uaDir` (+142 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **109 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FuncionarioPatrimonial` connect `FuncionarioPatrimonial` to `driverid_service.py`, `models.py`, `Cliente`, `Command`, `OrdemServico`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `PerfilUsuario` connect `models.py` to `Command`, `Cliente`, `models_perfil.py`, `Command`, `recomprimir_fotos.py`, `FuncionarioPatrimonial`, `OrdemServico`, `OSOperacional`, `Mirroring History Migration`, `Command`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `Command` connect `Command` to `OrdemServico`, `FuncionarioPatrimonial`, `Cliente`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Are the 29 inferred relationships involving `PerfilUsuario` (e.g. with `.handle()` and `Command`) actually correct?**
  _`PerfilUsuario` has 29 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `FuncionarioPatrimonial` (e.g. with `AgenteForm` and `ArmamentoForm`) actually correct?**
  _`FuncionarioPatrimonial` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `Cliente` (e.g. with `AgenteAdmin` and `ArmamentoAdmin`) actually correct?**
  _`Cliente` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `Agente` (e.g. with `AgenteAdmin` and `ArmamentoAdmin`) actually correct?**
  _`Agente` has 19 INFERRED edges - model-reasoned connections that need verification._