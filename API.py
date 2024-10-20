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

@app.route('/insert', methods=['POST'])
def insert():
    return

@app.route('/delete')
def delete():
    return

@app.route('/update')
def update():
    return

@app.route('/leitura', methods=['GET'])
def leitura():
    return

@app.route('/transacao')
def transacao():
    return

app.run()
