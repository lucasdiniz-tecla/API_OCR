# Usa imagem oficial do Python
FROM python:3.11-slim

# Instala dependências do sistema (Tesseract + Poppler)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos para o container
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app .

# Expõe a porta usada pelo FastAPI
EXPOSE 8000

# Comando para rodar o servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
