import models.connection as database
# from models.consulta import retorna_auto_increment
from flask import flash
# db = database.conexao()
# cursor = db.cursor()

def zera_banco():
    try:    
        db = database.conexao()
        cursor = db.cursor()
        sql=""" delete from resultados where id >=1;"""
        cursor.execute(sql)
        db.commit()
        # retorna_auto_increment()
    except:
        flash("Erro de conexão com o banco de dados")
    
    # retorna_auto_increment()
    
# def retorna_auto_increment():
#     db = database.conexao()
#     cursor = db.cursor()
#     sql=""" alter table resultados auto_increment = 1;"""
#     cursor.execute(sql)
#     db.commit()
#     cursor.close()
#     db.close()
    
    
    
    