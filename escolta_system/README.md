# Sistema Operacional — Smith Segurança Privada

Sistema de gestão operacional para empresa de escolta armada.
Desenvolvido em Django + SQLite.

---

## Requisitos

- Python 3.8+
- pip

---

## Instalação e execução

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Criar o banco de dados e aplicar migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Criar o superusuário (acesso ao sistema)

```bash
python manage.py createsuperuser
```

Digite o usuário, e-mail (opcional) e senha quando solicitado.

### 4. Iniciar o servidor

```bash
python manage.py runserver
```

### 5. Acessar o sistema

Abra o navegador em: **http://127.0.0.1:8000**

---

## Módulos disponíveis (fase 1 — Cadastros)

| Módulo       | URL             | Descrição                              |
|--------------|-----------------|----------------------------------------|
| Dashboard    | /               | Painel resumo com totais               |
| Agentes      | /agentes/       | Cadastro de agentes de escolta         |
| Viaturas     | /viaturas/      | Cadastro da frota                      |
| Rastreadores | /rastreadores/  | Tecnologia de rastreamento (SASCAR...) |
| Armamento    | /armamento/     | Registro e custódia de armamento       |
| Clientes     | /clientes/      | Empresas contratantes                  |
| Admin        | /admin/         | Painel administrativo Django           |

---

## Estrutura do projeto

```
escolta_system/
├── manage.py
├── requirements.txt
├── README.md
├── escolta_system/          # Configurações Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── cadastros/               # App principal
    ├── models.py            # Agente, Viatura, Rastreador, Armamento, Cliente
    ├── views.py             # CRUD completo para cada módulo
    ├── forms.py             # Formulários Django
    ├── urls.py              # Rotas
    ├── admin.py             # Admin customizado
    └── templates/
        └── cadastros/
            ├── base.html
            ├── login.html
            ├── dashboard.html
            ├── agente_list.html / agente_form.html
            ├── viatura_list.html / viatura_form.html
            ├── rastreador_list.html / rastreador_form.html
            ├── armamento_list.html / armamento_form.html
            ├── cliente_list.html / cliente_form.html
            └── confirm_delete.html
```

---

## Próximos módulos (fase 2)

- **Operações / Folhas** — criação de ordens de serviço com agentes, viaturas, rotas
- **Motoristas escoltados** — dados dos motoristas e carretas
- **Atualização de status** — início/fim de viagem, chegada, km rodados
- **Relatórios** — PDF das folhas de operação

---

## Comandos úteis

```bash
# Resetar banco de dados
python manage.py flush

# Criar novo superusuário
python manage.py createsuperuser

# Gerar migrações após alterar models.py
python manage.py makemigrations && python manage.py migrate
```
