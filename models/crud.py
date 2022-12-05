import models.connection as database
db = database.conexao()
cursor = db.cursor()

def zera_banco():
    sql=""" delete from resultados where id >=1;"""
    cursor.execute(sql)
    db.commit()
    retorna_auto_increment()
    
def retorna_auto_increment():

    sql=""" alter table resultados auto_increment = 1;"""
    cursor.execute(sql)
    db.commit()
    
    
    
    