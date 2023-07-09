# -*- coding: utf-8 -*-
import json
from models.docente import contador
from models.consulta import *
import statistics

def graficos(busca):
    nota = contador(busca)
    lista = []
    content = {}
    for n in nota:
        content = {'Ano': n[0], 'Estratos': n[1], 'Quantidade':n[2]}
        lista.append(content)
        content = {}

    json_object = json.dumps(lista,indent=4)
    with open("arq.json","w") as outfile:
        outfile.write(json_object)
        
def pizza():
    valor = perc()
    lista = []
    content = {}
    
    for n in valor:
        content = {'Total':n[0],'Periodico':n[1],'Conferencia':n[2],'PercConferencia':n[4], 'PercPeriodico':n[3] }
        lista.append(content)
        content = {}
        
    json_object = json.dumps(lista, indent=4)
    with open ("pizza.json", "w") as outfile:
        outfile.write(json_object)
    
def pizza_por_docente(docente):
    valor = perc_docente(docente)
    lista = []
    content = {}
    
    for n in valor:
        content = {'Total':n[0],'Periodico':n[1],'Conferencia':n[2],'PercConferencia':n[4], 'PercPeriodico':n[3] }
        lista.append(content)
        content = {}
        json_object = json.dumps(lista, indent=4)
    with open ("pizza_docente.json", "w") as outfile:
        outfile.write(json_object)
        
def grafico_media():
    nota = media_docentes()
    
    notas = []
    
    for n in nota:
        notas.append(n[1])
    mediana = statistics.median(notas)
    print(mediana)
    
        
    lista = []
    content = {}
    for n in nota:
        
        content = {'Docente': n[0], 'Média': n[1],'Mediana':mediana}
        lista.append(content)
        content = {}
        
    
    json_object = json.dumps(lista,indent=4)
    with open("media_docentes.json","w") as outfile:
        outfile.write(json_object)