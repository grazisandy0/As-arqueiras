# rotas.py
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "sua_chave_secreta_aqui"

# Conexão com o banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="seu_usuario",
    password="sua_senha",
    database="as_arqueiras_db"
)

cursor = db.cursor(dictionary=True)

# ======== ROTAS DE PÁGINA ========

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/loja")
def loja():
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    return render_template("loja.html", produtos=produtos)

@app.route("/produto/<int:produto_id>")
def produto(produto_id):
    cursor.execute("SELECT * FROM produtos WHERE id=%s", (produto_id,))
    produto = cursor.fetchone()
    if not produto:
        return "Produto não encontrado", 404
    return render_template("produto.html", produto=produto)

@app.route("/carrinho")
def carrinho():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    usuario_id = session["usuario_id"]
    cursor.execute("""
        SELECT c.id AS carrinho_id, p.id AS produto_id, p.nome, p.preco, p.imagem, c.quantidade
        FROM carrinho c
        JOIN produtos p ON c.id_produto = p.id
        WHERE c.id_usuario=%s
    """, (usuario_id,))
    itens = cursor.fetchall()
    return render_template("carrinho.html", itens=itens)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/noticias")
def noticias():
    cursor.execute("SELECT * FROM noticias ORDER BY data_publicacao DESC")
    noticias = cursor.fetchall()
    return render_template("noticias.html", noticias=noticias)

# ======== ROTAS DE AÇÃO ========

@app.route("/autenticar", methods=["POST"])
def autenticar():
    email = request.form["email"]
    senha = request.form["senha"]
    cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
    usuario = cursor.fetchone()
    if usuario and check_password_hash(usuario["senha_hash"], senha):
        session["usuario_id"] = usuario["id"]
        session["usuario_nome"] = usuario["nome"]
        return redirect(url_for("home"))
    return "Email ou senha incorretos", 401

@app.route("/registrar", methods=["POST"])
def registrar():
    nome = request.form["nome"]
    email = request.form["email"]
    senha = request.form["senha"]
    senha_hash = generate_password_hash(senha)
    cursor.execute("INSERT INTO usuarios (nome, email, senha_hash, data_cadastro) VALUES (%s,%s,%s,%s)",
                   (nome, email, senha_hash, datetime.now()))
    db.commit()
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/adicionar_carrinho", methods=["POST"])
def adicionar_carrinho():
    if "usuario_id" not in session:
        return jsonify({"erro": "Usuário não logado"}), 401
    usuario_id = session["usuario_id"]
    produto_id = request.form["produto_id"]
    quantidade = int(request.form.get("quantidade", 1))
    
    # Verifica se já existe no carrinho
    cursor.execute("SELECT * FROM carrinho WHERE id_usuario=%s AND id_produto=%s", (usuario_id, produto_id))
    item = cursor.fetchone()
    if item:
        cursor.execute("UPDATE carrinho SET quantidade=quantidade+%s WHERE id=%s", (quantidade, item["id"]))
    else:
        cursor.execute("INSERT INTO carrinho (id_usuario, id_produto, quantidade) VALUES (%s,%s,%s)",
                       (usuario_id, produto_id, quantidade))
    db.commit()
    return redirect(url_for("carrinho"))

@app.route("/remover_carrinho", methods=["POST"])
def remover_carrinho():
    if "usuario_id" not in session:
        return jsonify({"erro": "Usuário não logado"}), 401
    carrinho_id = request.form["carrinho_id"]
    cursor.execute("DELETE FROM carrinho WHERE id=%s", (carrinho_id,))
    db.commit()
    return redirect(url_for("carrinho"))

@app.route("/filtrar_produtos", methods=["GET"])
def filtrar_produtos():
    categoria = request.args.get("categoria")
    tamanho = request.args.get("tamanho")
    preco_min = request.args.get("preco_min")
    preco_max = request.args.get("preco_max")
    
    query = "SELECT * FROM produtos WHERE 1=1"
    params = []

    if categoria:
        query += " AND categoria=%s"
        params.append(categoria)
    if tamanho:
        query += " AND tamanho=%s"
        params.append(tamanho)
    if preco_min:
        query += " AND preco >= %s"
        params.append(preco_min)
    if preco_max:
        query += " AND preco <= %s"
        params.append(preco_max)
    
    cursor.execute(query, tuple(params))
    produtos = cursor.fetchall()
    return jsonify(produtos)

# ======== ROTAS DE API (opcional) ========

@app.route("/api/produtos")
def api_produtos():
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    return jsonify(produtos)

@app.route("/api/produto/<int:produto_id>")
def api_produto(produto_id):
    cursor.execute("SELECT * FROM produtos WHERE id=%s", (produto_id,))
    produto = cursor.fetchone()
    return jsonify(produto)

@app.route("/api/carrinho")
def api_carrinho():
    if "usuario_id" not in session:
        return jsonify({"erro": "Usuário não logado"}), 401
    usuario_id = session["usuario_id"]
    cursor.execute("""
        SELECT c.id AS carrinho_id, p.id AS produto_id, p.nome, p.preco, p.imagem, c.quantidade
        FROM carrinho c
        JOIN produtos p ON c.id_produto = p.id
        WHERE c.id_usuario=%s
    """, (usuario_id,))
    itens = cursor.fetchall()
    return jsonify(itens)

# ======== EXECUTAR APP ========
if __name__ == "__main__":
    app.run(debug=True)

