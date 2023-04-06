# # import mysql.connector
#
# # '''
# # local access
# # '''
#
# # '''
# # user = 'root'
# # pwd = 'Qwer@1234'
# # host = 'localhost'
# # database = 'lattes4web'
# # '''
#
# # '''
# # container access
# # '''
# # user = 'root'
# # pwd = 'qwe123'
# # host = '172.17.0.2'
# # database = 'lattes4web'
# # port=3306
#
# # def conexao():
# #     try:
# #         db = mysql.connector.connect(user=user,password= pwd,host=host, database=database,port=port)
# #         # print("Connected!")
# #     except:
# #         print("YOU SHALL NOT PASS!")
# #     return db
#
#
#
# import sqlite3
# conn = sqlite3.connect('lattes4web.db')
# cursor = conn.cursor()
#
# def conexao():
#     conn = sqlite3.connect('lattes4web.db')
#     conn.row_factory = sqlite3.Row()
#     return conn
#
#
#
# # cursor.execute("""
# #             CREATE TABLE resultados(
# #             id INTEGER NOT NULL primary key autoincrement,
# #             nome_docente text NOT NULL,
# #             documento text NOT NULL,
# #             ano_evento text NOT NULL,
# #             titulo text NOT NULL,
# #             doi text NOT NULL,
# #             sigla text NOT NULL,
# #             nome_evento text NOT NULL,
# #             autores text NOT NULL,
# #             estratos text,
# #             notas text
# #             );
# # """)
# # print("Criado com sucesso")
# # conn.close()
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, inspect
from flask import flash

def conexao():
    database_url = 'sqlite:///../teste.db'
    engine = create_engine(database_url, echo=True)
    return engine


def criar_tabela():
    create_db = """
                CREATE TABLE resultados(
                id INTEGER NOT NULL primary key autoincrement,
                nome_docente text NOT NULL,
                documento text NOT NULL,
                ano_evento text NOT NULL,
                titulo text NOT NULL,
                doi text NOT NULL,
                sigla text NOT NULL,
                nome_evento text NOT NULL,
                autores text NOT NULL,
                estratos text,
                notas text
                );
    """
    conn = engine.connect()
    trans = conn.begin()

    try:
        conn.execute(create_db)
    except Exception as e:
        flash(e)
    trans.commit()
    conn.close()


# class Resultado(db.Model):
#     id = db.Column('id', db.Integer,primary_key=True, autoincrement=True)
#     nome_docente = db.Column('nome_docente', db.String(255),nullable=False)
#     documento = db.Column('documento', db.String(30),nullable=False)
#     ano_evento = db.Column('ano_evento', db.String(4),nullable=False)
#     titulo = db.Column('titulo', db.Text,nullable=False)
#     doi = db.Column('doi', db.String(100),nullable=False)
#     sigla = db.Column('sigla', db.String(30),nullable=False)
#     nome_evento = db.Column('nome_evento', db.Text,nullable=False)
#     autores = db.Column('autores', db.Text,nullable=False)
#     estratos = db.Column('estratos', db.String(11),nullable=False)
#     notas = db.Column('notas', db.String(100),nullable=False)
#     def __init__(self,nome_docente,documento,ano_evento,titulo,doi,sigla,nome_evento,autores,estratos,notas):
#         self.nome_docente=nome_docente
#         self.documento=documento
#         self.ano_evento=ano_evento
#         self.titulo=titulo
#         self.doi=doi
#         self.sigla=sigla
#         self.nome_evento=nome_evento
#         self.autores=autores
#         self.estratos=estratos
#         self.notas=notas