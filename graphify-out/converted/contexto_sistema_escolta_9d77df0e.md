<!-- converted from contexto_sistema_escolta.docx -->


JR SEGURANÇA
Departamento de Escolta Armada
SISTEMA DE GESTÃO DE ESCOLTA
Contexto Técnico Completo
Versão: Maio 2026

grupojr.up.railway.app

# 1. Visão Geral do Sistema
O Sistema de Gestão de Escolta é uma aplicação web desenvolvida sob medida para a JR Segurança — empresa de segurança privada especializada em escolta armada. O sistema gerencia todo o ciclo operacional: do cadastro de agentes e viaturas até a execução das ordens de serviço, rastreamento GPS em tempo real e faturamento.

URL de Produção: https://grupojr.up.railway.app
Plataforma de Deploy: Railway.app (cloud PaaS)
Framework: Django (Python) — aplicação monolítica
Banco de Dados: PostgreSQL (Railway managed)
Armazenamento de Arquivos: Web Volume Railway (/app/media)
Servidor Web: Gunicorn (gthread, 2 workers × 4 threads)
Static Files: WhiteNoise com compressão
Autenticação: Django Auth nativa (sessão + login/logout)
Fuso horário: America/Sao_Paulo (UTC-3)
## 1.1 Stack Técnica

# 2. Módulos do Sistema
## 2.1 Cadastros (Base)
Módulo de cadastros mestres — dados que alimentam toda a operação.
### Agentes
Cadastro completo dos agentes de escolta: dados pessoais, documentação (CPF, RG, CNH, CNV), armamento vinculado, colete vinculado e status (Ativo / Afastado / Inativo). Inclui consulta automática de certidão TJDFT e certidão TRF 1ª Região via integração InfoSimples (SOAP).
- Funções disponíveis: Agente de Escolta, Motorista Escolta, Supervisor, Coordenador
- Certidões: TJDFT e TRF consultadas via API SOAP (zeep) — status, detalhe e PDF armazenados
- Fotos de agentes armazenadas em media/agentes/
### Viaturas
Cadastro das viaturas da frota com tipo, marca/modelo, ano, cor, placa (única), número de frota, MCT ID (Omnilink), RENAVAM, chassi, validade CRLV e seguro.
- MCT ID: identificador da unidade no sistema Omnilink (rastreador GPS)
- Status: Ativa / Em manutenção / Inativa
### Rastreadores
Cadastro de rastreadores físicos vinculados às viaturas. Campo separado de Viatura — permite controlar hardware independentemente do veículo.
### Armamento
Controle individual de armas: tipo, marca, modelo, calibre, número de série, número CR, registro SINARM/SIGMA, validade. Cada arma é vinculada a um agente por meio da Equipe.
### Coletes Balísticos
Registro de coletes com marca, numeração, nível de proteção (IIA a IV) e validade. Vinculados individualmente a cada agente na Equipe.
### Clientes
Cadastro de empresas contratantes com razão social, nome fantasia, CNPJ, inscrição estadual, endereço. Vinculados às OS e às Tabelas de Preço.
- Inativação lógica (ativo=False) ou exclusão definitiva com proteção por FK
## 2.2 Operacional
### Equipes
Composição operacional de 2 agentes + 2 armas + 2 coletes + 1 viatura. Status: Ativa / Em Serviço / Finalizada / Inativa. Ao finalizar uma equipe, os recursos são liberados automaticamente.
- Proteção: não permite excluir equipe vinculada a OS em aberto
- Snapshot: ao vincular equipe a uma OS, todos os dados são copiados (snap_*) para preservar o histórico mesmo se a equipe for alterada
### Ordens de Serviço (OS)
Núcleo do sistema. Gerencia todo o ciclo de vida de uma escolta:
- Numeração automática: formato ANO+SEQÜENCIAL (ex: 20260017) — MAX+1, resistente a deleções
- Dados: cliente, solicitante, forma de solicitação, tipo de viagem, previsão, origem/destino, equipe, observações
- Status progressivo: Aberta → Em Viagem → Em Operação → Encerrando → Concluída → Finalizada / Cancelada
- Snapshot da equipe: agentes, armas, coletes, viatura copiados no momento da vinculação
- Veículos Escoltados: até 4 por OS (placa cavalo, placa carreta 1 e 2, motorista)
- Tipos de viagem: Urbana, Rodoviária, Administrativa, Preservação
### Execução / Marcos Operacionais (OSOperacional)
Tabela OneToOne com OrdemServico que armazena toda a execução real da OS:
- Marcos de data/hora: Início de Viagem, Chegada Operação, Início Operação, Término Operação, Término de Viagem
- KM em cada marco (para cálculo de distância percorrida)
- Coordenadas GPS em cada marco
- Nº Folha, Pedágio registrado
- Token UUID para link externo (acesso do agente em campo)
- Status da OS atualizado automaticamente ao salvar marcos
### Link Externo do Agente (Field)
Interface mobile-first acessível via URL pública com token UUID. Permite que o agente em campo:
- Registre marcos de data/hora e KM com GPS automático
- Tire fotos em cada marco (FotoMarco)
- Registre paradas com motivo, duração e fotos (Parada + FotoParada)
- Registre incidentes com tipo, gravidade, BO e fotos (Incidente + FotoIncidente)
- Fotografe veículos escoltados antes/depois (FotoVeiculoEscoltado)
- Registre troca de motorista com fotos de CNH (TrocaMotorista + FotoTrocaMotorista)
- Registre despesas com comprovante foto (DespesaOS)
- Capture assinatura digital via canvas (AssinaturaOS: agente1, agente2, motorista, supervisor)
- Salve pedágio avulso
O link pode ser gerado e desativado pela gestão. Cada OS tem um token único e permanente.
## 2.3 Rastreamento GPS — Integração Omnilink
Integração com a plataforma Omnilink para rastreamento em tempo real da frota.
### Mapa de Frota (omnilink_frota)
Página interativa com mapa Leaflet mostrando todas as viaturas cadastradas com MCT ID:
- Marcadores coloridos: Azul = Em Operação (OS ativa), Amarelo = Em Deslocamento (ignição ligada), Verde = Disponível (ignição desligada), Cinza = Sem sinal (>1h)
- Barra lateral com lista ordenada por prioridade (Em Operação primeiro)
- Para viaturas Em Operação: exibe número da OS, cliente, rota (origem→destino), agentes e horário de saída
- Popup com informações detalhadas ao clicar no marcador — inclui dados da OS quando em operação
- Auto-refresh a cada 60 segundos com countdown visual
- Tema claro/escuro com persistência em localStorage
- Sumário no header: contadores por categoria
### Detecção de Status "Em Operação"
A detecção usa dois caminhos complementares (OR) para máxima confiabilidade:
- 1) Status da OS = em_operacao ou encerrando
- 2) Marcos OSOperacional: chegada_operacao ou inicio_operacao preenchidos E termino_viagem vazio — cobre OS cujo status não foi atualizado
Fonte da placa: snap_viatura_placa (registrado na vinculação da equipe) com fallback para equipe→viatura.
### Rastreamento Individual de OS
Cada OS tem página de rastreamento individual com posição atual e histórico de rota via Omnilink (SOAP API).
### Espelhamentos Omnilink
Gestão de espelhamentos de rastreamento — compartilhamento de posição de viatura com outras centrais Omnilink:
- Criar, aceitar, cancelar espelhamentos via API SOAP
- Armazenamento local (EspelhamentoEnviado) dos espelhamentos enviados
- Interface AJAX para gestão em tempo real
## 2.4 Faturamento
### Tabelas de Preço
Configuração de tarifas por cliente e tipo de viagem:
- Valor base da escolta, franquia de KM e horas, excedentes por KM e hora
- Regras de pedágio: não cobrar, fixo ou percentual
- Validade e controle de reajuste (datas de início, último e próximo reajuste)
### Boletim de Medição
Documento de cobrança gerado automaticamente a partir dos marcos da OS:
- Horas realizadas calculadas entre chegada_operacao e termino_operacao
- KM calculado entre inicio_operacao e termino_operacao
- Excedentes calculados automaticamente vs. franquia contratada
- Pedágio: fixo da tabela ou valor real registrado pelo agente
- Acréscimo e desconto manuais
- Exportação em PDF (ReportLab) e Excel (openpyxl)
- Status: Em Aberto / Faturado / Cancelado
## 2.5 Patrimonial
Módulo independente para controle de funcionários patrimoniais (vigilância patrimonial — sem vínculo com OS de escolta):
- Tipos: Vigilante Armado/Desarmado, Líder de Vigilância, Porteiro, Brigadista
- Documentação: CPF, RG, CNH, CNV, curso de formação e validades
- Status: Ativo / Afastado / Inativo
- Dashboard patrimonial com visão consolidada
## 2.6 Dashboards
### Dashboard Principal
Visão executiva com:
- Contadores de OS por status (abertas, em operação, encerrando, concluídas)
- OS por cliente (gráfico AJAX)
- Alertas de documentos vencidos (CNV, CNH, CRLV, seguro)
- Acesso rápido aos módulos
### Dashboard Operacional
Visão em tempo real das operações ativas com equipes, viaturas e status atual.

# 3. Estrutura do Banco de Dados
O banco PostgreSQL contém os seguintes modelos principais:
## 3.1 Relações Principais
- OrdemServico → Equipe (FK SET_NULL) + snapshot dos dados
- OrdemServico → OSOperacional (OneToOne CASCADE)
- OrdemServico → BoletimMedicao (OneToOne PROTECT)
- OrdemServico → VeiculoEscoltado, FotoMarco, Parada, Incidente, etc. (FK CASCADE)
- Equipe → Agente ×2, Armamento ×2, Colete ×2, Viatura (FK PROTECT/SET_NULL)
- TabelaPreco → Cliente (FK PROTECT)
- BoletimMedicao → TabelaPreco (FK PROTECT)

# 4. Fluxo Operacional Completo
## 4.1 Ciclo de uma OS
## 4.2 Gestão de Fotos e Arquivos
Todas as fotos seguem o padrão de compressão automática:
- Formato: JPEG, largura máxima 1280px, qualidade 72
- Correção de orientação EXIF automática
- Armazenamento: /app/media/os_fotos/<numero_os>/<tipo>/<uuid>.jpg
- Retrocompressão: management command recomprimir_fotos disponível

# 5. Infraestrutura e Deploy
## 5.1 Railway — Configuração
Serviço: Web (Gunicorn)
Procfile (release phase): python manage.py migrate && collectstatic && criar_developer
Procfile (web): gunicorn escolta_system.wsgi --timeout 300 --workers 2 --worker-class gthread --threads 4
Banco: PostgreSQL gerenciado (acessível via DATABASE_URL)
Arquivos de mídia: Web Volume persistente montado em /app/media (MEDIA_ROOT env var)

### Variáveis de Ambiente Necessárias
## 5.2 Segurança
- HTTPS obrigatório em produção (SECURE_SSL_REDIRECT=True)
- HSTS: 86400s (1 dia) — progressivo até 1 ano + preload
- Cookies de sessão e CSRF seguros (secure=True)
- X-Frame-Options: DENY
- Autenticação: Django Auth nativa com @login_required em todas as views
- Usuário developer criado automaticamente no release phase
## 5.3 Cache
Cache em memória local (LocMemCache). Suficiente para a escala atual. Para múltiplos workers em produção futura, migrar para Redis.
- Timeout padrão: 300s
- Usado no dashboard e chamadas Omnilink

# 6. Integrações Externas
## 6.1 Omnilink (Rastreamento GPS)
Integração via SOAP (zeep) com a plataforma Omnilink para rastreamento em tempo real.
- Posição atual de cada viatura (lat/lng, velocidade, ignição, odômetro)
- Histórico de rota por OS
- Criação e gestão de espelhamentos entre centrais
- Lookup por placa (método novo) com fallback por MCT ID em hexadecimal
- Geocodificação reversa via Nominatim quando cidade não vem da API
## 6.2 InfoSimples (Certidões)
Integração via SOAP (zeep) para consulta de antecedentes judiciais dos agentes:
- Certidão TJDFT (Tribunal de Justiça do DF e Territórios)
- Certidão TRF 1ª Região — Seção DF
- Resultado: status, detalhe textual, PDF armazenado em media/certidoes/
## 6.3 Nominatim (Geocodificação)
API OpenStreetMap usada como fallback de geocodificação reversa quando a API Omnilink não retorna a cidade. Converte coordenadas lat/lng em endereço textual.

# 7. Histórico de Melhorias Recentes (Maio 2026)
## 7.1 Rastreamento — Status "Em Operação" no Mapa
Implementação de destaque visual para viaturas com OS ativa:
- Marcadores azuis com pulso animado para viaturas Em Operação
- Legenda e sumário no header atualizados
- Dados da OS exibidos na sidebar e popup (número, cliente, rota, agentes, saída)
- Detecção robusta: OR entre status da OS e marcos OSOperacional — garante detecção mesmo quando status não foi atualizado
- Placa resolvida por snap_viatura_placa com fallback equipe→viatura
## 7.2 Performance — Compressão de Imagens
- 155 MB liberados no web volume Railway via compressão retroativa
- 54 fotos recomprimidas para JPEG 1280px / qualidade 72
- Management command recomprimir_fotos disponível para execução futura
- Upload automático já comprime novas fotos no momento do salvamento
## 7.3 Estabilidade — Gunicorn gthread
- Migração de worker sync para gthread (--worker-class gthread --threads 4)
- Timeout aumentado para 300s (evita SIGKILL ao servir arquivos grandes)
- Elimina bloqueio de worker ao servir fotos via socket.sendfile
## 7.4 Informações da OS no Mapa
- API omnilink_frota_posicoes retorna os_info para viaturas Em Operação
- Sidebar exibe: número da OS, cliente, origem→destino, agentes, horário de saída
- Popup ao clicar no marcador exibe as mesmas informações com estilo visual diferenciado

# 8. URLs e Rotas Principais
## 8.1 Cadastros
## 8.2 Operacional
## 8.3 Link do Agente em Campo
## 8.4 Faturamento

# 9. Observações Técnicas e Próximos Passos
## 9.1 Pontos de Atenção
- Cache em memória local: com 2 workers Gunicorn, o cache não é compartilhado entre workers. Para consistência em produção futura, migrar para Redis.
- Mídia: o volume Railway é persistente mas single-node. Backups regulares recomendados. Para escala futura, migrar para S3/GCS.
- HSTS progressivo: atualmente em 86400s (1 dia). Aumentar para 30 dias após 1 mês estável, e para 1 ano após isso.
- Snap de equipe: os dados snap_* são registrados na vinculação. Se a equipe for alterada depois, o snap preserva o estado original — comportamento correto para rastreabilidade.
- Status da OS: o status é atualizado automaticamente pelo os_operacional_save view quando marcos são salvos. OS antigas podem ter marcos preenchidos sem atualização de status — coberto pela lógica dual do mapa.
## 9.2 Comandos de Management Disponíveis
## 9.3 Convenções de Código
- Views: todas protegidas por @login_required
- Fotos: comprimidas via Pillow no momento do upload (max 1280px, JPEG q72, EXIF corrigido)
- Numeração de OS: MAX+1 (não COUNT+1) — resistente a deleções
- Snap de equipe: copiado em os_detalhe_novo quando equipe é vinculada
- API Omnilink: timeout configurado por request; cache de resultados

Documento gerado automaticamente em Maio 2026
| Componente | Tecnologia / Versão |
| --- | --- |
| Backend | Django ≥ 3.1 (Python) |
| Banco | PostgreSQL via dj-database-url + psycopg2 |
| Imagens | Pillow ≥ 9.0 (compressão JPEG, EXIF) |
| PDF | ReportLab |
| Excel | openpyxl |
| SOAP/API | zeep (integração Omnilink) |
| Config | python-decouple (variáveis de ambiente) |
| HTTP Client | requests ≥ 2.31 |
| Mapas Frontend | Leaflet.js 1.9.4 + Stadia Maps / OpenStreetMap |
| Geocodificação | Nominatim (OpenStreetMap) — fallback reverso |
| Model | Tabela Django | Descrição |
| --- | --- | --- |
| Agente | cadastros_agente | Agentes de escolta com documentação completa |
| Viatura | cadastros_viatura | Frota da empresa com MCT ID Omnilink |
| Rastreador | cadastros_rastreador | Dispositivos GPS físicos |
| Armamento | cadastros_armamento | Armas com registro SINARM |
| Colete | cadastros_colete | Coletes balísticos com validade |
| Cliente | cadastros_cliente | Empresas contratantes |
| Equipe | cadastros_equipe | 2 agentes + viatura + armas + coletes |
| OrdemServico | cadastros_ordemservico | OS com snapshot da equipe e status |
| OSOperacional | cadastros_osoperacional | Marcos, KM, GPS, token de campo |
| VeiculoEscoltado | cadastros_veiculoescoltado | Veículos escoltados por OS (max 4) |
| FotoMarco | cadastros_fotomarco | Fotos por marco (chegada, início, etc.) |
| Parada | cadastros_parada | Paradas com motivo e duração |
| FotoParada | cadastros_fotoparada | Fotos das paradas |
| Incidente | cadastros_incidente | Ocorrências com gravidade e BO |
| FotoIncidente | cadastros_fotoincidente | Fotos dos incidentes |
| FotoVeiculoEscoltado | cadastros_fotoveiculoescoltado | Fotos antes/depois do veículo |
| TrocaMotorista | cadastros_trocamotorista | Troca de motorista em rota |
| FotoTrocaMotorista | cadastros_fototrocamotorista | Fotos da troca (CNH etc.) |
| AssinaturaOS | cadastros_assinaturaos | Assinaturas digitais (canvas) |
| DespesaOS | cadastros_despesaos | Despesas com comprovante foto |
| TabelaPreco | cadastros_tabelapreco | Tarifas por cliente e tipo de viagem |
| BoletimMedicao | cadastros_boletimmedicao | Faturamento calculado por OS |
| EspelhamentoEnviado | cadastros_espelhamentoenviado | Espelhamentos Omnilink enviados |
| FuncionarioPatrimonial | cadastros_funcionariopatrimonial | Vigilantes patrimoniais |
| PerfilUsuario | cadastros_perfilusuario | Perfil/permissões do usuário Django |
| Status | Trigger | O que acontece |
| --- | --- | --- |
| Aberta | Criação da OS | OS criada com dados do cliente e previsão; equipe pode ser vinculada |
| Em Viagem | Marco: Início de Viagem salvo | Agente registra saída via link field |
| Em Operação | Marco: Chegada Operação ou Início Operação salvo | Viatura aparece em azul no mapa de rastreamento |
| Encerrando | Marco: Término Operação salvo | Operação encerrada; aguardando retorno |
| Concluída | Marco: Término de Viagem salvo | Equipe retornou; pronto para faturar |
| Finalizada | Ação manual "Finalizar" | Boletim de medição gerado; OS arquivada |
| Cancelada | Ação manual "Cancelar" | Com ou sem deslocamento; data/tipo registrados |
| Variável | Descrição |
| --- | --- |
| DJANGO_SECRET_KEY | Chave secreta Django (obrigatória) |
| DJANGO_DEBUG | False em produção |
| DJANGO_ALLOWED_HOSTS | grupojr.up.railway.app |
| DJANGO_CSRF_TRUSTED_ORIGINS | https://grupojr.up.railway.app |
| DATABASE_URL | URL PostgreSQL (fornecida pelo Railway) |
| MEDIA_ROOT | /app/media (volume Railway) |
| OMNILINK_* | Credenciais da API Omnilink (SOAP) |
| INFOSIMPLES_* | Credenciais da API InfoSimples (certidões) |
| URL | Name | Descrição |
| --- | --- | --- |
| /agentes/ | agente_list | Lista de agentes |
| /viaturas/ | viatura_list | Lista de viaturas |
| /armamento/ | armamento_list | Lista de armamentos |
| /coletes/ | colete_list | Lista de coletes |
| /clientes/ | cliente_list | Lista de clientes |
| /rastreadores/ | rastreador_list | Lista de rastreadores |
| URL | Name | Descrição |
| --- | --- | --- |
| /operacional/os/ | os_list | Lista de OS |
| /operacional/os/<pk>/ | os_detalhe | Detalhe/edição da OS |
| /operacional/os/<pk>/operacional/ | os_operacional_save | Salva marcos e atualiza status |
| /operacional/os/<pk>/print/ | os_print | Impressão da OS |
| /operacional/os/<pk>/email/ | os_email_html | HTML para e-mail |
| /operacional/equipes/ | equipe_list | Lista de equipes |
| /operacional/rastreamento/ | omnilink_frota | Mapa de rastreamento |
| /operacional/rastreamento/posicoes/ | omnilink_frota_posicoes | API JSON de posições |
| /operacional/espelhamentos/ | espelhamento_list | Gestão de espelhamentos |
| URL | Função |
| --- | --- |
| /os/field/<token>/ | Interface mobile do agente |
| /os/field/<token>/marco/salvar/ | Salva marcos + atualiza status OS |
| /os/field/<token>/foto-marco/ | Upload de fotos por marco |
| /os/field/<token>/parada/salvar/ | Registra parada |
| /os/field/<token>/incidente/salvar/ | Registra incidente |
| /os/field/<token>/foto-veiculo/ | Foto do veículo escoltado |
| /os/field/<token>/assinatura/ | Captura assinatura digital |
| /os/field/<token>/despesa/salvar/ | Registra despesa |
| URL | Name | Descrição |
| --- | --- | --- |
| /faturamento/tabelas/ | tabela_preco_list | Tabelas de preço |
| /boletim/ | boletim_list | Boletins de medição |
| /boletim/export/pdf/ | boletim_export_pdf | Exporta PDF |
| /boletim/export/xlsx/ | boletim_export_xlsx | Exporta Excel |
| Comando | Função |
| --- | --- |
| python manage.py migrate | Aplica migrações de banco |
| python manage.py collectstatic | Coleta arquivos estáticos |
| python manage.py criar_developer --senha X | Cria/atualiza usuário developer |
| python manage.py recomprimir_fotos | Recomprime fotos existentes (JPEG 1280px/q72) |
| python manage.py recomprimir_fotos --dry-run | Simula sem alterar arquivos |
| python manage.py recomprimir_fotos --limite N | Processa no máximo N fotos |