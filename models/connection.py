import sqlite3

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, inspect
from flask import flash

def conexao():
    conn = sqlite3.connect(database='lattes4web.db',check_same_thread=False)
    # flash("Abrindo conexão")
    return conn

conn = conexao()

def tabela_resultados():
    create_db = """
                CREATE TABLE IF NOT EXISTS resultados(
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
    

    try:
        conn.execute(create_db)
    except Exception as e:
        print(e)
    # conn.close()

# def tabela_periodicos():
#     sql ="""
#             CREATE TABLE periodicos(
#             id INTEGER NOT NULL primary key autoincrement,
#             issn text NOT NULL,
#             titulo text NOT NULL,
#             estratos text NOT NULL
#             );
#     """
    
#     try:
#         conn.execute(sql)
#     except Exception as e:
#         print(e)


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