## Olá! Bem-vindo ao projeto Eco Libras 👋

Este é um guia super rápido para você começar a trabalhar no projeto.

---

## ⚡ Opção Rápida (Docker - Recomendado)

### Pré-requisitos:
1. Instalar [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. Instalar [Git](https://git-scm.com/downloads)

### Passos:

```powershell
# 1. Clonar o projeto
git clone https://github.com/sergioxv2006/eco-libras.git
cd C:\Users\seu_nome_de_usuário\eco-libras

# 2. Para e remove containers e redes, e limpa tudo o que foi criado
docker-compose down

# 3. Força o Docker a reconstruir todas as imagens do seu projeto do zero
docker compose build --no-cache

# 4. Reconstrói o que mudou e depois sobe os containers
docker-compose up --build

# 5. Abrir no navegador
# http://localhost:5000
```

**Pronto! 🎉** O banco de dados já vem configurado e populado com dados de exemplo.

---

## 🐌 Opção Manual (Sem Docker)

### Pré-requisitos:
1. Python 3.11+ instalado
2. Git instalado

### Passos:

```powershell
# 1. Clonar o projeto
git clone https://github.com/sergioxv2006/eco-libras.git
cd C:\Users\seu_nome_de_usuário\eco-libras

# 2. Criar ambiente virtual
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Rodar o projeto
python -m APP.run (fora da pasta APP)

# 5. Abrir no navegador
# http://localhost:5000
```

---

## 📂 Estrutura do Projeto

```
eco-libras/
├── APP/                    # Código da aplicação Flask
│   ├── templates/          # HTML (páginas web)
│   ├── static/             # CSS, JS, imagens
│   ├── models.py           # Modelos do banco de dados
│   └── routes.py           # Rotas da API
├── instance/               # Banco de dados SQLite
│   └── data_bank.db        # **BANCO COMPARTILHADO**
├── run.py                  # Arquivo principal
└── requirements.txt        # Dependências Python
```

---

## 🔑 Acesso Admin

- **URL**: http://localhost:5000/admin
- **Usuário**: (verifique o arquivo `.env`)
- **Senha**: (verifique o arquivo `.env`)

---

## 🛠️ Comandos Úteis

### Com Docker:

```powershell
# Ver logs
docker-compose logs -f

# Parar containers
docker-compose down

# Reiniciar
docker-compose restart

# Limpar tudo e recomeçar
docker-compose down -v
docker-compose up --build
```

### Sem Docker:

```powershell
# Rodar servidor
python run.py

# Ativar ambiente virtual (sempre antes de trabalhar)
.\.venv\Scripts\Activate.ps1
```

---

## 🐛 Problemas Comuns

### "Porta 5000 já em uso"
```powershell
# Parar processo na porta 5000 (Windows)
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process

# OU mudar a porta no docker-compose.yml para 8080:
ports:
  - "8080:5000"
```

### "Banco de dados não encontrado"
```powershell
# Verificar se arquivo existe
Test-Path instance\data_bank.db

# Se não existir, pergunte ao time ou faça pull do Git
git pull origin main
```

### "Mudanças no código não aparecem"
```powershell
# Com Docker: reiniciar
docker-compose restart

# Sem Docker: parar (Ctrl+C) e rodar novamente
python run.py
```

---

## 📚 Documentação Completa

- **Docker detalhado**: `DOCKER.md`
- **Compartilhamento**: `SHARING.md`
- **README principal**: `README.md`

---

## 💬 Dúvidas?

1. Leia a documentação acima
2. Pergunte no grupo/chat do time
3. Abra uma issue no GitHub

---

## 🎯 Próximos Passos

1. ✅ Rodar o projeto localmente
2. ✅ Explorar o site em http://localhost:5000
3. ✅ Acessar área admin
4. 📖 Ler `README.md` para entender a estrutura
5. 🚀 Começar a contribuir!

**Boa sorte! 🚀**
