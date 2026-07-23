<!-- converted from Manual_Developer_GrupoJR_v3.docx -->

📘 MANUAL DO DESENVOLVEDOR
Sistema de Escolta — Grupo JR
Guia Completo para Iniciantes
📋 ÍNDICE
1️⃣ Seção 1 — Conceitos Essenciais
Antes de mexer em qualquer arquivo, entenda o que cada peça do sistema faz:
2️⃣ Seção 2 — Estrutura do Projeto
Seu projeto está na pasta: D:\Sistema Escolta\escolta_system
3️⃣ Seção 3 — O que foi implementado
Nesta versão o link do agente foi completamente expandido. Agora ele tem 7 abas completas:
🗂️ Novas abas do link do agente
🗄️ Novos models no banco de dados
4️⃣ Seção 4 — Como aplicar mudanças no projeto
📋 Arquivos que foram entregues e onde colocar
🔄 Passo a passo após substituir os arquivos
1.  Substitua os 4 arquivos nas pastas corretas.
2.  Abra o PowerShell e entre na pasta do projeto:
cd "D:\Sistema Escolta\escolta_system"
3.  Gere as migrations:
python manage.py makemigrations
4.  Aplique as migrations localmente:
python manage.py migrate
5.  Teste no servidor local:
python manage.py runserver
6.  Se tudo funcionar, faça o deploy (seção 6).
5️⃣ Seção 5 — Git e GitHub
Git é um sistema de versionamento — ele registra cada mudança que você faz no código. GitHub é onde esse histórico fica guardado na nuvem.
Comandos essenciais do dia a dia
Ver o que mudou:
git status
Preparar todos os arquivos modificados:
git add .
Registrar as mudanças com uma descrição:
git commit -m "descrição do que você fez"
Enviar para o GitHub (e acionar o deploy no Railway):
git push
Erros comuns no Git
6️⃣ Seção 6 — Deploy no Railway
Deploy é o processo de publicar uma versão nova do sistema na internet. No seu caso, acontece automaticamente quando você faz git push.
Fluxo completo de um deploy
1.  Faça suas alterações no código.
2.  Abra o PowerShell e entre na pasta:
cd "D:\Sistema Escolta\escolta_system"
3.  Adicione os arquivos:
git add .
4.  Faça o commit:
git commit -m "descrição da mudança"
5.  Envie para o GitHub:
git push
6.  O Railway detecta automaticamente e inicia o deploy.
7.  Acompanhe em: Railway → serviço web → Deployments → View Logs.
8.  Aguarde aparecer: Booting worker with pid — significa que subiu! ✅
Start Command do Railway
Este comando fica em: Railway → serviço web → Settings → Deploy → Custom Start Command
python manage.py collectstatic --noinput && python manage.py migrate && gunicorn escolta_system.wsgi:application --bind 0.0.0.0:$PORT
7️⃣ Seção 7 — Banco de Dados PostgreSQL
O banco PostgreSQL fica no Railway, no serviço Postgres. O Django se conecta a ele através da variável de ambiente DATABASE_URL.
O que são Migrations?
Migrations são arquivos que descrevem mudanças no banco. Sempre que você altera um model (models.py), precisa criar e aplicar uma migration.
Criar migration depois de alterar models.py:
python manage.py makemigrations
Aplicar as migrations no banco:
python manage.py migrate
Variáveis de ambiente importantes
🗑️ Seção 8 — Limpeza de Dados
Esta seção explica como excluir dados do banco de produção (Railway) de forma segura, seja por categoria completa ou individualmente.
📡 Passo 1 — Conectar ao banco do Railway
Como o banco de produção fica no Railway, você precisa informar a URL do banco antes de abrir o shell Django.
1.1  No Railway → serviço Postgres → Variables → copie o valor de DATABASE_PUBLIC_URL
1.2  No PowerShell, execute os 3 comandos abaixo em ordem:
cd "D:\Sistema Escolta\escolta_system"
$env:DATABASE_URL="postgresql://postgres:SUA_SENHA@SEU_HOST:PORTA/railway"
python manage.py shell
🗂️ Passo 2 — Excluir por categoria (tudo de uma vez)
Cole os comandos abaixo dentro do shell Django conforme o que deseja apagar:

▶ Apagar TUDO (Boletins + OS + Equipes + Agentes)
from cadastros.models import Agente, OrdemServico, BoletimMedicao, Equipe
BoletimMedicao.objects.all().delete()
OrdemServico.objects.all().delete()
Equipe.objects.all().delete()
Agente.objects.all().delete()
print("✅ Tudo apagado!")

▶ Apagar apenas Agentes
from cadastros.models import Agente
Agente.objects.all().delete()

▶ Apagar apenas Ordens de Serviço
from cadastros.models import OrdemServico
OrdemServico.objects.all().delete()

▶ Apagar apenas Boletins de Medição
from cadastros.models import BoletimMedicao
BoletimMedicao.objects.all().delete()

▶ Apagar apenas Equipes
from cadastros.models import Equipe
Equipe.objects.all().delete()

▶ Apagar apenas Clientes
from cadastros.models import Cliente
Cliente.objects.all().delete()

🎯 Passo 3 — Excluir registro individual
Para excluir apenas um registro específico, use o ID ou outro campo identificador:

▶ Excluir agente pelo nome
from cadastros.models import Agente
Agente.objects.filter(nome="NOME DO AGENTE").delete()

▶ Excluir agente pelo CPF
from cadastros.models import Agente
Agente.objects.filter(cpf="000.000.000-00").delete()

▶ Excluir OS pelo número
from cadastros.models import OrdemServico
OrdemServico.objects.filter(numero="OS-20260001").delete()

▶ Excluir OS pelo ID
from cadastros.models import OrdemServico
OrdemServico.objects.filter(id=1).delete()

▶ Excluir equipe pelo nome
from cadastros.models import Equipe
Equipe.objects.filter(nome="BRAVA").delete()

▶ Consultar antes de excluir (verificar o que existe)
from cadastros.models import Agente, OrdemServico, Equipe, BoletimMedicao
print("Agentes:", Agente.objects.count())
print("OS:", OrdemServico.objects.count())
print("Equipes:", Equipe.objects.count())
print("Boletins:", BoletimMedicao.objects.count())

🚪 Passo 4 — Sair do shell
Após executar os comandos, saia do shell com:
exit()
9️⃣ Seção 9 — Backup do Banco de Dados
Passo a passo do backup
Passo 1 — Adicionar PostgreSQL ao PATH (toda vez que abrir o terminal):
$env:Path = ";C:\Program Files\PostgreSQL\18\bin;" + $env:Path
Passo 2 — Confirmar que o pg_dump está funcionando:
pg_dump --version
Deve aparecer: pg_dump (PostgreSQL) 18.x
Passo 3 — Copiar a DATABASE_PUBLIC_URL no Railway → serviço Postgres → Variables → ⋮ → Copy Value
Passo 4 — Executar o backup:
pg_dump "postgresql://usuario:senha@host:porta/railway" -F c -f "D:\backup_escolta.dump"
Se o terminal voltar ao prompt sem erro: backup feito com sucesso! ✅
Como restaurar um backup
pg_restore -d "postgresql://usuario:senha@host:porta/railway" --clean "D:\backup_escolta.dump"
🔟 Seção 10 — Problemas Comuns e Soluções
1️⃣1️⃣ Seção 11 — Checklist Completo de Deploy
Use esta lista antes de cada deploy importante:
| Versão 3.0 • Abril 2026
Django + PostgreSQL + Railway + GitHub |
| --- |
| Seção | Conteúdo |
| --- | --- |
| 1. Conceitos Essenciais | O que é cada tecnologia usada |
| 2. Estrutura do Projeto | Como os arquivos estão organizados |
| 3. O que foi implementado | Funcionalidades novas do sistema |
| 4. Como aplicar mudanças | Passo a passo para substituir arquivos |
| 5. Git e GitHub | Versionamento e envio de código |
| 6. Deploy no Railway | Como publicar o sistema online |
| 7. Banco de Dados | Migrations e gestão de dados |
| 8. Limpeza de Dados | Como excluir dados por categoria ou individualmente |
| 9. Backup do Banco | Como proteger seus dados |
| 10. Problemas Comuns | Erros frequentes e soluções |
| 11. Checklist de Deploy | Passo a passo completo |
| 🔧 Tecnologia | O que faz no seu projeto |
| --- | --- |
| 🐍 Django | Framework Python que cria o site, as páginas, o banco de dados e as rotas de URL. |
| 🐘 PostgreSQL | Banco de dados onde ficam salvos todos os dados: agentes, OS, clientes, usuários. |
| 🚂 Railway | Servidor na nuvem onde o site fica publicado e acessível pela internet. |
| 🐙 GitHub | Repositório onde o código-fonte fica guardado e versionado (histórico de mudanças). |
| 🦄 Gunicorn | Servidor web que roda o Django em produção (mais robusto que o runserver). |
| ⬜ WhiteNoise | Biblioteca que serve os arquivos estáticos (CSS, JS, imagens) em produção. |
| 🔗 dj-database-url | Converte a URL do banco PostgreSQL para o formato que o Django entende. |
| 💡 Resumindo o fluxo: Você escreve o código → sobe para o GitHub → o Railway pega do GitHub e publica automaticamente na internet. |
| --- |
| 📁 Arquivo / Pasta | Para que serve |
| --- | --- |
| escolta_system/settings.py | Configurações do projeto: banco, apps instalados, idioma, etc. |
| escolta_system/urls.py | URLs principais do projeto (raiz). |
| cadastros/models.py | Define as tabelas do banco. Inclui os novos models de campo. |
| cadastros/views.py | Lógica de cada página. Inclui as views AJAX do link do agente. |
| cadastros/urls.py | Rotas do app. Inclui as 14 novas rotas do link de campo. |
| cadastros/migrations/ | Histórico de mudanças no banco. NUNCA delete manualmente. |
| cadastros/templates/ | Arquivos HTML das páginas. Inclui o novo os_field_link.html. |
| requirements.txt | Lista de pacotes Python necessários. |
| manage.py | Ferramenta de linha de comando do Django. |
| Aba | O que o agente pode fazer |
| --- | --- |
| ⏱ Marcos | Registrar horários e KM de início/chegada/término. Com foto por marco. |
| 🅿️ Paradas | Registrar paradas com motivo (abastecimento, refeição, mecânica...), horário, localização e fotos. |
| ⚠️ Incidentes | Registrar ocorrências com tipo, gravidade (baixa/média/alta/crítica), descrição, BO e fotos. |
| 🚛 Veículos | Tirar fotos do veículo escoltado antes e depois da escolta. |
| 🔄 Motoristas | Registrar troca de motorista com dados de quem saiu e quem entrou, com fotos de CNH. |
| 💰 Despesas | Registrar despesas e créditos (combustível, pedágio, refeição) com foto do comprovante. |
| ✍️ Assinaturas | Capturar assinatura digital via canvas touch do agente e do motorista escoltado. |
| Model (tabela) | O que armazena |
| --- | --- |
| FotoMarco | Fotos tiradas em cada marco operacional (início/chegada/término). |
| Parada | Registros de paradas durante a OS (motivo, horário, localização). |
| FotoParada | Fotos vinculadas a cada parada. |
| Incidente | Ocorrências durante a OS (tipo, gravidade, descrição, BO). |
| FotoIncidente | Fotos vinculadas a cada incidente. |
| FotoVeiculoEscoltado | Fotos do veículo escoltado (antes/depois). |
| TrocaMotorista | Registro de troca de motorista durante a OS. |
| FotoTrocaMotorista | Fotos da troca de motorista (CNH, rosto). |
| AssinaturaOS | Assinatura digital capturada via canvas touch. |
| DespesaOS | Despesas e créditos registrados pelo agente. |
| Arquivo recebido | Substitui / vai em |
| --- | --- |
| models.py | cadastros/models.py → substitui o arquivo inteiro |
| views.py | cadastros/views.py → substitui o arquivo inteiro |
| urls.py | cadastros/urls.py → substitui o arquivo inteiro |
| os_field_link.html | cadastros/templates/cadastros/os_field_link.html → substitui o arquivo inteiro |
| ✅ Esses arquivos já estão prontos para substituição direta. Não é necessário copiar e colar trecho por trecho. Basta substituir o arquivo inteiro pelo novo. |
| --- |
| ⚠️ O migrate roda automaticamente no Railway durante o deploy. Mas rode localmente primeiro para garantir que não há erros antes de subir. |
| --- |
| ⚠️ Sempre faça o git add e commit DENTRO da pasta correta: D:\Sistema Escolta\escolta_system |
| --- |
| Mensagem de Erro | O que significa | Solução |
| --- | --- | --- |
| nothing to commit, working tree clean | Nenhum arquivo foi alterado. | Verifique se está na pasta certa. |
| modified: escolta_system (modified content) | O projeto é um submódulo Git. | Entre na pasta interna e faça o commit de lá. |
| Everything up-to-date | O GitHub já tem o código mais recente. | O push foi ignorado. Não há problema. |
| error: failed to push some refs | Alguém fez mudanças no GitHub. | Rode git pull antes do git push. |
| Parte do comando | O que faz |
| --- | --- |
| collectstatic --noinput | Copia CSS, JS e imagens para a pasta staticfiles. |
| migrate | Aplica mudanças no banco de dados automaticamente. |
| gunicorn ... --bind | Inicia o servidor web na porta correta. |
| ✅ Configuração atual: O settings.py lê a variável DATABASE_URL automaticamente. Se ela existir, usa PostgreSQL. Se não (ambiente local), usa SQLite. |
| --- |
| ⚠️ No Railway, o migrate roda automaticamente no deploy (está no Start Command). Localmente, você precisa rodar manualmente. |
| --- |
| Variável | Para que serve |
| --- | --- |
| DATABASE_URL | URL de conexão ao PostgreSQL. Configurada como ${Postgres.DATABASE_URL} no serviço web. |
| DATABASE_PUBLIC_URL | URL externa do banco. Usada para conectar de fora do Railway (ex: pg_dump local). |
| SECRET_KEY | Chave secreta do Django. Nunca compartilhe ou coloque no código-fonte. |
| DEBUG | Define se o Django mostra erros detalhados. Em produção deve ser False. |
| 🔴 IMPORTANTE: Sempre faça backup antes de excluir qualquer dado! Execute o backup da Seção 9 antes de continuar. |
| --- |
| ⚠️ Substitua a URL pelo valor real copiado do Railway. Sem isso, o shell vai usar o banco local (SQLite) e os dados de produção não serão afetados. |
| --- |
| ⚠️ A ordem de exclusão importa! Sempre apague primeiro os itens que dependem de outros: Boletins → OS → Equipes → Agentes. Apagar na ordem errada pode gerar erros de integridade. |
| --- |
| Resultado | O que significa |
| --- | --- |
| (3, {'cadastros.Agente': 3}) | 3 agentes foram deletados com sucesso. |
| (0, {}) | Nenhum registro encontrado — tabela já estava vazia ou banco errado. |
| OperationalError: could not translate host name | A DATABASE_URL está incorreta. Verifique a URL do Railway. |
| OperationalError: connection refused | Banco inacessível. Verifique se o serviço Postgres está ativo no Railway. |
| 🔴 REGRA DE OURO: Sempre faça backup ANTES de qualquer alteração grande, antes de recriar serviços no Railway, ou pelo menos uma vez por semana. |
| --- |
| 💡 Salve o arquivo .dump também no Google Drive ou pendrive para ter uma cópia extra fora do computador. |
| --- |
| Problema | Causa | Solução |
| --- | --- | --- |
| Site mostra 'Service Unavailable' | Gunicorn não iniciou ou crashou. | Ver logs em Deployments → View Logs e corrigir o erro indicado. |
| ModuleNotFoundError: No module named X | Pacote faltando no requirements.txt. | Adicionar o pacote no requirements.txt e fazer git push. |
| Dados somem após deploy | Banco foi recriado ou migration rodou do zero. | Fazer backup antes de deploys grandes. Nunca recriar o serviço Postgres sem necessidade. |
| pg_dump version mismatch | Versão do pg_dump diferente do servidor. | Instalar a versão correta do PostgreSQL Tools (mesma do servidor Railway). |
| collectstatic KeyError | Erro no settings.py ou pacote faltando. | Verificar se whitenoise e dj-database-url estão no requirements.txt. |
| Login não funciona após deploy | Usuários foram recriados pelas migrations. | Usar credenciais padrão: admin_user / admin123 e depois alterar a senha. |
| git push não ativa o deploy | Branch errada ou repositório desconectado. | Verificar em Railway → Settings → Source se o GitHub está conectado na branch main. |
| Foto não aparece após upload | MEDIA_ROOT ou MEDIA_URL não configurado. | Confirmar no settings.py: MEDIA_URL = '/media/' e MEDIA_ROOT = BASE_DIR / 'media'. |
| Erro 500 ao abrir link do agente | Migration não foi aplicada no Railway. | Verificar logs do Railway. O migrate roda no Start Command automaticamente no deploy. |
| delete() retorna (0, {}) | Shell local está usando SQLite, não o Railway. | Definir $env:DATABASE_URL com a URL real do Railway antes de abrir o shell. |
| could not translate host name | DATABASE_URL com valor de exemplo/errado. | Copiar a URL real em Railway → Postgres → Variables → DATABASE_PUBLIC_URL. |
|  | Ação |
| --- | --- |
| ☐ | Fazer backup do banco antes de começar. |
| ☐ | Verificar se todos os arquivos novos foram colocados nas pastas corretas. |
| ☐ | Abrir o PowerShell na pasta: D:\Sistema Escolta\escolta_system |
| ☐ | Rodar: python manage.py makemigrations (se alterou models.py) |
| ☐ | Rodar: python manage.py migrate (localmente primeiro) |
| ☐ | Testar localmente: python manage.py runserver |
| ☐ | Rodar: git status (verificar quais arquivos mudaram) |
| ☐ | Rodar: git add . |
| ☐ | Rodar: git commit -m "descrição clara do que foi feito" |
| ☐ | Rodar: git push |
| ☐ | Acessar Railway → serviço web → Deployments |
| ☐ | Aguardar o deploy ficar Active (verde) |
| ☐ | Clicar em View Logs e verificar se aparece 'Booting worker' |
| ☐ | Acessar o site e testar as funcionalidades alteradas |
| ☐ | Fazer backup após confirmar que está tudo funcionando |
| 📌 REFERÊNCIA RÁPIDA — COMANDOS MAIS USADOS
Entrar na pasta do projeto:
cd "D:\Sistema Escolta\escolta_system"
Deploy completo:
git add . && git commit -m "sua mensagem" && git push
Conectar ao banco do Railway (limpeza de dados):
$env:DATABASE_URL="postgresql://postgres:SENHA@HOST:PORTA/railway"
python manage.py shell
Backup do banco:
$env:Path = ";C:\Program Files\PostgreSQL\18\bin;" + $env:Path
pg_dump "DATABASE_PUBLIC_URL" -F c -f "D:\backup_escolta.dump" |
| --- |