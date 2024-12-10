# Usar uma imagem base oficial do Python
FROM python:3.10-slim

# Definir o diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Definir a variável de ambiente para garantir que o Django não rode interativamente
ENV PYTHONUNBUFFERED=1

# Copiar o arquivo de dependências para dentro do contêiner
COPY requirements.txt /app/

# Instalar as dependências do Python
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copiar o restante da aplicação para dentro do contêiner
COPY . /app/

# Expor a porta 8000 para o contêiner
EXPOSE 8000

# Instalar o Gunicorn
RUN pip install gunicorn

# Define o comando para iniciar o servidor Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "certificados_ondina_backend.wsgi:application"]
