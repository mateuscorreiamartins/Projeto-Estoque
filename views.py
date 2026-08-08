from main import app
from flask import render_template, request, redirect, url_for, session, flash
from models.models import db, Usuario, Produto, Movimentacao
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Rotas

# Redirecionando para a página de login
@app.route("/")
def homepage():
    return redirect(url_for("login"))


# Rota de Login (Autenticação e Sessão) 
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_input = request.form.get('login')
        senha_input = request.form.get('senha')
        
        # Busca o usuário no banco de dados
        user = Usuario.query.filter_by(login=login_input).first()
        
        # 2. Verifica se o utilizador existe e se a senha digitada corresponde ao hash salvo
        if user and check_password_hash(user.senha, senha_input):
            # Inicia a Sessão de Usuário
            session['user_id'] = user.id_usuario
            session['user_nome'] = user.nome
            session['user_perfil'] = user.tipo_acesso # Administrador ou Comum
            return redirect(url_for('dashboard'))
        else:
            # Caso o login não exista ou a senha seja incorreta
            flash('Login ou senha incorretos.')
            
    return render_template('login.html')




# 2. Dashboard (Visualização com Alertas de Estoque) 
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    produtos = Produto.query.all()
    # A lógica para quantidade mínima está no HTML
    return render_template('dashboard.html', produtos=produtos)


# Cadastro de Produto (Validações Obrigatórias e Numéricas) 
@app.route('/produto/novo', methods=['GET', 'POST'])
def cadastrar_produto():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        preco = request.form.get('preco')
        qtd_min = request.form.get('quantidade_minima')
        qtd_atual = request.form.get('quantidade_atual')
        categoria = request.form.get('categoria')

        # Validação: Campos Obrigatórios
        if not all([nome, preco, qtd_min, qtd_atual]):
            flash('Preencha todos os campos obrigatórios.')
            return redirect(url_for('cadastrar_produto'))

        # Validação: Impedir texto em campos numéricos
        try:
            novo_produto = Produto(
                nome=nome,
                preco=float(preco),
                quantidade_minima=float(qtd_min),
                quantidade_atual=float(qtd_atual),
                categoria=categoria
            )
            db.session.add(novo_produto)
            db.session.commit()
            flash('Produto cadastrado com sucesso!')
            return redirect(url_for('dashboard'))
        except ValueError:
            flash('Preço e quantidades devem ser números válidos.')
            
    return render_template('produto_form.html')

# 4. Movimentação (Entrada e Saída)
@app.route('/movimentacao/<int:id_produto>', methods=['GET', 'POST'])
def movimentar(id_produto):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    produto = Produto.query.get_or_404(id_produto)
    
    if request.method == 'POST':
        tipo = request.form.get('tipo_movimentacao') # 'entrada' ou 'saida'
        qtd = request.form.get('quantidade')
        
        try:
            qtd = float(qtd)
            if tipo == 'entrada':
                produto.quantidade_atual += qtd
            else:
                if produto.quantidade_atual < qtd:
                    flash('Saldo insuficiente para saída.')
                    return redirect(url_for('movimentar', id_produto=id_produto))
                produto.quantidade_atual -= qtd
            
            # Registra o histórico da movimentação
            nova_mov = Movimentacao(
                tipo_movimentacao=tipo,
                quantidade=qtd,
                data_hora=datetime.now(),
                id_usuario=session['user_id'],
                id_produto=produto.id_produto
            )
            db.session.add(nova_mov)
            db.session.commit()
            flash('Estoque atualizado!')
            return redirect(url_for('dashboard'))
        except ValueError:
            flash('Informe uma quantidade numérica válida.')
            
    return render_template('movimentacao_form.html', produto=produto)

# 5. Cadastro de Usuário (Somente Administrador) 
@app.route('/usuario/novo', methods=['GET', 'POST'])
def cadastrar_usuario():
    if session.get('user_perfil') != 'Administrador':
        flash('Acesso restrito ao Administrador.')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        login_novo = request.form.get('login') 
        senha_nova = request.form.get('senha') 
        perfil = request.form.get('tipo_acesso')
        
        # Validação básica
        if not all([nome, login_novo, senha_nova, perfil]):
            flash('Todos os campos sao obrigatorios.')
            return redirect(url_for('cadastrar_usuario'))

        # Tenta salvar no banco de dados
        try:
            novo_usuario = Usuario(
                nome=nome,
                login=login_novo,
                senha=generate_password_hash(senha_nova),
                tipo_acesso=perfil
            )
            db.session.add(novo_usuario)
            db.session.commit()
            flash(f'Utilizador {login_novo} criado com sucesso!')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao criar utilizador. O login pode ja existir.')
            
    return render_template('usuario_form.html')

@app.route('/produto/excluir/<int:id_produto>', methods=['POST'])
def excluir_produto(id_produto):
    # Apenas Administradores podem excluir produtos
    if session.get('user_perfil') != 'Administrador':
        flash('Acesso negado. Apenas administradores podem excluir itens.')
        return redirect(url_for('dashboard'))
    
    produto = Produto.query.get_or_404(id_produto)
    
    # Verifica se existem movimentações ligadas ao produto
    movimentacoes = Movimentacao.query.filter_by(id_produto=id_produto).first()
    if movimentacoes:
        flash('Nao e possivel excluir um produto que ja possui movimentacoes registadas.')
        return redirect(url_for('dashboard'))

    try:
        db.session.delete(produto)
        db.session.commit()
        flash('Produto removido com sucesso!')
    except Exception:
        db.session.rollback()
        flash('Erro ao tentar excluir o produto.')
        
    return redirect(url_for('dashboard'))

@app.route('/historico')
def visualizar_historico():
    # Verifica se o utilizador está logado
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Procura todas as movimentações ordenadas pela data mais recente
    historico = Movimentacao.query.order_by(Movimentacao.data_hora.desc()).all()
    
    return render_template('historico.html', historico=historico)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))