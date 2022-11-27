import models.connection as database

def zera_banco():
    db = database.conexao()
    cursor = db.cursor()
    
    
    sql=""" delete from resultados where id >=1;"""
    cursor.execute(sql)
    db.commit()
    retorna_auto_increment()
    
def retorna_auto_increment():
    db = database.conexao()
    cursor = db.cursor()
    
    
    sql=""" alter table resultados auto_increment = 1;"""
    cursor.execute(sql)
    db.commit()
    
    
    