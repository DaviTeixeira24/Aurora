import os
import subprocess
from pathlib import Path

def create_flask_project(project_name):
    '''
    Função para criar um projeto Flask básico com Docker e venv.
    Parâmetros:
        project_name: Nome do projeto (pasta onde o projeto será criado).
    Retorna:
        None
    '''
    # estrutura do projeto
    folders = [
        project_name,
        f"{project_name}/templates",
        f"{project_name}/static/css",
        f"{project_name}/static/js",
        f"{project_name}/static/images",
    ]

    # Arquivos básicos
    files = {
        # arquivo de configuração do Flask
        f"{project_name}/app.py": """\
from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    '''
    Rota principal que renderiza o template index.html.
    A variável de ambiente DOCKER é passada para o template.
    '''
    # Verifica se a variável de ambiente DOCKER está definida
    return render_template("index.html", docker=os.getenv("DOCKER", "xxxx"))

@app.route("/hello")
def hello():
    '''
    Rota adicional que renderiza o template hello.html.
    A variável de ambiente DOCKER é passada para o template.
    '''
    # Verifica se a variável de ambiente DOCKER está definida
    return jsonify(
        {
            "docker": os.getenv("DOCKER", "não"),
            "message": "Hello, World!"
        },)


# main
# Executa a aplicação Flask
if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True  # Para templates Jinja2
    # Executa o servidor Flask na porta 5000
    app.run(host='0.0.0.0', debug=True, port=5000)
""",
# arquivo de requisitos
        f"{project_name}/requirements.txt": """\
flask>=2.0.0
Flask-Cors>=3.0.10
Flask-RESTful>=0.3.8
Flask-SocketIO>=5.0.1
Flask-SQLAlchemy>=2.4.4
Flask-Testing>=0.8.1
Flask-WTF>=0.14.3
gunicorn>=20.0.4
requests>=2.25.1
SQLAlchemy>=1.3.18
SQLAlchemy-Utils>=0.36.8
python-dotenv>=0.15.0
python-socketio>=5.0.1
python-engineio>=4.0.0
jinja2>=2.11.3
""",

# arquivo de configuração do Docker
        f"{project_name}/Dockerfile": """\
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
""",

# arquivo de configuração do Docker Compose
        f"{project_name}/docker-compose.yml": """\
version: "3.8"

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DOCKER=sim
      - FLASK_ENV=development
      - TEMPLATES_AUTO_RELOAD=True
    volumes:
      - .:/app
    command: flask run --host=0.0.0.0 --port=5000 --reload
""",

# arquivo de configuração da variável de ambiente
        f"{project_name}/.env": """\
# Variáveis de ambiente (opcional)
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
""",

# arquivo de template HTML
        f"{project_name}/templates/index.html": """\
<!DOCTYPE html>
<html>
<head>
    <title>Meu App Flask</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <h1>Olá, Flask!</h1>
    <p>Seu projeto foi criado automaticamente.</p>
    <p>Rodando no Docker? {{ docker }}</p>
</body>
</html>
""",

# arquivo de script css
        f"{project_name}/static/css/style.css": """\
body {
    font-family: Arial, sans-serif;
    margin: 20px;
    line-height: 1.6;
}
h1 {
    color: #0066cc;
}
"""
    }

    # Criando pastas e arquivos
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
    
    for file_path, content in files.items():
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    # Criar venv (opcional)
    venv_path = os.path.join(project_name, "venv")
    subprocess.run(["python", "-m", "venv", venv_path], check=True)

    # Instalar dependências no venv
    if os.name == "nt":
        pip_path = os.path.join(venv_path, "Scripts", "pip")
    else:
        pip_path = os.path.join(venv_path, "bin", "pip")
    
    subprocess.run([pip_path, "install", "-r", f"{project_name}/requirements.txt"], check=True)

    # Mensagem de sucesso da criação do projeto
    print(f"\n Projeto Flask + Docker criado: '{project_name}'")
    print("\n Para desenvolver localmente (com venv):")
    print(f"cd {project_name}")
    print("source venv/bin/activate  # Linux/Mac")
    print("venv\\Scripts\\activate   # Windows")
    print("python app.py\n")
    
    print(" Para rodar com Docker:")
    print(f"cd {project_name}")
    print("docker-compose up --build\n")
    print("Acesse: http://localhost:5000")

# main
# Executa a função principal 
if __name__ == "__main__":
    # pergunta o nome do projeto
    project_name = input("Nome do projeto Flask: ").strip()
    # função de criação do projeto
    create_flask_project(project_name)
