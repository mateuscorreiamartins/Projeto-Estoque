# Projeto-Estoque

Este é um sistema web desenvolvido em Python utilizando o framework Flask para o controle e gestão de entrada e saída de produtos/materiais.

# Como Clonar e Rodar o Projeto

Siga o passo a passo abaixo para rodar e testar o projeto:

Abra o terminal do seu VS Code na pasta onde deseja guardar o projeto e execute:

git clone <URL_DO_REPOSITORIO_AQUI>

Instalar as Dependências

Certifique-se de que possui o Python 3.x instalado. Na raiz do projeto, execute o comando abaixo para instalar todas as bibliotecas necessárias listadas no requirements.txt (incluindo Flask, SQLAlchemy, Werkzeug, etc):

pip install -r requirements.txt

# Primeiro login no sistema

Rode o script abaixo (pasta raiz do projeto) para criar o banco de dados local, gerar todas as tabelas e cadastrar o usuário administrador padrão:

popular_banco.py

Login: admin
Senha: 123

(Você verá uma mensagem no terminal confirmando o sucesso da criação do banco e do usuário admin com a senha).

# Para executar

Para rodar a aplicação, execute o arquivo principal: main.py

O console exibirá que o servidor está no ar e escutando na porta 5000, basta copiar todo o endereço e colar no navegador.

# Funcionalidades Principais

Autenticação e Sessão de Usuário: Sistema seguro de login com controle de perfis de acesso (Administrador e Comum).
Criptografia por Hash (Werkzeug): Armazenamento seguro de senhas através de algoritmos de hash de sentido único, protegendo as credenciais de ponta a ponta.
Gestão de Estoque: Cadastro de produtos, controle de quantidades, categorias e valores monetários.
Alertas de Estoque Baixo: Visualização destacada para produtos que estão abaixo do nível mínimo de estoque configurado.
Histórico de Movimentações: Registro detalhado de cada entrada e saída de produto, vinculado ao usuário que executou a ação.
Integridade de Dados: Proteção contra exclusão acidental de produtos que possuam histórico de movimentações ativo (restrição em nível de banco de dados).

# Estrutura Organizacional

├── instance/              # Pasta local criada dinamicamente contendo o banco SQLite (ignorado pelo Git)
├── models/                # Modelos de dados e representação lógica das tabelas
├── static/                # Arquivos estáticos
├── templates/             # Páginas HTML 
├── views.py               # Rotas, controladores e lógica de negócios da aplicação
├── schema.sql             # Script SQL de modelagem do banco físico
├── popular_banco.py       # Script utilitário para inicializar e popular o banco de dados
├── main.py                # Ponto de entrada da aplicação
└── .gitignore             # Arquivo de exclusão de arquivos locais do Git
