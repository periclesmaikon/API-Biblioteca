import psycopg2 #Biblioteca para conectar com o postgres
from flask import Flask, request

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


@app.route('/deleteAutor', methods=['POST'])
def deleteAutor():
    try:

        autor_nome = request.json['autor_nome']
        cursor = bd.cursor() 
        cursor.execute('''
            DELETE FROM biblioteca.Autor WHERE nome = (autor_nome)
            VALUES (%s);''', (autor_nome))
        bd.commit() 
        return {"message": "Autor removido com sucesso!"}, 201
    
    except psycopg2.Error as e:
        bd.rollback() 
        return {"Erro:": str(e)}, 400

    finally:
        cursor.close()


@app.route('/deleteLivro', methods=['POST'])
def deleteLivro():
    try:

        livro_isbn = request.json['livro_isbn']
        cursor = bd.cursor() 
        cursor.execute('''
            DELETE FROM biblioteca.livro WHERE isbn = (livro_isbn)
            VALUES (%s);''', (livro_isbn))
        bd.commit() 

        return {"message": "Livro removido com sucesso!"}, 201
    
    except psycopg2.Error as e:
        bd.rollback() 
        return {"Erro:": str(e)}, 400

    finally:
        cursor.close()
            

@app.route('/updateautor', methods=['PUT']) #Atualização na tabela autor (entidade)
def updateAutor():
    try:
        # Obtendo dados da requisição
	autor_antigo = request.json['autor_antigo']
        autor_novo = request.json['autor_novo']
        genero = request.json['genero']
        nacionalidade = request.json['nacionalidade']
	

        cursor = bd.cursor() #Inicia cursor
        cursor.execute('''
            UPDATE biblioteca.autor SET nome = %s, genero_principal = %s, nacionalidade=%s WHERE nome = %s;''', (autor_novo, genero, nacionalidade, autor_antigo))
        bd.commit() #Confirma a atualização

        return {"message": "Autor atualizado com sucesso!"}, 200
    
    except psycopg2.Error as e:
        bd.rollback() #Reverte a atualização
        return {"Erro:": str(e)}, 400

    finally:
        cursor.close()

@app.route('/updatelivro', methods=['PUT'])
def updateLivro():
    try:
        # Obtendo dados da requisição
        livro_isbn = request.json['isbn']  # ISBN do livro que deseja atualizar
        novo_nome = request.json['novo_nome']
        novo_num_pag = request.json['novo_num_pag']
        nova_sinopse = request.json['nova_sinopse']
        novo_genero = request.json['novo_genero']
        nova_class_indic = request.json['nova_class_indic']
        novo_formato = request.json['novo_formato']

        cursor = bd.cursor()
        cursor.execute('''
            UPDATE biblioteca.livro
            SET nome = %s, num_pag = %s, sinopse = %s, genero = %s, class_indic = %s, formato = %s
            WHERE isbn = %s;''',
            (novo_nome, novo_num_pag, nova_sinopse, novo_genero, nova_class_indic, novo_formato, livro_isbn))
        bd.commit()

        return {"message": "Livro atualizado com sucesso!"}, 200

    except psycopg2.Error as e:
        bd.rollback()
        return {"Erro:": str(e)}, 400

    finally:
        cursor.close()

@app.route('/updateescreveu', methods=['PUT'])
def updateEscreveu():
    try:
        # Obtendo dados da requisição
        autor_nome = request.json['autor_nome']
        livro_isbn = request.json['livro_isbn']
        nova_data_escrito = request.json['nova_data_escrito']
        nova_sequencia = request.json['nova_sequencia']

        cursor = bd.cursor()
        cursor.execute('''
            UPDATE biblioteca.escreveu
            SET data_escrito = %s, sequencia = %s
            WHERE autor_nome = %s AND livro_isbn = %s;''',
            (nova_data_escrito, nova_sequencia, autor_nome, livro_isbn))
        bd.commit()

        return {"message": "Relação 'Escreveu' atualizada com sucesso!"}, 200

    except psycopg2.Error as e:
        bd.rollback()
        return {"Erro:": str(e)}, 400

    finally:
        cursor.close()

@app.route('/leitura', methods=['GET'])
def leitura():
    return

@app.route('/transacao')
def transacao():
    return

app.run()
