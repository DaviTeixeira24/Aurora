# Imagem base Python
FROM python:3.10-slim

# Diretório de trabalho
WORKDIR /app

# Copiar requirements e instalar dependências

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o resto do projeto
COPY . .

# Variáveis de ambiente (opcional)
ENV FLASK_APP=app.py
ENV FLASK_ENV=development


# Expor a porta do Flask
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["flask", "run", "--host=0.0.0.0", "--debug"]
