import models.connection as database


db = database.conexao()
def lista():

    sql="select id, nome_docente, documento,ano_evento, titulo,doi,sigla,nome_evento, autores,estratos, notas from resultados r;"
    cursor = db.cursor()
    cursor.execute(sql.upper())
    resultado = cursor.fetchall()

    return resultado

def busca_prof():
    
    sql=""" SELECT distinct(nome_docente) FROM resultados"""
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    
    return resultado

def soma_nota():

    sql = (""" SELECT distinct nome_docente , sum(notas) from resultados where nome_docente in
                    (select distinct(nome_docente) from resultados)group by nome_docente;""")
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    return resultado


def contador_estratos():

    sql = ('select DISTINCT(nome_docente), count(estratos), estratos, ano_evento from resultados group by nome_docente, estratos, ano_evento; ')
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    
    return resultado

def titulos_qualis():
    sql = ('SELECT DISTINCT titulo FROM resultados r group by titulo having COUNT(*) >1 ;')
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    
    return resultado

def qualis_repetidos(titulo):
    sql = ("SELECT distinct titulo, notas, estratos, count(*) FROM resultados r WHERE "+
                   "titulo like '%"+titulo+"%' group by titulo, notas, estratos having COUNT(*) >1 ;")
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    return resultado

def update_qualis_repetido(titulo,valor):
    sql = "update resultados set notas = '"+valor+"' where titulo = '"+titulo+"';"
    cursor = db.cursor()
    cursor.execute(sql)
    try:
        db.commit()
        print("Atualizado com Sucesso!")
    except:
        db.rollback()
        print("Sem Sucesso!")
    # db.close()