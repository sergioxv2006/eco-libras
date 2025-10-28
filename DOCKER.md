# 🐳 Docker - Eco Libras

## Pré-requisitos

- [Docker](https://www.docker.com/get-started) instalado
- [Docker Compose](https://docs.docker.com/compose/install/) instalado

## 🚀 Como usar

### 1. Buildar e iniciar a aplicação

```powershell
# Buildar a imagem e iniciar os containers
docker-compose up --build
```

### 2. Acessar a aplicação

Abra o navegador em: `http://localhost:5000`

### 3. Parar os containers

```powershell
# Parar sem remover os containers
docker-compose stop

# Parar e remover os containers
docker-compose down
```

## 📦 Compartilhamento do Banco de Dados

O banco de dados SQLite está mapeado no volume `./instance:/app/instance`, garantindo:

✅ **Persistência**: Dados não são perdidos ao parar o container  
✅ **Compartilhamento**: Todos os desenvolvedores usando o mesmo `instance/data_bank.db` terão o mesmo banco  
✅ **Backup automático**: O arquivo está no host e pode ser versionado no Git

### Para compartilhar com outros desenvolvedores:

1. **Via Git** (recomendado para times pequenos):
   ```powershell
   git add instance/data_bank.db
   git commit -m "Adicionar banco de dados inicial"
   git push
   ```

2. **Via Docker Hub** (para distribuição pública):
   ```powershell
   # Buildar e fazer push da imagem
   docker build -t seu-usuario/eco-libras:latest .
   docker push seu-usuario/eco-libras:latest
   ```

3. **Via arquivo compartilhado**:
   - Compartilhe o arquivo `instance/data_bank.db` via Google Drive, Dropbox, etc.
   - Outros devs colocam o arquivo na pasta `instance/` antes de rodar

## 🛠️ Comandos úteis

```powershell
# Ver logs da aplicação
docker-compose logs -f web

# Acessar o shell do container
docker-compose exec web bash

# Reiniciar apenas a aplicação
docker-compose restart web

# Remover tudo (containers, volumes, imagens)
docker-compose down -v --rmi all
```

## 🔧 Desenvolvimento

O código está mapeado como volume, então mudanças no código local refletem automaticamente no container (hot reload ativado).

### Estrutura de volumes:
- `./instance` → `/app/instance` (banco de dados)
- `./APP` → `/app/APP` (código da aplicação)
- `./run.py` → `/app/run.py` (arquivo principal)

## 🐛 Troubleshooting

### Porta 5000 já em uso?
```powershell
# Mudar a porta no docker-compose.yml
ports:
  - "8080:5000"  # Acessar em localhost:8080
```

### Banco de dados corrompido?
```powershell
# Restaurar do backup
cp instance/data_bank.db.backup instance/data_bank.db
docker-compose restart web
```

### Reconstruir do zero?
```powershell
docker-compose down -v
docker-compose up --build
```

## 📝 Notas

- O banco SQLite é compartilhado via volume mapeado
- Para produção, considere migrar para PostgreSQL ou MySQL
- O arquivo `.dockerignore` otimiza o build excluindo arquivos desnecessários
