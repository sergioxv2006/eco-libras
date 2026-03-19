# Imagem base Python
FROM python:3.12-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements primeiro (cache de layers)
COPY APP/requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código da aplicação
COPY APP/ ./APP/

# Criar diretório instance se não existir
RUN mkdir -p /app/instance

# Expor porta 5000
EXPOSE 5000

# Variáveis de ambiente padrão
ENV FLASK_APP=run.py
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1

# Comando para rodar a aplicação
CMD ["python", "-m", "APP.run"]
