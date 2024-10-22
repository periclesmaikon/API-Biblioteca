import psycopg2 #Biblioteca para conectar com o postgres
from flask import Flask, jsonify, request
from psycopg2.extras import DictCursor

#Conexão com o BD
bd = psycopg2.connect(
            host="bd-biblioteca.ctupybkjn6q7.us-east-1.rds.amazonaws.com",
            database="postgres",
            user="aluno",
            password="aluno2024"
    )

app = Flask(__name__)   #Inicia a API

@app.route('/')
def home():
    return "API - BIBLIOTECA"

@app.route('/insertautor', methods=['POST']) #Inserção na tabela autor (entidade)
def insertAutor():
    try:
        # Obtendo dados da requisição
        autor = request.json['autor']
        genero = request.json['genero']
        nacionalidade = request.json['nacionalidade']

        cursor = bd.cursor() #Inicia cursor
        cursor.execute('''
            INSERT INTO biblioteca.autor (nome, genero_principal, nacionalidade)
            VALUES (%s, %s, %s);''',
            (autor, genero, nacionalidade))
        bd.commit() #Confirma a inserção

        return {"message": "Autor inserido com sucesso!"}, 201
    
    except psycopg2.Error as e:
        bd.rollback() #Reverte a inserção
        return {"Erro:": str(e)}, 400

    finally:
        cursor.close()

@app.route('/insertlivro', methods=['POST']) #Inserção na tabela livro (entidade)
def insertLivro():
    try:
        # Obtendo dados da requisição
        isbn = request.json['isbn']
        nome = request.json['nome']
        num_pag = request.json['num_pag']
        sinopse = request.json['sinopse']
        genero = request.json['genero']
        class_indic = request.json['class_indic']
        formato = request.json ['formato']


        cursor = bd.cursor() #Inicia cursor
        cursor.execute('''
            INSERT INTO biblioteca.livro (isbn, nome, num_pag, sinopse, genero, class_indic, formato)
            VALUES (%s, %s, %s, %s, %s, %s, %s);''',
            (isbn, nome, num_pag, sinopse, genero, class_indic, formato))
        bd.commit() #Confirma a inserção

        return {"message": "Livro inserido com sucesso!"}, 201
    
    except psycopg2.Error as e:
        bd.rollback() #Reverte a inserção
        return {"Erro:": str(e)}, 400

    finally:
        cursor.close()

@app.route('/insertescreveu', methods=['POST']) #Inserção na tabela escreveu (relação)
def insertEscreveu():
    try:
        # Obtendo dados da requisição
        autor_nome = request.json['autor_nome']
        livro_isbn = request.json['livro_isbn']
        data_escrito = request.json['data_escrito']
        sequencia = request.json['sequencia']

        cursor = bd.cursor() #Inicia cursor
        cursor.execute('''
            INSERT INTO biblioteca.escreveu (autor_nome, livro_isbn, data_escrito, sequencia)
            VALUES (%s, %s, %s, %s);''',
            (autor_nome, livro_isbn, data_escrito, sequencia))
        bd.commit() #Confirma a inserção

        return {"message": "Relação escreveu inserido com sucesso!"}, 201
    
    except psycopg2.Error as e:
        bd.rollback() #Reverte a inserção
        return {"Erro:": str(e)}, 400

    finally:
        cursor.close()


@app.route('/deleteAutor', methods=['DELETE'])
def deleteAutor():
    try:

        autor_nome = request.json['autor_nome']
        cursor = bd.cursor() 
        cursor.execute('''
            DELETE FROM biblioteca.Autor WHERE nome = (autor_nome)
            VALUES (%s);''', (autor_nome))
        bd.commit() 
        return {"message": "Autor removido com sucesso!"}, 204
    
    except psycopg2.Error as e:
        bd.rollback() 
        return {"Erro:": str(e)}, 400

    finally:
        cursor.close()


@app.route('/deleteLivro', methods=['DELETE'])
def deleteLivro():
    try:

        livro_isbn = request.json['livro_isbn']
        cursor = bd.cursor() 
        cursor.execute('''
            DELETE FROM biblioteca.livro WHERE isbn = (livro_isbn)
            VALUES (%s);''', (livro_isbn))
        bd.commit() 

        return {"message": "Livro removido com sucesso!"}, 204
    
    except psycopg2.Error as e:
        bd.rollback() 
        return {"Erro:": str(e)}, 400

    finally:
        cursor.close()
            

@app.route('/update')
def update():
    return

@app.route('/leituraAutor', methods=['GET'])
def leituraAutor():
    try:

        cursor = bd.cursor(cursor_factory=DictCursor)
        query = "SELECT * FROM biblioteca.autor;"
        cursor.execute(query)
        autores = cursor.fetchall()
        if not autores:
            app.abort(404, "Autores não encontrados")
        return jsonify([dict(autor) for autor in autores]), 200
    
    except psycopg2.Error as e:
            print(f"Erro ao buscar dados: {e}")
            app.abort(500, "Erro ao buscar dados no banco de dados")

    finally:
        cursor.close()

@app.route('/leituraLivro', methods=['GET'])
def leituraLivro():
    try:

        cursor = bd.cursor(cursor_factory=DictCursor)
        query = "SELECT * FROM biblioteca.livro;"
        cursor.execute(query)
        livros = cursor.fetchall()
        if not livros:
            app.abort(404, "Livros não encontrados")
        return jsonify([dict(livro) for livro in livros]), 200
    
    except psycopg2.Error as e:
            print(f"Erro ao buscar dados: {e}")
            app.abort(500, "Erro ao buscar dados no banco de dados")

    finally:
        cursor.close()
    

@app.route('/leituraEscreveu', methods=['GET'])
def leituraEscreveu():
    try:

        cursor = bd.cursor(cursor_factory=DictCursor)
        query = "SELECT * FROM biblioteca.escreveu;"
        cursor.execute(query)
        escritos = cursor.fetchall()
        if not escritos:
            app.abort(404, "Dados não encontrados")
        return jsonify([dict(escreveu) for escreveu in escritos]), 200
    
    except psycopg2.Error as e:
            print(f"Erro ao buscar dados: {e}")
            app.abort(500, "Erro ao buscar dados no banco de dados")

    finally:
        cursor.close()

@app.route('/transacao')
def transacao():
    return

app.run()
