import models.connection as database

db = database.conexao()
cursor = db.cursor()
def contador(nome_docente):

    sql = "select ano_evento,estratos,count(estratos) from resultados where nome_docente = '"+nome_docente+"' group by estratos, ano_evento order by ano_evento asc"
    resultado = cursor.execute(sql)

    return resultado

def todosContador():
    sql = "select ano_evento, estratos, count(estratos) as quantidade from resultados group by estratos, ano_evento order by ano_evento asc"
    resultado = cursor.execute(sql)
    
    return resultado

def periodicos():
    sql = "select count(1) from resultados where documento = 'Periodico' GROUP by nome_docente,documento"
    resultado = cursor.execute(sql)
    return resultado

