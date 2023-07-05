import models.connection as database


db = database.conexao()
def lista():

    sql="select id, nome_docente, documento,ano_evento, titulo,doi,sigla,nome_evento, autores,estratos, notas from resultados r order by ano_evento asc;"
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
                    (select distinct(nome_docente) from resultados)group by nome_docente order by ano_evento asc;""")
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

#verificar quais titulos se repetem e quais docentes publicaram
def titulos_repetidos(titulo):
    sql = ("SELECT titulo, nome_docente FROM resultados r WHERE titulo like '%"+titulo+"%' group by nome_docente ;")
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
        print(titulo +"Atualizado com Sucesso!")
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

def atualizar(id,nome_docente,titulo,doi,sigla,nome_evento,estratos, nota):
    sql = ("update resultados set nome_docente = '"+nome_docente+"',"+
           "titulo = '"+titulo+"', doi = '"+doi+"', sigla= '"+sigla+"', nome_evento = '"+nome_evento+"', estratos = '"+estratos+"', notas = '"+nota+"' where id = "+id+";")
    cursor = db.cursor()
    cursor.execute(sql)
    try:
        db.commit()
        print(titulo +"Atualizado com Sucesso!")
    except:
        db.rollback()
        print("Sem Sucesso!")
        
def total_estratos():
    sql = 'SELECT ano_evento,estratos, COUNT(estratos) from resultados r group by ano_evento,estratos;'
    
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    
    return resultado

def perc():
    sql = ("select distinct total, 'Periodico', 'Conferencia', round(periodico * 100 / total,3 ) as percentual_periodico, round(conferencia * 100 / total,3 ) as percentual_conferencia "+
        "from (select "+
        "(select count(1) from resultados r ) as total,"
        "(select count(1) from resultados r where r.documento = 'Periodico' ) as periodico,"+
        "(select count(1) from resultados r where r.documento = 'Conferencia' ) as conferencia from resultados);")
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    
    return resultado

def perc_docente(docente):
    sql =( "select distinct total, 'periodico', 'conferencia', round(periodico * 100 / total,3 ) as percentual_periodico, round(conferencia * 100 / total,3 ) as percentual_conferencia "+
          "from (select "+
            "(select count(1) from resultados r where nome_docente = '"+docente+"' ) as total,"+
            "(select count(documento) from resultados r where r.documento = 'Periodico' and  r.nome_docente = '"+docente+"' ) as periodico,"+
            "(select count(documento) from resultados r where r.documento = 'Conferencia' and  r.nome_docente = '"+docente+"' ) as conferencia from resultados);")
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