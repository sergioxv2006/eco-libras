# 🤝 Guia de Compartilhamento - Eco Libras

Este guia explica como compartilhar o projeto e o banco de dados com outros desenvolvedores.

## 📦 Opções de Compartilhamento

### Opção 1: Via GitHub (Recomendado)

#### Para o desenvolvedor original:

```powershell
# 1. Adicionar arquivos Docker ao Git
git add Dockerfile docker-compose.yml .dockerignore DOCKER.md

# 2. Adicionar o banco de dados (CUIDADO: apenas para desenvolvimento!)
git add instance/data_bank.db

# 3. Commit e push
git commit -m "Adicionar configuração Docker e banco de dados"
git push origin main
```

#### Para outros desenvolvedores:

```powershell
# 1. Clonar o repositório
git clone https://github.com/sergioxv2006/eco-libras.git
cd eco-libras

# 2. Iniciar com Docker
docker-compose up --build

# Pronto! O banco de dados já vem junto no repositório
```

---

### Opção 2: Via Docker Hub (Público)

#### Publicar imagem:

```powershell
# 1. Fazer login no Docker Hub
docker login

# 2. Buildar a imagem com tag
docker build -t seu-usuario/eco-libras:latest .

# 3. Fazer push
docker push seu-usuario/eco-libras:latest
```

#### Atualizar docker-compose.yml:

```yaml
services:
  web:
    image: seu-usuario/eco-libras:latest  # Usar imagem publicada
    # Remover a linha 'build: .'
```

#### Outros desenvolvedores:

```powershell
# Apenas fazer pull e rodar
docker-compose pull
docker-compose up
```

---

### Opção 3: Via Arquivo Compartilhado (Google Drive, Dropbox, etc.)

#### Você:

```powershell
# 1. Criar backup do banco
Copy-Item instance\data_bank.db eco-libras-db-backup.db

# 2. Compartilhar via Google Drive/Dropbox
# Compartilhe o arquivo 'eco-libras-db-backup.db'
```

#### Outros desenvolvedores:

```powershell
# 1. Clonar o repo (sem o banco)
git clone https://github.com/sergioxv2006/eco-libras.git
cd eco-libras

# 2. Baixar o banco compartilhado e colocar na pasta instance
# Criar pasta se não existir
New-Item -ItemType Directory -Force -Path instance
Copy-Item C:\Downloads\eco-libras-db-backup.db instance\data_bank.db

# 3. Rodar com Docker
docker-compose up --build
```

---

## 🔄 Sincronização de Dados

### Atualizar banco de dados de outros devs:

```powershell
# 1. Você faz mudanças no banco e committa
git add instance/data_bank.db
git commit -m "Atualizar banco: novos termos adicionados"
git push

# 2. Outros devs fazem pull
git pull

# 3. Reiniciar Docker para aplicar
docker-compose restart
```

### Criar backup antes de atualizar:

```powershell
# Sempre faça backup antes de sobrescrever
Copy-Item instance\data_bank.db instance\data_bank.db.backup
git pull
```

---

## ⚠️ Avisos Importantes

### 🔴 NÃO faça isso em PRODUÇÃO:
- Nunca versione banco de dados com dados reais de usuários no Git
- Use variáveis de ambiente para credenciais sensíveis

### ✅ Boas práticas para desenvolvimento:
- Use um banco "seed" (dados de exemplo) para compartilhar
- Use migrations (Flask-Migrate) para sincronizar schemas

---

## 🛠️ Comandos Úteis

### Exportar/Importar banco:

```powershell
# Exportar (fazer backup)
Copy-Item instance\data_bank.db backup_$(Get-Date -Format yyyyMMdd).db

# Importar (restaurar backup)
Copy-Item backup_20250122.db instance\data_bank.db
docker-compose restart
```

### Resetar banco (começar do zero):

```powershell
# Apagar banco atual
Remove-Item instance\data_bank.db

# Recriar banco vazio
docker-compose up
# O Flask vai criar automaticamente as tabelas vazias
```

### Verificar diferenças no banco:

```powershell
# Ver se há mudanças não commitadas
git status instance/

# Ver diferenças (binário, então não mostra conteúdo)
git diff instance/data_bank.db
```

---

## 📞 Suporte

Se outros desenvolvedores tiverem problemas:

1. **Banco não aparece**: Verificar se `instance/data_bank.db` existe
2. **Permissões negadas**: Rodar como administrador (Windows) ou com `sudo` (Linux/Mac)
3. **Porta 5000 ocupada**: Mudar porta no `docker-compose.yml` (linha `"5000:5000"`)

---

## 🎓 Próximos Passos

Para projetos maiores, considere:

- **PostgreSQL**: Banco relacional robusto
- **Docker Volumes**: Para persistência melhor
- **CI/CD**: GitHub Actions para deploy automático
- **Migrations**: Versionamento de schema do banco

Veja: `DOCKER.md` para mais detalhes técnicos.
