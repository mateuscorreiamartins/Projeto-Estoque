from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Inicialização do banco
db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    tipo_acesso = db.Column(db.Enum('Administrador', 'Comum'), nullable=False) 
    nome = db.Column(db.String(60), nullable=False)
    login = db.Column(db.String(100), unique=True, nullable=False) 
    senha = db.Column(db.String(128), nullable=False) 


class Produto(db.Model):
    __tablename__ = 'produto'
    id_produto = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    nome = db.Column(db.String(50), nullable=False) 
    preco = db.Column(db.Numeric(10, 2), nullable=False) 
    categoria = db.Column(db.String(45), nullable=True) 
    quantidade_minima = db.Column(db.Float, nullable=False) 
    quantidade_atual = db.Column(db.Float, nullable=False) 


class Movimentacao(db.Model):
    __tablename__ = 'movimentacao'
    id_movimentacao = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    tipo_movimentacao = db.Column(db.Enum('entrada', 'saida'), nullable=False) 
    quantidade = db.Column(db.Float, nullable=False) 
    data_hora = db.Column(db.DateTime, default=datetime.now, nullable=False) 
    
    # Chaves Estrangeiras (FK) que ligam as tabelas Usuario e Produto
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    id_produto = db.Column(db.Integer, db.ForeignKey('produto.id_produto'), nullable=False)

    # Criam o link para usar mov.produto e mov.usuario no HTML
    produto = db.relationship('Produto', backref='movimentacoes')
    usuario = db.relationship('Usuario', backref='movimentacoes')
