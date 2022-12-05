import models.connection as database


db = database.conexao()
cursor = db.cursor()

def lista():

    sql=""" SELECT * FROM resultados """
    cursor.execute(sql)
    resultado = cursor.fetchall()
    
    return resultado

def busca_prof():
    
    sql=""" SELECT distinct(nome_docente) FROM resultados"""
    cursor.execute(sql)
    resultado = cursor.fetchall()
    
    return resultado

def soma_nota():

    cursor.execute('SELECT distinct(nome_docente), sum(notas) from resultados where nome_docente in'
                   +'(select distinct(nome_docente) from resultados) group by nome_docente')
    resultado = cursor.fetchall()
    
    return resultado

def contador_estratos():

    cursor.execute('select DISTINCT(nome_docente), count(estratos), estratos, ano_evento from resultados group by nome_docente, estratos, ano_evento; ')
    resultado = cursor.fetchall()
    
    return resultado