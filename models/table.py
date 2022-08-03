from flask import flash
from app import db

cursor = db.connection.cursor()

cursor.execute(''' create database if not exists lattes4web; 
               use lattes4web;
               create table projetos(
                   id int(11) not null auto_increment primary key,
                   nome varchar(255) not null,
                   titulo text not null,
                   ano_inicio varchar(4) not null,
                   natureza varchar(25) not null, 
                   coordenador varchar(255) not null,
                   financiamento varchar(255), 
                   integrantes text not null) ''')
flash("Database Criado com sucesso!")
