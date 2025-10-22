# Script para compartilhar o projeto com outros desenvolvedores

Write-Host "🐳 Eco Libras - Setup Docker" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan
Write-Host ""

# Verificar se Docker está instalado
Write-Host "Verificando Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker encontrado: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker não encontrado! Instale em: https://www.docker.com/get-started" -ForegroundColor Red
    exit 1
}

# Verificar se Docker Compose está instalado
Write-Host "Verificando Docker Compose..." -ForegroundColor Yellow
try {
    $composeVersion = docker-compose --version
    Write-Host "✅ Docker Compose encontrado: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Compose não encontrado!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Opções:" -ForegroundColor Cyan
Write-Host "1. Buildar e iniciar a aplicação"
Write-Host "2. Parar os containers"
Write-Host "3. Ver logs"
Write-Host "4. Limpar tudo (reset completo)"
Write-Host "5. Exportar banco de dados"
Write-Host "6. Importar banco de dados"
Write-Host "0. Sair"
Write-Host ""

$opcao = Read-Host "Escolha uma opção"

switch ($opcao) {
    "1" {
        Write-Host "🚀 Buildando e iniciando aplicação..." -ForegroundColor Green
        docker-compose up --build -d
        Write-Host ""
        Write-Host "✅ Aplicação rodando em http://localhost:5000" -ForegroundColor Green
        Write-Host "📊 Ver logs: docker-compose logs -f web" -ForegroundColor Yellow
    }
    "2" {
        Write-Host "⏹️  Parando containers..." -ForegroundColor Yellow
        docker-compose down
        Write-Host "✅ Containers parados" -ForegroundColor Green
    }
    "3" {
        Write-Host "📋 Mostrando logs (Ctrl+C para sair)..." -ForegroundColor Yellow
        docker-compose logs -f web
    }
    "4" {
        Write-Host "⚠️  ATENÇÃO: Isso vai remover todos os containers, volumes e imagens!" -ForegroundColor Red
        $confirmacao = Read-Host "Tem certeza? (s/n)"
        if ($confirmacao -eq "s") {
            docker-compose down -v --rmi all
            Write-Host "✅ Limpeza completa realizada" -ForegroundColor Green
        } else {
            Write-Host "Operação cancelada" -ForegroundColor Yellow
        }
    }
    "5" {
        Write-Host "💾 Exportando banco de dados..." -ForegroundColor Yellow
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $backupFile = "backup_$timestamp.db"
        Copy-Item "instance\data_bank.db" $backupFile
        Write-Host "✅ Backup salvo em: $backupFile" -ForegroundColor Green
    }
    "6" {
        Write-Host "📥 Importar banco de dados" -ForegroundColor Yellow
        $sourceFile = Read-Host "Digite o caminho do arquivo .db"
        if (Test-Path $sourceFile) {
            Copy-Item $sourceFile "instance\data_bank.db" -Force
            Write-Host "✅ Banco de dados importado com sucesso!" -ForegroundColor Green
            Write-Host "⚠️  Reinicie os containers para aplicar: docker-compose restart" -ForegroundColor Yellow
        } else {
            Write-Host "❌ Arquivo não encontrado: $sourceFile" -ForegroundColor Red
        }
    }
    "0" {
        Write-Host "👋 Até logo!" -ForegroundColor Cyan
        exit 0
    }
    default {
        Write-Host "❌ Opção inválida!" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "📖 Mais informações: DOCKER.md" -ForegroundColor Cyan
