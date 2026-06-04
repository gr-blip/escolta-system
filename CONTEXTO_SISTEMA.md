# Sistema Escolta — Contexto Completo

> **Última atualização:** 2026-05-28
> **Stack:** Django 3.1+ | PostgreSQL (Railway) | Deploy: Railway (gunicorn)
> **URL Produção:** https://grupojr.up.railway.app
> **Código:** `D:\Sistema Escolta\`

---

## 1. Visão Geral

Sistema web para gerenciamento operacional de **escolta armada** da empresa **JR Segurança e Vigilância Patrimonial Ltda**. Controla todo o ciclo de vida de uma operação de escolta: desde o cadastro de recursos (agentes, viaturas, armamento) até o faturamento do cliente, passando pela execução operacional em campo com rastreamento GPS em tempo real.

### Módulos Principais

| Módulo | Descrição |
|--------|-----------|
| **Cadastros** | Agentes, Viaturas, Rastreadores, Armamento, Coletes, Clientes |
| **Operacional** | Equipes, Ordens de Serviço (OS), dados operacionais, link externo do agente |
| **Faturamento** | Tabelas de preço, Boletins de medição, exportação PDF/XLSX |
| **Patrimonial** | Funcionários de 3 empresas: JR Segurança, JRS Facilities, Freelance |
| **Rastreamento** | Integração Omnilink (SOAP) para GPS de viaturas |
| **Processos Judiciais** | Integração DriverID para consulta de processos por CPF |

---

## 2. Estrutura do Projeto

```
D:\Sistema Escolta\
├── manage.py
├── settings.py                    # Settings do projeto (escolta_system)
├── urls.py                        # URL routing principal
├── wsgi.py
├── Procfile                       # Deploy Railway
├── requirements.txt
├── .env                           # Variáveis de ambiente
├── db.sqlite3                     # SQLite local (dev)
├── CLAUDE.md
│
├── escolta_system/                # Pacote Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── cadastros/                     # App principal (TUDO fica aqui)
│   ├── models.py                  # ~1100 linhas, 20+ models
│   ├── models_perfil.py           # PerfilUsuario (nível de acesso)
│   ├── views.py                   # ~4680 linhas, 100+ views
│   ├── urls.py                    # ~167 rotas
│   ├── forms.py                   # Forms para cadastros
│   ├── admin.py                   # Admin registrations
│   ├── permissoes.py              # Decorators: developer_required, admin_required
│   ├── signals.py                 # Auto-consulta DriverID ao criar FuncionarioPatrimonial
│   ├── omnilink.py                # Integração SOAP Omnilink (GPS)
│   ├── os_pdf.py                  # PDF da OS (ReportLab, A4 landscape)
│   ├── boletim_export.py          # PDF/XLSX do Boletim de Medição
│   ├── pdf_processo.py            # PDF consulta processos (DriverID)
│   ├── INTEGRACAO.py              # Guia de integração (docs)
│   ├── cadastros_extras.py        # Template tag: get_item
│   │
│   ├── services/
│   │   └── driverid_service.py    # API DriverID (processos judiciais)
│   │
│   ├── management/commands/
│   │   ├── consultar_processos.py # Cron: consulta periódica DriverID
│   │   ├── criar_developer.py     # Cria usuário developer
│   │   ├── backup_to_google.py    # Backup para Google Drive
│   │   ├── importar_freelance.py  # Importação em massa
│   │   ├── importar_jrs_facilities.py
│   │   ├── recomprimir_fotos.py   # Manutenção de fotos
│   │   └── ...
│   │
│   ├── templates/cadastros/       # ~51 templates HTML
│   │   ├── base.html              # Layout principal (sidebar, dark/light theme)
│   │   ├── dashboard.html
│   │   ├── os_*.html              # Templates de OS
│   │   ├── boletim_*.html         # Templates de faturamento
│   │   ├── patrimonial_*.html     # Templates patrimoniais
│   │   └── ...
│   │
│   ├── static/cadastros/
│   │   ├── style.css              # CSS principal
│   │   ├── logo.png
│   │   └── toasts.js              # Notificações toast
│   │
│   ├── templatetags/
│   │   └── cadastros_extras.py    # Filtro get_item
│   │
│   ├── fixtures/
│   │   └── centrais_omnilink.json # Centrais de rastreamento
│   │
│   └── migrations/                # 47 migrations
│
└── media/                         # Uploads (fotos, PDFs, certidões)
```

---

## 3. Modelos de Dados

### 3.1 Cadastros Base

| Model | Descrição | Campos-chave |
|-------|-----------|--------------|
| `Agente` | Agentes de escolta | nome, cpf, rg, telefone, cnh, cnv, funcao, status, foto, endereco |
| `Viatura` | Veículos da frota | placa (unique), marca_modelo, ano, cor, frota, mct_id, renavam, chassi |
| `Rastreador` | Rastreadores GPS | marca, modelo, numero_serie (unique) |
| `Armamento` | Armas | tipo, marca, modelo, calibre, numero_serie, registro_cr |
| `Colete` | Coletes à prova de balas | marca, numeracao, protecao (níveis IIA a IV), validade |
| `Cliente` | Clientes (empresas) | razao_social, cnpj (unique), ativo, endereco, cidade_uf |

### 3.2 Operacional

| Model | Descrição | Campos-chave |
|-------|-----------|--------------|
| `Equipe` | Equipe de 2 agentes + equipamentos | agente1, agente2, armamento_agente1/2, colete1/2, viatura |
| `OrdemServico` | OS de escolta | numero (auto), cliente, tipo_viagem, cidade_origem/destino, equipe, status, **snap_*** (snapshot) |
| `OSOperacional` | Dados de execução da OS | 5 marcos (inicio_viagem → termino_viagem), KM, GPS lat/lng, pedágio |
| `VeiculoEscoltado` | Veículo do cliente sendo escoltado | veiculo, placa_cavalo/carreta, motorista |
| `FotoMarco` | Fotos em cada marco | os, marco, foto, lat/lng |
| `Parada` | Paradas durante a OS | motivo (abastecimento, refeição, mecânica...), inicio/fim, GPS |
| `Incidente` | Ocorrências | tipo (acidente, roubo, avaria...), gravidade, descricao, bo_numero |
| `TrocaMotorista` | Troca de motorista | motorista_saindo, motorista_entrando |
| `AssinaturaOS` | Assinaturas digitais | tipo (agente1/2, motorista, supervisor), imagem |
| `DespesaOS` | Despesas/créditos | tipo, natureza, valor, comprovante |

### 3.3 Faturamento

| Model | Descrição |
|-------|-----------|
| `TabelaPreco` | Tabela de preço por cliente/rota: valor_escolta, franquia_km/horas, excedente_km/hora, pedágio |
| `BoletimMedicao` | Boletim vinculado à OS: calcula horas, KM, excedentes, valor_total |

### 3.4 Patrimonial

| Model | Descrição |
|-------|-----------|
| `FuncionarioPatrimonial` | Funcionários de 3 empresas (JR Segurança, JRS Facilities, Freelance). Cargo livre para Freelance/JRS |
| `ConsultaProcesso` | Consultas DriverID: cpf, status_cpf, total_processos, resultado_json, pdf_file |

### 3.5 Integração

| Model | Descrição |
|-------|-----------|
| `EspelhamentoEnviado` | Espelhamentos Omnilink enviados (rastreamento) |
| `PerfilUsuario` | Nível de acesso: developer, admin, operador, financeiro |

### 3.6 Padrão Snapshot

A `OrdemServico` usa campos `snap_*` para preservar dados da equipe/viatura mesmo após exclusão. Preenchidos automaticamente ao criar a OS.

### 3.7 Numeração OS

Formato: `AAAANNNN` (ex: `20260041`). Gerado automaticamente via `MAX+1` no `save()`, resiliente a deleções.

---

## 4. Controle de Acesso

### Níveis de Perfil (`PerfilUsuario`)

| Nível | Acesso |
|-------|--------|
| `developer` | Total + oculto nas listagens |
| `admin` | Total visível |
| `operador` | Operacional comum |
| `financeiro` | Apenas faturamento |

### Decorators (`permissoes.py`)

- `@developer_required` — apenas developer
- `@admin_required` — admin ou developer
- `is_developer(user)`, `is_admin(user)` — helpers para templates

### Template usage

```html
{% if request.user.perfil.is_developer %} ... {% endif %}
```

---

## 5. Fluxo Operacional

### 5.1 Ciclo de Vida da OS

```
Aberta → Em Viagem → Em Operação → Encerrando → Concluída → Finalizada
                                                           → Cancelada
```

### 5.2 Marcos Operacionais (OSOperacional)

1. **Início de Viagem** — KM, GPS, foto
2. **Chegada Operação** — KM, GPS, foto
3. **Início Operação** — KM, GPS, foto
4. **Término Operação** — KM, GPS, foto
5. **Término de Viagem** — KM, GPS, foto

### 5.3 Link Externo do Agente (Field)

Cada OS pode gerar um link UUID (`/os/field/<token>/`) para o agente em campo registrar:
- Marcos (com foto + GPS)
- Paradas (com foto)
- Incidentes (com foto)
- Fotos de veículos escoltados
- Trocas de motorista
- Assinaturas digitais (canvas)
- Despesas/créditos
- Pedágio

### 5.4 Cálculo do Boletim de Medição

```
horas_realizadas = término_operação - max(previsão_início, chegada_operação)
                  (se início_op < previsão, usa início_op como base)
km_realizado = km_termino_operação - km_inicio_operação
horas_excedentes = max(0, horas - franquia_horas)
km_excedente = max(0, km - franquia_km)
valor_total = valor_escolta + exc_km + exc_horas + pedágio + acréscimo - desconto
```

---

## 6. Integrações

### 6.1 Omnilink (Rastreamento GPS)

- **Protocolo:** SOAP/WSDL v1.159
- **Endpoint:** `https://wstt.omnilink.com.br/iasws/iasws.asmx?WSDL`
- **Credenciais:** hardcoded em `omnilink.py`
- **Funcionalidades:**
  - Posição atual de viaturas
  - Histórico de rota (7 dias)
  - Posição avulsa (sob demanda)
  - Espelhamentos (envio/recebimento)
- **Cache:** Redis-like via Django cache (posicao: 30s, historico: 5min)

### 6.2 DriverID (Processos Judiciais)

- **Fluxo:** Login JWT → POST CPF → Polling resultado → Processos detalhados
- **Credenciais:** `DRIVERID_EMAIL`, `DRIVERID_PASSWORD` (env vars)
- **Endpoint:** `DRIVERID_API_URL` (env var)
- **Trigger automático:** Signal `post_save` em `FuncionarioPatrimonial` (background thread)
- **Trigger agendado:** Management command `consultar_processos` (cron a cada 2 meses)
- **Endpoint HTTP:** `/patrimonial/auto-consultar/<token>/` (cron-job.org)

### 6.3 InfoSimples (Certidões)

- Consulta de certidão TJDFT e TRF para agentes
- Token: `INFOSIMPLES_TOKEN` (env var)

### 6.4 Google Drive (Backup)

- Management command `backup_to_google`
- Credenciais OAuth2 via env vars

---

## 7. Templates e UI

### Layout

- **Base:** `base.html` — sidebar colapsável, dark/light theme (localStorage)
- **Fontes:** Plus Jakarta Sans + JetBrains Mono
- **CSS:** `style.css` (custom, sem framework)
- **Toasts:** `toasts.js` para notificações

### Navegação (Sidebar)

```
Principal
  └── Dashboard
Cadastros (oculto para financeiro)
  ├── Agentes
  ├── Viaturas
  ├── Rastreadores
  ├── Armamento
  ├── Coletes
  └── Clientes
Operacional
  ├── Dashboard Operacional
  ├── Equipes
  ├── Ordens de Serviço
  ├── Rastreamento (Omnilink)
  └── Espelhamentos
Patrimonial
  ├── Dashboard
  ├── JR Segurança
  ├── JRS Facilities
  └── Freelance
Faturamento
  ├── Tabelas de Preço
  └── Boletins de Medição
Admin (developer/admin only)
  └── Usuários
```

### Templates por Módulo

| Módulo | Templates |
|--------|-----------|
| Dashboard | `dashboard.html`, `dashboard_operacional.html` |
| Cadastros | `*_list.html`, `*_form.html` (agentes, viaturas, etc.) |
| OS | `os_list.html`, `os_nova.html`, `os_detalhe.html`, `os_print.html`, `os_email.html`, `os_cancelar.html` |
| Field Link | `os_field_link.html`, `os_field_desativado.html` |
| Boletim | `boletim_list.html`, `boletim_detalhe.html` |
| Patrimonial | `patrimonial_dashboard.html`, `funcionario_patrimonial_*.html`, `jrsfacilities_*.html`, `freelance_*.html` |
| Rastreamento | `omnilink_frota.html`, `espelhamento_list.html` |

---

## 8. Geração de Documentos

### 8.1 PDF da OS (`os_pdf.py`)

- **Formato:** A4 landscape, 2 páginas
- **Biblioteca:** ReportLab
- **Conteúdo:** Identificação, marcos, fotos, veículos, assinaturas

### 8.2 Boletim de Medição (`boletim_export.py`)

- **PDF:** A3 landscape, 30 colunas (A-AD)
- **XLSX:** OpenPyXL
- **Cores:** Azul escuro headers, rosa (encerramento), amarelo (horas), laranja (totais)

### 8.3 PDF Consulta Processos (`pdf_processo.py`)

- **Formato:** A4 portrait
- **Conteúdo:** Dados do funcionário, status CPF, lista de processos

---

## 9. Deploy e Infraestrutura

### Railway

- **Procfile:**
  ```
  release: python manage.py migrate && python manage.py collectstatic --noinput && python manage.py criar_developer --senha Smith26
  web: gunicorn escolta_system.wsgi --log-file - --timeout 300 --workers 2 --worker-class gthread --threads 4
  ```
- **Banco:** PostgreSQL via `DATABASE_URL`
- **Static:** WhiteNoise (CompressedManifest)
- **Media:** `MEDIA_ROOT` via env var (volume persistente ou S3)

### Variáveis de Ambiente

| Variável | Descrição |
|----------|-----------|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` para dev |
| `DATABASE_URL` | PostgreSQL connection string |
| `MEDIA_ROOT` | Path para uploads |
| `INFOSIMPLES_TOKEN` | API InfoSimples |
| `DRIVERID_API_URL` | Endpoint DriverID |
| `DRIVERID_EMAIL` | Login DriverID |
| `DRIVERID_PASSWORD` | Senha DriverID |

---

## 10. Comandos de Gerenciamento

| Comando | Descrição |
|---------|-----------|
| `criar_developer` | Cria/redefine usuário developer |
| `consultar_processos` | Consulta processos judiciais (cron 2 meses) |
| `backup_to_google` | Backup para Google Drive |
| `importar_freelance` | Importa funcionários freelance |
| `importar_jrs_facilities` | Importa funcionários JRS Facilities |
| `recomprimir_fotos` | Recomprime fotos existentes |
| `corrigir_boletins_cancelados` | Corrige boletins de OS canceladas |
| `fix_total_processos` | Corrige total de processos |

---

## 11. Dependências

```
Django>=3.1
Pillow>=9.0           # Manipulação de imagens
gunicorn              # WSGI server
whitenoise            # Static files
dj-database-url       # DATABASE_URL parsing
psycopg2-binary       # PostgreSQL
reportlab             # Geração de PDF
openpyxl              # Geração de XLSX
zeep                  # SOAP client (Omnilink)
python-decouple==3.8  # Env vars
requests>=2.31.0      # HTTP client
google-api-python-client  # Google Drive
google-auth-httplib2
google-auth-oauthlib
```

---

## 12. Observações Importantes

### Encoding Windows
- Arquivos `.py` editados no Windows podem ter problemas de CRLF/BOM
- Usar scripts Python para editar arquivos `.py` evita SyntaxError

### Dados em Produção
- **NUNCA** alterar banco de produção sem confirmar com Wilker
- Sistema em uso real com dados de clientes reais

### Campos `snap_*`
- Dados da equipe são "fotografados" ao criar a OS
- Preservam informações mesmo se a equipe/viatura for excluída depois
- Fallback: `snap_*` primário, dados do Agente via equipe como fallback

### Background Threads
- Tarefas longas (consulta DriverID) usam `threading.Thread` com `daemon=True`
- Railway/gunicorn tem timeout de 300s — endpoints HTTP retornam 200 imediatamente

### Faturamento
- `BoletimMedicao.calcular()` usa `previsao_inicio` como base (não `criado_em`)
- Se operação inicia antes do previsto, usa `inicio_operacao` como base
- Pedágio: se `valor_pedagio` já foi digitado manualmente, não sobrescreve

### Clientes de Teste
- JRS Facilities e JR Segurança são excluídos dos gráficos do dashboard
- Dashboard conta apenas clientes ativos
