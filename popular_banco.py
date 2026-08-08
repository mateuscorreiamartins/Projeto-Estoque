from main import app
from models.models import db, Usuario
from werkzeug.security import generate_password_hash

with app.app_context():
    # Cria o arquivo .db e todas as tabelas automaticamente se não existirem
    db.create_all()
    
    # Cria o administrador
    primeiro_admin = Usuario(
        nome='Administrador do Sistema',
        login='admin',
        senha=generate_password_hash('123'),
        tipo_acesso='Administrador'
    )
    
    # Guarda no banco de dados
    db.session.add(primeiro_admin)
    db.session.commit()
    
    print("======================================================")
    print(" Sucesso! Banco de dados criado e tabelas geradas.")
    print(" Utilizador 'admin' criado.")
    print(" Acesse com: \nLogin: admin | Senha: 123")
    print("======================================================")