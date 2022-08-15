create database lattes4web;
use lattes4web;

create table projetos(
id int(11) not null auto_increment,
nome varchar(255) not null,
titulo text not null,
ano_inicio varchar(4) not null,
natureza varchar(100) not null,
coordenador varchar(255),
financiamento text,
integrantes text,
primary key (id)
);