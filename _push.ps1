# _push.ps1 — Pipeline completo: graphify → commit → push → deploy Railway
#
# USO:
#   .\_push.ps1                          # pede a mensagem interativamente
#   .\_push.ps1 "feat: minha mudança"    # passa a mensagem como argumento
#
# O script faz, na ordem:
#   1. Remove locks do git (problema comum no Windows)
#   2. git read-tree HEAD  (sincroniza o index com HEAD — evita ruído)
#   3. git add -A          (stageia todas as mudanças)
#   4. graphify update .   (atualiza o grafo do projeto)
#   5. git add graphify-out/ (stageia o grafo atualizado)
#   6. git commit          (com a mensagem fornecida)
#   7. git push origin main → dispara deploy automático no Railway

param(
    [string]$Msg = ""
)

$ErrorActionPreference = "Stop"
$RepoDir = "D:\Sistema Escolta"

Set-Location $RepoDir

Write-Host ""
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor DarkCyan
Write-Host "  Sistema Escolta — pipeline de deploy" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor DarkCyan
Write-Host ""

# ── 1. Remover locks ─────────────────────────────────────────────────────
Write-Host "[1/6] Removendo locks do git..." -ForegroundColor Yellow
Remove-Item ".git\index.lock"            -Force -ErrorAction SilentlyContinue
Remove-Item ".git\HEAD.lock"             -Force -ErrorAction SilentlyContinue
Remove-Item ".git\refs\heads\main.lock"  -Force -ErrorAction SilentlyContinue
Write-Host "      OK" -ForegroundColor Green

# ── 2. Sincronizar index com HEAD ─────────────────────────────────────────
Write-Host "[2/6] Sincronizando index (git read-tree HEAD)..." -ForegroundColor Yellow
git read-tree HEAD
if ($LASTEXITCODE -ne 0) {
    Write-Host "      AVISO: git read-tree falhou — continuando mesmo assim." -ForegroundColor DarkYellow
}
Write-Host "      OK" -ForegroundColor Green

# ── 3. Staging das alterações de código ──────────────────────────────────
Write-Host "[3/6] Staging das alterações (git add -A)..." -ForegroundColor Yellow
git add -A
if ($LASTEXITCODE -ne 0) { Write-Host "ERRO no git add" -ForegroundColor Red; exit 1 }
Write-Host "      OK" -ForegroundColor Green

# ── 4. Graphify update ───────────────────────────────────────────────────
Write-Host "[4/6] Atualizando grafo do projeto (graphify)..." -ForegroundColor Yellow
$graphifyOK = $false
try {
    & graphify update . 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) { $graphifyOK = $true }
} catch {
    # graphify não instalado ou falhou
}

if ($graphifyOK) {
    git add graphify-out/ 2>&1 | Out-Null
    Write-Host "      Grafo atualizado." -ForegroundColor Green
} else {
    Write-Host "      graphify nao encontrado ou falhou — grafo nao atualizado." -ForegroundColor DarkYellow
}

# ── 5. Verificar se há algo para commitar ────────────────────────────────
$statusLines = git status --porcelain
if (-not $statusLines) {
    Write-Host ""
    Write-Host "  Nada para commitar. Repositorio limpo." -ForegroundColor DarkYellow
    Write-Host ""
    exit 0
}

Write-Host ""
Write-Host "  Arquivos modificados:" -ForegroundColor Cyan
git status --short
Write-Host ""

# ── 6. Mensagem do commit ─────────────────────────────────────────────────
if (-not $Msg) {
    $Msg = Read-Host "[5/6] Mensagem do commit"
    if (-not $Msg) {
        $Msg = "chore: update $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
        Write-Host "      Usando mensagem automatica: $Msg" -ForegroundColor DarkYellow
    }
}

git commit -m $Msg
if ($LASTEXITCODE -ne 0) { Write-Host "ERRO no git commit" -ForegroundColor Red; exit 1 }
Write-Host "      Commit criado." -ForegroundColor Green

# ── 7. Push → Railway ────────────────────────────────────────────────────
Write-Host "[6/6] Enviando para Railway (git push)..." -ForegroundColor Yellow
git push origin main
if ($LASTEXITCODE -ne 0) { Write-Host "ERRO no git push" -ForegroundColor Red; exit 1 }

Write-Host ""
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor DarkGreen
Write-Host "  Deploy iniciado com sucesso!" -ForegroundColor Green
Write-Host "  Producao: https://grupojr.up.railway.app" -ForegroundColor Green
Write-Host "  Railway:  https://railway.app/dashboard" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor DarkGreen
Write-Host ""
