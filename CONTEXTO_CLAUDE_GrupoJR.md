# 🧠 CONTEXTO DO PROJETO — Sistema de Escolta Grupo JR
> Cole este bloco inteiro no início de qualquer conversa com o Claude para que ele entenda o projeto sem precisar dos arquivos.

---

## 🏢 Sobre o projeto

- **Nome:** Sistema de Escolta — JR Segurança / Depto. de Escolta Armada
- **URL de produção:** https://grupojr.up.railway.app
- **Stack:** Django (Python) + PostgreSQL + Railway + GitHub + Gunicorn + WhiteNoise
- **Pasta local:** `D:\Sistema Escolta\escolta_system`
- **App principal:** `cadastros`
- **Dependências:** Django, Pillow, dj-database-url, gunicorn, psycopg2-binary, whitenoise, reportlab, openpyxl

---

## ⚙️ Infraestrutura

| Serviço | Detalhe |
|---|---|
| Servidor | Railway (cloud) |
| Banco produção | PostgreSQL no Railway |
| Banco local | SQLite (quando DATABASE_URL não está definida) |
| Deploy | Automático via git push → GitHub → Railway |
| Start Command | `python manage.py migrate && python manage.py collectstatic --noinput && gunicorn escolta_system.wsgi --log-file - --timeout 120 --workers 2` |

### Variáveis de ambiente no Railway
- `DATABASE_URL` → URL interna do PostgreSQL (usada pelo serviço web)
- `DATABASE_PUBLIC_URL` → URL externa (usada para acessar de fora, ex: pg_dump, shell local)
- `SECRET_KEY` → Chave secreta Django
- `DEBUG` → False em produção
- `MEDIA_ROOT` → `/app/media` (aponta para o volume persistente montado no Railway)

### Volume de mídia (Railway)
- **Nome:** web-volume
- **Mount path:** `/app/media`
- As fotos enviadas pelos agentes são salvas neste volume e persistem entre deploys.
- Sem o volume, os arquivos de mídia são apagados a cada novo deploy (disco efêmero).
- O `settings.py` lê o caminho via `MEDIA_ROOT = os.environ.get('MEDIA_ROOT', os.path.join(BASE_DIR, 'media'))`.

---

## 📁 Estrutura de arquivos

```
escolta_system/
├── escolta_system/
│   ├── settings.py       # Configurações (banco, apps, idioma, MEDIA_ROOT via env)
│   └── urls.py           # URLs raiz (inclui re_path para servir /media/ em produção)
├── cadastros/
│   ├── models.py         # Todos os models do sistema
│   ├── models_perfil.py  # Model PerfilUsuario
│   ├── views.py          # Lógica das páginas + views AJAX
│   ├── urls.py           # Rotas do app (inclui rotas AJAX do link do agente)
│   ├── forms.py
│   ├── admin.py
│   ├── boletim_export.py # Exportação PDF/Excel do boletim (reportlab + openpyxl)
│   ├── permissoes.py     # Decorators developer_required / admin_required
│   ├── migrations/       # NUNCA deletar manualmente
│   └── templates/cadastros/
│       ├── base.html           # Template base com navbar e layout responsivo
│       ├── os_field_link.html  # Link externo do agente (8 abas)
│       ├── os_detalhe.html     # Detalhe da OS (usa variável 'op' para dados operacionais)
│       └── dashboard.html      # Painel de Avisos (alertas CNH/CNV/Colete)
├── static/               # Arquivos estáticos (CSS, logo, etc.)
├── media/                # Uploads locais (em produção: volume /app/media no Railway)
├── Procfile              # gunicorn para Railway
├── runtime.txt           # versão Python
├── limpar_dados.py       # Script utilitário de limpeza
├── requirements.txt
└── manage.py
```

---

## 🗄️ Models (tabelas do banco)

### CADASTROS

#### `Agente`
Campos: `foto`, `nome`, `cpf` (unique), `rg`, `telefone`, `data_nascimento`, `cnh`, `cnh_validade`, `cnh_categoria` (default 'B'), `cnv`, `cnv_validade`, `funcao` (agente_escolta/motorista_escolta/supervisor/coordenador), `status` (ativo/afastado/inativo), `observacoes`, `criado_em`, `atualizado_em`

#### `Viatura`
Campos: `tipo`, `marca_modelo`, `ano`, `cor`, `placa` (unique), `frota`, `mct_id`, `renavam`, `chassi`, `crlv_validade`, `seguro_validade`, `status` (ativa/manutencao/inativa), `observacoes`, `criado_em`, `atualizado_em`

#### `Rastreador`
Campos: `marca`, `modelo`, `numero_serie` (unique), `status` (online/offline/manutencao), `criado_em`, `atualizado_em`

#### `Armamento`
Campos: `tipo` (pistola/revolver/espingarda/rifle), `marca`, `modelo`, `calibre`, `numero_serie` (unique), `numero_cano`, `registro_cr`, `registro_validade`, `data_aquisicao`, `criado_em`, `atualizado_em`

#### `Colete`
Campos: `marca`, `numeracao`, `protecao` (Nivel IIA/II/IIIA/III/IV, default IIIA), `validade`, `criado_em`, `atualizado_em`

#### `Cliente`
Campos: `razao_social`, `nome_fantasia`, `cnpj` (unique), `ativo` (BooleanField, default True), `inscricao_estadual`, `endereco`, `cidade_uf`, `cep`, `criado_em`, `atualizado_em`
> Clientes são **inativados** em vez de excluídos. Busca automática de CNPJ no cadastro.

### OPERACIONAL

#### `Equipe`
Campos: `nome`, `agente1` (FK→Agente, PROTECT), `agente2` (FK→Agente, PROTECT), `armamento_agente1` (FK→Armamento, PROTECT), `armamento_agente2` (FK→Armamento, PROTECT), `armamento_extra` (FK→Armamento, SET_NULL, nullable), `colete1` (FK→Colete, PROTECT), `colete2` (FK→Colete, PROTECT), `viatura` (FK→Viatura, SET_NULL, nullable), `status` (ativa/inativa/em_servico/finalizada), `observacoes`, `criado_em`, `atualizado_em`

#### `OrdemServico`
Campos: `numero` (auto-gerado: `ANOxxxx` via `save()`, unique), `cliente` (FK→Cliente, PROTECT), `solicitante`, `forma_solicitacao` (email/telefone/whatsapp), `tipo_viagem` (urbana/rodoviaria/administrativa), `previsao_inicio`, `previsao_retorno`, `imediata` (BooleanField), `cidade_origem`, `uf_origem` (default 'GO'), `cidade_destino`, `uf_destino` (default 'GO'), `equipe` (FK→Equipe, SET_NULL), `status` (aberta/em_viagem/em_operacao/encerrando/concluida/finalizada/cancelada), `finalizada_em`, `observacoes`, `criado_em`, `atualizado_em`

Snapshot da equipe (preservado mesmo após excluir equipe): `snap_equipe_nome`, `snap_agente1_nome/cpf/rg/telefone/cnh/cnv/foto`, `snap_agente2_nome/cpf/rg/telefone/cnh/cnv/foto`, `snap_viatura_modelo/placa/cor/frota/mct`

Property: `is_finalizada` → `status == 'finalizada'`

#### `OSOperacional` (OneToOne → OrdemServico)
Dados de execução: `numero_folha`, `token` (UUID para link externo), `link_ativo` (BooleanField)
Marcos de tempo: `inicio_viagem`, `chegada_operacao`, `inicio_operacao`, `termino_operacao`, `termino_viagem`
KM em cada marco: `km_inicio_viagem`, `km_chegada_operacao`, `km_inicio_operacao`, `km_termino_operacao`, `km_termino_viagem`, `pedagio` (DecimalField)
GPS de cada marco: `gps_*_lat/lng` (10 campos DecimalField 10,7)
Properties calculadas: `tempo_chegada`, `tempo_inicio_op`, `tempo_termino_op`, `tempo_termino_viagem` (formato HH:MM), `km_trecho_chegada`, `km_trecho_termino_op`, `km_total`

#### `VeiculoEscoltado`
Campos: `os` (FK→OrdemServico, CASCADE), `veiculo`, `placa_cavalo`, `placa_carreta`, `placa_carreta2`, `motorista`, `ordem` (PositiveSmallIntegerField, default 1)
> Máximo de 4 veículos por OS. Cadastro também disponível pelo agente no campo (aba Veículos do link externo).

### LINK EXTERNO DO AGENTE (8 abas)

> Acesso via `os/field/<uuid:token>/` — sem login, autenticado apenas pelo token UUID da `OSOperacional`.

#### `FotoMarco`
Fotos dos marcos operacionais. Campos: `os` (FK, CASCADE), `marco` (inicio_viagem/chegada_operacao/inicio_operacao/termino_operacao/termino_viagem), `foto` (ImageField, upload via `_foto_upload_path`), `latitude`, `longitude`, `criado_em`
⚠️ Regra: **1 foto por marco por OS**. Upload substitui a anterior (deleta arquivo físico + reutiliza registro). Cooldown de 2 minutos no frontend após cada upload (contagem regressiva visível `⏳ 119s...` via `sessionStorage`).

#### `Parada`
Campos: `os` (FK, CASCADE), `motivo` (abastecimento/refeicao/banheiro/mecanica/fiscal/aguardando/outro), `descricao`, `inicio`, `fim` (nullable), `latitude`, `longitude`, `criado_em`, `atualizado_em`
Property: `duracao_minutos`

#### `FotoParada`
Campos: `parada` (FK→Parada, CASCADE), `foto`, `criado_em`
> Property `os` retorna `self.parada.os` (usado por `_foto_upload_path`).

#### `Incidente`
Campos: `os` (FK, CASCADE), `tipo` (acidente/tentativa_roubo/avaria_carga/pane_viatura/atividade_suspeita/outro), `gravidade` (baixa/media/alta/critica, default media), `descricao`, `ocorrido_em`, `latitude`, `longitude`, `bo_numero`, `criado_em`, `atualizado_em`

#### `FotoIncidente`
Campos: `incidente` (FK→Incidente, CASCADE), `foto`, `criado_em`
> Property `os` retorna `self.incidente.os`.

#### `FotoVeiculoEscoltado`
Campos: `veiculo` (FK→VeiculoEscoltado, CASCADE), `momento` (antes/depois/outro, default antes), `foto`, `criado_em`
> Property `os` retorna `self.veiculo.os`.

#### `TrocaMotorista`
Campos: `os` (FK, CASCADE), `veiculo_escoltado` (FK→VeiculoEscoltado, SET_NULL, nullable), `motorista_saindo`, `motorista_entrando`, `ocorrido_em`, `motivo`, `latitude`, `longitude`, `criado_em`

#### `FotoTrocaMotorista`
Campos: `troca` (FK→TrocaMotorista, CASCADE), `foto`, `criado_em`
> Property `os` retorna `self.troca.os`.

#### `AssinaturaOS`
Campos: `os` (FK, CASCADE), `tipo` (agente1/agente2/motorista/supervisor), `nome`, `imagem` (ImageField — gerada do canvas), `criado_em`
Restrição: `unique_together = [('os', 'tipo')]`

#### `DespesaOS`
Campos: `os` (FK, CASCADE), `tipo` (combustivel/refeicao/hospedagem/pedagio/estacionamento/outro), `natureza` (despesa/credito), `descricao`, `valor` (DecimalField), `comprovante` (ImageField, nullable), `ocorrido_em`, `criado_em`

### FATURAMENTO

#### `TabelaPreco`
Campos: `cliente` (FK→Cliente, PROTECT), `nome`, `tipo_viagem` (urbana/rodoviaria/administrativa/**todas**), `situacao` (ativo/inativo), `data_inclusao` (auto_now_add), `inicio_contrato`, `ultimo_reajuste`, `proximo_reajuste`, `valor_escolta`, `franquia_km`, `franquia_horas` (HHH:MM), `excedente_km`, `excedente_hora`, `cobrar_pedagio` (sim/nao), `pedagio_fixo`, `pedagio_percent`
Método: `franquia_horas_minutos()` → converte HHH:MM em minutos inteiros

#### `BoletimMedicao`
Campos: `os` (OneToOne→OrdemServico, CASCADE), `tabela` (FK→TabelaPreco, SET_NULL), `valor_escolta`, `franquia_km`, `franquia_horas` (HHH:MM), `excedente_km`, `excedente_hora`, `cobrar_pedagio`, `pedagio_fixo`, `pedagio_percent`, `km_realizado`, `horas_realizadas` (HHH:MM), `km_excedente`, `horas_excedentes` (HHH:MM), `valor_excedente_km`, `valor_excedente_hora`, `valor_pedagio`, `valor_total`, `km_trecho_chegada`, `observacoes`, `criado_em`, `atualizado_em`

---

## 🌐 URLs principais

### App principal (cadastros/urls.py)
```
/                          → dashboard
/agentes/                  → CRUD agentes
/viaturas/                 → CRUD viaturas
/rastreadores/             → CRUD rastreadores
/armamento/                → CRUD armamento
/coletes/                  → CRUD coletes
/clientes/                 → CRUD clientes
/operacional/equipes/      → CRUD equipes
/operacional/os/           → listagem OS
/operacional/os/nova/      → nova OS
/operacional/os/<pk>/      → detalhe OS (usa variáveis 'operacional' e 'op' no contexto)
/operacional/os/<pk>/print/
/operacional/os/<pk>/email/
/os/field/<uuid:token>/    → link externo do agente
```

### Sub-rotas AJAX do link externo (token)
- `foto-marco/` (POST), `foto-marco/<pk>/delete/`
- `parada/salvar/`, `parada/<pk>/delete/`
- `incidente/salvar/`, `incidente/<pk>/delete/`
- `foto-veiculo/`, `foto-veiculo/<pk>/delete/`
- `troca-motorista/salvar/`, `troca-motorista/<pk>/delete/`
- `assinatura/`
- `despesa/salvar/`, `despesa/<pk>/delete/`
- `veiculo/salvar/`, `veiculo/<pk>/delete/`

### URLs raiz (escolta_system/urls.py)
```python
# Serve arquivos de mídia em produção (DEBUG=False)
re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
```
⚠️ **Importante:** usar `re_path` com `serve` — o `static()` só funciona com `DEBUG=True`.

---

## 🔐 Permissões (permissoes.py)

```python
from .permissoes import developer_required, admin_required, is_developer, is_admin
```

| Nível | Acesso |
|---|---|
| `developer` | Total + usuário oculto nas listagens |
| `admin` | Total visível |
| `operador` | Acesso operacional comum |

Decorators: `@developer_required` (só developer), `@admin_required` (admin + developer).
Templates: `{% if request.user.perfil.is_developer %}` / `{% if request.user.perfil.is_admin %}`

---

## 🗑️ Comandos para limpeza de dados (banco do Railway)

### Conectar ao banco de produção
```powershell
cd "D:\Sistema Escolta\escolta_system"
$env:DATABASE_URL="postgresql://postgres:SENHA@HOST:PORTA/railway"
python manage.py shell
```
> A URL real está em: Railway → serviço Postgres → Variables → DATABASE_PUBLIC_URL

### Apagar tudo (ordem obrigatória)
```python
from cadastros.models import (Agente, OrdemServico, BoletimMedicao, Equipe,
                               FotoMarco, Parada, Incidente, DespesaOS,
                               AssinaturaOS, TrocaMotorista)
BoletimMedicao.objects.all().delete()
OrdemServico.objects.all().delete()  # cascade deleta OS e tudo vinculado
Equipe.objects.all().delete()
Agente.objects.all().delete()
```

### Apagar por categoria individual
```python
from cadastros.models import Agente
Agente.objects.all().delete()

from cadastros.models import OrdemServico
OrdemServico.objects.all().delete()

from cadastros.models import BoletimMedicao
BoletimMedicao.objects.all().delete()

from cadastros.models import Equipe
Equipe.objects.all().delete()

from cadastros.models import Cliente
Cliente.objects.all().delete()
```

### Apagar registro individual
```python
# Por nome
Agente.objects.filter(nome="NOME DO AGENTE").delete()

# Por CPF
Agente.objects.filter(cpf="000.000.000-00").delete()

# Por número da OS
OrdemServico.objects.filter(numero="20260001").delete()

# Por ID
OrdemServico.objects.filter(id=1).delete()

# Equipe pelo nome
Equipe.objects.filter(nome="BRAVA").delete()
```

### Consultar quantos registros existem
```python
from cadastros.models import Agente, OrdemServico, Equipe, BoletimMedicao
print("Agentes:", Agente.objects.count())
print("OS:", OrdemServico.objects.count())
print("Equipes:", Equipe.objects.count())
print("Boletins:", BoletimMedicao.objects.count())
```

### Interpretando resultados
- `(3, {'cadastros.Agente': 3})` → 3 registros deletados com sucesso
- `(0, {})` → tabela vazia ou banco errado (sem DATABASE_URL do Railway)
- `could not translate host name` → URL do banco incorreta
- `connection refused` → serviço Postgres offline no Railway

---

## 🚀 Deploy

```powershell
cd "D:\Sistema Escolta\escolta_system"
git add .
git commit -m "descrição da mudança"
git push
```
Acompanhar em: Railway → serviço web → Deployments → View Logs
Confirmar com: `Booting worker with pid` ✅

---

## 💾 Backup

```powershell
$env:Path = ";C:\Program Files\PostgreSQL\18\bin;" + $env:Path
pg_dump "DATABASE_PUBLIC_URL" -F c -f "D:\backup_escolta.dump"
```

### Restaurar
```powershell
pg_restore -d "DATABASE_PUBLIC_URL" --clean "D:\backup_escolta.dump"
```

---

## 🔄 Histórico de alterações

### Abril/2026
- **Tela de login:** animação CSS + logo JR via static file (em vez de base64).
- **Identidade visual:** renomeado de "Grupo JR" para **JR Segurança** em todos os templates, boletim export e OS print.
- **Clientes — Nome Fantasia:** campo `nome_fantasia` adicionado ao model. Busca automática de CNPJ no formulário de cadastro. Inativar em vez de excluir (campo `ativo`).
- **Aba Veículos no link externo:** agente pode cadastrar/excluir veículos escoltados diretamente no campo. Novas rotas: `veiculo/salvar/` e `veiculo/<pk>/delete/`.
- **Layout 100% responsivo:** refactor do `base.html` e `os_field_link.html` para mobile.
- **Logo via static file:** removido base64 inline, logo carregada via `{% static %}`.
- **Link externo expandido para 8 abas:** adicionadas fotos (marcos, veículos), paradas, incidentes, troca de motoristas, assinaturas digitais e despesas/créditos. Novos models: `FotoMarco`, `Parada`, `FotoParada`, `Incidente`, `FotoIncidente`, `FotoVeiculoEscoltado`, `TrocaMotorista`, `FotoTrocaMotorista`, `AssinaturaOS`, `DespesaOS`. Migration: `0022_despesaos_trocamotorista_parada_incidente_and_more`.
- **Foto de marco (link do agente):** limitado a 1 foto por etapa. Upload substitui a foto anterior — backend: `os_field_foto_marco` em `views.py` busca registro existente com `filter().first()`, deleta arquivo físico (`foto.delete(save=False)`) e reutiliza o registro; retorna `substituida: true/false` no JSON. Frontend (`os_field_link.html`): ao receber sucesso, remove todas as `.foto-thumb` do grid antes de inserir a nova; cooldown de 2 minutos no label/input usando `sessionStorage`, com contagem regressiva visível (`⏳ 119s`...). Arquivos alterados: `cadastros/views.py` e `cadastros/templates/cadastros/os_field_link.html`.
- **Painel de Avisos (Dashboard):** tela renomeada de "Dashboard" para "Painel de Avisos". Adicionada seção de alertas de vencimento com janela de 60 dias (2 meses). Exibe 3 cards: 🪪 CNH (agentes ativos com `cnh_validade ≤ hoje+60`), 🔫 CNV (agentes ativos com `cnv_validade ≤ hoje+60`), 🦺 Coletes (`validade ≤ hoje+60`). Badge **Vencida** (vermelho) se já passou, **Vence em X dias** (amarelo) se dentro do prazo. Quando tudo em dia exibe ✅. Arquivos alterados: `cadastros/views.py` (função `dashboard`) e `cadastros/templates/cadastros/dashboard.html`.
- **Volume persistente de mídia no Railway:** criado volume `web-volume` montado em `/app/media`. Variável de ambiente `MEDIA_ROOT=/app/media` adicionada no Railway. `settings.py` atualizado para ler `MEDIA_ROOT` via `os.environ.get()`. Fotos dos agentes e OS agora persistem entre deploys.
- **Serviço de mídia em produção:** `escolta_system/urls.py` atualizado para usar `re_path` com `django.views.static.serve` em vez de `static()` (que só funciona com `DEBUG=True`). Fotos acessíveis via `/media/...` em produção.
- **Fix contexto OS detalhe:** view `os_detalhe` agora passa `'op'` além de `'operacional'` no contexto do template. O template `os_detalhe.html` usa a variável `op` para exibir Data/Hora, KM e GPS dos marcos — sem esse fix os campos apareciam vazios mesmo com dados no banco.
- **Fix JS do link externo (getCookie + token):** o template `os_field_link.html` não tinha `getCookie` nem `const token` definidos no JavaScript, causando falha silenciosa ao salvar veículos escoltados. Adicionadas as definições no início do bloco `<script>`.
- **Fix encoding views.py:** labels da `MARCOS_LISTA` estavam com encoding corrompido (double-encoding UTF-8/latin-1) causando exibição de caracteres estranhos nos títulos das fotos na OS. Corrigido com script Python de substituição direta por codepoints unicode.
- **Aba Veículos — simplificação de fotos:** removida distinção "Fotos antes/após da escolta". Agora há apenas um botão 📷 **Foto** por veículo (momento fixo `antes`). Arquivo alterado: `cadastros/templates/cadastros/os_field_link.html`.
- **Aba Veículos — máscara de placa:** adicionada função `mascaraPlaca()` no JS do link externo. Campos Placa Cavalo, Placa Carreta e Placa Carreta 2 agora aplicam máscara automática `AAA-0000` conforme o agente digita.
- **Fix deploy Railway (13/04/2026):** resolvidos em sequência: (1) `STATIC_ROOT` ausente no `settings.py` → adicionado `STATIC_ROOT = BASE_DIR / 'staticfiles'`; (2) `gunicorn` não instalado → adicionado ao `requirements.txt`; (3) `CSRF_TRUSTED_ORIGINS` e `ALLOWED_HOSTS` ausentes → adicionados com domínio `grupojr.up.railway.app`; (4) `dj_database_url` e `psycopg2-binary` ausentes no `requirements.txt` → adicionados; (5) `settings.py` configurado para usar PostgreSQL via `DATABASE_URL` com fallback para SQLite local; (6) conflito de migrations (`DuplicateTable`) → resolvido com `--fake` no Start Command do Railway.
- **Migração de dados SQLite → PostgreSQL:** dados exportados do SQLite local via `dumpdata` com script Python (encoding UTF-8 forçado) e importados no PostgreSQL do Railway via `loaddata` com `DATABASE_URL` definida no ambiente.
- **Deploy 3b — remover `--fake` do Start Command (23/04/2026):** o Start Command antigo usava `migrate --fake` herdado de uma crise no Deploy inicial (13/04). Isso fazia com que QUALQUER migration nova entrasse como `FAKED` sem criar a tabela — descoberto quando a `0029_funcionariopatrimonial` foi deployada e bateu `relation does not exist` no primeiro GET. Fix: atualizado o Start Command para `python manage.py migrate && python manage.py collectstatic --noinput && gunicorn escolta_system.wsgi --log-file - --timeout 120 --workers 2` (sem `--fake`, com 2 workers e timeout 120s alinhados ao Procfile). A tabela `cadastros_funcionariopatrimonial` foi criada manualmente via SQL DDL no Data tab porque o registro já estava marcado como `FAKED` em `django_migrations`.
- **Deploy 4a — servir `/media/` em produção (23/04/2026):** fotos de agentes, funcionários patrimoniais, marcos de OS, paradas, incidentes, veículos, trocas, assinaturas e comprovantes apareciam como placeholder quebrado em produção. Causa raiz: (1) `urls.py` usava `static(settings.MEDIA_URL, ...)`, helper que **só funciona com `DEBUG=True`** — em produção o Django nem roteava `/media/*` (404); (2) `settings.py` tinha `MEDIA_ROOT` hardcoded (`BASE_DIR / 'media'`) ignorando a env var `MEDIA_ROOT=/app/media` já configurada no Railway. Fix: (1) `MEDIA_ROOT = os.environ.get('MEDIA_ROOT', str(BASE_DIR / 'media'))` no settings; (2) no `urls.py`, `if settings.DEBUG: static(...) else: re_path(r'^media/(?P<path>.*)$', django.views.static.serve, {'document_root': ...})`. **Insight crítico:** o volume `web-volume` (50 GB) do Railway está montado em `/app/media` e é persistente entre deploys — os arquivos físicos nunca foram embora, só não eram servidos. Após o deploy do fix, TODAS as fotos antigas voltaram automaticamente, zero re-upload necessário. **Atenção operacional:** NÃO clicar em `Wipe Volume` nem `Delete Volume` no painel Railway do web-volume — destrói todas as fotos sem backup.
- **Deploy 4b — fix gerador de número OS (24/04/2026):** erro `duplicate key value violates unique constraint "cadastros_ordemservico_numero_key"` ao tentar criar nova OS. Causa raiz: `OrdemServico.save()` em `cadastros/models.py` usava `.count()` dos registros do ano pra gerar o próximo número. Se alguma OS é deletada, `count()` fica menor que o maior número existente → colisão. Cenário real: só existia `20260002` em produção (a `20260001` foi deletada em algum momento); `count() = 1` → gerou `20260002` → DUPLICATE KEY. Fix: trocado `count()` por `aggregate(Max('numero'))` extraindo os 4 últimos dígitos e incrementando. Validado em produção: nova OS gerada como `20260003` (MAX era `20260002`). Limitação conhecida: race condition em alta concorrência simultânea não resolvida — se necessário no futuro, usar `select_for_update()` em transação.
- **Deploy 4c — fix ClienteForm salvando `ativo=False` (24/04/2026):** cliente novo cadastrado pelo form sumia imediatamente da lista. Causa raiz: `ClienteForm` em `cadastros/forms.py` incluía o campo `ativo` no `ModelForm`, mas o template `cliente_form.html` **não renderiza** o checkbox. No POST o campo não é enviado → Django interpreta como checkbox desmarcado → salva `ativo=False` → `cliente_list` (que filtra `ativo=True` por padrão) não mostra. Fix: adicionado `'ativo'` ao `exclude = [...]` do `ClienteForm.Meta`. Agora o campo nem chega ao form; o POST não toca nele; Django usa o default do model (`BooleanField(default=True)`) → cliente novo sai automaticamente ativo. A toggle ativo/inativo continua pela view dedicada `cliente_inativar` (botão vermelho na coluna Ações), independente do form. **Recuperação de dados em prod:** 1 cliente órfão (WILKER MONTALVAO, id=3) foi reativado via `UPDATE cadastros_cliente SET ativo = true WHERE id = 3;` no Data tab do Railway antes do merge. Em dev, reativados 2 clientes (WILKER + SMITH) via `Cliente.objects.filter(ativo=False).update(ativo=True)` no shell. Validado em produção: 2 clientes novos (JR SEGURANCA LTDA, JRS FACILITES LTDA) cadastrados após o deploy apareceram na lista como Ativo automaticamente.

---

## ⚠️ Regras importantes

1. **Nunca deletar** a pasta `cadastros/migrations/` manualmente
2. **Sempre fazer backup** antes de qualquer alteração grande no banco
3. **Ordem de exclusão:** Boletins → OS (cascade limpa tudo vinculado) → Equipes → Agentes
4. **Shell local usa SQLite** se `$env:DATABASE_URL` não estiver definida — delete `(0, {})` significa banco errado
5. **O migrate roda automaticamente** no Railway (está no Start Command)
6. **Credenciais padrão após migrations do zero:** admin_user / admin123
7. **Número da OS** é gerado automaticamente como `ANOxxxx` (ex: `20260001`) no método `save()` de `OrdemServico`
8. **Upload de fotos** salvas em `media/os_fotos/<numero_os>/<tipo_model>/<uuid>.ext` via `_foto_upload_path` — em produção o caminho base é `/app/media` (volume Railway)
9. **Link externo** (`os/field/<token>/`) não requer login — autenticado apenas pelo UUID token da `OSOperacional`
10. **`PerfilUsuario`** é criado automaticamente via signal `post_save` ao criar qualquer `User`
11. **Mídia em produção** usa `re_path` com `serve` no `urls.py` raiz — nunca usar `static()` com `DEBUG=False`
12. **Template os_detalhe.html** usa variável `op` (não `operacional`) para dados de execução da OS — a view deve passar ambas no contexto
13. **JS do link externo** requer `const token` e `function getCookie` definidos no início do bloco `<script>`