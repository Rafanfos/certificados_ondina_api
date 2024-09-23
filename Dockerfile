# Dockerfile

# Base image com Python
FROM python:3.10-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o arquivo de dependências
COPY requirements.txt /app/

# Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante da aplicação
COPY . /app/

# Definir a variável de ambiente para garantir que o Django não execute interativamente
ENV PYTHONUNBUFFERED=1

# Comando para rodar o Django
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "seu_projeto.wsgi:application"]
