import xlrd
import os
import PyPDF2
import glob
import xml.etree.ElementTree as ET
from flask import render_template
import models.BaseDeCorrecoes
import mysql.connector


'''
heroku access
'''

user= 'b96e08051c345f'
pwd= '2503c6ba'
host= 'us-cdbr-east-06.cleardb.net'
database= 'heroku_34fb507d853ce4f'

'''
local access

user = 'root'
pwd = 'Qwer@1234'
host = 'localhost'
database = 'lattes4web'
'''
try:
    db = mysql.connector.connect(user=user,password= pwd,host=host, database=database)
    
except:
    print("not connect")


def import_project():
    xi = 1
    curriculos = []
    anos_validos = {'2017','2018','2019','2020'}
    respAno = ''

    print('Importando documentos: QUALIS_novo.pdf')
    pdf = open("arquivos/QUALIS_novo.pdf", "rb")  # Script ler PDF inicio
    pdf_reader = PyPDF2.PdfFileReader(pdf)
    n = pdf_reader.numPages

    resultado_total = ['']
    for i in range(0, n):
        page = pdf_reader.getPage(i)
        pg_extraida = page.extractText().split("\n")
    #    Script ler PDF fim
        resultado_total = (resultado_total + pg_extraida)

    print('Importanto documento: QualisEventosComp.xls...')
    workbook2 = xlrd.open_workbook('arquivos/QualisEventosComp.xls')  # Script ler xls
    worksheet2 = workbook2.sheet_by_index(1)

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
                if trab.tag == 'DADOS-BASICOS-DO-TRABALHO' and trab.attrib['NATUREZA'] == 'COMPLETO' and trab.attrib['ANO-DO-TRABALHO'] in anos_validos:
                    conferencia = 'Conferencia;'
                    conferencia = conferencia + trab.attrib['ANO-DO-TRABALHO'] + ';' + trab.attrib['TITULO-DO-TRABALHO'] + ';' + trab.attrib['DOI'] + ';' + trab.attrib['NATUREZA']
                    # ano_projeto = trab.attrib['ANO-DO-TRABALHO']
                    trabalho_valido = True
                    cont = cont + 1
                if trabalho_valido and trab.tag == 'DETALHAMENTO-DO-TRABALHO':
                        conferencia = conferencia + ';' + trab.attrib['NOME-DO-EVENTO'] + ';' + trab.attrib['TITULO-DOS-ANAIS-OU-PROCEEDINGS']
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
                
                
                ###############################################
                if (doi == str('10.1109/iV.2017.37').upper()):
                    estratos = 'A4'
                    condicao = '-'
                elif(doi == str('10.1109/iV.2017.29').upper()):
                    estratos = 'A4'
                    condicao = '-'
                elif(doi == str('10.1109/IV-2.2019.00019').upper()):
                    estratos = 'A4'
                    autor = autores #resultado[11]
                    condicao = '-'
                elif(doi == str('10.1109/IV-2.2019.00020').upper()):
                    estratos = 'A4'
                    autor = autores #resultado[11]
                    condicao = '-'
                elif(doi == str('10.1109/iccw.2018.8403776').upper()): #ICC Workshops
                    estratos = 'B3'
                    condicao = '-'
                elif(doi == str('10.1145/3084226.3084278').upper()): #EASE
                    estratos = 'A3'
                    condicao = '-'
                elif(doi == str('10.1145/3210459.3210462').upper()): #EASE
                    estratos = 'A3'
                    condicao = '-'
                elif(doi == str('10.1109/IMOC.2017.8121084').upper()):
                    estratos = 'B4'
                    condicao = '-'
                elif(doi == str('10.1109/icton.2017.8024977').upper()):
                    estratos = 'A4'
                    condicao = '-'
                elif(doi == str('10.1109/IV-2.2019.00033').upper()):
                    estratos = 'A4'
                    autor = autores #resultado[7]
                    condicao = '-'
                elif(doi == str('10.1145/3275245.3275290').upper()):
                    estratos = 'B1'
                    condicao = '-'
                elif(str('Brazilian Symposium on Computer Networks and Distributed Systems').upper() in str(tituloAnais).upper()):
                    estratos = 'A4'
                    condicao = '-'
                elif(str('Brazilian Symposium on Computer Networks and Distributed Systems').upper() in str(resultado[7]).upper()):
                    estratos = 'A4'
                    condicao = '-'
                elif(str('Proceedings of the 18th Brazilian Symposium on Human Factors in Computing Systems').upper() in str(tituloAnais).upper()):
                    estratos = 'B1'
                    condicao = '-'
                elif(str('Anais do I Workshop de Computação Urbana').upper() in str(tituloAnais).upper()):
                    estratos = 'B1'
                    condicao = '-'
                elif(str('The 33rd ACM/SIGAPP Symposium On Applied Computing').upper() in str(tituloAnais).upper()):
                    estratos = 'A2'
                    condicao = '-'
                elif(str('Proceedings of 2018 International Joint Conference on Neural Networks').upper() in str(tituloAnais).upper()):
                    estratos = 'A2'
                    condicao = '-'
                ###########################################
                    				
                if (condicao != '-'):
                    for row_num in range(worksheet2.nrows):                #Comparação por SIGLA no resultado[6]
                        if row_num == 0:
                            continue
                        row = worksheet2.row_values(row_num)
                        if (' {} '.format(row[0]) in tituloAnais):
                            if (row[0] != 'SBRC'):
                                sigla = row[0]
                                estratos = row[8]
                                break
                        elif ('({})'.format(row[0]) in tituloAnais):
                            sigla = row[0]
                            estratos = row[8]
                            break
                        elif ('({} '.format(row[0]) in tituloAnais):
                            sigla = row[0]
                            estratos = row[8]
                            break
                        elif ('{}&'.format(row[0]) in tituloAnais):
                            sigla = row[0]
                            estratos = row[8]
                            break
                        elif ('{}_'.format(row[0]) in tituloAnais):
                            sigla = row[0]
                            #					print(row[8] + ' --> ' + sigla)# + ' #6_#')
                            estratos = row[8]
                            break
                        elif (' {}2'.format(row[0]) in tituloAnais):
                            sigla = row[0]
                            #					print(row[8] + ' --> ' + sigla)# + ' # 62#')
                            estratos = row[8]
                            break
                        # Comparação por SIGLA no resultado[5]
                        elif (' {} '.format(row[0]) in nomeEvento):
                            sigla = row[0]
                            #					print(row[8] + ' --> ' + sigla)# + ' # 5 #')
                            estratos = row[8]
                            break
                        elif ('({})'.format(row[0]) in nomeEvento):
                            sigla = row[0]
                            #					print(row[8] + ' --> ' + sigla)# + ' #(5)')
                            estratos = row[8]
                            break
                        elif ('({} '.format(row[0]) in nomeEvento):
                            sigla = row[0]
                            #					print(row[8] + ' --> ' + sigla)# + ' #(5 #')
                            estratos = row[8]
                            break
                        elif ('{}&'.format(row[0]) in nomeEvento):
                            sigla = row[0]
                            #					print(row[8] + ' --> ' + sigla)# + ' #5&#')
                            estratos = row[8]
                            break
                        elif ('{}_'.format(row[0]) in nomeEvento):
                            sigla = row[0]
                            #					print(row[8] + ' --> ' + sigla)# + ' #5_#')
                            estratos = row[8]
                            break
                        elif (' {}2'.format(row[0]) in nomeEvento):
                            sigla = row[0]
                            #					print(row[8] + ' --> ' + sigla)# + ' # 52#')
                            estratos = row[8]
                            break
                        elif ('XVII {}'.format(row[0]) in str(nomeEvento).upper()):
                            sigla = row[0]
                            #					print(row[8] + ' --> ' + sigla)# + ' #XVII 5up#')
                            estratos = row[8]
                            break
                        elif ('({})'.format(row[0]) in resultado[7]):
                            sigla = row[0]
                            #					print(row[8] + ' --> ' + sigla)# + '#(5)')
                            estratos = row[8]
                            break
                        else:
                            sigla = '-'
                            estratos = '-'
                    # print(resultado)                #imprime resultado completo
                    # print(tituloAnais)               #imprime apenas o titulo-do-anais-ou-periodico, resultado[6]
                    # print(nomeEvento)                #imprime apenas o nome-do-evento, resultado[5]
                    # print(estratos)      
                    for row_num in range(worksheet2.nrows):                       #Comparação por nome
                        if row_num == 0:
                            continue
                        row = worksheet2.row_values(row_num)
                        if (estratos == '-'):
                            if (str(row[1]).upper() in str(resultado[6]).upper()):
                                sigla = row[0]
                                estratos = row[8]
                                break
                            elif (row[1] in resultado[5]):
                                sigla = row[0]
                                estratos = row[8]
                                break
                            elif (row[1] in resultado[7]):
                                sigla = row[0]
                                estratos = row[8]
                                break
                    for row_num in range(worksheet2.nrows):                #Comparação por SIGLA casos especiais
                        if row_num == 0:
                            continue
                        row = worksheet2.row_values(row_num)
                        if (estratos == '-'):
                            if (" ({}'2019)".format(row[0]) in resultado[6]):
                                sigla = row[0]
                                estratos = row[8]
                                break
                            elif ("{}'18 ".format(row[0]) in resultado[6] and row[0] != 'ER'):
                                sigla = row[0]
                                estratos = row[8]
                                break
                documento.append(resultado[0])
                ano_evento.append(resultado[1])
                siglas.append(sigla)
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
                estratoss.append(estratos)
                
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
                
                notas.append(nota)
                
                if (nota != 'SEM QUALIS'):                  #Contador de estratos das conferências
                    totalNota = totalNota + nota
                if (estratos != '-'):
                    if (resultado[1] == '2017'):
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
                    elif (resultado[1] == '2018'):
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
                    elif (resultado[1] == '2019'):
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
                    elif (resultado[1] == '2020'):
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
                
                print(nomeProf," | ", resultado[0], " | ", resultado[1]," | ", tituloAnais," | ", doi," | ", sigla ," | ",nomeEvento," | ", autor," | ", estratos," | ", nota)
                c = db.cursor()
                
                data  = """ insert into resultados (nome_docente, documento, ano_evento, titulo, doi, sigla, nome_evento, autores,estratos, notas)
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                                            
                c.execute(data,(nomeProf, resultado[0], resultado[1], tituloAnais, doi, sigla ,nomeEvento, autor, estratos, nota))
                db.commit()
                
        for trabalhos in root.iter('ARTIGO-PUBLICADO'):           #Varrer currículo
            autores = ''
            trabalho_valido = False
            for trab in trabalhos.iter():
                if trab.tag == 'DADOS-BASICOS-DO-ARTIGO' and trab.attrib['NATUREZA'] == 'COMPLETO' and trab.attrib['ANO-DO-ARTIGO'] in anos_validos:
                    periodico = 'Periodico;'
                    periodico = periodico + trab.attrib['ANO-DO-ARTIGO'] + ';'+ trab.attrib['TITULO-DO-ARTIGO'] +';' + trab.attrib['DOI'] +';' + trab.attrib['NATUREZA']
                    trabalho_valido = True
                    cont = cont + 1
                if trabalho_valido and trab.tag == 'DETALHAMENTO-DO-ARTIGO':
                    periodico = periodico + ';'+ trab.attrib['TITULO-DO-PERIODICO-OU-REVISTA']				
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
                ##################################################### Base de correção dos Periódicos
                if(doi == str('10.14209/jcis.2019.22').upper()):
                    estratos2 = 'A4'
                elif(doi == str('10.1155/2017/2865482').upper()):
                    estratos2 = 'B1'
                elif(doi == str('10.1177/1475921718799070').upper()):
                    estratos2 = 'A1'
                elif(doi == str('10.1007/s00530-015-0501-6').upper()):
                    estratos2 = 'A2'
                elif(doi == str('10.1016/j.compenvurbsys.2017.05.001').upper()):
                    estratos2 = 'A1'
                elif(doi == str('10.1002/spe.2637').upper()):
                    estratos2 = 'A3'
                elif(doi == str('10.1177/1475921718799070').upper()):
                    estratos2 = 'A1'
                elif(doi == str('10.1590/0074-02760170111').upper()):
                    estratos2 = 'A2'
                elif(doi == str('10.1002/nem.2055').upper()):
                    estratos2 = 'A4'
                elif(str('REVISTA DA ABET').upper() in str(resultado2[5]).upper()):
                    estratos2 = 'A4'
                elif(str('Journal of Communication and Information Systems').upper() in str(resultado2[5]).upper()):
                    estratos2 = 'A4' 
                    #######################################################
                    
                if (estratos2 == ''):
                    for i in range(0,len(resultado_total)):                   #Comparação por nome
                        # nomePeriodico = str(resultado2[5]).upper()
                        if (str(resultado2[5]).upper() in resultado_total[i]):
                            if (' {} '.format(str(resultado2[5]).upper()) in resultado_total[i]):
                            #print(resultado_total[i+1])
                                # #estratos2 = '-'
                                continue
                            if (len(resultado2[5]) == len(resultado_total[i])):
		#						print(resultado_total[i+1])
                                estratos2 = resultado_total[i+1]
                                break
                            elif (len(resultado2[5]) < len(resultado_total[i])):
                                if ('{} (PRINT)'.format(str(resultado2[5]).upper()) == resultado_total[i]):
		#							print(resultado_total[i+1])
                                    estratos2 = resultado_total[i+1]
		#							print(estratos2)
                                    break
                                if ('{} (ONLINE)'.format(str(resultado2[5]).upper()) == resultado_total[i]):
                                    #								print(resultado_total[i+1])
                                    estratos2 = resultado_total[i+1]
		#							print(estratos2)
                                    break
                                elif ('ACS {}'.format(str(resultado2[5]).upper()) == resultado_total[i]):
                                    #								print(resultado_total[i+1])
                                    estratos2 = resultado_total[i+1]
		#							print(estratos2)
                                    break
                                elif ('THE {}'.format(str(resultado2[5]).upper()) == resultado_total[i]):
		#							print(resultado_total[i+1])
                                    estratos2 = resultado_total[i+1]
		#							print(estratos2)
                                    break
                                elif ('{} (19'.format(str(resultado2[5]).upper()) in resultado_total[i]):
                                    #								print(resultado_total[i+1])
                                    estratos2 = resultado_total[i+1]
		#							print(estratos2)
                                    break
                                elif (len(resultado_total[i]) - len(resultado2[5]) <= 12):
                                    if ('{} ('.format(str(resultado2[5]).upper()) in resultado_total[i]):
		#								print(resultado_total[i+1])
                                        estratos2 = resultado_total[i+1]
		#								print(estratos2)
										#print(resultado_total[i])
                                        break
                                    else:
                                        same = input(resultado2[5] + ' é o mesmo que ' + resultado_total[i] + '? (S/N) \n')
                                        resp = False
                                        while (resp == False):
                                            if (same == 's' or same == 'S'):
                                                #											print(resultado_total[i+1])
                                                estratos2 = resultado_total[i+1]
                                                resp = True
                                                break
                                            elif (same == 'n' or same == 'N'):
                                                estratos2 = '-'
                                                resp = True
                                            else:
                                                same = input('Letra inválida. Digite "S" para sim ou "N" para não \n.')
                                elif (len(resultado_total[i]) - len(resultado2[5]) > 12):
                                    if ('{} ('.format(str(resultado2[5]).upper()) in resultado_total[i]):
                                        same = input(resultado2[5] + ' é o mesmo que ' + resultado_total[i] + '? (S/N) \n')
                                        resp = False
                                        while (resp == False):
                                            if (same == 's' or same == 'S'):
                                                #print(resultado_total[i+1])
                                                estratos2 = resultado_total[i+1]
                                                resp = True
                                                break
                                            elif (same == 'n' or same == 'N'):
                                                    estratos2 = '-'
                                                    resp = True
                                            else:
                                                resp = input('Letra inválida. Digite "S" para sim ou "N" para não. \n')
                        elif (str(resultado2[6]).upper() in resultado_total[i]):
                            #print(resultado_total[i+1])
                            estratos2 = resultado_total[i+1]
                            break
                        else:
                            estratos2 = '-'
                                					
		    	# print(resultado2[5])   #imprime apenas o nome do periódico
				#print(estratos2)      #imprime só o estrato
				#print(resultado2)     #imprime o resultado completo
                # documento.append(resultado2[0])
                # ano_evento.append(resultado2[1])
                sigla = '-'
                if ('COMPLETO' in resultado2[5]):                        #Correção de tabela, elimina o "COMPLETO" do lugar errado
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
						# worksheet.write(x, 3, '-')
                    nomeEvento = resultado2[5]
                    autor = resultado2[6]
                estratos2 = estratos2
                # worksheet.write(x, 7, estratos2)
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
					
				# worksheet.write(x, 8, nota)
                notas.append(nota)
                    
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
                print(nomeProf," | ", resultado2[0]," | ", resultado2[1]," | ", tituloAnais," | ", doi," | ", sigla ," | ",nomeEvento," | ", autor," | ", estratos2," | ", nota)
                c = db.cursor()
                data  = """ insert into resultados (nome_docente, documento, ano_evento, titulo, doi, sigla, nome_evento, autores,estratos, notas)
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                                            
                c.execute(data,(nomeProf, resultado2[0], resultado2[1], tituloAnais, doi, sigla ,nomeEvento, autor, estratos2, nota))
                db.commit()
                c.close()
        totalNotas = []
        totalNotas.append(totalNota)
        print('Total de publicações = {}'.format(cont))            #Quantidade de documentos válidos de cada professor
        print('Pontuação total = {}'.format(totalNota))            #Nota do professor
        print('------------------------------------------------------------')
        
        # worksheet.write(x, 7, 'Nota Total')
		# worksheet.write(x, 8, totalNota)
        # if (respAno == '1'):
        #     contTotalc = cont17c + cont18c + cont19c + cont20c
        #     contTotalp = cont17p + cont18p + cont19p + cont20p
        # elif (respAno == '2'):
        #     contTotalc = cont17c
        #     contTotalp = cont17p
        #     totalNota = nota17
        # elif (respAno == '3'):
        #     contTotalc = cont18c
        #     contTotalp = cont18p
        #     totalNota = nota18
        # elif (respAno == '4'):
        #     contTotalc = cont19c
        #     contTotalp = cont19p
        #     totalNota = nota19
        # elif (respAno == '5'):
        #     contTotalc = cont20c
        #     contTotalp = cont20p
        #     totalNota = nota20
        
            
    return render_template("projetos.html")
