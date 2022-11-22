import mysql.connector
import models.connection as database



def lista():
    db = database.conexao()
    cursor = db.cursor()
    
    sql=""" SELECT * FROM resultados """
    cursor.execute(sql)
    resultado = cursor.fetchall()
    
    return resultado

def busca_prof():
    db = database.conexao()
    cursor = db.cursor()
    
    sql=""" SELECT distinct(nome_docente) FROM resultados"""
    cursor.execute(sql)
    resultado = cursor.fetchall()
    
    return resultado

def total_notas():
    db = database.conexao()
    cursor = db.cursor()
    
    sql=""" SELECT sum(notas), nome_docente FROM resultados"""
    cursor.execute(sql)
    resultado = cursor.fetchall()
    
    return resultado