import xlrd
import os
import PyPDF2
import glob
import xml.etree.ElementTree as ET
from flask import redirect, render_template
import models.BaseDeCorrecoes
import models.connection as database
from models.consulta import *
# from models.crud import zera_banco
from googletrans import Translator
from models.consulta import * #qualis_repetidos,update_qualis_repetido
# from models.corrige_notas import *
# from models.EventosQualis import EventosQualis
from openpyxl import Workbook, load_workbook

db = database.conexao()

def import_project(anos):
    
    translator = Translator(service_urls=['translate.google.com'])    
    
    # zera_banco()
    
    xi = 1
    curriculos = []
    eventosQualis = []
    anos_validos = []
    
    for validos in anos:
        anos_validos.append(validos)
        # validos +1
    respAno = ''

    print('Importando documentos: QUALIS_novo.pdf')
    pdf = open("arquivos/QUALIS_novo.pdf", "rb")  # Script ler PDF inicio
    pdf_reader = PyPDF2.PdfFileReader(pdf,strict=False)
    n = pdf_reader.numPages

    resultado_total = ['']
    for i in range(0, n):
        page = pdf_reader.getPage(i)
        pg_extraida = page.extractText().split("\n")
    #    Script ler PDF fim
        resultado_total = (resultado_total + pg_extraida)

    print('Importanto documento: Qualis.xlsx...')
    # workbook2 = xlrd.open_workbook('arquivos/QualisEventosComp.xls')  # Script ler xls
    # worksheet2 = workbook2.sheet_by_index(1)
    workbook2 = load_workbook('arquivos/QualisConferencias.xlsx')
    worksheet2 = workbook2.active
    x = 0
    somaNotas = 0
    cont = 0
    nomeProfs = []
    resultados = []
    documento = []
    ano_evento = []
    titulosAnais = []
    doi = []
    siglas = []
    nomeEvento = []
    autor = []
    estratoss = []
    totalNotas = []
    issn = []

    print('Lendo currículo(s)... \n')
    for f in glob.glob('curriculos/*.xml'):
        curriculos.append(f)
        cont = cont+1

    curriculos.sort()
    i = 1
    print("currículos importados: "+str(cont))
    for m in range(0, len(curriculos)):
        tree = ET.parse(curriculos[m])
        root = tree.getroot()
        cont = 0
        totalNota = 0
        totalNotas = 0
        trabalho_valido = False
        autores = ''
        conferencia = ''
        periodico = ''
        notas = []
        ####################################################################################
        # Contadores de Conferências por ano
        cont17c = 0
        cont18c = 0
        cont19c = 0
        cont20c = 0
        # Contadores de Periódicos por ano
        cont17p = 0
        cont18p = 0
        cont19p = 0
        cont20p = 0
        # Contadores de Nota por ano
        nota17 = 0
        nota18 = 0
        nota19 = 0
        nota20 = 0
        # Contadores de estratos por conferência em 2017
        c17A1 = 0
        c17A2 = 0
        c17A3 = 0
        c17A4 = 0
        c17B1 = 0
        c17B2 = 0
        c17B3 = 0
        c17B4 = 0
        c17C = 0
        # Contadores de estratos por periódico em 2017
        p17A1 = 0
        p17A2 = 0
        p17A3 = 0
        p17A4 = 0
        p17B1 = 0
        p17B2 = 0
        p17B3 = 0
        p17B4 = 0
        p17C = 0
        # Contadores de estratos por conferência em 2018
        c18A1 = 0
        c18A2 = 0
        c18A3 = 0
        c18A4 = 0
        c18B1 = 0
        c18B2 = 0
        c18B3 = 0
        c18B4 = 0
        c18C = 0
        # Contadores de estratos por periódico em 2018
        p18A1 = 0
        p18A2 = 0
        p18A3 = 0
        p18A4 = 0
        p18B1 = 0
        p18B2 = 0
        p18B3 = 0
        p18B4 = 0
        p18C = 0
        # Contadores de estratos por conferência em 2019
        c19A1 = 0
        c19A2 = 0
        c19A3 = 0
        c19A4 = 0
        c19B1 = 0
        c19B2 = 0
        c19B3 = 0
        c19B4 = 0
        c19C = 0
        # Contadores de estratos por periódico em 2019
        p19A1 = 0
        p19A2 = 0
        p19A3 = 0
        p19A4 = 0
        p19B1 = 0
        p19B2 = 0
        p19B3 = 0
        p19B4 = 0
        p19C = 0
        # Contadores de estratos por conferência em 2020
        c20A1 = 0
        c20A2 = 0
        c20A3 = 0
        c20A4 = 0
        c20B1 = 0
        c20B2 = 0
        c20B3 = 0
        c20B4 = 0
        c20C = 0
        # Contadores de estratos por periódico em 2020
        p20A1 = 0
        p20A2 = 0
        p20A3 = 0
        p20A4 = 0
        p20B1 = 0
        p20B2 = 0
        p20B3 = 0
        p20B4 = 0
        p20C = 0
        ##################################################################################
        

        for t in root.iter('DADOS-GERAIS'):  # Imprimir nome do professor
            nomeProf = str(t.attrib['NOME-COMPLETO']).upper()
            print('Analisando publicações de {}'.format(nomeProf))
            x = x + 2
            
        x = x + 1
        
        for trabalhos in root.iter('TRABALHO-EM-EVENTOS'):  # Varre currículo
            autores = ''
            trabalho_valido = False
            for trab in trabalhos.iter():  # Laço para identificar as conferências válidas
                if trab.tag == 'DADOS-BASICOS-DO-TRABALHO' and trab.attrib['NATUREZA'] == 'COMPLETO' and trab.attrib['ANO-DO-TRABALHO'] in str(anos_validos):
                    conferencia = 'Conferencia;'
                    conferencia = conferencia + trab.attrib['ANO-DO-TRABALHO'] + ';' + trab.attrib['TITULO-DO-TRABALHO'] + ';' + trab.attrib['DOI'] + ';' + trab.attrib['NATUREZA']
                    # ano_projeto = trab.attrib['ANO-DO-TRABALHO']
                    trabalho_valido = True
                    cont = cont + 1
                if trabalho_valido and trab.tag == 'DETALHAMENTO-DO-TRABALHO':
                        conferencia = conferencia + ';' + trab.attrib['NOME-DO-EVENTO'].replace("amp;","") + ';' + trab.attrib['TITULO-DOS-ANAIS-OU-PROCEEDINGS'].replace("amp;","")
                if trabalho_valido and trab.tag == 'AUTORES':
                    if autores:
                        autores = autores + '/ ' + trab.attrib['NOME-COMPLETO-DO-AUTOR']
                    else:
                        autores = trab.attrib['NOME-COMPLETO-DO-AUTOR']
            if trabalho_valido: 
                resultado = (conferencia + ';' + autores)
                resultado = resultado.split(";")
                estratos = ''
                condicao = ''
                sigla = '-'
                doi = str(resultado[3]).upper()
                nomeEvento = resultado[5]
                tituloAnais = resultado[6]
                autor = resultado[7]
                    				
                if (condicao != '-'):

                    for i,rows in enumerate(worksheet2.values): #Comparação por SIGLA no resultado[6]
                        if i == 0:
                            continue
                        if (' {} '.format(rows[0]) in tituloAnais):
                            if (rows[0] != 'SBRC'):
                                sigla = rows[0]
                                estratos = rows[-1]
                                break
                        elif ('({})'.format(rows[0]) in tituloAnais):
                            sigla = rows[0]
                            estratos = rows[-1]
                            break
                        elif ('({} '.format(rows[0]) in tituloAnais):
                            sigla = rows[0]
                            estratos = rows[-1]
                            break
                        elif ('{}&'.format(rows[0]) in tituloAnais):
                            sigla = rows[0]
                            estratos = rows[-1]
                            break
                        elif ('{}_'.format(rows[0]) in tituloAnais):
                            sigla = rows[0]
                            
                            estratos = rows[-1]
                            break
                        elif (' {}2'.format(rows[0]) in tituloAnais):
                            sigla = rows[0]
                            
                            estratos = rows[-1]
                            break
                        
                        elif (' {} '.format(rows[0]) in nomeEvento): # Comparação por SIGLA no resultado[5]
                            sigla = rows[0]
                            
                            estratos = rows[-1]
                            break
                        elif ('({})'.format(rows[0]) in nomeEvento):
                            sigla = rows[0]
                            
                            estratos = rows[-1]
                            break
                        elif ('({} '.format(rows[0]) in nomeEvento):
                            sigla = rows[0]
                            
                            estratos = rows[-1]
                            break
                        elif ('{}&'.format(rows[0]) in nomeEvento):
                            sigla = rows[0]
                            
                            estratos = rows[-1]
                            break
                        elif ('{}_'.format(rows[0]) in nomeEvento):
                            sigla = rows[0]
                            
                            estratos = rows[-1]
                            break
                        elif (' {}2'.format(rows[0]) in nomeEvento):
                            sigla = rows[0]
                           
                            estratos = rows[-1]
                            break
                        elif ('XVII {}'.format(rows[0]) in str(nomeEvento).upper()):
                            sigla = rows[0]
                            
                            estratos = rows[-1]
                            break
                        elif ('({})'.format(rows[0]) in resultado[7]):
                            sigla = rows[0]
                            
                            estratos = rows[-1]
                            break
                        
                        elif rows[1] == tituloAnais:
                            sigla = rows[0]
                            estratos = rows[-1]
                            break
                        
                        else:
                            sigla = '-'
                            estratos = '-'
                          
                        if (estratos == '-'):  #Comparação por nome
                            if (str(rows[1]).upper() == str(resultado[5]).upper()):
                                sigla = rows[0]
                                estratos = rows[-1]
                                break
                            elif (str(rows[1]).upper() in str(resultado[6]).upper()):
                                sigla = rows[0]
                                estratos = rows[-1]
                                break
                            
                            elif (rows[1] in resultado[5]):
                                sigla = rows[0]
                                estratos = rows[-1]
                                break
                            elif (rows[1] in resultado[7]):
                                sigla = rows[0]
                                estratos = rows[-1]
                                break
                                
                    for rows in worksheet2.values:
                        
                        if (estratos == '-'):
                            if (" ({}'2019)".format(rows[0]) in resultado[6]): #Comparação por SIGLA casos especiais
                                sigla = rows[0]
                                estratos = rows[-1]
                                break
                            elif ("{}'18 ".format(rows[0]) in resultado[6] and rows[0] != 'ER'):
                                sigla = rows[0]
                                estratos = rows[-1]
                                break
                # documento.append(resultado[0])
                # ano_evento.append(resultado[1])
                # siglas.append(sigla)
                if ('COMPLETO' in tituloAnais):                          #Correção de tabela, elimina o "COMPLETO" do lugar errado
                    tituloAnais = (resultado[2] + resultado [3] + resultado[4])
                    doi = (resultado[5])
                    nomeEvento = (resultado[8] + ' / ' + autor)
                    autor = (resultado[9])
                elif ('COMPLETO' in nomeEvento):
                    tituloAnais = (resultado[2] + resultado[3])
                    doi = (resultado[4])
                    nomeEvento = (autor + ' / ' + resultado[6])
                    autor = (resultado[8])
                else:
                    tituloAnais = (resultado[2])
                    if (resultado[3] != ''):
                        doi = (resultado[3])
                    else:
                        doi = ('-')
                    nomeEvento = (nomeEvento)
                    if (len(resultado) > 8):
                        if (nomeProf in str(autor).upper()):
                            autor = (autor)
                        elif (nomeProf in str(resultado[8]).upper()):
                            autor = (resultado[8])
                    else:
                        autor = (autor)
                # estratoss.append(estratos)
                
                nota = 'SEM QUALIS'             #Calcula a nota do estrato
                if (estratos == 'A1'):
                    nota = models.BaseDeCorrecoes.A1c
                elif (estratos == 'A2'):
                    nota = models.BaseDeCorrecoes.A2c
                elif (estratos == 'A3'):
                    nota = models.BaseDeCorrecoes.A3c
                elif (estratos == 'A4'):
                    nota = models.BaseDeCorrecoes.A4c
                elif (estratos == 'B1'):
                    nota = models.BaseDeCorrecoes.B1c
                elif (estratos == 'B2'):
                    nota = models.BaseDeCorrecoes.B2c
                elif (estratos == 'B3'):
                    nota = models.BaseDeCorrecoes.B3c
                elif (estratos == 'B4'):
                    nota = models.BaseDeCorrecoes.B4c
                elif (estratos == 'C'):
                    nota = models.BaseDeCorrecoes.Cc
                
                # notas.append(nota)
                
                if (nota != 'SEM QUALIS'):                  #Contador de estratos das conferências
                    totalNota = totalNota + nota
                if (estratos != '-'):
                    if (resultado[1] == str(anos_validos)[0]):
                        cont17c = cont17c + 1
                        if (nota != 'SEM QUALIS'):          #somador de notas de 2017
                            nota17 = nota17 + nota
                        if (estratos == 'A1'):
                            c17A1 = c17A1 + 1
                        elif (estratos == 'A2'):
                            c17A2 = c17A2 + 1
                        elif (estratos == 'A3'):
                                c17A3 = c17A3 + 1
                        elif (estratos == 'A4'):
                            c17A4 = c17A4 + 1
                        elif (estratos == 'B1'):
                            c17B1 = c17B1 + 1
                        elif (estratos == 'B2'):
                                c17B2 = c17B2 + 1
                        elif (estratos == 'B3'):
                            c17B3 = c17B3 + 1
                        elif (estratos == 'B4'):
                            c17B4 = c17B4 + 1
                        elif (estratos == 'C'):
                            c17C = c17C + 1
                    elif (resultado[1] == str(anos_validos)[1]):
                        cont18c = cont18c + 1
                        if (nota != 'SEM QUALIS'):          #somador de notas de 2018
                            nota18 = nota18 + nota
                        if (estratos == 'A1'):
                            c18A1 = c18A1 + 1
                        elif (estratos == 'A2'):
                            c18A2 = c18A2 + 1
                        elif (estratos == 'A3'):
                            c18A3 = c18A3 + 1
                        elif (estratos == 'A4'):
                            c18A4 = c18A4 + 1
                        elif (estratos == 'B1'):
                            c18B1 = c18B1 + 1
                        elif (estratos == 'B2'):
                            c18B2 = c18B2 + 1
                        elif (estratos == 'B3'):
                            c18B3 = c18B3 + 1
                        elif (estratos == 'B4'):
                            c18B4 = c18B4 + 1
                        elif (estratos == 'C'):
                            c18C = c18C + 1
                    elif (resultado[1] == str(anos_validos)[2]):
                        cont19c = cont19c + 1
                        if (nota != 'SEM QUALIS'):          #somador de notas de 2019
                            nota19 = nota19 + nota
                        if (estratos == 'A1'):
                            c19A1 = c19A1 + 1
                        elif (estratos == 'A2'):
                            c19A2 = c19A2 + 1
                        elif (estratos == 'A3'):
                            c19A3 = c19A3 + 1
                        elif (estratos == 'A4'):
                            c19A4 = c19A4 + 1
                        elif (estratos == 'B1'):
                            c19B1 = c19B1 + 1
                        elif (estratos == 'B2'):
                            c19B2 = c19B2 + 1
                        elif (estratos == 'B3'):
                            c19B3 = c19B3 + 1
                        elif (estratos == 'B4'):
                            c19B4 = c19B4 + 1
                        elif (estratos == 'C'):
                            c19C = c19C + 1
                    elif (resultado[1] == str(anos_validos)[3]):
                        cont20c = cont20c + 1
                        if (nota != 'SEM QUALIS'):          #somador de notas de 2020
                            nota20 = nota20 + nota
                        if (estratos == 'A1'):
                            c20A1 = c20A1 + 1
                        elif (estratos == 'A2'):
                            c20A2 = c20A2 + 1
                        elif (estratos == 'A3'):
                            c20A3 = c20A3 + 1
                        elif (estratos == 'A4'):
                            c20A4 = c20A4 + 1
                        elif (estratos == 'B1'):
                            c20B1 = c20B1 + 1
                        elif (estratos == 'B2'):
                            c20B2 = c20B2 + 1
                        elif (estratos == 'B3'):
                            c20B3 = c20B3 + 1
                        elif (estratos == 'B4'):
                            c20B4 = c20B4 + 1
                        elif (estratos == 'C'):
                            c20C = c20C + 1
                
                #x = x + 1
                
                # print(nomeProf," | ", resultado[0], " | ", resultado[1]," | ", tituloAnais," | ", doi," | ", sigla ," | ",nomeEvento," | ", autor," | ", estratos," | ", nota)
                
                if(estratos == '' or estratos == '-' or estratos == ' C'):
                    estratos= 'C'
                    nota = '0'
                    
                c = db.cursor()
                
                data  = """ insert into resultados (nome_docente, documento, ano_evento, titulo, doi, sigla, nome_evento, autores,estratos, notas)
                                VALUES (?,?,?,?,?,?,?,?,?,?)"""
                                            
                c.execute(data,(nomeProf, resultado[0], resultado[1], tituloAnais, doi, sigla ,nomeEvento, autor, estratos, nota))
                db.commit()
                
                e1 = []

                e1.append(tituloAnais)

                eventosQualis.append(e1)
                
                
        for trabalhos in root.iter('ARTIGO-PUBLICADO'):           #Varrer currículo
            autores = ''
            trabalho_valido = False
            for trab in trabalhos.iter():
                if trab.tag == 'DADOS-BASICOS-DO-ARTIGO' and trab.attrib['NATUREZA'] == 'COMPLETO' and trab.attrib['ANO-DO-ARTIGO'] in str(anos_validos):
                    periodico = 'Periodico;'
                    periodico = periodico + trab.attrib['ANO-DO-ARTIGO'] + ';'+ trab.attrib['TITULO-DO-ARTIGO'] +';' + trab.attrib['DOI'] +';' + trab.attrib['NATUREZA']
                    trabalho_valido = True
                    cont = cont + 1
                if trabalho_valido and trab.tag == 'DETALHAMENTO-DO-ARTIGO':
                    periodico = periodico + ';'+ trab.attrib['TITULO-DO-PERIODICO-OU-REVISTA'].replace(";","")
                    periodico = periodico.replace("&amp","&")
                    issn = trab.attrib['ISSN']		
                    issn = issn[0:4]+ '-' + issn[4:8]
                if trabalho_valido and trab.tag == 'AUTORES':
                    if autores: 
                        autores = autores + '/ '+ trab.attrib['NOME-COMPLETO-DO-AUTOR']
                    else:
                        autores = trab.attrib['NOME-COMPLETO-DO-AUTOR']
                
            if trabalho_valido:
                resultado2 = (periodico + ';' + autores)
                resultado2 = resultado2.split(";")
                estratos2 = ''
                doi = str(resultado2[3]).upper()
                nomeEvento = resultado2[5]
                sigla2= '-'
                                  
                #     ######################################################
                # if str(resultado2[5]) == translator.translate(str(resultado2[5]),src="en",dest="pt"):
                #     nomeEvento = translator.translate(str(resultado2[5]),src="en",dest="pt")
                #     print(nomeEvento)
                # elif str(resultado2[5]) == translator.translate(str(resultado2[5]),src="pt",dest="en"):
                #     nomeEvento = translator.translate(str(resultado2[5]),src="pt",dest="en")
                #     print(nomeEvento)
                # # nomeEvento = resultado2[5]
                # # print(nomeEvento)
                
                
                if (estratos2 == ''):

                    for i in range(0,len(resultado_total)):
                        resultado_issn = resultado_total[i][0:9]
                        if(issn in resultado_issn):
                            print('yes')
                            estratos2 = resultado_total[i][-2:]
                            # print(resultado_total[i][-2:])
                            
                            
                if ('COMPLETO' in nomeEvento):                        #Correção de tabela, elimina o "COMPLETO" do lugar errado
                    tituloAnais = (resultado2[2] + resultado2[3])
                    doi = (resultado2[4])
                    nomeEvento = resultado2[6]
                    autor = resultado2[7]
                else:
                    tituloAnais = resultado2[2]
                    if (resultado2[3] != ''):
                        doi = resultado2[3]
                    else:
                        doi = '-'
						
                    nomeEvento = nomeEvento
                    autor = resultado2[6]
                estratos2 = estratos2
                
                nota = 'SEM QUALIS'               #Calcula nota do estrato
                if (estratos2 == 'A1'):
                    nota = models.BaseDeCorrecoes.A1p
                elif (estratos2 == 'A2'):
                    nota = models.BaseDeCorrecoes.A2p
                elif (estratos2 == 'A3'):
                    nota = models.BaseDeCorrecoes.A3p
                elif (estratos2 == 'A4'):
                    nota = models.BaseDeCorrecoes.A4p
                elif (estratos2 == 'B1'):
                    nota = models.BaseDeCorrecoes.B1p
                elif (estratos2 == 'B2'):
                    nota = models.BaseDeCorrecoes.B2p
                elif (estratos2 == 'B3'):
                    nota = models.BaseDeCorrecoes.B3p
                elif (estratos2 == 'B4'):
                    nota = models.BaseDeCorrecoes.B4p
                elif (estratos2 == 'C'):
                    nota = models.BaseDeCorrecoes.Cp
					
				
                # notas.append(nota)
                    
                if (nota != 'SEM QUALIS'):            #Contador de estratos dos periódicos
                    totalNota = totalNota + nota
                if (estratos2 != '-'):
                    if (resultado2[1] == '2017'):
                        cont17p = cont17p + 1
                        if (nota != 'SEM QUALIS'):          #somador de notas de 2017
                            nota17 = nota17 + nota
                        if (estratos2 == 'A1'):
                            p17A1 = p17A1 + 1
                        elif (estratos2 == 'A2'):
                            p17A2 = p17A2 + 1
                        elif (estratos2 == 'A3'):
                            p17A3 = p17A3 + 1
                        elif (estratos2 == 'A4'):
                            p17A4 = p17A4 + 1
                        elif (estratos2 == 'B1'):
                            p17B1 = p17B1 + 1
                        elif (estratos2 == 'B2'):
                            p17B2 = p17B2 + 1
                        elif (estratos2 == 'B3'):
                            p17B3 = p17B3 + 1
                        elif (estratos2 == 'B4'):
                            p17B4 = p17B4 + 1
                        elif (estratos2 == 'C'):
                            p17C = p17C + 1
                    elif (resultado2[1] == '2018'):
                        cont18p = cont18p + 1
                        if (nota != 'SEM QUALIS'):          #somador de notas de 2018
                            nota18 = nota18 + nota
                        if (estratos2 == 'A1'):
                            p18A1 = p18A1 + 1
                        elif (estratos2 == 'A2'):
                            p18A2 = p18A2 + 1
                        elif (estratos2 == 'A3'):
                            p18A3 = p18A3 + 1
                        elif (estratos2 == 'A4'):
                            p18A4 = p18A4 + 1
                        elif (estratos2 == 'B1'):
                            p18B1 = p18B1 + 1
                        elif (estratos2 == 'B2'):
                            p18B2 = p18B2 + 1
                        elif (estratos2 == 'B3'):
                            p18B3 = p18B3 + 1
                        elif (estratos2 == 'B4'):
                            p18B4 = p18B4 + 1
                        elif (estratos2 == 'C'):
                            p18C = p18C + 1
                    elif (resultado2[1] == '2019'):
                        cont19p = cont19p + 1
                        if (nota != 'SEM QUALIS'):          #somador de notas de 2019
                            nota19 = nota19 + nota
                        if (estratos2 == 'A1'):
                            p19A1 = p19A1 + 1
                        elif (estratos2 == 'A2'):
                            p19A2 = p19A2 + 1
                        elif (estratos2 == 'A3'):
                            p19A3 = p19A3 + 1
                        elif (estratos2 == 'A4'):
                            p19A4 = p19A4 + 1
                        elif (estratos2 == 'B1'):
                            p19B1 = p19B1 + 1
                        elif (estratos2 == 'B2'):
                            p19B2 = p19B2 + 1
                        elif (estratos2 == 'B3'):
                            p19B3 = p19B3 + 1
                        elif (estratos2 == 'B4'):
                            p19B4 = p19B4 + 1
                        elif (estratos2 == 'C'):
                            p19C = p19C + 1
                    elif (resultado2[1] == '2020'):
                        cont20p = cont20p + 1
                        if (nota != 'SEM QUALIS'):          #somador de notas de 2020
                            nota20 = nota20 + nota
                        if (estratos2 == 'A1'):
                            p20A1 = p20A1 + 1
                        elif (estratos2 == 'A2'):
                            p20A2 = p20A2 + 1
                        elif (estratos2 == 'A3'):
                            p20A3 = p20A3 + 1
                        elif (estratos2 == 'A4'):
                            p20A4 = p20A4 + 1
                        elif (estratos2 == 'B1'):
                            p20B1 = p20B1 + 1
                        elif (estratos2 == 'B2'):
                            p20B2 = p20B2 + 1
                        elif (estratos2 == 'B3'):
                            p20B3 = p20B3 + 1
                        elif (estratos2 == 'B4'):
                            p20B4 = p20B4 + 1
                        elif (estratos2 == 'C'):
                            p20C = p20C + 1
                            
                            
                # x = x + 1
                # print(nomeProf," | ", resultado2[0]," | ", resultado2[1]," | ", tituloAnais," | ", doi," | ", sigla ," | ",nomeEvento," | ", autor," | ", estratos2," | ", nota)
                if(estratos2 == '' or estratos2 == '-' or estratos2 == ' C'):
                    estratos2= 'C'
                    nota = '0'
                    
                c = db.cursor()
                data  = """ insert into resultados (nome_docente, documento, ano_evento, titulo, doi, sigla, nome_evento, autores,estratos, notas)
                                VALUES (?,?,?,?,?,?,?,?,?,?)"""
                                            
                c.execute(data,(nomeProf, resultado2[0], resultado2[1], tituloAnais, doi, sigla2 ,nomeEvento, autor, estratos2, nota))
                db.commit()
                c.close()
                e2 = []

                e2.append(tituloAnais)

                eventosQualis.append(e2)
                
            
        
        totalNotas = []
        totalNotas.append(totalNota)
        print('Total de publicações = {}'.format(cont))            #Quantidade de documentos válidos de cada professor
        print('Pontuação total = {}'.format(totalNota))            #Nota do professor
        print('------------------------------------------------------------')
        print(str(anos_validos))


    titulosRepetidos = titulos_qualis()
    for tits in titulosRepetidos:
        for t in tits:
            rep = qualis_repetidos(titulo=t)
            for r in rep:
                print(r)
                if r[0] == t:
                    media = float(r[1]) / float(r[3])
                    update_qualis_repetido(titulo=r[0],valor=str(media))
                    # showinfo(title="VALIDADO",message="Corrigido com Sucesso!")
                    break
    return redirect('/resultado_total')
