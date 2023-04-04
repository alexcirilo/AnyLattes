create database lattes4web;
use lattes4web;

-- create table projetos(
-- id int(11) not null auto_increment,
-- nome varchar(255) not null,
-- titulo text not null,
-- ano_inicio varchar(4) not null,
-- natureza varchar(100) not null,
-- coordenador varchar(255),
-- financiamento text,
-- integrantes text,
-- primary key (id)
-- );

create table resultados(
id int(11) not null auto_increment,
nome_docente varchar(255) not null,
documento varchar(30) not null, 
ano_evento varchar(4) not null, 
titulo text not null, 
doi varchar(100) not null, 
sigla varchar(30) not null, 
nome_evento text not null, 
autores text not null,
estratos varchar(11), 
notas varchar(100),
primary key (id)
);