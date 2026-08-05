from main import app
from models.models import db, Usuario

with app.app_context():
    # Verifica se o administrador já existe para evitar duplicados
    admin_existente = Usuario.query.filter_by(login='admin').first()
    
    if not admin_existente:
        # Criando o primeiro utilizador
        primeiro_admin = Usuario(
            nome='Administrador do Sistema',
            login='admin',
            senha='123', # Senha simples para teste inicial
            tipo_acesso='Administrador'
        )
        
        db.session.add(primeiro_admin)
        db.session.commit()
        print("Sucesso! Usuário 'admin' criado.")
        print("Acesse com -> Login: admin | Senha: 123")
    else:
        print("O usuário 'admin' já existe no banco de dados.")
