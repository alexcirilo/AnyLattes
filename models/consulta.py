# -*- coding: utf-8 -*-
import models.connection as database
from flask import flash


db = database.conexao()

def lista_por_titulo(titulo,docente):
    sql = "select * from resultados where titulo ='"+titulo+"' and nome_docente = '"+docente+"' "
    
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    
    if len(resultado)!=0 :
        return resultado
    else:
        return 0

def lista_por_id(id):
    sql = "select * from resultados where id ='"+id+"' "
    
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchone()
    return resultado

def lista():

    sql="select id, nome_docente, documento,ano_evento, titulo,doi,sigla,nome_evento, autores,estratos, round(notas,5) from resultados r order by ano_evento asc;"
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

    sql = (""" SELECT distinct nome_docente , round(sum(notas),3) from resultados where nome_docente in
                    (select distinct(nome_docente) from resultados)group by nome_docente order by nome_docente asc;""")
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    return resultado

def soma_nota_docente(docente):

    sql = (" SELECT distinct nome_docente , round(sum(notas),3) from resultados where nome_docente in"+
                    "(select distinct(nome_docente) from resultados where nome_docente = '"+docente+"')group by nome_docente order by ano_evento asc;")
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    return resultado


def contador_estratos():

    sql = ('select DISTINCT(nome_docente), count(estratos), estratos, ano_evento from resultados group by nome_docente, estratos, ano_evento order by ano_evento asc')
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
    sql = ("SELECT distinct titulo, notas, estratos, count(*) FROM resultados r WHERE titulo like '%"+titulo+"%' group by titulo, notas, estratos having COUNT(*) >1 ;")
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    return resultado

def titulo_repetido(titulo):
    sql = "select distinct titulo, notas, estratos, count(*), nome_docente from resultados r where titulo LIKE '%"+titulo+"%' group by nome_docente;"
    
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    if len(resultado)!=0 :
        return resultado
    else:
        return 0

#verificar quais titulos se repetem e quais docentes publicaram
def titulos_repetidos():
    # sql = ("select nome_docente, titulo from resultados r where titulo like '%"+titulo+"%' GROUP by titulo HAVING count(*)>1")
    sql = "SELECT distinct titulo, nome_docente FROM resultados r WHERE titulo in (SELECT DISTINCT titulo FROM resultados r group by titulo having COUNT(*) >1) group by titulo,nome_docente  order by titulo;"
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    return resultado

def titulo_repetidos(titulo):
    sql = ("select nome_docente, titulo from resultados r where titulo like '%"+titulo+"%' GROUP by titulo HAVING count(*)>1")
    # sql = "SELECT distinct titulo, nome_docente FROM resultados r WHERE titulo in (SELECT DISTINCT titulo FROM resultados r group by titulo having COUNT(*) >1) group by titulo,nome_docente  order by titulo;"
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    return resultado

def docente_titulos_repetidos():
    sql = "SELECT distinct  nome_docente FROM resultados r WHERE titulo in (SELECT DISTINCT titulo FROM resultados r group by titulo having COUNT(*) >1) group by titulo,nome_docente  order by titulo;"
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
        print(titulo +" Atualizado com Sucesso!")
    except:
        db.rollback()
        print("Sem Sucesso!")
    # db.close()
def mostra_publicacao(id):
    sql = "select id, nome_docente, titulo, doi, sigla, nome_evento, estratos from resultados r where id= "+id+";"
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchone()
    return resultado

def mostra_dados_faltantes(id):
    sql = "select id, nome_docente, titulo, autores, sigla, nome_evento from resultados r where id= "+id+";"
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchone()
    return resultado

def atualizar(id,doi,sigla,nome_evento,estratos, nota, versao):
    
    versao = versao + 1
    
    sql = ("update resultados set doi = '"+doi+"', sigla= '"+sigla+"', nome_evento = '"+nome_evento+"', estratos = '"+estratos+"', notas = '"+nota+"', versao = "+str(versao)+" where id = "+id+";")
    cursor = db.cursor()
    cursor.execute(sql)
    
    db.commit()
    print("Atualizado com Sucesso!")

        
def total_estratos():
    sql = 'SELECT ano_evento,estratos, COUNT(estratos) from resultados r group by ano_evento,estratos;'
    
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    
    return resultado

def perc():
    sql = ("select distinct total, 'Periódico', 'Conferência', round(periodico * 100 / total,3 ) as percentual_periodico, round(conferencia * 100 / total,3 ) as percentual_conferencia "+
        "from (select "+
        "(select count(1) from resultados r ) as total,"
        "(select count(1) from resultados r where r.documento like '%Peri%' ) as periodico,"+
        "(select count(1) from resultados r where r.documento like '%Conf%' ) as conferencia from resultados);")
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    
    return resultado

def perc_docente(docente):
    sql =( "select distinct total, 'Periódico', 'Conferência', round(periodico * 100 / total,3 ) as percentual_periodico, round(conferencia * 100 / total,3 ) as percentual_conferencia "+
          "from (select "+
            "(select count(1) from resultados r where nome_docente = '"+docente+"' ) as total,"+
            "(select count(documento) from resultados r where r.documento like '%Peri%' and  r.nome_docente = '"+docente+"' ) as periodico,"+
            "(select count(documento) from resultados r where r.documento like '%Conf%' and  r.nome_docente = '"+docente+"' ) as conferencia from resultados);")
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    
    return resultado

def busca_conferencias():
    sql = "SELECT COUNT(1) FROM RESULTADOS WHERE DOCUMENTO = 'Conferencia' group by nome_docente, documento;"
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    return resultado

#media todos docentes
def media_docentes():
    sql = "select nome_docente, round(sum(notas),3) as media from resultados r group by nome_docente ;"
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    return resultado

def deletar_docente(docente):
    
    resultado = False
    sql = "delete from resultados where nome_docente = '"+docente+"'; "
    cursor = db.cursor()
    cursor.execute(sql)
    try:
        print(docente + " Removido com Sucesso!")
        flash(docente + " Removido com Sucesso!")
        db.commit()
        resultado = True
    except:
        db.rollback()
        print("Sem Sucesso!")
        resultado = False
    return resultado
    

def lista_especifica(docente):
    sql = "select nome_docente, titulo from resultados where nome_docente = '"+docente+"'"
    
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    return resultado

def update_notas(nota, titulo):
    sql = "update resultados set notas = '"+nota+"' where titulo = '"+titulo+"' "
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    