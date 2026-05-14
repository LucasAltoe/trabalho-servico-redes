# backend/Dockerfile
# Este arquivo ensina o Docker a montar a imagem do backend.

# 1. Parte da imagem oficial do Python 3.11 (versão enxuta)
FROM python:3.11-slim

# 2. Define a pasta de trabalho dentro do container
WORKDIR /app

# 3. Copia o arquivo de dependências e instala os pacotes
#    (feito antes de copiar o código para aproveitar o cache do Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copia o restante do código da aplicação
COPY app/ ./app/

# 5. Informa que o container vai escutar na porta 8080
EXPOSE 8080

# 6. Comando que inicia o servidor quando o container sobe
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
