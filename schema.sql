CREATE TABLE usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_acesso TEXT NOT NULL CHECK (tipo_acesso IN ('Administrador', 'Comum')),
    nome VARCHAR(60) NOT NULL,
    login VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(128) NOT NULL -- para guardar o Hash Werkzeug
);

CREATE TABLE produto (
    id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(50) NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    categoria VARCHAR(45) NULL, 
    quantidade_minima REAL NOT NULL, 
    quantidade_atual REAL NOT NULL
);

CREATE TABLE movimentacao (
    id_movimentacao INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_movimentacao TEXT NOT NULL CHECK (tipo_movimentacao IN ('entrada', 'saida')),
    quantidade REAL NOT NULL,
    data_hora DATETIME NOT NULL,
    id_usuario INTEGER NOT NULL,
    id_produto INTEGER NOT NULL,
    -- Restrições de Chave Estrangeira (FK)
    FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario) ON DELETE RESTRICT,
    FOREIGN KEY (id_produto) REFERENCES produto (id_produto) ON DELETE RESTRICT
);