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
        

def usuario(login, senha):
    try:
        db = database.conexao()
        cursor = db.cursor()
        sql = "select * from usuarios where login  = '"+login+"' and senha = '"+senha+"'"
        cursor.execute(sql)
        resultado = cursor.fetchone()
        return resultado
    except:
        flash("Usuário não encontrado")

def valida_usuario(nome, login):
    
    db = database.conexao()
    cursor = db.cursor()
    sql = "select * from usuarios where nome  = '"+nome+"' and login = trim('"+login+"')"
    cursor.execute(sql)
    resultado = cursor.fetchall()
    if len(resultado)!=0 :
        return resultado
    elif resultado == None:
        return 0
    else:
        return 0

def salvar_usuario(nome, login, senha):
    db = database.conexao()
    cursor = db.cursor()
    sql = (" insert into usuarios (nome, login, senha) "+
        "VALUES(?,?,?)")
    cursor.execute(sql,(nome,login, senha))
    db.commit()
    print(nome +" Salvo com Sucesso!")


def atualiza_usuario(nome, login, senha):
    try:
        db = database.conexao()
        cursor = db.cursor()
        sql = ("update usuarios set nome = '"+nome+"', login = '"+login+"', senha = '"+senha+"' "+
            "where login = '"+login+"' and nome = '"+nome+"' ")
        cursor.execute(sql)
        db.commit()
        print(nome +" atualizado com Sucesso!")
    except:
        print("Não foi possível atualizar")
        

    
    
    