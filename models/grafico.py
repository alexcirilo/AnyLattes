# -*- coding: utf-8 -*-
import json
from models.docente import contador
from models.consulta import *
import statistics
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# from wordcloud import WordCloud
# import nltk
# import wordcloud
from models.gerar_nuvem import *

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

def grafico_colaboracao():
    lista_docente = []
    G = nx.Graph()
    docente = docente_titulos_repetidos()

    for doc in docente:
        for d in doc:
            lista_docente.append(d)
            d = d.split()[0] +" "+ d.split()[-1]
            G.add_node(d)
            
    valor = titulos_repetidos()

    for i in range(0,len(valor)):
            atual = valor[i][0]
            anterior = valor[i-1][0]
            
            docente1 = valor[i][1].split()[0] + ' ' + valor[i][1].split()[-1]
            # print(docente1)
            docente2 = valor[i-1][1].split()[0] + ' ' + valor[i-1][1].split()[-1]
            # print(docente2)
            if atual == anterior:
                G.add_edge(docente1, docente2)
    A = nx.adjacency_matrix(G)
    # fig = plt.figure(1,figsize=(20,15),dpi=100)
    # nx.draw_circular(G, with_labels=True, node_size=5000,font_size=15)
    # plt.savefig("static/images/matriz_colaboracao_circular.png")
    return G
    
def tipo_grafo(valor, G):
    # plt.cla()
    
    if valor == 'circular':
        fig = plt.figure(1,figsize=(18,15),dpi=100)
        nx.draw_circular(G, with_labels=True, node_size=5000,font_size=15)
        plt.savefig("static/images/matriz_colaboracao_circular.png")

    elif valor == 'kamada_kawai':
        fig = plt.figure(1,figsize=(18,15),dpi=100)
        nx.draw_kamada_kawai(G, with_labels=True, node_size=5000,font_size=15)
        plt.savefig("static/images/matriz_colaboracao_kamada_kawai.png")
        
    elif valor == 'planar':
        fig = plt.figure(1,figsize=(18,15),dpi=100)
        nx.draw_planar(G, with_labels=True, node_size=5000,font_size=15)
        plt.savefig("static/images/matriz_colaboracao_planar.png")
        
    elif valor == 'random':
        fig = plt.figure(1,figsize=(18,15),dpi=100)
        nx.draw_random(G, with_labels=True, node_size=5000,font_size=15)
        plt.savefig("static/images/matriz_colaboracao_random.png")
        
    plt.clf()
    
def nuvem_de_palavras():    
    nuvem_geral()
    
    
def nuvem_por_docente(docente):
    nuvem_especifica(docente)
    

    
    