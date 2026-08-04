from flask import Flask
from models.models import db
from os import getenv
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do ficheiro .env primeiro
load_dotenv() 

# Inicializa o Flask
app = Flask(__name__)

# Configurações da Aplicação
# Busca a chave no .env para garantir que as informações estão seguras
app.config['SECRET_KEY'] = getenv('SECRET_KEY') 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 4. Inicializa o banco de dados com as configurações do app
db.init_app(app)

# 5. Cria o banco de dados (estoque.db) e as tabelas 
with app.app_context():
    db.create_all()

# 6. Importa as rotas
from views import *

if __name__ == "__main__":
    app.run(debug=True)
