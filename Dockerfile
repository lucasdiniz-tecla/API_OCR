# Usa imagem base leve com Python
FROM python:3.11-slim

# Instala dependências do sistema, incluindo poppler-utils
RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-por \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY . .

# Instala dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta que o Render usa
EXPOSE 10000

# Comando para iniciar o servidor FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
