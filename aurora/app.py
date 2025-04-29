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


#Criando rotas
@app.route("/sobre.html")
def sobre():
    return render_template("sobre.html")

@app.route("/contato.html")
def contato():
    return  render_template("contato.html")

@app.route("/equipe.html")
def equipe():
    return render_template("equipe.html")

@app.route("/index.html")
def chat():
    return render_template("index.html")


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
