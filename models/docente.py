import models.connection as database

# db = database.conexao()
# cursor = db.cursor()
def contador(nome_docente):
    # cursor.execute("select ano_evento ,estratos, COUNT(estratos)" +
    #                "from resultados r where nome_docente = %s"+
    #                "GROUP BY estratos, nome_docente, ano_evento order by estratos asc")
    
    # cursor.execute("select ano_evento, estratos,COUNT(estratos) from resultados where nome_docente = "+nome_docente+")"
    sql = "select ano_evento,estratos,count(estratos) from resultados where nome_docente = '"+nome_docente+"' group by estratos, ano_evento"
    cursor = g.conn.cursor()
    cursor.execute(sql)
    # cursor.close()
    # db.close()
    return resultado