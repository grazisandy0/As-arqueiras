-- ======================================
-- Banco de Dados: AsArqueiras
-- ======================================
CREATE DATABASE IF NOT EXISTS AsArqueiras;
USE AsArqueiras;

-- ======================================
-- Tabela: users
-- ======================================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_admin TINYINT(1) DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Exemplo de usuário
INSERT INTO users (username, email, password_hash, is_admin)
VALUES 
('graziela', 'graziela@example.com', '$2y$10$EXEMPLOHASHDA1234567890abcdef', 1),
('jogador1', 'jogador1@example.com', '$2y$10$EXEMPLOHASHDA1234567890abcdef', 0);

-- ======================================
-- Tabela: products
-- ======================================
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    stock INT DEFAULT 0,
    size VARCHAR(10),
    category VARCHAR(50),
    image_url VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Exemplos de produtos
INSERT INTO products (name, description, price, stock, size, category, image_url)
VALUES
('Camiseta Arqueiras Alpha', 'Camiseta oficial As Arqueiras, tecido premium.', 129.90, 50, 'M', 'Camisa', 'https://via.placeholder.com/240x300?text=Camiseta+1'),
('Camiseta Arqueiras Beta', 'Camiseta oficial As Arqueiras, edição limitada.', 149.90, 30, 'G', 'Camisa', 'https://via.placeholder.com/240x300?text=Camiseta+2'),
('Camiseta Arqueiras Gamma', 'Camiseta oficial As Arqueiras, design exclusivo.', 99.90, 20, 'P', 'Camisa', 'https://via.placeholder.com/240x300?text=Camiseta+3');

-- ======================================
-- Tabela: cart_items
-- ======================================
CREATE TABLE IF NOT EXISTS cart_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT DEFAULT 1,
    added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- ======================================
-- Tabela: orders
-- ======================================
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pendente',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ======================================
-- Tabela: order_items
-- ======================================
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- ======================================
-- Tabela: news
-- ======================================
CREATE TABLE IF NOT EXISTS news (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    category VARCHAR(50),
    content TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Exemplos de notícias
INSERT INTO news (title, category, content)
VALUES
('O Poder da IA nos Games: "Gerações de Conteúdo" Chegam aos MMORPGs!', 'Tecnologia / MMORPG', 'A Inteligência Artificial (IA) generativa está deixando de ser uma promessa e se tornando realidade nos jogos. Desenvolvedores de MMORPGs estão começando a usar IAs para criar missões secundárias dinâmicas e diálogos com NPCs que se adaptam às escolhas individuais de cada jogador em tempo real.'),
('Novo Patch Bate Recorde de Download', 'Atualização / MMORPG', '[Jogo X] lançou o Patch 3.01 "Vingança do Arqueiro" na madrugada. Mais de 10 milhões de jogadores tentaram atualizar simultaneamente, causando picos no servidor. Destaque para o nerf na classe Mago e o novo mapa de Inverno.');

-- ======================================
-- Tabela: sessions (opcional para login)
-- ======================================
CREATE TABLE IF NOT EXISTS sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    session_token VARCHAR(255) NOT NULL,
    expires_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
