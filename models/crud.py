import models.connection as database

from flask import flash


def zera_banco():
    try:    
        db = database.conexao()
        cursor = db.cursor()
        sql=""" delete from resultados where id >=1;"""
        cursor.execute(sql)
        db.commit()
    except:
        flash("Erro de conexão com o banco de dados")
    

    
    
    