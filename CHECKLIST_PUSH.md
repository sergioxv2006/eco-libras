# ✅ Checklist: Compartilhar Projeto no GitHub

## Antes de fazer push:

### 1. ✅ Verificar arquivos criados
- [ ] `Dockerfile` - Configuração do container
- [ ] `docker-compose.yml` - Orquestração de containers
- [ ] `.dockerignore` - Otimização do build
- [ ] `DOCKER.md` - Documentação Docker
- [ ] `COMPARTILHAMENTO.md` - Guia de compartilhamento
- [ ] `START_AQUI.md` - Guia para novos devs
- [ ] `.env.example` - Template de variáveis
- [ ] `.gitignore` - Atualizado para permitir banco
- [ ] `docker-helper.ps1` - Script auxiliar
- [ ] `README.md` - Atualizado com Docker

### 2. ✅ Criar arquivo .env (se não existir)
```powershell
Copy-Item .env.example .env
# Editar .env com suas credenciais reais
```

### 3. ✅ Testar Docker localmente
```powershell
# Buildar e rodar
docker-compose up --build

# Acessar http://localhost:5000 e testar:
# - Página inicial
# - Glossário
# - Admin (login)
# - Adicionar termo

# Se tudo OK, parar containers
docker-compose down
```

### 4. ✅ Verificar banco de dados
```powershell
# Verificar se existe
Test-Path instance\data_bank.db
# Deve retornar: True

# Verificar tamanho (deve ter dados)
(Get-Item instance\data_bank.db).Length
# Deve ser > 0 bytes
```

### 5. ✅ Adicionar ao Git

```powershell
# Ver status
git status

# Adicionar arquivos Docker
git add Dockerfile
git add docker-compose.yml
git add .dockerignore
git add docker-helper.ps1

# Adicionar documentação
git add DOCKER.md
git add COMPARTILHAMENTO.md
git add START_AQUI.md
git add README.md

# Adicionar exemplo de .env (SEM o .env real!)
git add .env.example

# Adicionar .gitignore atualizado
git add .gitignore

# IMPORTANTE: Adicionar banco de dados (apenas para dev!)
git add instance/data_bank.db
```

### 6. ✅ Commit e Push

```powershell
# Commit
git commit -m "feat: Adicionar configuração Docker e banco compartilhado

- Dockerfile para containerização
- docker-compose.yml para orquestração
- Documentação completa (DOCKER.md, COMPARTILHAMENTO.md, START_AQUI.md)
- Script auxiliar docker-helper.ps1
- Banco de dados incluído para desenvolvimento colaborativo
- .gitignore atualizado
- README.md atualizado com instruções Docker"

# Push para o GitHub
git push origin branch-paulo
```

---

## 📧 Compartilhar com outros Devs:

Envie para eles:

```
Olá! 👋

O projeto Eco Libras agora está pronto para colaboração com Docker!

🔗 GitHub: https://github.com/sergioxv2006/eco-libras
📂 Branch: branch-paulo

Para começar, siga o guia rápido:
👉 START_AQUI.md

Documentação completa:
- DOCKER.md - Setup Docker
- COMPARTILHAMENTO.md - Como compartilhar dados
- README.md - Visão geral do projeto

Qualquer dúvida, me chama! 🚀
```

---

## 🎯 Após o push

### Os Devs devem fazer:

```powershell
# 1. Clonar
git clone https://github.com/sergioxv2006/eco-libras.git
cd eco-libras

# 2. Checkout na branch certa
git checkout branch-paulo

# 3. Rodar Docker
docker-compose up --build

# 4. Acessar
# http://localhost:5000
```

---

## ⚠️ Avisos Importantes

### ✅ OK para DESENVOLVIMENTO:
- Incluir banco SQLite com dados de exemplo
- Compartilhar via Git
- Usar Docker Compose

### ❌ NUNCA em PRODUÇÃO:
- Banco de dados no Git com dados reais
- Credenciais no código
- SQLite para apps com muitos usuários

---

## 🔄 Atualizações futuras

Quando fizer mudanças no banco:

```powershell
# 1. Fazer mudanças no site (adicionar termos, etc.)

# 2. Commitar banco atualizado
git add instance/data_bank.db
git commit -m "update: Adicionar novos termos ao glossário"
git push

# 3. Avisar o time para fazer pull
# Eles fazem: git pull origin branch-paulo
# E depois: docker-compose restart
```

---

## ✨ Pronto!

Agora seu projeto está pronto para colaboração! 🎉

Seu amigo pode clonar, buildar e rodar com apenas 3 comandos.
